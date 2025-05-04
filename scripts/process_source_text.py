import argparse
import os
import re
import datetime
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from markdown_it import MarkdownIt
from mdit_plain.renderer import PlainTextRenderer
import tiktoken

# --- Constants ---
TOKEN_ENCODING = "cl100k_base"  # Using a common model for token counting
DEFAULT_MAX_TOKENS = 20000      # Target chunk size in tokens (as per requirement 3)
DEFAULT_OUTPUT_DIR = "source_materials/processed"
CHUNK_FILENAME_PREFIX = "chunk"
INDEX_FILENAME = "index.md"

# --- Regex Patterns ---
CITATION_PATTERNS = [
    re.compile(r'\((?:[^),]+,)?\s*\d{4}(?:,\s*pp?\.\s*\d+(?:-\d+)?)?\)', re.IGNORECASE), # (Author, YYYY, p. #), (YYYY, p. #), (YYYY)
    re.compile(r'§\s*\d+'), # §#
    # Add more specific patterns if needed
]
HEADER_PATTERN = re.compile(r'^(#+)\s+(.*)') # Find headers at the start of a line
YAML_FRONTMATTER_PATTERN = re.compile(r'^---\s*$(.*?)^---\s*$', re.MULTILINE | re.DOTALL)

# --- Helper Functions ---

def count_tokens(text: str, encoding_name: str = TOKEN_ENCODING) -> int:
    """Counts the number of tokens in a text string using tiktoken."""
    try:
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(text))
        return num_tokens
    except Exception as e:
        print(f"Warning: Error counting tokens: {e}. Falling back to word count.")
        return len(text.split()) # Simple word count as fallback

def get_plain_text(md_content: str) -> str:
    """Converts Markdown content to plain text."""
    md = MarkdownIt(renderer_cls=PlainTextRenderer)
    # Remove YAML frontmatter before rendering to plain text
    md_content_no_yaml = YAML_FRONTMATTER_PATTERN.sub('', md_content).strip()
    return md.render(md_content_no_yaml).strip()

def generate_summary(text: str, max_length: int = 500) -> str:
    """Generates a simple summary (first N characters of plain text). Placeholder."""
    plain_text = get_plain_text(text)
    summary = plain_text[:max_length].replace('\n', ' ')
    if len(plain_text) > max_length:
        summary += "..."
    return summary

def generate_key_concepts(text: str) -> list[str]:
    """Placeholder for key concept extraction."""
    # TODO: Implement actual NLP key concept extraction
    return []

def generate_arguments(text: str) -> list[str]:
    """Placeholder for argument extraction."""
    # TODO: Implement actual NLP argument extraction
    return []

def extract_citations_with_context(text: str) -> list[dict]:
    """
    Extracts potential citations and their approximate location (paragraph index).
    Returns a list of dicts: {'citation': str, 'paragraph_index': int, 'context_snippet': str}
    """
    citations_found = []
    paragraphs = split_into_paragraphs(text)
    for i, paragraph in enumerate(paragraphs):
        para_citations = []
        for pattern in CITATION_PATTERNS:
            para_citations.extend(pattern.findall(paragraph))
        
        if para_citations:
            # Create a snippet (e.g., first 100 chars of paragraph)
            snippet = paragraph[:100].replace('\n', ' ') + ('...' if len(paragraph) > 100 else '')
            for citation in set(para_citations): # Unique citations per paragraph
                citations_found.append({
                    "citation": citation,
                    "paragraph_index": i,
                    "context_snippet": snippet
                    # TODO: Add more precise location info if possible (line numbers?)
                })
    return citations_found

def split_into_paragraphs(text: str) -> list[str]:
    """Splits text into paragraphs based on double newlines."""
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]

def generate_safe_filename(title: str, max_len: int = 50) -> str:
    """Generates a filesystem-safe name from a title."""
    # Remove invalid chars
    safe_name = re.sub(r'[<>:"/\\|?*]', '', title)
    # Replace spaces/punctuation with underscores
    safe_name = re.sub(r'[\s\W]+', '_', safe_name)
    # Trim leading/trailing underscores
    safe_name = safe_name.strip('_')
    # Limit length
    return safe_name[:max_len]

def get_source_id(file_path: Path) -> str:
    """Generates a unique ID for the source file."""
    # Use a hash of the relative path for consistency
    hasher = hashlib.sha1(str(file_path).encode('utf-8'))
    return hasher.hexdigest()[:10] # Short hash

def parse_markdown_structure(content: str) -> Tuple[Optional[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Parses Markdown content into a list of sections based on headers.
    Returns a tuple: (metadata, list_of_sections)
    """
    metadata = {}
    # Extract YAML frontmatter
    yaml_match = YAML_FRONTMATTER_PATTERN.search(content)
    if yaml_match:
        yaml_content = yaml_match.group(1)
        content_start_index = yaml_match.end()
        try:
            # Basic YAML parsing (replace with pyyaml if needed for complex types)
            for line in yaml_content.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
        except Exception as e:
            print(f"Warning: Could not parse YAML frontmatter: {e}")
        content = content[content_start_index:] # Content after frontmatter
    else:
        content = content # No frontmatter found

    sections = []
    lines = content.splitlines()
    current_section = None
    section_content_lines = []

    for line in lines:
        header_match = HEADER_PATTERN.match(line)
        if header_match:
            # Save previous section if exists
            if current_section is not None:
                current_section['content'] = "\n".join(section_content_lines).strip()
                sections.append(current_section)

            # Start new section
            level = len(header_match.group(1))
            title = header_match.group(2).strip()
            current_section = {"title": title, "level": level, "content": ""}
            section_content_lines = []
        elif current_section is not None:
            section_content_lines.append(line)
        elif not sections and line.strip(): # Content before the first header
             # Start implicit root section
             current_section = {"title": "Introduction", "level": 0, "content": ""}
             section_content_lines.append(line)


    # Add the last section
    if current_section is not None:
        current_section['content'] = "\n".join(section_content_lines).strip()
        sections.append(current_section)
    elif not sections and content.strip(): # Handle case with no headers at all
        sections.append({"title": "Full Text", "level": 0, "content": content.strip()})


    return metadata, sections

def build_section_tree(sections: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Builds a hierarchical tree from a flat list of sections."""
    root = {"title": "root", "level": -1, "children": [], "content": ""} # Dummy root
    stack = [root] # Stack of parent sections

    for section in sections:
        level = section['level']
        title = section['title']
        content = section['content']

        # Find the correct parent on the stack
        while stack[-1]['level'] >= level:
            stack.pop()

        parent = stack[-1]
        new_node = {
            "title": title,
            "level": level,
            "content": content,
            "children": [],
            "parent_title": parent['title'] if parent['level'] != -1 else None,
            "chunks": [], # To store info about generated chunk files
            "summary": "",
            "concepts": [],
            "arguments": [],
            "citations": [],
            "metadata": {}, # Section specific metadata
            "path": "" # Path relative to source_id dir
        }
        parent['children'].append(new_node)
        stack.append(new_node)

    return root # Return the dummy root, its children are the top-level sections

def chunk_node_content(node: Dict[str, Any], max_tokens: int) -> List[Dict[str, Any]]:
    """
    Chunks the content of a node if it's a leaf or needs subdivision.
    Handles subdivision of oversized paragraphs.
    Returns list of chunk dicts: {'title': str, 'content': str, 'token_count': int, 'citations': list}
    """
    chunks = []
    section_content = node['content']
    section_title = node['title']
    chunk_index = 1

    if not section_content.strip():
        return chunks

    paragraphs = split_into_paragraphs(section_content)
    current_chunk_content = ""
    current_chunk_tokens = 0

    for i, paragraph in enumerate(paragraphs):
        paragraph_tokens = count_tokens(paragraph)

        # --- Subdivision Logic ---
        if paragraph_tokens > max_tokens:
            # 1. Finish any existing chunk
            if current_chunk_content:
                chunk_title = f"{section_title} (Part {chunk_index})"
                chunk_citations = extract_citations_with_context(current_chunk_content)
                chunks.append({
                    "title": chunk_title,
                    "content": current_chunk_content.strip(),
                    "token_count": current_chunk_tokens,
                    "citations": chunk_citations
                })
                current_chunk_content = ""
                current_chunk_tokens = 0
                chunk_index += 1

            # 2. Subdivide the large paragraph (simple sentence split for now)
            # TODO: Improve subdivision (e.g., respect markdown, use NLP sentence splitting)
            sentences = re.split(r'(?<=[.!?])\s+', paragraph) # Basic sentence split
            sub_chunk_content = ""
            sub_chunk_tokens = 0
            sub_chunk_index = 1
            for sentence in sentences:
                sentence_tokens = count_tokens(sentence)
                if sub_chunk_tokens + sentence_tokens <= max_tokens:
                    sub_chunk_content += sentence + " "
                    sub_chunk_tokens += sentence_tokens
                else:
                    # Finish sub-chunk
                    if sub_chunk_content:
                        sub_title = f"{section_title} (Part {chunk_index}, SubPart {sub_chunk_index})"
                        sub_citations = extract_citations_with_context(sub_chunk_content)
                        chunks.append({
                            "title": sub_title,
                            "content": sub_chunk_content.strip(),
                            "token_count": sub_chunk_tokens,
                            "citations": sub_citations
                        })
                        sub_chunk_index += 1
                    # Start new sub-chunk
                    sub_chunk_content = sentence + " "
                    sub_chunk_tokens = sentence_tokens

            # Add remaining sub-chunk
            if sub_chunk_content:
                 sub_title = f"{section_title} (Part {chunk_index}, SubPart {sub_chunk_index})"
                 sub_citations = extract_citations_with_context(sub_chunk_content)
                 chunks.append({
                     "title": sub_title,
                     "content": sub_chunk_content.strip(),
                     "token_count": sub_chunk_tokens,
                     "citations": sub_citations
                 })
            chunk_index += 1 # Increment main chunk index after handling the large paragraph
            continue # Move to the next paragraph

        # --- Regular Chunking ---
        if current_chunk_tokens + paragraph_tokens <= max_tokens:
            current_chunk_content += paragraph + "\n\n"
            current_chunk_tokens += paragraph_tokens
        else:
            # Finish the current chunk
            if current_chunk_content:
                chunk_title = f"{section_title} (Part {chunk_index})"
                chunk_citations = extract_citations_with_context(current_chunk_content)
                chunks.append({
                    "title": chunk_title,
                    "content": current_chunk_content.strip(),
                    "token_count": current_chunk_tokens,
                    "citations": chunk_citations
                })
                chunk_index += 1
            # Start a new chunk
            current_chunk_content = paragraph + "\n\n"
            current_chunk_tokens = paragraph_tokens

    # Add the last remaining chunk
    if current_chunk_content:
        chunk_title = f"{section_title} (Part {chunk_index})"
        chunk_citations = extract_citations_with_context(current_chunk_content)
        chunks.append({
            "title": chunk_title,
            "content": current_chunk_content.strip(),
            "token_count": current_chunk_tokens,
            "citations": chunk_citations
        })

    return chunks


def process_node_recursive(node: Dict[str, Any], base_output_dir: Path, source_metadata: Dict[str, Any], max_tokens: int, json_data_list: List[Dict[str, Any]], chunk_file_counter: Dict[str, int]):
    """
    Recursively processes a node in the section tree, creates directories,
    chunks content, generates index.md, and collects JSON data.
    """
    is_leaf = not node['children']
    node_title_safe = generate_safe_filename(node['title'])
    
    # Determine current path relative to base_output_dir
    if node['level'] == -1: # Dummy root
        current_path_relative = Path() # Should not happen if called correctly
    elif node['level'] == 0:
         current_path_relative = Path(f"level_{node['level']}")
    else:
        # Find parent path - requires parent info or passing path down
        # This part needs refinement - let's pass path down
        parent_path = node.get("parent_path", Path()) # Get from node if passed down
        current_path_relative = parent_path / f"level_{node['level']}_{node_title_safe}"

    node["path"] = str(current_path_relative) # Store relative path
    current_output_dir = base_output_dir / current_path_relative
    current_output_dir.mkdir(parents=True, exist_ok=True)

    print(f"{'  ' * (node['level'] + 1)}Processing Node: {node['title']} -> {current_output_dir}")

    # --- Process Content (Chunking for Leaf Nodes) ---
    node_chunks_info = []
    if is_leaf and node['content'].strip():
        generated_chunks = chunk_node_content(node, max_tokens)
        for chunk_data in generated_chunks:
            chunk_file_counter['count'] += 1
            chunk_filename = f"{CHUNK_FILENAME_PREFIX}_{chunk_file_counter['count']:04d}.md"
            chunk_filepath = current_output_dir / chunk_filename
            chunk_rel_filepath = current_path_relative / chunk_filename

            # Write chunk file
            try:
                with open(chunk_filepath, 'w', encoding='utf-8') as cf:
                    cf.write(f"# {chunk_data['title']}\n\n")
                    cf.write(f"*Source Section:* {node['title']}\n")
                    if node.get('parent_title'):
                         cf.write(f"*Parent Section:* {node['parent_title']}\n")
                    cf.write(f"*Source File:* {source_metadata.get('source_file_relative', 'N/A')}\n")
                    cf.write(f"*Token Count:* ~{chunk_data['token_count']}\n")
                    # Add basic citation list to chunk metadata
                    if chunk_data['citations']:
                         cf.write(f"*Potential Citations ({len(chunk_data['citations'])}):*\n")
                         for cit in chunk_data['citations'][:5]: # Limit preview
                             cf.write(f"  - {cit['citation']} (Para. ~{cit['paragraph_index']})\n")
                         if len(chunk_data['citations']) > 5:
                             cf.write("  - ... (see index for full list)\n")
                    cf.write("\n---\n\n")
                    cf.write(chunk_data['content'])
                print(f"{'  ' * (node['level'] + 2)}- Wrote chunk: {chunk_filepath.name}")

                chunk_info = {
                    "filename": chunk_filename,
                    "filepath_relative": str(chunk_rel_filepath),
                    "title": chunk_data['title'],
                    "token_count": chunk_data['token_count'],
                    "citations": chunk_data['citations'], # Detailed citations list
                    "summary": generate_summary(chunk_data['content'], 150) # Short summary for chunk
                }
                node_chunks_info.append(chunk_info)
                node['chunks'].append(chunk_info) # Link chunk info back to the node

            except Exception as e:
                print(f"Error writing chunk file {chunk_filepath}: {e}")
                # Add error to JSON data?

    # --- Generate Node Metadata (Summary, Concepts, Arguments) ---
    node['summary'] = generate_summary(node['content'])
    node['concepts'] = generate_key_concepts(node['content'])
    node['arguments'] = generate_arguments(node['content'])
    # Collect citations from all chunks within this node (if leaf)
    if is_leaf:
        node['citations'] = [cit for chunk in node['chunks'] for cit in chunk['citations']]
    
    # --- Recursively Process Children ---
    child_node_summaries = []
    for child_node in node['children']:
        child_node["parent_path"] = current_path_relative # Pass down parent path
        process_node_recursive(child_node, base_output_dir, source_metadata, max_tokens, json_data_list, chunk_file_counter)
        # Collect summary info for parent's index
        child_node_summaries.append({
            "title": child_node['title'],
            "path": child_node['path'],
            "summary": child_node['summary']
        })


    # --- Generate index.md for the Current Node ---
    index_filepath = current_output_dir / INDEX_FILENAME
    try:
        with open(index_filepath, 'w', encoding='utf-8') as idx_f:
            idx_f.write(f"# Index: {node['title']}\n\n")
            idx_f.write(f"*Level:* {node['level']}\n")
            if node.get('parent_title'):
                 idx_f.write(f"*Parent:* {node['parent_title']}\n")
            idx_f.write(f"*Source File:* {source_metadata.get('source_file_relative', 'N/A')}\n")
            if source_metadata.get('title'):
                 idx_f.write(f"*Source Title:* {source_metadata['title']}\n")
            if source_metadata.get('author'):
                 idx_f.write(f"*Source Author:* {source_metadata['author']}\n")
            idx_f.write("\n")

            idx_f.write("## Section Summary\n\n")
            idx_f.write(f"{node['summary']}\n\n")

            if node['concepts']:
                idx_f.write("## Key Concepts\n\n")
                for concept in node['concepts']:
                    idx_f.write(f"- {concept}\n")
                idx_f.write("\n")

            if node['arguments']:
                idx_f.write("## Main Arguments\n\n")
                for argument in node['arguments']:
                    idx_f.write(f"- {argument}\n") # Or more detailed summary
                idx_f.write("\n")

            # Links to Children (Subdirectories)
            if node['children']:
                idx_f.write("## Sub-Sections\n\n")
                for child_summary in child_node_summaries:
                     # Use relative path from current index to child dir
                     child_dir_name = Path(child_summary['path']).name
                     idx_f.write(f"- **[{child_summary['title']}]({child_dir_name}/{INDEX_FILENAME})**: {child_summary['summary']}\n")
                idx_f.write("\n")

            # Links to Chunks (Leaf Files)
            if node['chunks']:
                idx_f.write("## Text Chunks\n\n")
                for chunk in node['chunks']:
                    idx_f.write(f"- **[{chunk['title']}]({chunk['filename']})** (Tokens: ~{chunk['token_count']})\n")
                    # Optionally add chunk summary here too
                    # idx_f.write(f"  - Summary: {chunk['summary']}\n")
                idx_f.write("\n")

            # Detailed Citations (Only at deepest level - approximated by being a leaf node)
            if is_leaf and node['citations']:
                idx_f.write("## Detailed Citations Found in Chunks\n\n")
                # Group citations by chunk for clarity in index
                citations_by_chunk = {}
                for chunk in node['chunks']:
                    if chunk['citations']:
                        citations_by_chunk[chunk['filename']] = chunk['citations']

                for chunk_filename, citations in citations_by_chunk.items():
                     chunk_title = next((c['title'] for c in node['chunks'] if c['filename'] == chunk_filename), chunk_filename)
                     idx_f.write(f"### In Chunk: [{chunk_title}]({chunk_filename})\n\n")
                     for cit in citations:
                         idx_f.write(f"- **Citation:** `{cit['citation']}`\n")
                         idx_f.write(f"  - **Context:** (Paragraph ~{cit['paragraph_index']}) \"{cit['context_snippet']}\"\n")
                         # TODO: Add location in cited work if extractable
                         # idx_f.write(f"  - **Cited Location:** [e.g., p. 123]\n")
                     idx_f.write("\n")

        print(f"{'  ' * (node['level'] + 2)}- Wrote index: {index_filepath.name}")
    except Exception as e:
        print(f"Error writing index file {index_filepath}: {e}")
        # Add error to JSON data?

    # --- Collect Data for JSON Output ---
    # Exclude raw content from JSON, keep summaries, metadata, links, etc.
    json_node_data = {
        "level": node['level'],
        "title": node['title'],
        "path_relative": node['path'],
        "summary": node['summary'],
        "concepts": node['concepts'],
        "arguments": node['arguments'],
        "metadata": node['metadata'], # Add section specific metadata if any
        "children_paths": [child['path'] for child in node['children']],
        "chunk_files": [
            {
                "filename": chunk['filename'],
                "filepath_relative": chunk['filepath_relative'],
                "title": chunk['title'],
                "token_count": chunk['token_count'],
                "summary": chunk['summary'],
                 # Include detailed citations directly linked to chunks in JSON
                "citations": chunk['citations']
            } for chunk in node['chunks']
        ]
        # Explicitly exclude 'content', 'children', 'chunks' (full objects)
    }
    json_data_list.append(json_node_data)


# --- Main Execution Logic ---

def main():
    parser = argparse.ArgumentParser(description="Process Markdown source file hierarchically for the Hegel Philosophy Suite.")
    parser.add_argument(
        "--input_path",
        type=str,
        required=True,
        help="Path to the single input Markdown file.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Path to the base output directory (defaults to '{DEFAULT_OUTPUT_DIR}'). Processed files will be in a subdirectory named by source_id.",
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=DEFAULT_MAX_TOKENS,
        help=f"Maximum token count for each chunk (defaults to {DEFAULT_MAX_TOKENS}).",
    )
    args = parser.parse_args()

    source_file_path = Path(args.input_path)
    output_base_dir = Path(args.output_dir)
    max_tokens = args.max_tokens

    if not source_file_path.is_file() or source_file_path.suffix.lower() != ".md":
        print(f"Error: Input path '{source_file_path}' is not a valid Markdown file.")
        return

    print(f"Starting processing for: {source_file_path}")

    # --- Read Source File ---
    try:
        with open(source_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {source_file_path}: {e}")
        # TODO: Add error to JSON output
        return

    # --- Prepare Output Directory ---
    source_id = get_source_id(source_file_path)
    source_output_dir = output_base_dir / source_id
    source_output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {source_output_dir}")

    # --- Parse Structure ---
    source_metadata, sections = parse_markdown_structure(content)
    source_metadata['source_file_original'] = str(source_file_path)
    source_metadata['source_file_relative'] = source_file_path.name # Keep it simple for now
    source_metadata['source_id'] = source_id
    source_metadata['processing_timestamp'] = datetime.datetime.now().isoformat()

    if not sections:
        print("Error: No sections found in the document.")
        # TODO: Add error to JSON output
        return

    # --- Build Hierarchy ---
    section_tree_root = build_section_tree(sections)
    # Add source metadata to the root node (or handle separately in JSON)
    section_tree_root['metadata'] = source_metadata

    # --- Process Hierarchy Recursively ---
    json_data_collected = [] # List to store data for each node/chunk
    chunk_file_counter = {'count': 0} # Use dict for pass-by-reference

    # Add overall metadata to JSON list first
    json_data_collected.append({
        "type": "metadata",
        "source_id": source_id,
        "source_file_original": str(source_file_path),
        "source_file_relative": source_metadata['source_file_relative'],
        "processing_timestamp": source_metadata['processing_timestamp'],
        "root_output_directory_relative": str(source_id),
        **source_metadata # Include parsed metadata like title, author
    })

    # Process top-level sections (children of the dummy root)
    for top_level_node in section_tree_root['children']:
        top_level_node["parent_path"] = Path() # Root sections have no parent path part
        process_node_recursive(
            top_level_node,
            source_output_dir, # Pass the specific output dir for this source
            source_metadata,
            max_tokens,
            json_data_collected,
            chunk_file_counter
        )

    # --- Generate Final JSON Output ---
    final_json_output = {
        "processing_status": "success", # TODO: Add error handling
        "source_metadata": json_data_collected[0], # First item is metadata
        "hierarchy_data": json_data_collected[1:] # Rest are node/chunk data
    }

    # Print JSON to stdout
    try:
        print("\n--- JSON Output ---")
        print(json.dumps(final_json_output, indent=2))
        print("--- End JSON Output ---")
    except Exception as e:
        print(f"Error generating JSON output: {e}")

    print(f"\nFinished processing {source_file_path.name}. Total chunks: {chunk_file_counter['count']}")

if __name__ == "__main__":
    main()