# User Guide: Material Processing and System Workflows

This guide provides an overview of how to prepare raw source materials for use within the Philoso-Roo system, details the organization of the `source_materials/raw/` directory, and illustrates common system workflows through user stories.

## 1. Raw Source Material Preparation

The Philoso-Roo system primarily processes Markdown files. Raw source materials in other formats (e.g., PDF, EPUB, DOCX) must first be converted to Markdown.

### 1.1. Conversion to Markdown

*   **PDF Files:**
    *   **Tools:** Use dedicated PDF-to-Markdown converters. Many online tools or standalone software options are available (e.g., `pandoc`, Adobe Acrobat Pro).
    *   **Manual Steps:** Review the converted Markdown for formatting issues, especially for complex layouts, footnotes, and special characters. Manual cleanup is often necessary to ensure accuracy.
    *   **Best Practices:**
        *   For scanned PDFs (images of text), Optical Character Recognition (OCR) is required. Ensure the OCR quality is high.
        *   Pay attention to how headers, lists, and blockquotes are converted.
        *   Verify that footnotes and endnotes are handled appropriately (e.g., converted to inline notes or standard Markdown footnote syntax).
*   **EPUB Files:**
    *   **Tools:** `pandoc` is a highly effective command-line tool for EPUB to Markdown conversion. Calibre is another popular e-book management tool that offers conversion capabilities.
    *   **Manual Steps:** Check for consistent header levels, proper list formatting, and ensure that any embedded images or special formatting are either preserved or noted.
    *   **Best Practices:** EPUBs often have internal navigation (Table of Contents). Ensure this structure is reflected in the Markdown, typically through appropriate header usage.
*   **DOCX Files:**
    *   **Tools:** `pandoc` is excellent for DOCX to Markdown. Microsoft Word itself can save to plain text, which can then be manually formatted to Markdown, though direct conversion is usually better.
    *   **Manual Steps:** Review for correct conversion of styles (headings, bold, italics), tables, and lists.
    *   **Best Practices:** Clean up any proprietary Word formatting that doesn't translate well to Markdown.

### 1.2. Standard Markdown Format

Once converted, the Markdown file should adhere to standard Markdown syntax. The [`scripts/process_source_text.py`](scripts/process_source_text.py:1) script expects:

*   **Clear Headers:** Use `#`, `##`, `###`, etc., for section titles.
*   **Paragraphs:** Separated by a blank line.
*   **YAML Frontmatter (Optional but Recommended):** The script can parse basic YAML frontmatter for metadata like `title`, `author`, `course_code`, `material_type`, `publication_date`, and `tags`. Example:
    ```yaml
    ---
    title: "Phenomenology of Spirit - Introduction"
    author: "G.W.F. Hegel"
    course_code: "PHL316"
    material_type: "reading"
    publication_date: "1807"
    tags: ["hegel", "phenomenology", "idealism"]
    ---
    ```
    This metadata can supplement information inferred from the file path.

## 2. `source_materials/raw/` Directory

### 2.1. Purpose

The `source_materials/raw/` directory is the designated location for storing all original, unprocessed source materials before they are converted (if necessary) and processed by the [`scripts/process_source_text.py`](scripts/process_source_text.py:1) script. Keeping raw materials here ensures a clean separation between original files and their processed, chunked versions found in `source_materials/processed/`.

### 2.2. Organization and Usage Guidelines

The structure of the `source_materials/raw/` directory should mirror the intended structure of the `source_materials/processed/` directory to facilitate consistent path-based metadata extraction by the processing script.

*   **Base Path:** `source_materials/raw/`
*   **Sub-directory Structure:**
    *   **Course-Specific Materials:**
        *   Path: `source_materials/raw/courses/[COURSE_CODE]/[TYPE]/[FILENAME.ext]`
        *   `[COURSE_CODE]`: The code for the course (e.g., `PHL316`, `PHL400`).
        *   `[TYPE]`: The type of material. It is recommended to use subdirectories like:
            *   `lectures/`
            *   `readings/`
            *   `notes/`
        *   `[FILENAME.ext]`: The original filename of the raw material (e.g., `Hegel_Phenomenology_Spirit_Introduction.md`, `Lecture1_Notes.pdf`).
        *   **Example:** `source_materials/raw/courses/PHL316/readings/Hegel_Phenomenology_Spirit_Introduction.md`
    *   **General Library Materials:**
        *   Path: `source_materials/raw/library/[TYPE]/[FILENAME.ext]` (Optional `[TYPE]` subdirectory)
        *   `[TYPE]`: Optional subdirectory for type, e.g., `primary_texts/`, `secondary_literature/`.
        *   `[FILENAME.ext]`: The original filename.
        *   **Example:** `source_materials/raw/library/primary_texts/Kant_Critique_Pure_Reason.epub`
        *   Alternatively, for a flatter library structure: `source_materials/raw/library/Kant_Critique_Pure_Reason.epub`

The processing script ([`scripts/process_source_text.py`](scripts/process_source_text.py:1)) can infer `course_code` and `material_type` from the path if this structure is followed, supplementing any metadata provided in YAML frontmatter.

## 3. System Workflow User Stories

These user stories illustrate common interactions with the Philoso-Roo system:

### User Story 1: Adding and Processing a New PDF Textbook for a Course

*   **As a user (e.g., a student or researcher),**
*   **I want to** add a new PDF textbook for my "PHL316" course and process it,
*   **So that** its content is chunked, indexed, and available for analysis by the system's philosophical modes.

**Workflow Steps:**

1.  **Convert PDF to Markdown:** The user converts the PDF textbook (e.g., "Fichte_ScienceOfKnowledge.pdf") into a Markdown file ("Fichte_ScienceOfKnowledge.md") using a tool like `pandoc`. They review and clean up the Markdown.
2.  **Place Raw Material:** The user places the "Fichte_ScienceOfKnowledge.md" file into the appropriate directory: `source_materials/raw/courses/PHL316/readings/Fichte_ScienceOfKnowledge.md`.
3.  **Initiate Processing:** The user (or an automated trigger via the [`philosophy-orchestrator`](.roomodes:272)) invokes the [`philosophy-text-processor`](.roomodes:280) mode.
4.  **Script Execution:** The [`philosophy-text-processor`](.roomodes:280) mode executes [`scripts/process_source_text.py`](scripts/process_source_text.py:1), providing the path to the raw file and any necessary metadata (e.g., `--course_code PHL316 --material_type reading`).
5.  **System Processing:**
    *   The script reads the Markdown file.
    *   It determines metadata (course, type, title) from arguments and file path.
    *   It generates a unique `material_id` (e.g., `phl316_reading_fichte_scienceofknowledge_abcdef`).
    *   It creates the output directory structure: `source_materials/processed/courses/PHL316/readings/phl316_reading_fichte_scienceofknowledge_abcdef/chunks/`.
    *   It chunks the text into smaller Markdown files within the `chunks/` directory.
    *   It creates `source_materials/processed/courses/PHL316/readings/phl316_reading_fichte_scienceofknowledge_abcdef/index.md` with metadata and a list of chunks.
    *   It updates `source_materials/processed/master_index.json` with an entry for the new material.
    *   It updates `source_materials/processed/courses/PHL316/index.md` to list this new reading.
6.  **Availability:** The processed material is now available for querying and analysis by other modes via the `master_index.json` and individual index files.

### User Story 2: Finding Materials Related to a Concept

*   **As a user (e.g., a researcher),**
*   **I want to** find all processed materials (lectures, readings, library texts) related to the philosophical concept of "Absolute Idealism",
*   **So that** I can conduct a comprehensive review of how this concept is treated across different sources.

**Workflow Steps:**

1.  **Initiate Search/Query:** The user interacts with a relevant mode (e.g., [`philosophy-secondary-lit`](.roomodes:304) or a dedicated search interface if available, possibly via [`philosophy-orchestrator`](.roomodes:272)).
2.  **Mode Action (Querying `master_index.json`):**
    *   The mode reads and parses `source_materials/processed/master_index.json`.
    *   It filters entries where the `tags` array contains "absolute_idealism" (or similar relevant tags like "idealism", "hegel", "schelling" if the query is broader).
    *   It can further filter by `material_type` (e.g., only "reading" or "lecture") if specified by the user.
3.  **Mode Action (Retrieving Details):**
    *   For each matching entry in `master_index.json`, the mode uses the `path_to_index` field to locate and read the corresponding individual `[ID]/index.md` file.
    *   This provides more specific metadata, summaries, and the list of chunks for each relevant material.
4.  **Present Results:** The mode presents the user with a list of materials (titles, summaries, paths) that match the query. The user can then choose to view specific materials or chunks.
5.  **Further Analysis:** The user can then instruct analysis modes to work with these identified materials.

### User Story 3: Understanding Links Between Lecture, Source, and Concepts

*   **As a user (e.g., a student reviewing a lecture),**
*   **I want to** understand how a specific point in a lecture transcript (e.g., on "Hegel's notion of Aufhebung") is linked to the original source material it discusses and related concepts in the Knowledge Base,
*   **So that** I can deepen my understanding of the lecture content and its philosophical context.

**Workflow Steps:**

1.  **Identify Point of Interest:** The user is reviewing a processed lecture chunk, say `source_materials/processed/courses/PHL316/lectures/PHL316_lec_hegel_logic_part1/chunks/chunk_005.md`, which discusses "Aufhebung".
2.  **Mode Action (e.g., [`philosophy-class-analysis`](.roomodes:296)):**
    *   **Check Lecture Index:** The mode first consults the lecture's `index.md` (`source_materials/processed/courses/PHL316/lectures/PHL316_lec_hegel_logic_part1/index.md`). The YAML frontmatter of this index might contain:
        *   `tags` like "hegel", "logic", "aufhebung".
        *   A `related_readings` or `discusses_material_ids` field, potentially linking to the `material_id` of the primary Hegel text being discussed (e.g., `hegel_science_logic_being_processed`).
    *   **Query Knowledge Base:** The mode queries the `philosophy-knowledge-base/` for entries related to "Aufhebung". This might involve:
        *   Searching for concept files like `philosophy-knowledge-base/concepts/aufhebung.md`.
        *   Searching relationship files or a KB index for connections between "Aufhebung" and other concepts or arguments.
    *   **Cross-Reference with Source Material:** If the lecture index links to a primary source (e.g., `hegel_science_logic_being_processed`), the mode can:
        *   Access the `index.md` for that primary source.
        *   Search its chunks or metadata for mentions of "Aufhebung" or related terms.
        *   Look for `dynamic_roles` in the primary source's `index.md` or `master_index.json` entry that might link it to this specific lecture or inquiry.
3.  **Present Information:** The mode presents the user with:
    *   Links to the relevant sections in the original source material (if identified).
    *   Summaries or links to KB entries for "Aufhebung" and related concepts.
    *   Any explicit relationships defined in the KB between the lecture, the source text, and the concept.

This allows the user to trace the discussion from the lecture back to its origins and explore its conceptual underpinnings within the system's knowledge.