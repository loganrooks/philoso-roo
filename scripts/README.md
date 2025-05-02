# Script Documentation: `process_source_text.py`

## Overview

This Python script (`process_source_text.py`) is designed to process large Markdown source texts, specifically for the Hegel Philosophy Suite project. It performs the following main functions:

1.  **Parses** input Markdown files.
2.  **Splits** the text into sections based on Markdown headers (`#`, `##`, `###`).
3.  **Chunks** these sections into smaller, manageable pieces based on a maximum token count, attempting to respect paragraph boundaries.
4.  **Extracts** potential citations (e.g., `(Author, YYYY, p. #)`, `§#`) within each chunk.
5.  **Generates** an `index.md` file for each processed source file, containing summaries, key concepts (placeholder), links to the generated chunk files, and metadata.
6.  **Outputs** the processed chunks and index files into a structured directory (`source_materials/processed/[source_file_name]/`).

## Dependencies

The script requires several Python libraries. These are listed in the `requirements.txt` file.

To install the dependencies, navigate to the `scripts/` directory in your terminal and run:

```bash
pip install -r requirements.txt
```

## Usage

The script is run from the command line.

```bash
python process_source_text.py <input_path> [options]
```

**Arguments:**

*   `<input_path>` (Required):
    *   Path to a single input Markdown file (`.md`).
    *   Path to a directory containing Markdown files. If a directory is provided, the script will scan it for `.md` files. By default, it scans only the top level; use the `-r` flag for recursive scanning.
*   `-o` or `--output` (Optional):
    *   Specifies the base directory where processed output will be saved.
    *   Defaults to `../source_materials/processed` (relative to the `scripts` directory).
    *   Each source file will have its own subdirectory created within this base directory (e.g., `../source_materials/processed/my_source_file/`).
*   `-t` or `--max-tokens` (Optional):
    *   Sets the target maximum number of tokens per chunk.
    *   Defaults to `1500`. The script uses the `cl100k_base` encoding via `tiktoken` for counting.
*   `-r` or `--recursive` (Optional):
    *   If the `<input_path>` is a directory, this flag enables recursive searching for `.md` files within subdirectories.

**Examples:**

1.  **Process a single file:**
    ```bash
    python process_source_text.py ../Readings/Mar11/Hegel_PhenomenologyOfSpirit_SS483-487.md
    ```
    *(Output will go to `../source_materials/processed/Hegel_PhenomenologyOfSpirit_SS483-487/`)*

2.  **Process all `.md` files in a directory (non-recursively) with custom output:**
    ```bash
    python process_source_text.py ../Readings/Mar18/ -o ../my_custom_output
    ```

3.  **Process all `.md` files in a directory recursively with a different token limit:**
    ```bash
    python process_source_text.py ../source_materials/raw/ -r -t 1000
    ```
    *(Output will go to `../source_materials/processed/`)*

## Processing Logic Overview

1.  **Argument Parsing:** Reads command-line arguments for input, output, token limit, and recursion.
2.  **File Discovery:** Identifies the `.md` file(s) to be processed based on the input path and recursion flag.
3.  **File Reading:** Reads the content of each source Markdown file.
4.  **Header Splitting:** Uses regex to identify Markdown headers (`#`, `##`, `###`) and splits the content into logical sections based on these headers.
5.  **Chunking:**
    *   Each section is further divided into paragraphs.
    *   Paragraphs are iteratively added to a chunk until the `max_tokens` limit is approached.
    *   The script attempts to avoid splitting paragraphs mid-way, but very large paragraphs might be placed in their own chunk even if exceeding the limit.
6.  **Citation Extraction:** Applies predefined regular expressions to the content of each chunk to find potential citation patterns.
7.  **Metadata & Indexing:**
    *   For each chunk, metadata (title, source section, token count, citations) is stored.
    *   For each section, a simple summary is generated (placeholder).
    *   An `index.md` file is created for the source file, listing all sections with their summaries and links to the corresponding chunk files. A list of all chunks with details is also included.
8.  **File Writing:**
    *   Creates the necessary output directories (`output_base_dir / source_file_stem /`).
    *   Writes each processed chunk to its own Markdown file (`chunk_xxxx.md`) within the source file's directory. Chunk files include metadata headers.
    *   Writes the generated `index.md` file to the source file's directory.

## Notes

*   The summary and key concept generation are currently placeholders and produce very basic output. This functionality may be enhanced in future versions or delegated to other modes/tools.
*   The header splitting logic assumes headers start at the beginning of a line.
*   The chunking logic prioritizes respecting paragraph boundaries but may create oversized chunks if a single paragraph exceeds the token limit.