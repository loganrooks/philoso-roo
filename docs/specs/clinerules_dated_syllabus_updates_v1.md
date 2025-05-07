# Specification: .clinerules Updates for Dated Material & AI Syllabus Integration V1

**Date:** 2025-05-07
**Author:** Architect Mode
**Version:** 1.0
**Status:** Draft

## 1. Introduction

This document specifies the necessary modifications to the `.clinerules` files for relevant Philoso-Roo system modes to support the integration of dated course materials (lectures, readings) and AI-driven syllabus processing. These changes are based on the architectural guidelines detailed in:

*   [`docs/plans/dated_course_material_integration_plan_v1.md`](docs/plans/dated_course_material_integration_plan_v1.md:1)
*   [`docs/architecture/architecture_v18.md`](docs/architecture/architecture_v18.md:1) (specifically V18.3.7)
*   [`docs/proposals/syllabus_integration_architecture_v1.md`](docs/proposals/syllabus_integration_architecture_v1.md:1)
*   [`docs/proposals/source_material_architecture_v1.md`](docs/proposals/source_material_architecture_v1.md:1)

The goal is to enable modes to effectively manage, process, and utilize temporally-aware course content.

## 2. General Principles for `.clinerules` Updates

All affected modes should adhere to the following general principles in their updated `.clinerules`:

*   **Master Index Interaction:** Modes interacting with source materials must be capable of querying and interpreting `source_materials/processed/master_index.json`, including new date-related fields (`lecture_date`, `assigned_date`, `term_start_date`, etc.) and syllabus-specific metadata (`is_active_syllabus`).
*   **Syllabus Data Utilization:** Modes involved in course progression workflows must be able to access and utilize the structured data from `extracted_data.json` located within a processed syllabus directory (e.g., `source_materials/processed/courses/[COURSE_CODE]/syllabuses/[SYLLABUS_ID]/extracted_data.json`).
*   **Temporal Querying:** Modes should be able to perform queries based on dates, week tags (e.g., `PHL316_Week_2`), and topic tags derived from syllabuses or dated material metadata.
*   **AI Syllabus Parsing Interaction:** Modes directly involved in or consuming the output of syllabus parsing must align with the AI-driven approach. This means the primary parsing logic resides within an AI agent (e.g., `philosophy-syllabus-processor`), not in general-purpose scripts.
*   **Standard Compliance:** All `.clinerules` must adhere to the latest version of `docs/standards/clinerules_standard_v2.md`, including sections for `identity`, `description`, `input_schema`, `memory_bank_strategy`, `general_rules`, `error_handling`, and `mode_specific_workflows`.

## 3. Mode-Specific `.clinerules` Modifications

### 3.1. `philosophy-syllabus-processor` (or Designated AI Analysis Mode)

This mode is responsible for the AI-driven parsing of syllabuses.

*   **`identity`**:
    *   `name`: "Philosophy Syllabus Processor"
    *   `description`: "Parses course syllabuses using AI to extract structured data (schedule, topics, readings, assignments), matches materials, and proposes updates to system indices for temporal organization."
*   **`input_schema`**:
    ```json
    {
      "type": "object",
      "properties": {
        "syllabus_file_path": { "type": "string", "description": "Absolute or relative path to the raw syllabus file (e.g., .md, .pdf, .docx)." },
        "course_code": { "type": "string", "description": "The course code, e.g., PHL316." },
        "term": { "type": "string", "description": "The academic term, e.g., Fall, Spring." },
        "year": { "type": "integer", "description": "The academic year, e.g., 2025." },
        "is_active_syllabus": { "type": "boolean", "default": true, "description": "Indicates if this is the currently active syllabus for the course offering." }
      },
      "required": ["syllabus_file_path", "course_code", "term", "year"]
    }
    ```
*   **`mode_specific_workflows`**:
    *   **`process_syllabus`**:
        1.  **Receive Input:** Get `syllabus_file_path`, `course_code`, `term`, `year`, `is_active_syllabus`.
        2.  **Generate Syllabus ID:** Construct `SYLLABUS_ID` (e.g., `[course_code]_syllabus_[term][year]_processed`).
        3.  **Prepare Processed Directory:** Ensure `source_materials/processed/courses/[COURSE_CODE]/syllabuses/[SYLLABUS_ID]/` exists.
        4.  **Read/Convert Syllabus:**
            *   Read the content of `syllabus_file_path`.
            *   If not Markdown, convert to Markdown (this mode might delegate to a specialized MCP or have internal conversion capabilities for common formats like PDF/DOCX). Store as `syllabus_content.md` in the processed directory.
        5.  **AI-Driven Parsing:**
            *   Utilize internal AI capabilities to parse `syllabus_content.md` (or the original file if AI can handle its format directly).
            *   Extract: course details, weekly schedule (week, dates, topic, readings, assignments), grading policy, learning outcomes.
            *   For each reading/lecture identified: Attempt to match with existing `material_id`s in `master_index.json` based on title, author, and proximity to syllabus dates.
        6.  **Generate `extracted_data.json`:** Store the structured data in `source_materials/processed/courses/[COURSE_CODE]/syllabuses/[SYLLABUS_ID]/extracted_data.json`.
        7.  **Propose Index Updates (Output for Orchestrator):**
            *   **`master_index.json` update proposal:**
                *   New entry for this syllabus: `id`, `path_to_index`, `title`, `material_type: "syllabus"`, `course_code`, `term`, `year`, `is_active_syllabus`, `path_to_extracted_data`.
                *   Add temporal tags (e.g., `[COURSE_CODE]_Week_[N]`, `[COURSE_CODE]_Topic_[TOPIC_SLUG]`) to associated lecture/reading entries in `master_index.json` based on syllabus schedule and matched `material_id`s.
            *   **Course `index.md` update proposal (`source_materials/processed/courses/[COURSE_CODE]/index.md`):**
                *   Add/update section listing this syllabus.
                *   If `is_active_syllabus`, embed/summarize key info (weekly topics, consolidated readings).
            *   **Syllabus `index.md` creation (`.../[SYLLABUS_ID]/index.md`):**
                *   Metadata: `course_code`, `term`, `year`, `is_active_syllabus`, link to `extracted_data.json`, link to `syllabus_content.md`.
        8.  **Log Actions:** Update mode-specific log in `phil-memory-bank/`.
*   **`memory_bank_strategy`**: Log key actions, decisions, paths of files read/written, and summaries of proposed updates.

### 3.2. `philosophy-text-processor`

*   **`identity`**:
    *   `name`: "Philosophy Text Processor"
    *   `description`: "Orchestrates the processing of general source texts (lectures, readings) using `scripts/process_source_text.py`. Extracts date metadata for dated materials. Parses script output and performs direct KB writes. Updates relevant indices."
*   **`input_schema`**: (Ensure it includes/prioritizes)
    ```json
    {
      // ... other existing properties
      "material_date": { "type": "string", "format": "date", "description": "YYYY-MM-DD, extracted from path or provided directly for dated lectures/readings." }
    }
    ```
*   **`mode_specific_workflows`**:
    *   **`process_dated_material` (for lectures/readings):**
        1.  Receive `raw_material_path`, `course_code`, `material_type`, `material_date`, etc.
        2.  Execute [`scripts/process_source_text.py`](scripts/process_source_text.py:1) via `execute_command`, passing `--material_date [material_date]` and other relevant arguments.
        3.  Script generates processed files, `index.md` (with `lecture_date` or `assigned_date` in YAML), and updates `master_index.json` (with `lecture_date` or `assigned_date`).
        4.  Mode parses JSON output from script (if any further KB writes are its responsibility beyond script's direct `master_index.json` update).
        5.  Ensure root processed index (`source_materials/processed/index.md`) is updated.
    *   **`process_library_material` (for non-dated, non-course specific):**
        *   Existing workflow, ensure it doesn't conflict with dated material logic.
    *   **Interaction with Syllabus Processing:**
        *   This mode itself does not parse syllabuses.
        *   It may be invoked by `philosophy-orchestrator` or `philosophy-syllabus-processor` to process individual reading/lecture files identified in a syllabus if they are not yet in `master_index.json`. The `--material_date` would be derived from the syllabus context.
*   **`memory_bank_strategy`**: Log processing of dated materials, including extracted dates and generated IDs.

### 3.3. `philosophy-pre-lecture`

*   **`identity`**:
    *   `name`: "Philosophy Pre-Lecture Analyzer"
    *   `description`: "Identifies and analyzes assigned readings for upcoming lectures using syllabus data and date metadata, generating preparatory questions and concepts."
*   **`input_schema`**:
    ```json
    {
      // ... other existing properties
      "course_code": { "type": "string" },
      "reference_date": { "type": "string", "format": "date", "description": "Upcoming lecture date or start date of the week to prepare for." },
      "reference_week": { "type": "integer", "description": "Optional: Week number to prepare for." },
      "reference_topic": { "type": "string", "description": "Optional: Topic to prepare for." }
    }
    ```
*   **`mode_specific_workflows`**:
    *   **`prepare_for_lecture`**:
        1.  **Identify Active Syllabus:** Query `master_index.json` for the active syllabus for the given `course_code` (e.g., where `is_active_syllabus: true` or latest by term/year).
        2.  **Access Syllabus Data:** Read the `extracted_data.json` from the active syllabus's processed directory.
        3.  **Identify Relevant Readings:**
            *   Filter `weekly_schedule` in `extracted_data.json` based on `reference_date`, `reference_week`, or `reference_topic`.
            *   Extract `matched_material_id`s for assigned readings.
            *   Alternatively, if syllabus data is insufficient, query `master_index.json` for readings of the `course_code` with `assigned_date` matching or near `reference_date`, or matching week/topic tags.
        4.  **Analyze Readings:** For each identified reading `material_id`:
            *   Read its `index.md` and relevant chunks from `source_materials/processed/`.
            *   Perform pre-lecture analysis (summaries, key questions, initial concepts).
        5.  **Store Analysis in KB:** Write analysis to KB, tagging with `course_code`, `reference_date` (or week/topic tags), and the `material_id` of the reading.
*   **`memory_bank_strategy`**: Log identified readings, analysis performed, and KB entries created/updated.

### 3.4. `philosophy-class-analysis`

*   **`identity`**:
    *   `name`: "Philosophy Class Session Analyzer"
    *   `description`: "Analyzes processed lecture transcripts, integrating them with pre-lecture reading analysis and syllabus context to identify key conceptual developments."
*   **`input_schema`**:
    ```json
    {
      // ... other existing properties
      "course_code": { "type": "string" },
      "lecture_id": { "type": "string", "description": "Material ID of the processed lecture." },
      "lecture_date": { "type": "string", "format": "date", "description": "Date of the lecture (for context retrieval)." }
    }
    ```
*   **`mode_specific_workflows`**:
    *   **`analyze_lecture_in_context`**:
        1.  **Analyze Lecture:** Read `index.md` and chunks for the given `lecture_id`.
        2.  **Retrieve Context:**
            *   Query KB for pre-lecture analysis related to `course_code` and `lecture_date` (or associated week/topic tags from syllabus).
            *   Access active syllabus's `extracted_data.json` for the week/topic corresponding to `lecture_date`.
        3.  **Integrate & Analyze:** Synthesize lecture content with pre-reading analysis and syllabus topics.
        4.  **Store Analysis in KB:** Write integrated analysis to KB, linking to lecture, readings, and concepts, tagged with temporal context.
*   **`memory_bank_strategy`**: Log lecture analyzed, contextual data retrieved, and key findings.

### 3.5. `philosophy-secondary-lit`

*   **`identity`**:
    *   `name`: "Philosophy Secondary Literature Analyst"
    *   `description`: "Retrieves and analyzes secondary literature relevant to concepts and topics identified from primary course materials, considering their temporal context."
*   **`input_schema`**:
    ```json
    {
      // ... other existing properties
      "course_code": { "type": "string", "description": "Optional: For course-contextualized secondary lit search." },
      "current_topic": { "type": "string", "description": "Topic derived from current lecture/reading analysis." },
      "current_date_or_week_tag": { "type": "string", "description": "Date or week tag for temporal relevance." },
      "primary_material_ids": { "type": "array", "items": { "type": "string" }, "description": "IDs of primary materials being discussed." }
    }
    ```
*   **`mode_specific_workflows`**:
    *   **`find_relevant_secondary_lit`**:
        1.  **Identify Search Terms:** Based on `current_topic` and content of `primary_material_ids`.
        2.  **Query KB & External Sources:**
            *   Search `master_index.json` and KB for existing secondary literature tagged with relevant topics/authors.
            *   (If MCP enabled) Use search MCPs for external secondary literature.
        3.  **Filter by Relevance:** Prioritize secondary literature that discusses the `primary_material_ids` or is contextually relevant to `current_topic` and `current_date_or_week_tag`.
        4.  **Analyze & Link:** Analyze retrieved secondary literature and link findings to primary materials and concepts in KB.
*   **`memory_bank_strategy`**: Log search queries, retrieved literature, and links created.

### 3.6. `philosophy-orchestrator`

*   **`identity`**:
    *   `name`: "Philosophy Workflow Orchestrator"
    *   `description`: "Manages complex philosophical research workflows, including dated material processing, syllabus integration, and temporally-aware analysis sequences."
*   **`mode_specific_workflows`**:
    *   **`manage_syllabus_processing_workflow`**:
        1.  Receive trigger to process a new syllabus (e.g., from user, file system watcher).
        2.  Delegate to `philosophy-syllabus-processor` with syllabus path, course code, term, year.
        3.  Receive proposed index updates from `philosophy-syllabus-processor`.
        4.  Verify and apply updates to `master_index.json` and course `index.md`.
        5.  Potentially trigger `philosophy-text-processor` for any readings/lectures mentioned in the syllabus that are not yet processed.
    *   **`execute_course_progression_workflow`**:
        1.  Determine current week/topic based on date or user input.
        2.  Delegate to `philosophy-pre-lecture` for upcoming readings.
        3.  After lecture date, delegate lecture processing to `philosophy-text-processor`.
        4.  Delegate post-lecture analysis to `philosophy-class-analysis`.
        5.  Optionally, delegate secondary literature search to `philosophy-secondary-lit`.
*   **`memory_bank_strategy`**: Log workflow initiations, delegations, and outcomes.

## 4. Conclusion

These `.clinerules` modifications aim to equip the Philoso-Roo system modes with the necessary capabilities to handle dated course materials and leverage AI-driven syllabus processing effectively. This will enable more sophisticated, temporally-aware analysis and a richer understanding of course progression.