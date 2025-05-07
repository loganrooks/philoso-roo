import argparse
import os
import re
import datetime
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import shutil # Added for rmtree
import warnings # Added import
from markdown_it import MarkdownIt
from mdit_plain.renderer import RendererPlain as PlainTextRenderer
import tiktoken

# --- Constants ---
TOKEN_ENCODING = "cl100k_base"
DEFAULT_MAX_TOKENS = 20000
DEFAULT_OUTPUT_DIR = "source_materials/processed"
CHUNK_FILENAME_PREFIX = "chunk"
INDEX_FILENAME = "index.md"

# --- Regex Patterns ---
CITATION_PATTERNS = [
    re.compile(r'\((?:[^),]+,)?\s*\d{4}(?:,\s*pp?\.\s*\d+(?:-\d+)?)?\)', re.IGNORECASE),
    re.compile(r'§\s*\d+'),
]
HEADER_PATTERN = re.compile(r'^(#+)\s+(.*)')
YAML_FRONTMATTER_PATTERN = re.compile(r'^---\s*$(.*?)^---\s*$', re.MULTILINE | re.DOTALL)

# --- Core Utility Functions ---

def count_tokens(text: str, encoding_name: str = TOKEN_ENCODING) -> int:
    """Counts the number of tokens in a text string using tiktoken."""
    try:
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(text))
        return num_tokens
    except Exception as e:
        warnings.warn(f"Error counting tokens: {e}. Falling back to word count.", UserWarning)
        return len(text.split())

def get_plain_text(md_content: str) -> str:
    """Converts Markdown content to plain text, removing YAML frontmatter."""
    md = MarkdownIt(renderer_cls=PlainTextRenderer)
    md_content_no_yaml = YAML_FRONTMATTER_PATTERN.sub('', md_content).strip()
    plain_text = md.render(md_content_no_yaml)
    # Replace multiple newlines with a single newline
    processed_text = re.sub(r'\n{2,}', '\n', plain_text)
    return processed_text.strip()

def generate_summary(text: str, max_length: int = 500) -> str:
    """Generates a simple summary (first N characters of plain text)."""
    plain_text = get_plain_text(text) # This is already stripped and newlines somewhat normalized
    
    # Further normalize to single line for consistent summary, then strip again.
    single_line_text = plain_text.replace('\n', ' ').strip()

    if len(single_line_text) > max_length:
        return single_line_text[:max_length].rstrip() + "..."
    else: # Handles len <= max_length
        return single_line_text

def generate_safe_filename(title: str, max_len: int = 50) -> str:
    """Generates a filesystem-safe name from a title."""
    safe_name = re.sub(r'[<>:"/\\|?*]', '', title)
    safe_name = re.sub(r'[\s\W]+', '_', safe_name)
    safe_name = safe_name.strip('_')
    return safe_name[:max_len]

def split_into_paragraphs(text: str) -> list[str]:
    """Splits text into paragraphs based on double newlines."""
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]

# --- V1 Architecture Specific Helper Functions ---

def generate_material_id(title: str, material_type: Optional[str] = None, course_code: Optional[str] = None) -> str:
    """Generates a human-readable, unique material ID for V1 architecture."""
    parts = []
    if course_code:
        parts.append(course_code.lower())
    if material_type:
        type_abbr = material_type.lower().replace("_material", "").replace("personal_", "")
        parts.append(type_abbr)
    
    title_slug = generate_safe_filename(title, max_len=100)
    parts.append(title_slug)
    
    title_hash = hashlib.sha1(title.encode('utf-8')).hexdigest()[:6]
    
    base_id = "_".join(parts)
    if len(base_id) > 150:
        base_id = base_id[:140] + "_" + title_hash
    else:
        base_id = base_id + "_" + title_hash
        
    return generate_safe_filename(base_id, max_len=160).lower()

def parse_markdown_structure_and_frontmatter(content: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Parses Markdown content for YAML frontmatter and a flat list of sections based on headers.
    Returns a tuple: (frontmatter_metadata, list_of_sections)
    """
    frontmatter_metadata = {}
    yaml_match = YAML_FRONTMATTER_PATTERN.search(content)
    content_after_yaml = content
    if yaml_match:
        yaml_content = yaml_match.group(1)
        content_after_yaml = content[yaml_match.end():]
        try:
            for line in yaml_content.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter_metadata[key.strip()] = value.strip().strip('"').strip("'") # Basic unquoting
        except Exception as e:
            print(f"Warning: Could not parse YAML frontmatter: {e}")

    sections = []
    lines = content_after_yaml.splitlines()
    current_section_content_lines = []
    current_section_title = "Introduction" # Default for content before first header
    current_section_level = 0
    has_started_first_section = False

    for line_num, line in enumerate(lines):
        header_match = HEADER_PATTERN.match(line)
        if header_match:
            if has_started_first_section or current_section_content_lines: # Save previous section
                sections.append({
                    "title": current_section_title,
                    "level": current_section_level,
                    "content": "\n".join(current_section_content_lines).strip()
                })
            current_section_level = len(header_match.group(1))
            current_section_title = header_match.group(2).strip()
            current_section_content_lines = []
            has_started_first_section = True
        else:
            if not has_started_first_section and line.strip(): # Content before any explicit header
                has_started_first_section = True # Start implicit first section
            if has_started_first_section: # Only add lines if a section has started
                 current_section_content_lines.append(line)

    # Add the last section
    if has_started_first_section or current_section_content_lines:
        sections.append({
            "title": current_section_title,
            "level": current_section_level,
            "content": "\n".join(current_section_content_lines).strip()
        })
    elif not sections and content_after_yaml.strip(): # Handle case with no headers at all but content exists
        sections.append({"title": "Full Text", "level": 0, "content": content_after_yaml.strip()})
        
    return frontmatter_metadata, sections

def build_section_tree_for_v1(sections: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Builds a simple root node whose children are the top-level sections.
    This is used by the V1 chunking logic in main which processes a flat list of sections.
    """
    root = {"title": "root", "level": -1, "children": [], "content": ""}
    for section_data in sections:
        root['children'].append({
            "title": section_data['title'],
            "level": section_data['level'],
            "content": section_data['content'],
            "parent_title": "root", # For consistency if chunk_node_content expects it
            "children": [], # V1 doesn't use nested children for output structure
            "chunks": [],
            "summary": "", "concepts": [], "arguments": [], "citations": [], "metadata": {}, "path": ""
        })
    return root

def extract_citations_with_context(text: str) -> list[dict]:
    """Extracts potential citations and their approximate location."""
    citations_found = []
    paragraphs = split_into_paragraphs(text)
    for i, paragraph in enumerate(paragraphs):
        para_citations = []
        for pattern in CITATION_PATTERNS:
            para_citations.extend(pattern.findall(paragraph))
        if para_citations:
            snippet = paragraph[:100].replace('\n', ' ') + ('...' if len(paragraph) > 100 else '')
            for citation in set(para_citations):
                citations_found.append({
                    "citation": citation,
                    "paragraph_index": i,
                    "context_snippet": snippet
                })
    return citations_found

def chunk_section_content(section_title: str, section_content: str, max_tokens: int) -> List[Dict[str, Any]]:
    """
    Chunks the content of a single section.
    Handles subdivision of oversized paragraphs.
    Returns list of chunk dicts: {'title': str, 'content': str, 'token_count': int, 'citations': list}
    """
    chunks = []
    chunk_index = 1

    if not section_content.strip():
        return chunks

    paragraphs = split_into_paragraphs(section_content)
    current_chunk_content_lines = []
    current_chunk_tokens = 0

    for paragraph in paragraphs:
        paragraph_tokens = count_tokens(paragraph)

        if paragraph_tokens > max_tokens: # Oversized paragraph
            if current_chunk_content_lines: # Finalize existing chunk first
                chunk_title = f"{section_title} (Part {chunk_index})"
                final_content = "\n\n".join(current_chunk_content_lines)
                chunks.append({
                    "title": chunk_title, "content": final_content.strip(),
                    "token_count": count_tokens(final_content),
                    "citations": extract_citations_with_context(final_content)
                })
                current_chunk_content_lines = []
                current_chunk_tokens = 0
                chunk_index += 1
            
            # Subdivide the large paragraph
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)
            sub_chunk_content_lines = []
            sub_chunk_tokens = 0
            sub_part_index = 1
            for sentence in sentences:
                sentence_tokens = count_tokens(sentence)
                if sub_chunk_tokens + sentence_tokens <= max_tokens and sub_chunk_content_lines: # Add to current sub-chunk
                    sub_chunk_content_lines.append(sentence)
                    sub_chunk_tokens += sentence_tokens
                elif sentence_tokens <= max_tokens : # Start new sub-chunk or it's the first sentence
                    if sub_chunk_content_lines: # Finalize previous sub-chunk
                        sub_title = f"{section_title} (Part {chunk_index}, SubPart {sub_part_index})"
                        final_sub_content = " ".join(sub_chunk_content_lines)
                        chunks.append({
                            "title": sub_title, "content": final_sub_content.strip(),
                            "token_count": count_tokens(final_sub_content),
                            "citations": extract_citations_with_context(final_sub_content)
                        })
                        sub_part_index += 1
                    sub_chunk_content_lines = [sentence]
                    sub_chunk_tokens = sentence_tokens
                else: # Sentence itself is too large, add as its own chunk (best effort)
                    if sub_chunk_content_lines: # Finalize previous sub-chunk
                         sub_title = f"{section_title} (Part {chunk_index}, SubPart {sub_part_index})"
                         final_sub_content = " ".join(sub_chunk_content_lines)
                         chunks.append({
                            "title": sub_title, "content": final_sub_content.strip(),
                            "token_count": count_tokens(final_sub_content),
                            "citations": extract_citations_with_context(final_sub_content)
                         })
                         sub_part_index += 1
                         sub_chunk_content_lines = []
                         sub_chunk_tokens = 0

                    sub_title = f"{section_title} (Part {chunk_index}, SubPart {sub_part_index})"
                    chunks.append({
                        "title": sub_title, "content": sentence.strip(),
                        "token_count": sentence_tokens, # This will be > max_tokens
                        "citations": extract_citations_with_context(sentence)
                    })
                    sub_part_index += 1

            if sub_chunk_content_lines: # Add remaining sub-chunk
                sub_title = f"{section_title} (Part {chunk_index}, SubPart {sub_part_index})"
                final_sub_content = " ".join(sub_chunk_content_lines)
                chunks.append({
                    "title": sub_title, "content": final_sub_content.strip(),
                    "token_count": count_tokens(final_sub_content),
                    "citations": extract_citations_with_context(final_sub_content)
                })
            chunk_index += 1
            continue

        # Regular chunking
        if current_chunk_tokens + paragraph_tokens <= max_tokens and current_chunk_content_lines:
            current_chunk_content_lines.append(paragraph)
            current_chunk_tokens += paragraph_tokens
        elif paragraph_tokens <= max_tokens : # Start new chunk or it's the first paragraph
            if current_chunk_content_lines: # Finalize existing chunk
                chunk_title = f"{section_title} (Part {chunk_index})"
                final_content = "\n\n".join(current_chunk_content_lines)
                chunks.append({
                    "title": chunk_title, "content": final_content.strip(),
                    "token_count": count_tokens(final_content),
                    "citations": extract_citations_with_context(final_content)
                })
                chunk_index += 1
            current_chunk_content_lines = [paragraph]
            current_chunk_tokens = paragraph_tokens
        else: # Paragraph itself is too large (should have been caught by oversized logic, but as fallback)
            if current_chunk_content_lines: # Finalize existing chunk
                chunk_title = f"{section_title} (Part {chunk_index})"
                final_content = "\n\n".join(current_chunk_content_lines)
                chunks.append({
                    "title": chunk_title, "content": final_content.strip(),
                    "token_count": count_tokens(final_content),
                    "citations": extract_citations_with_context(final_content)
                })
                chunk_index += 1
                current_chunk_content_lines = []
                current_chunk_tokens = 0
            # Add large paragraph as its own chunk
            chunk_title = f"{section_title} (Part {chunk_index})"
            chunks.append({
                "title": chunk_title, "content": paragraph.strip(),
                "token_count": paragraph_tokens, # This will be > max_tokens
                "citations": extract_citations_with_context(paragraph)
            })
            chunk_index += 1


    if current_chunk_content_lines: # Add the last remaining chunk
        chunk_title = f"{section_title} (Part {chunk_index})"
        final_content = "\n\n".join(current_chunk_content_lines)
        chunks.append({
            "title": chunk_title, "content": final_content.strip(),
            "token_count": count_tokens(final_content),
            "citations": extract_citations_with_context(final_content)
        })
    return chunks

# --- V1 Architecture Processing Functions ---

def determine_material_metadata_and_paths(
    args: argparse.Namespace, 
    source_file_path: Path, 
    frontmatter: Dict[str, Any]
) -> Dict[str, Any]:
    """Determines material_id, output paths, etc., for V1 architecture."""
    course_code = args.course_code or frontmatter.get('course_code')
    if not course_code:
        try:
            if "courses" in source_file_path.parts:
                courses_index = source_file_path.parts.index("courses")
                if len(source_file_path.parts) > courses_index + 1:
                    course_code = source_file_path.parts[courses_index + 1]
        except ValueError: pass

    material_type = args.material_type or frontmatter.get('material_type')
    material_type_category = None
    if material_type:
        if material_type == "lecture": material_type_category = "lectures"
        elif material_type == "reading": material_type_category = "readings"
        elif material_type == "note": material_type_category = "notes"
    else:
        if course_code:
            path_str = str(source_file_path).lower()
            if "/lectures/" in path_str: material_type, material_type_category = "lecture", "lectures"
            elif "/readings/" in path_str: material_type, material_type_category = "reading", "readings"
            elif "/notes/" in path_str: material_type, material_type_category = "note", "notes"
        if not material_type: material_type = "library_material"

    source_type = args.source_type or frontmatter.get('source_type')
    if not source_type:
        if course_code: source_type = "course_material"
        elif material_type == "library_material": source_type = "library_primary"
        elif material_type == "note": source_type = "personal_note"

    title = args.title or frontmatter.get('title') or source_file_path.stem.replace('_', ' ').replace('-', ' ')
    title_for_id = title if title else source_file_path.stem
    material_id = generate_material_id(title_for_id, material_type, course_code)

    processed_base_dir = Path(args.output_dir)
    is_course_material = bool(course_code)
    if is_course_material and material_type_category:
        material_base_path = processed_base_dir / "courses" / course_code.upper() / material_type_category / material_id
    elif not is_course_material:
        material_base_path = processed_base_dir / "library" / material_id
    else:
        print(f"Warning: Could not determine output path for {source_file_path}. Defaulting to library.")
        material_base_path = processed_base_dir / "library" / material_id
        is_course_material = False
        
    course_index_md_path = None
    if is_course_material:
        course_index_md_path = processed_base_dir / "courses" / course_code.upper() / INDEX_FILENAME

    return {
        "material_id": material_id, "title": title, "course_code": course_code,
        "material_type": material_type, "material_type_category": material_type_category,
        "source_type": source_type, "is_course_material": is_course_material,
        "processed_base_dir": processed_base_dir, "material_base_path": material_base_path,
        "chunks_dir": material_base_path / "chunks",
        "material_index_md_path": material_base_path / INDEX_FILENAME,
        "course_index_md_path": course_index_md_path,
        "original_input_path": source_file_path,
        "authors": frontmatter.get('authors', []), "work_title": frontmatter.get('work_title'),
        "section_title": frontmatter.get('section_title'),
        "publication_date": frontmatter.get('publication_date'),
        "tags": frontmatter.get('tags', []),
    }

def create_output_directories(
    base_output_dir: Path,
    course_code: Optional[str],
    material_type_category: Optional[str], # Changed from material_type to material_type_category for consistency with determine_material_metadata_and_paths
    material_id: str,
    force_update: bool = False
) -> Tuple[Path, Path]:
    """Creates the necessary output directories for processed material."""
    if course_code and material_type_category:
        material_base_path = base_output_dir / "courses" / course_code.upper() / material_type_category / material_id
    else: # Library material
        material_base_path = base_output_dir / "library" / material_id
    
    chunks_dir = material_base_path / "chunks"

    if force_update and material_base_path.exists():
        shutil.rmtree(material_base_path)
        print(f"Force update: Removed existing directory {material_base_path}")

    material_base_path.mkdir(parents=True, exist_ok=True)
    chunks_dir.mkdir(parents=True, exist_ok=True)
    
    # Ensure parent directory for course index exists if it's a course material
    if course_code:
        course_dir = base_output_dir / "courses" / course_code.upper()
        course_dir.mkdir(parents=True, exist_ok=True)

    # Ensure the root processed_base_dir exists (for master_index.json)
    base_output_dir.mkdir(parents=True, exist_ok=True)
    
    return material_base_path, chunks_dir


def generate_and_write_chunks(
    sections: List[Dict[str, Any]], # Flat list of sections from parse_markdown_structure_and_frontmatter
    material_info: Dict[str, Any], 
    max_tokens: int
) -> List[Dict[str, Any]]:
    """Generates chunks from sections and writes them to files."""
    all_material_chunks_data = []
    chunk_file_counter = {'count': 0}

    for section in sections:
        section_title = section['title']
        section_content = section['content']
        
        node_chunks = chunk_section_content(section_title, section_content, max_tokens)
        
        for chunk_data in node_chunks:
            chunk_file_counter['count'] += 1
            chunk_filename = f"{CHUNK_FILENAME_PREFIX}_{chunk_file_counter['count']:04d}.md"
            chunk_filepath = material_info["chunks_dir"] / chunk_filename
            
            final_chunk_title = chunk_data['title']
            # Ensure section title is part of chunk title if not already
            if not section_title.lower() in final_chunk_title.lower() and section_title != "Full Text" and section_title != "Introduction":
                 final_chunk_title = f"{section_title} - {chunk_data['title']}"

            try:
                with open(chunk_filepath, 'w', encoding='utf-8') as cf:
                    cf.write(f"# {final_chunk_title}\n\n")
                    cf.write(f"*Original Section:* {section_title}\n")
                    cf.write(f"*Source File:* {Path(material_info['original_input_path']).name}\n")
                    cf.write(f"*Material ID:* {material_info['material_id']}\n")
                    cf.write(f"*Token Count (approx):* {chunk_data['token_count']}\n")
                    if chunk_data['citations']:
                         cf.write(f"*Potential Citations ({len(chunk_data['citations'])}):*\n")
                         for cit_obj in chunk_data['citations'][:5]:
                             cf.write(f"  - {cit_obj['citation']} (Para. ~{cit_obj['paragraph_index']})\n")
                         if len(chunk_data['citations']) > 5: cf.write("  - ... (see material index.md)\n")
                    cf.write("\n---\n\n")
                    cf.write(chunk_data['content'])
                
                all_material_chunks_data.append({
                    "filename": chunk_filename,
                    "title": final_chunk_title,
                    "content": chunk_data['content'], # Added content key
                    "token_count": chunk_data['token_count'],
                    "citations": chunk_data['citations'],
                    "summary": generate_summary(chunk_data['content'], 150)
                })
            except Exception as e:
                print(f"Error writing chunk file {chunk_filepath}: {e}")
    return all_material_chunks_data

def write_material_index_md(material_info: Dict[str, Any], all_chunks_data: List[Dict[str, Any]]):
    """Writes the material-specific index.md file for V1 architecture."""
    index_path = material_info["material_index_md_path"]
    print(f"Writing material index: {index_path}")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write(f"id: {material_info['material_id']}\n")
        f.write(f"title: \"{material_info['title']}\"\n")
        if material_info.get('authors'): f.write(f"authors: {json.dumps(material_info['authors'])}\n")
        if material_info.get('work_title'): f.write(f"work_title: \"{material_info['work_title']}\"\n")
        if material_info.get('section_title'): f.write(f"section_title: \"{material_info['section_title']}\"\n")
        if material_info.get('publication_date'): f.write(f"publication_date: \"{material_info['publication_date']}\"\n")
        f.write(f"material_type: {material_info['material_type']}\n")
        f.write(f"source_type: {material_info['source_type']}\n")
        if material_info.get('course_code'): f.write(f"course_code: {material_info['course_code']}\n")
        
        final_tags = set(material_info.get('tags', []))
        if material_info.get('course_code'): final_tags.add(f"course:{material_info['course_code']}")
        if material_info.get('authors'):
            for author in material_info['authors']: final_tags.add(f"author:{generate_safe_filename(author).lower()}")
        
        f.write(f"tags: {json.dumps(list(final_tags))}\n")
        f.write(f"dynamic_roles: []\n")
        f.write(f"summary: \"{generate_summary(material_info.get('full_text_for_summary', ''), 250).replace('\"', '\\\"')}\"\n")
        f.write(f"chunk_count: {len(all_chunks_data)}\n")
        f.write("list_of_chunks:\n")
        for chunk_data in all_chunks_data:
            f.write(f"  - file: \"chunks/{chunk_data['filename']}\"\n")
            f.write(f"    summary: \"{chunk_data.get('summary', 'N/A').replace('\"', '\\\"')}\"\n")
            f.write(f"    keywords: []\n")
        f.write("---\n\n")
        f.write(f"# Processed Chunks for: {material_info['title']}\n\n")
        for i, chunk_data in enumerate(all_chunks_data):
            f.write(f"- [{chunk_data.get('title', f'Chunk {i+1}')}](chunks/{chunk_data['filename']}) (Tokens: ~{chunk_data['token_count']})\n")

def update_master_index(master_index_path: Path, material_info: Dict[str, Any], all_chunks_data: List[Dict[str, Any]], force_update: bool = False):
    """Creates or updates the master_index.json file for V1 architecture."""
    master_data = []
    if master_index_path.exists():
        try:
            with open(master_index_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.strip(): # Ensure content is not empty before trying to load
                    master_data = json.loads(content) # Use json.loads for string content
                else:
                    master_data = [] # File is empty
            if not isinstance(master_data, list):
                warnings.warn(f"Master index file {master_index_path} does not contain a list. Initializing as empty list.", UserWarning)
                master_data = []
        except json.JSONDecodeError:
            warnings.warn(f"Master index file {master_index_path} is corrupted. A new one will be created.", UserWarning)
            master_data = []
        except Exception as e:
            warnings.warn(f"Error reading master index {master_index_path}: {e}. Starting with an empty index.", UserWarning)
            master_data = []

    entry = {
        "material_id": material_info.get('material_id'),
        "title": material_info.get('title'),
        "course_code": material_info.get('course_code'),
        "material_type": material_info.get('material_type'),
        "source_type": material_info.get('source_type'),
        "summary": material_info.get('summary') or generate_summary(material_info.get('full_text_for_summary', ''), 150),
        "source_path_original": str(material_info.get('original_input_path')),
        "processed_index_path": str(material_info.get('material_index_md_path').relative_to(material_info.get('processed_base_dir'))) if material_info.get('material_index_md_path') and material_info.get('processed_base_dir') else None,
        "chunk_count": len(all_chunks_data),
        "total_token_count": sum(chunk.get('token_count', 0) for chunk in all_chunks_data),
        "last_processed_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "authors": material_info.get('authors', []),
        "work_title": material_info.get('work_title'),
        "section_title": material_info.get('section_title'),
        "publication_date": material_info.get('publication_date'),
        "tags": material_info.get('tags', []),
        "dynamic_roles": material_info.get('dynamic_roles', [])
    }

    entry_updated_or_skipped = False
    entry_exists_idx = -1

    for i, existing_entry in enumerate(master_data):
        if existing_entry.get("material_id") == entry["material_id"]:
            entry_exists_idx = i
            break
    
    if entry_exists_idx != -1: # Entry found
        if force_update:
            master_data[entry_exists_idx] = entry
            print(f"Updating existing entry for {entry['material_id']} in master index due to force_update.")
            entry_updated_or_skipped = True
        else:
            warnings.warn(f"Entry for {entry['material_id']} already exists in {master_index_path} and force_update is False. Skipping update.", UserWarning)
            entry_updated_or_skipped = True # Considered "handled", no need to append
    
    if not entry_updated_or_skipped:
        master_data.append(entry)

    try:
        with open(master_index_path, 'w', encoding='utf-8') as f:
            json.dump(master_data, f, indent=4)
        # print(f"Updated master index: {master_index_path}") # Optional: for verbose logging
    except Exception as e:
        print(f"Error writing master index to {master_index_path}: {e}")

def update_course_index_md(course_index_path: Path, material_info: Dict[str, Any]):
    """Creates or updates the course-specific index.md file for V1 architecture."""
    if not course_index_path: return
    
    materials_for_course = []
    if course_index_path.exists():
        with open(course_index_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.search(r"- \*\*\[(.*?)\]\((.*?)\)\*\*", line)
                if match: materials_for_course.append({"title": match.group(1), "path": match.group(2)})

    new_material_path = f"../{material_info['material_type_category']}/{material_info['material_id']}/{INDEX_FILENAME}"
    entry_exists = False
    for item in materials_for_course:
        if Path(item["path"]).name == Path(new_material_path).name and \
           Path(item["path"]).parent.name == Path(new_material_path).parent.name:
            item["title"] = material_info["title"]
            entry_exists = True
            break
    if not entry_exists: materials_for_course.append({"title": material_info["title"], "path": new_material_path})
    
    materials_for_course.sort(key=lambda x: x['title'])
    print(f"Updating course index: {course_index_path}")
    with open(course_index_path, 'w', encoding='utf-8') as f:
        f.write(f"# Processed Materials for Course: {material_info['course_code']}\n\n")
        if not materials_for_course: f.write("No materials processed for this course yet.\n")
        else:
            for item in materials_for_course: f.write(f"- **[{item['title']}]({item['path']})**\n")

# --- Placeholder functions from original script (scope of refactor is not to implement them) ---
def generate_key_concepts(text: str) -> list[str]:
    """Placeholder for key concept extraction."""
    return []

def generate_arguments(text: str) -> list[str]:
    """Placeholder for argument extraction."""
    return []

# --- Main Processing Orchestration ---

def process_source_file(args: argparse.Namespace):
    """Main logic to process a single source file according to V1 architecture."""
    source_file_path = Path(args.input_path)
    
    if not source_file_path.is_file() or source_file_path.suffix.lower() != ".md":
        print(f"Error: Input path '{source_file_path}' is not a valid Markdown file.")
        return

    print(f"Starting processing for: {source_file_path}")

    try:
        with open(source_file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
    except Exception as e:
        print(f"Error reading file {source_file_path}: {e}")
        return

    frontmatter, sections = parse_markdown_structure_and_frontmatter(raw_content)
    
    material_info = determine_material_metadata_and_paths(args, source_file_path, frontmatter)
    material_info['full_text_for_summary'] = raw_content # For overall summary

    # create_output_directories now returns the paths, which are already in material_info
    # but we call it for its side effect of creating directories.
    # The function was refactored to take individual args instead of the whole dict.
    create_output_directories(
        base_output_dir=material_info['processed_base_dir'],
        course_code=material_info.get('course_code'),
        material_type_category=material_info.get('material_type_category'),
        material_id=material_info['material_id'],
        force_update=args.force_update
    )
    print(f"Output directory for this material: {material_info['material_base_path']}")

    if not sections:
        print("Warning: No headers/content found after frontmatter. Treating as single section if content exists.")
        # Use raw_content if sections list is empty but raw_content (after YAML) is not.
        content_for_single_section = YAML_FRONTMATTER_PATTERN.sub('', raw_content).strip()
        if content_for_single_section:
            sections = [{"title": material_info.get("title", "Full Text"), "level": 0, "content": content_for_single_section}]
        else:
            print("No processable content found in the file.")
            # Still create basic index files even if no chunks
            all_material_chunks_data = []


    if sections:
        all_material_chunks_data = generate_and_write_chunks(sections, material_info, args.max_tokens)
    else: # Ensure all_material_chunks_data exists even if no sections/chunks
        all_material_chunks_data = []


    write_material_index_md(material_info, all_material_chunks_data)
    
    master_index_path = material_info['processed_base_dir'] / "master_index.json"
    # Ensure tags are finalized for master index
    final_tags_for_master = set(material_info.get('tags', [])) # Start with tags from frontmatter/args
    if material_info.get('course_code'): final_tags_for_master.add(f"course:{material_info['course_code']}")
    if material_info.get('authors'):
        for author in material_info['authors']: final_tags_for_master.add(f"author:{generate_safe_filename(author).lower()}")
    material_info['tags'] = list(final_tags_for_master)
    update_master_index(master_index_path, material_info, all_material_chunks_data, args.force_update)

    if material_info["is_course_material"] and material_info["course_index_md_path"]:
        update_course_index_md(material_info["course_index_md_path"], material_info, args.force_update)

    print(f"\nFinished processing {source_file_path.name}. Total chunks: {len(all_material_chunks_data)}")
    print(f"Material ID: {material_info['material_id']}")
    print(f"Output at: {material_info['material_base_path']}")


from typing import List, Optional # Ensure List and Optional are imported if not already

def parse_arguments(args_list: Optional[List[str]] = None) -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Process Markdown source file for V1 architecture.")
    # Changed input_path to be positional and type Path
    parser.add_argument("input_path", type=Path, help="Path to the input Markdown file.")
    # Changed output_dir to type Path
    parser.add_argument("--output-dir", type=Path, default=Path(DEFAULT_OUTPUT_DIR), help=f"Base output directory (default: '{DEFAULT_OUTPUT_DIR}').")
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS, help=f"Max tokens per chunk (default: {DEFAULT_MAX_TOKENS}).")
    parser.add_argument("--course-code", type=str, default=None, help="Course code (e.g., PHL316).")
    parser.add_argument("--material-type", type=str, default=None, choices=['lecture', 'reading', 'note', 'library_material'], help="Type of material.")
    parser.add_argument("--source-type", type=str, default=None, choices=['course_material', 'library_primary', 'library_secondary', 'personal_note'], help="Source type.")
    parser.add_argument("--title", type=str, default=None, help="Material title (if not in frontmatter).")
    # Added force_update argument as it was in the original test expectation
    parser.add_argument("--force-update", action="store_true", help="Force update even if output appears current.")
    return parser.parse_args(args_list)

if __name__ == "__main__":
    cli_args = parse_arguments()
    process_source_file(cli_args)