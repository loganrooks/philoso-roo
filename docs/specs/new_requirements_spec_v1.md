# Hegel Philosophy Suite - New Requirements Specification V1

**Version:** 1.0
**Date:** 2025-05-01
**Status:** Draft
**Context:** This document outlines new requirements based on user feedback received [2025-05-01 19:21:04], specifically concerning source text processing and version control. This specification will inform the revision of the system architecture (target: `architecture_v12.md`) and the implementation plan (`philosophy_mode_improvement_plan_v2.md`).

---

## 1. New Mode: `philosophy-text-processor`

### 1.1. Goal

To pre-process large source texts (books, long essays, lectures) in Markdown format into a structured, indexed, and manageable format for efficient use by other philosophy modes, minimizing their context window usage.

### 1.2. Core Functionality

1.  **Input:** Accepts a path to a single Markdown file (`.md`) representing the source text.
2.  **Recursive Splitting:**
    *   Parses the Markdown file based on its header structure (`#`, `##`, `###`, etc.).
    *   Creates a hierarchical directory structure mirroring the document's logical sections (e.g., `source_materials/[source_id]/level_0/level_1_section_A/level_2_subsection_1/`).
    *   The naming convention should be generic (e.g., `level_0`, `level_1`, `level_2`...) rather than tied to specific terms like "Chapter" or "Section" to accommodate various source types. Level 0 represents the root of the document.
    *   Each terminal node (leaf) in the directory structure will contain a Markdown file representing the corresponding text chunk.
3.  **Chunk Size Constraint:** Each leaf Markdown file must contain **no more than 20,000 tokens**. If a section identified by headers exceeds this limit, it must be further subdivided intelligently (e.g., by paragraphs or smaller logical units) until all resulting chunks are below the threshold. These sub-chunks should be clearly marked as subdivisions of the original header section.
4.  **Index File Generation:**
    *   At each level of the directory hierarchy (including the root `level_0`), an `index.md` file shall be created.
    *   This `index.md` file will contain:
        *   A summary of the content covered within that directory/section.
        *   A list of key philosophical concepts discussed.
        *   A summary of the main arguments presented.
        *   Links to sub-directories or leaf files contained within.
        *   Metadata: Original source title, author (if available), section title/header.
5.  **Citation Extraction (Deepest Level):**
    *   For `index.md` files in directories containing only leaf text chunks (the deepest levels of the hierarchy), the index must also include detailed citation information extracted from the corresponding text chunks.
    *   This includes:
        *   The cited work/author.
        *   The specific location (e.g., page number, section) within the cited work.
        *   The location within the *current* source chunk where the citation occurs (e.g., line number range or paragraph identifier).
        *   A brief context snippet of the citation.
6.  **Output Location:** Processed texts will be stored in a designated directory structure, likely within `source_materials/processed/[source_id]/`. The `[source_id]` should be a unique identifier derived from the source file or metadata.

### 1.3. Implementation Considerations

1.  **Script-Based Processing:** The core splitting and file generation logic should be implemented via external scripts (e.g., Python) invoked by the mode, **not** using `write_to_file` for chunk creation due to inefficiency with large files. The mode will orchestrate the script execution.
2.  **Markdown Parsing Robustness:** The parsing logic must be robust enough to handle variations in Markdown formatting and potential inconsistencies.
3.  **Header/ToC Discrepancy Handling:** The processor should detect and log discrepancies between an explicit Table of Contents (if present) and the actual header structure found in the text. An optional interactive step or configuration could allow for correction.
4.  **Formatting Correction:** Implement a mechanism for suggesting and applying formatting corrections.
    *   *Proposal:* The AI component of the mode could identify potential formatting errors (e.g., incorrect header level). It generates a "correction manifest" file specifying the line number, the error type, and the suggested correction. A separate script function reads this manifest and applies the changes to the source *before* splitting, or potentially flags sections in the index.
5.  **Token Counting:** Accurate token counting (matching the LLM's method) is crucial for enforcing the chunk size limit.
6.  **Idempotency:** Processing the same source file multiple times should ideally produce the same output or update existing processed files intelligently.

### 1.4. Integration Points

1.  **`philosophy-orchestrator`:** Triggers the `philosophy-text-processor` when a new large source text is added or needs processing. Receives status updates and confirmation of completion.
2.  **`philosophy-evidence-manager`:**
    *   The text processor informs the evidence manager about the location and structure of the newly processed text chunks and index files.
    *   The evidence manager updates its internal knowledge base/index to reference these chunks and their metadata (summaries, concepts, arguments from `index.md`).
    *   The citation information extracted by the text processor is stored or indexed by the evidence manager for use by the citation manager.
3.  **Other Analysis Modes (e.g., `philosophy-pre-lecture`, `philosophy-class-analysis`):** Query the `philosophy-evidence-manager` to retrieve specific, relevant text chunks or index summaries instead of processing entire books, thus saving context.
4.  **`philosophy-citation-manager`:** Queries the `philosophy-evidence-manager` for the detailed citation information gathered by the text processor.

### 1.5. Configuration

*   Maximum token limit per chunk (default: 20,000).
*   Output directory base path.
*   Behavior on encountering formatting errors (e.g., log only, attempt auto-correct, request user intervention).

### 1.6. Potential Enhancements

*   Generate embeddings for chunks and summaries to facilitate semantic search via `philosophy-evidence-manager`.
*   Support for other input formats (e.g., PDF, DOCX) by integrating conversion tools before Markdown processing.
*   Cross-linking between related concepts or arguments mentioned in different index files.
*   Ability to re-process specific sections if the source Markdown is updated.

---

## 2. Version Control Integration

### 2.1. Goal

To implement a robust system for managing versions of key project artifacts, particularly essays during their drafting and revision process, and potentially processed source materials or configurations.

### 2.2. Core Requirements

1.  **Scope:** Primarily focus on versioning files within the `essay_prep/` directory, but consider applicability to `source_materials/processed/` and configuration files (`.clinerules`, `.roomodes`).
2.  **Mechanism:** Leverage Git as the underlying version control system. Assume Git is installed and available in the environment.
3.  **Workflow Integration:** Define how modes interact with the version control system.
    *   **`philosophy-essay-prep`:** Should be able to initiate versioning for a new essay, commit changes with descriptive messages (potentially AI-assisted), view history, checkout previous versions, and potentially create branches for alternative drafts.
    *   **`philosophy-draft-generator`:** When generating a new draft, it should be saved, and the `philosophy-essay-prep` mode should be prompted or automatically commit this new version.
    *   **`philosophy-citation-manager` / `philosophy-verification-agent`:** Changes made by these modes (e.g., adding citations, suggesting revisions) should result in new commits managed by `philosophy-essay-prep` or the orchestrator.
    *   **`philosophy-orchestrator`:** May coordinate commits at key stages of a workflow.
4.  **User Interaction:** Provide mechanisms for the user to trigger version control actions (commit, view history, checkout) via the orchestrator or relevant modes.
5.  **Commit Messages:** Encourage or enforce informative commit messages, potentially generated with AI assistance summarizing the changes made in that version.
6.  **Branching Strategy (Optional but Recommended):** Define a simple branching strategy if needed (e.g., a main branch for the primary essay version, feature branches for major revisions or alternative arguments).

### 2.3. Implementation Considerations

1.  **Tooling:** Modes will likely need to use the `execute_command` tool to run Git commands.
2.  **Error Handling:** Handle potential Git errors (e.g., merge conflicts, detached HEAD state) gracefully, potentially involving user intervention or delegation to a `debug` mode.
3.  **Repository Initialization:** Define the process for initializing Git repositories (e.g., one repo per essay in `essay_prep/[essay_id]/.git` or a single repo for the entire workspace). A single workspace repo is likely simpler initially.
4.  **`.gitignore`:** Ensure appropriate `.gitignore` files are used to exclude unnecessary files (e.g., temporary files, logs not meant for versioning).
5.  **Security:** Ensure no sensitive information is committed to the repository.

### 2.4. Integration Points

*   **All modes interacting with versioned files:** Need awareness of the version control system and protocols for committing changes.
*   **`philosophy-orchestrator`:** Coordinates versioning actions within larger workflows.
*   **User Interface/Interaction:** How the user interacts with versioning features.

---

## 3. Review of Potentially Affected Files (User Feedback Context)

*   **Requirement:** User requested a review of files potentially edited by a previous, possibly misconfigured, system instance due to flawed handover and context issues.
*   **Action:** This requires a separate investigation task, likely delegated to `holistic-reviewer` or `debug` mode, *after* the architecture is updated (V12) to include these new requirements. The review should cross-reference file modification timestamps with the problematic system instance's activity logs (if available in `activeContext.md` or specific mode logs).

---