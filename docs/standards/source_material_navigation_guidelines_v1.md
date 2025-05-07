# Navigating and Utilizing the `source_materials/processed/` Directory V1

**Version:** 1.0
**Date:** 2025-05-06
**Status:** Standard
**Relevant Architecture:** [`docs/proposals/source_material_architecture_v1.md`](docs/proposals/source_material_architecture_v1.md:1)

## 1. Introduction

This document provides comprehensive guidelines for all modes on how to navigate and effectively utilize the V1 architecture of the `source_materials/processed/` directory. Adherence to these guidelines will ensure consistent and efficient interaction with processed philosophical texts.

## 2. Overview of the Architecture

The `source_materials/processed/` directory employs a hybrid structure:

*   **Hierarchical Organization:** Top-level directories distinguish between `courses/` (for course-specific materials) and `library/` (for general research materials).
*   **Unique Identifiers (`material_id`):** Each processed item (lecture, reading, note, library material) has a unique `material_id` used in its directory name (e.g., `hegel_phenomenology_spirit_intro_processed`). The data field for this in index files is `id`.
*   **Master Index (`master_index.json`):** A global, machine-readable JSON index of all processed materials, located at the root of `source_materials/processed/`.
*   **Individual Material Indexes (`[ID]/index.md`):** Markdown files within each material's directory, containing detailed metadata and a list of its text chunks.
*   **Course Indexes (`courses/[COURSE_CODE]/index.md`):** Markdown files listing all processed materials for a specific course.
*   **Chunked Content:** Actual text content is stored in `[ID]/chunks/chunk_XXX.md` files.

## 3. Interpreting and Using Index Files

### 3.1. Master Index (`master_index.json`)

*   **Location:** `source_materials/processed/master_index.json`
*   **Purpose:** The primary entry point for discovering and filtering processed materials across the entire collection.
*   **Format:** A JSON array of objects, each representing one processed material.
*   **Key Fields per Entry:**
    *   `id`: Unique `material_id` (matches directory name).
    *   `path_to_index`: Relative path to the material's individual `index.md`.
    *   `title`: Full title of the processed material.
    *   `original_path`: Path to the raw source material.
    *   `material_type`: Type of material (e.g., `lecture`, `reading`, `note`, `library_material`).
    *   `source_type`: Broader category (e.g., `course_material`, `library_primary`, `library_secondary`, `personal_note`).
    *   `course_code`: Applicable course code (e.g., `PHL316`).
    *   `authors`: Array of author names.
    *   `work_title`: Title of the larger work, if applicable.
    *   `section_title`: Specific section processed, if applicable.
    *   `publication_date`: Original publication/lecture date.
    *   `processing_date`: Date the material was processed.
    *   `chunk_count`: Number of text chunks.
    *   `summary`: Brief summary of the material.
    *   `tags`: Array of static keywords (see Section 5).
    *   `dynamic_roles`: Array of objects defining the material's role in specific contexts (see Section 5.2). Updates to this field are managed by the `philosophy-orchestrator`.
*   **Usage:**
    *   **Targeted Retrieval:** Query this file (e.g., using JSON parsing tools or MCPs if available) to find materials matching specific criteria (author, title, tags, course code).
    *   **Exploratory Research:** Scan entries to discover materials related to a broad topic or author.
    *   **Context Management:** When querying, request only necessary fields to minimize context window impact if the file is very large. If the entire file is too large to load, modes should indicate this and request a strategy (e.g., querying via an MCP, or targeted `read_file` with line numbers if the structure is known to be relatively static and the system can assist).

### 3.2. Individual Material Index (`[ID]/index.md`)

*   **Location:** `source_materials/processed/[path_to_material]/[material_id]/index.md` (e.g., `source_materials/processed/library/kant_cpr_b_edition_processed/index.md`)
*   **Purpose:** Provides detailed metadata and a navigable list of text chunks for a *specific* processed material.
*   **Format:** Markdown with YAML frontmatter.
*   **YAML Frontmatter:** Contains a subset of metadata from `master_index.json` relevant to the specific item (e.g., `id` (which stores the `material_id`), `title`, `authors`, `tags`, `summary`, `chunk_count`) and a `list_of_chunks`.
    *   `list_of_chunks`: An array of objects, each with:
        *   `file`: Path to the chunk (e.g., `chunks/chunk_001.md`).
        *   `summary`: Brief summary of the chunk's content.
        *   `keywords`: Array of keywords specific to the chunk.
*   **Markdown Body:** A human-readable list of links to each chunk file, often with the chunk summary.
*   **Usage:**
    *   After identifying a relevant material via `master_index.json`, read this file to get specific metadata and the list of its chunks.
    *   Use the `list_of_chunks` (either from YAML or by parsing the Markdown body) to navigate to and read specific text chunks.

### 3.3. Course Index (`courses/[COURSE_CODE]/index.md`)

*   **Location:** `source_materials/processed/courses/[COURSE_CODE]/index.md` (e.g., `source_materials/processed/courses/PHL316/index.md`)
*   **Purpose:** Lists all processed lectures, readings, and notes for a specific course.
*   **Format:** Markdown.
*   **Content:** Typically a list of links to the individual `index.md` files of materials belonging to that course, possibly organized by material type (lectures, readings, notes).
*   **Usage:**
    *   When focusing on a specific course, this file can be a more direct entry point than `master_index.json` to see all available materials for that course.

## 4. Best Practices for Research and Retrieval

### 4.1. Targeted Information Retrieval

1.  **Start with `master_index.json`:** Formulate a query based on known information (author, title, specific keywords/tags, course).
2.  **Filter `master_index.json`:** Identify entries matching your query. Extract the `path_to_index` for relevant materials.
3.  **Read Individual `[ID]/index.md`:** For each relevant material, read its `index.md` to review detailed metadata and the `list_of_chunks`.
4.  **Access Chunks:** Use the chunk list to read specific `chunks/chunk_XXX.md` files containing the desired text.

### 4.2. Exploratory Research

1.  **Broad Scan of `master_index.json`:**
    *   Filter by broad topic tags (e.g., `topic:idealism`, `topic:ethics`).
    *   Filter by author (e.g., `author:kant`).
    *   Browse titles and summaries.
2.  **Course-Specific Exploration:**
    *   Read `courses/[COURSE_CODE]/index.md` to get an overview of materials for a particular course.
    *   From there, navigate to individual material `index.md` files that seem relevant.
3.  **Follow Connections:**
    *   Once a relevant material or chunk is found, its tags or summary might suggest related topics or authors to explore further in `master_index.json`.
    *   Examine `dynamic_roles` to see how a material has been used in other inquiries or essays, potentially leading to related lines of research.

## 5. Understanding and Using the Tagging System

Tags are crucial for filtering and locating relevant information. They are primarily found in the `tags` and `dynamic_roles` arrays within `master_index.json` and mirrored in the YAML frontmatter of individual `[ID]/index.md` files.

### 5.1. Static Tags (in `tags` array)

These are general keywords assigned during processing or by subsequent analysis.

*   **Standardized Prefixes (Recommended):**
    *   `course:[COURSE_CODE]` (e.g., `course:PHL316`)
    *   `topic:[TOPIC_NAME]` (e.g., `topic:being`, `topic:epistemology`)
    *   `author:[AUTHOR_NAME]` (e.g., `author:hegel`)
    *   `work:[WORK_TITLE_SLUG]` (e.g., `work:phenomenology-of-spirit`)
    *   `material_type:[TYPE]` (e.g., `material_type:lecture`, `material_type:primary_text`)
    *   `date:[YYYY]` or `date:[YYYY-MM-DD]`
*   **Custom Tags:** Other relevant keywords (e.g., `kant_critique`, `german_idealism`).
*   **Usage:** Use these tags in `master_index.json` queries to narrow down searches.

### 5.2. Dynamic Roles (in `dynamic_roles` array)

This system allows a material's role (e.g., primary, secondary) to be defined *relative to a specific context*.

*   **Format:** An array of objects, each with:
    *   `context_id`: An identifier for the context (e.g., `inquiry_id:inq_001_hegel_self_consciousness`, `essay_id:essay_003_hegel_vs_kant`, `concept_id:being`).
    *   `role`: The role of the material in that context (e.g., `primary_source`, `secondary_source`, `key_text`, `critique`, `supporting_evidence`).
*   **Example:**
    ```json
    "dynamic_roles": [
      {"context_id": "inquiry:hegel_being_sol", "role": "primary_source"},
      {"context_id": "essay:hegel_vs_kant_epistemology", "role": "key_text_hegel"}
    ]
    ```
*   **Usage:**
    *   When working within a specific inquiry or on a particular essay, modes can query `master_index.json` for materials that have been assigned a relevant role for that `context_id`.
    *   Analysis modes are responsible for proposing updates to these `dynamic_roles` to the `philosophy-orchestrator`, which manages the actual updates in `master_index.json` (and the corresponding individual `[material_id]/index.md`) as they determine a material's relevance to their current task.

## 6. Navigating the Folder Structure

*   **Top Level:**
    *   `source_materials/processed/courses/`: Contains materials specific to academic courses.
    *   `source_materials/processed/library/`: Contains general research materials.
*   **Course Materials:**
    *   `courses/[COURSE_CODE]/`: Navigate here for all materials related to a specific course.
    *   `courses/[COURSE_CODE]/index.md`: Read this first for an overview of the course's processed materials.
    *   `courses/[COURSE_CODE]/lectures/`, `readings/`, `notes/`: Further sub-organization by material type.
    *   `courses/[COURSE_CODE]/[TYPE]/[ID]/`: Directory for a specific processed item. Contains its `index.md` and `chunks/` subdirectory.
*   **Library Materials:**
    *   `library/[MATERIAL_ID]/`: Directory for a specific processed library item. Contains its `index.md` and `chunks/` subdirectory.
*   **General Navigation Strategy:**
    1.  Use `master_index.json` for initial discovery and filtering.
    2.  Use the `path_to_index` field from a `master_index.json` entry to locate the specific material's `index.md`.
    3.  Use the material's `index.md` to understand its structure and access its `chunks/`.

## 7. Considerations for Different Material Types

*   **Course-Specific Materials (Lectures, Readings, Notes for a Course):**
    *   Always check the `courses/[COURSE_CODE]/index.md` for a curated list.
    *   Tags like `course:[COURSE_CODE]` and potentially module/week tags (e.g., `PHL316_W2`) will be important for filtering in `master_index.json`.
    *   `dynamic_roles` will be particularly useful for tracking how these materials are used across different assignments or research questions within the course context.
*   **General Library Texts (Primary and Secondary):**
    *   These reside in `library/`.
    *   `material_type` and `source_type` tags in `master_index.json` help distinguish them.
    *   `dynamic_roles` are essential for defining their primary/secondary status relative to a specific research query, as a text might be primary for one question and secondary for another.

## 8. Conclusion

This V1 architecture and its associated navigation guidelines aim to provide a robust and flexible system for managing processed source materials. By understanding and utilizing the directory structure, index files, and tagging system as described, all modes can interact with these materials more effectively and efficiently. Future revisions to these guidelines will be made as the system evolves.