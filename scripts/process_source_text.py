import argparse
import os
import re
import datetime
from pathlib import Path
from markdown_it import MarkdownIt
from mdit_plain.renderer import PlainTextRenderer
import tiktoken

# --- Constants ---
# Using a common model for token counting, adjust if needed
TOKEN_ENCODING = "cl100k_base"
DEFAULT_MAX_TOKENS = 1500  # Target chunk size in tokens
OUTPUT_DIR_BASE = "source_materials/processed"
RAW_DIR_BASE = "source_materials/raw" # Default input if not specified

# --- Regex Patterns ---
# Basic citation patterns (can be expanded)
CITATION_PATTERNS = [
    re.compile(r'\((?:[^),]+,)?\s*\d{4}(?:,\s*pp?\.\s*\d+(?:-\d+)?)?\)', re.IGNORECASE), # (Author, YYYY, p. #), (YYYY, p. #), (YYYY)
    re.compile(r'§\s*\d+'), # §#
    # Add more specific patterns if needed
]
HEADER_PATTERN = re.compile(r'^(#+)\s+(.*)', re.MULTILINE)

# --- Helper Functions ---

def count_tokens(text: str, encoding_name: str = TOKEN_ENCODING) -> int:
    """Counts the number of tokens in a text string using tiktoken."""
    try:
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(text))
        return num_tokens
    except Exception as e:
        print(f"Error counting tokens: {e}")
        # Fallback or alternative counting method if tiktoken fails
        return len(text.split()) # Simple word count as fallback

def extract_citations(text: str) -> list[str]:
    """Extracts potential citations from a text block."""
    citations_found = []
    for pattern in CITATION_PATTERNS:
        citations_found.extend(pattern.findall(text))
    return sorted(list(set(citations_found))) # Return unique citations

def get_plain_text(md_content: str) -> str:
    """Converts Markdown content to plain text."""
    md = MarkdownIt(renderer_cls=PlainTextRenderer)
    return md.render(md_content).strip()

def generate_summary(text: str, max_length: int = 300) -> str:
    """Generates a simple summary (first N characters). Placeholder."""
    plain_text = get_plain_text(text)
    return plain_text[:max_length].replace('\n', ' ') + "..." if len(plain_text) > max_length else plain_text

def generate_key_concepts(text: str) -> list[str]:
    """Placeholder for key concept extraction."""
    # In a real scenario, this would involve NLP techniques.
    # For now, return empty or very basic extraction.
    return []

def split_into_paragraphs(text: str) -> list[str]:
    """Splits text into paragraphs based on double newlines."""
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]

def chunk_section(section_content: str, section_title: str, max_tokens: int) -> list[dict]:
    """
    Chunks a section of Markdown text based on max_tokens, trying to respect paragraphs.

    Returns:
        A list of dictionaries, each representing a chunk with 'title', 'content', 'token_count', 'citations'.
    """
    chunks = []
    current_chunk_content = ""
    current_chunk_tokens = 0
    chunk_index = 1

    paragraphs = split_into_paragraphs(section_content)

    for paragraph in paragraphs:
        paragraph_tokens = count_tokens(paragraph)

        # If a single paragraph exceeds max_tokens, split it (simple split for now)
        if paragraph_tokens > max_tokens:
            # If there's content in the current chunk, save it first
            if current_chunk_content:
                chunk_title = f"{section_title} (Chunk {chunk_index})"
                chunk_citations = extract_citations(current_chunk_content)
                chunks.append({
                    "title": chunk_title,
                    "content": current_chunk_content.strip(),
                    "token_count": current_chunk_tokens,
                    "citations": chunk_citations
                })
                current_chunk_content = ""
                current_chunk_tokens = 0
                chunk_index += 1

            # Simple split of the large paragraph (could be improved)
            # For now, just make it its own chunk, even if oversized
            chunk_title = f"{section_title} (Chunk {chunk_index})"
            chunk_citations = extract_citations(paragraph)
            chunks.append({
                "title": chunk_title,
                "content": paragraph,
                "token_count": paragraph_tokens,
                "citations": chunk_citations
            })
            chunk_index += 1
            continue # Move to the next paragraph

        # Check if adding the next paragraph exceeds the limit
        if current_chunk_tokens + paragraph_tokens <= max_tokens:
            current_chunk_content += paragraph + "\n\n"
            current_chunk_tokens += paragraph_tokens
        else:
            # Finish the current chunk
            if current_chunk_content:
                chunk_title = f"{section_title} (Chunk {chunk_index})"
                chunk_citations = extract_citations(current_chunk_content)
                chunks.append({
                    "title": chunk_title,
                    "content": current_chunk_content.strip(),
                    "token_count": current_chunk_tokens,
                    "citations": chunk_citations
                })
                chunk_index += 1

            # Start a new chunk with the current paragraph
            current_chunk_content = paragraph + "\n\n"
            current_chunk_tokens = paragraph_tokens

    # Add the last remaining chunk
    if current_chunk_content:
        chunk_title = f"{section_title} (Chunk {chunk_index})"
        chunk_citations = extract_citations(current_chunk_content)
        chunks.append({
            "title": chunk_title,
            "content": current_chunk_content.strip(),
            "token_count": current_chunk_tokens,
            "citations": chunk_citations
        })

    return chunks

def process_file(source_path: Path, output_base_dir: Path, max_tokens: int):
    """Processes a single Markdown source file."""
    print(f"Processing file: {source_path.name}...")
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {source_path}: {e}")
        return

    # Create output directory for this file
    file_output_dir = output_base_dir / source_path.stem
    file_output_dir.mkdir(parents=True, exist_ok=True)

    index_data = {
        "source_file": str(source_path.relative_to(source_path.parent.parent)), # Relative path from RAW_DIR_BASE assumed parent
        "processing_date": datetime.datetime.now().isoformat(),
        "sections": []
    }
    all_chunks_info = []
    chunk_counter = 0

    # Split by headers first
    sections = []
    last_pos = 0
    current_level = 0
    current_title = source_path.stem # Default title if no headers
    current_content = ""

    # Find all headers
    headers = [(match.group(1), match.group(2), match.start()) for match in HEADER_PATTERN.finditer(content)]

    if not headers:
        # If no headers, treat the whole file as one section
        sections.append({"title": current_title, "content": content, "level": 0})
    else:
        # Add content before the first header if any
        if headers[0][2] > 0:
             sections.append({"title": current_title, "content": content[:headers[0][2]].strip(), "level": 0})

        # Process content between headers
        for i, (level_hashes, title, start_pos) in enumerate(headers):
            level = len(level_hashes)
            # Get content from the end of the previous header/start to the beginning of this one
            section_content = content[last_pos:start_pos].strip()

            # Find the *actual* title and content of the *previous* section
            if i > 0:
                prev_level_hashes, prev_title, prev_start_pos = headers[i-1]
                prev_level = len(prev_level_hashes)
                # The content belongs to the *previous* header found
                sections.append({
                    "title": prev_title.strip(),
                    "content": section_content,
                    "level": prev_level
                })

            last_pos = start_pos + len(level_hashes) + len(title) + 1 # Position after the header line

        # Add the content after the last header
        last_header_level_hashes, last_header_title, last_header_start_pos = headers[-1]
        last_header_level = len(last_header_level_hashes)
        sections.append({
            "title": last_header_title.strip(),
            "content": content[last_pos:].strip(),
            "level": last_header_level
        })


    # Process each section: chunk, extract info, write chunks
    for section in sections:
        section_title = section["title"]
        section_content = section["content"]
        section_level = section["level"]

        if not section_content.strip():
            continue

        section_chunks = chunk_section(section_content, section_title, max_tokens)

        section_summary = generate_summary(section_content)
        section_key_concepts = generate_key_concepts(section_content)
        section_chunk_links = []

        for i, chunk_data in enumerate(section_chunks):
            chunk_counter += 1
            chunk_filename = f"chunk_{chunk_counter:04d}.md"
            chunk_filepath = file_output_dir / chunk_filename
            chunk_title = chunk_data['title']
            chunk_content = chunk_data['content']
            chunk_token_count = chunk_data['token_count']
            chunk_citations = chunk_data['citations']

            try:
                with open(chunk_filepath, 'w', encoding='utf-8') as cf:
                    cf.write(f"# {chunk_title}\n\n")
                    cf.write(f"*Source Section:* {section_title}\n")
                    cf.write(f"*Source File:* {index_data['source_file']}\n")
                    cf.write(f"*Token Count:* ~{chunk_token_count}\n")
                    if chunk_citations:
                        cf.write(f"*Potential Citations:* {', '.join(chunk_citations)}\n")
                    cf.write("\n---\n\n")
                    cf.write(chunk_content)
                print(f"  - Wrote chunk: {chunk_filepath.name}")
                chunk_link = f"[{chunk_title}]({chunk_filename})"
                section_chunk_links.append(chunk_link)
                all_chunks_info.append({
                    "filename": chunk_filename,
                    "title": chunk_title,
                    "section_title": section_title,
                    "token_count": chunk_token_count,
                    "citations": chunk_citations
                })
            except Exception as e:
                print(f"Error writing chunk file {chunk_filepath}: {e}")

        index_data["sections"].append({
            "title": section_title,
            "level": section_level,
            "summary": section_summary,
            "key_concepts": section_key_concepts,
            "chunk_links": section_chunk_links
        })

    # Generate and write the index file
    index_filepath = file_output_dir / "index.md"
    try:
        with open(index_filepath, 'w', encoding='utf-8') as idx_f:
            idx_f.write(f"# Index for: {index_data['source_file']}\n\n")
            idx_f.write(f"*Processed on:* {index_data['processing_date']}\n")
            idx_f.write(f"*Total Chunks:* {chunk_counter}\n\n")
            idx_f.write("---\n\n")
            idx_f.write("## Sections Overview\n\n")

            for section in index_data["sections"]:
                indent = "  " * (section['level']) # Indent based on header level
                idx_f.write(f"{indent}### {section['title']}\n\n")
                idx_f.write(f"{indent}- **Summary:** {section['summary']}\n")
                if section['key_concepts']:
                    idx_f.write(f"{indent}- **Key Concepts:** {', '.join(section['key_concepts'])}\n")
                if section['chunk_links']:
                    idx_f.write(f"{indent}- **Chunks:** {', '.join(section['chunk_links'])}\n")
                idx_f.write("\n")

            idx_f.write("---\n\n")
            idx_f.write("## All Chunks\n\n")
            for chunk_info in all_chunks_info:
                 idx_f.write(f"- [{chunk_info['title']}]({chunk_info['filename']}) "
                             f"(Section: {chunk_info['section_title']}, Tokens: ~{chunk_info['token_count']})\n")
                 if chunk_info['citations']:
                     idx_f.write(f"  - Citations: {', '.join(chunk_info['citations'])}\n")


        print(f"  - Wrote index: {index_filepath.name}")
    except Exception as e:
        print(f"Error writing index file {index_filepath}: {e}")

    print(f"Finished processing {source_path.name}.")


# --- Main Execution ---

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Process Markdown source files for the Hegel Philosophy Suite.")
    parser.add_argument(
        "input_path",
        type=str,
        help=f"Path to the input Markdown file or directory containing Markdown files (defaults to scanning '{RAW_DIR_BASE}' if directory).",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=OUTPUT_DIR_BASE,
        help=f"Path to the base output directory (defaults to '{OUTPUT_DIR_BASE}'). Processed files will be in subdirectories.",
    )
    parser.add_argument(
        "-t", "--max-tokens",
        type=int,
        default=DEFAULT_MAX_TOKENS,
        help=f"Maximum token count for each chunk (defaults to {DEFAULT_MAX_TOKENS}).",
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Recursively search for .md files in the input directory.",
    )
    return parser.parse_args()

def main():
    """Main function to orchestrate the processing."""
    args = parse_arguments()

    input_path = Path(args.input_path)
    output_base_dir = Path(args.output)
    max_tokens = args.max_tokens

    if not input_path.exists():
        print(f"Error: Input path '{input_path}' does not exist.")
        return

    files_to_process = []
    if input_path.is_file():
        if input_path.suffix.lower() == ".md":
            files_to_process.append(input_path)
        else:
            print(f"Error: Input file '{input_path}' is not a Markdown file (.md).")
            return
    elif input_path.is_dir():
        print(f"Scanning directory: {input_path}")
        if args.recursive:
            files_to_process.extend(sorted(input_path.rglob("*.md")))
        else:
            files_to_process.extend(sorted(input_path.glob("*.md")))
    else:
         print(f"Error: Input path '{input_path}' is neither a file nor a directory.")
         return

    if not files_to_process:
        print(f"No Markdown files found to process in '{input_path}'.")
        return

    print(f"Found {len(files_to_process)} Markdown file(s) to process.")

    output_base_dir.mkdir(parents=True, exist_ok=True)

    for file_path in files_to_process:
        process_file(file_path, output_base_dir, max_tokens)

    print("\nProcessing complete.")

if __name__ == "__main__":
    main()