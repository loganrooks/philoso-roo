# Proposal: Syllabus Integration Architecture V1

**Date:** 2025-05-07
**Author:** Architect Mode
**Version:** 1.0
**Status:** Draft
**Related Documents:**
- [`docs/proposals/source_material_architecture_v1.md`](docs/proposals/source_material_architecture_v1.md:1)
- [`docs/guides/user_guide_material_processing_workflows.md`](docs/guides/user_guide_material_processing_workflows.md:1)

## 1. Introduction

This document proposes an architecture for integrating course syllabuses into the `source_materials/` structure of the Philoso-Roo system. It builds upon the existing V1 Source Material Processed Directory Architecture and aims to address how syllabuses should be stored, processed, and how their information can be leveraged to enhance course material organization and temporal linking.

## 2. Goals

*   Define a clear storage location for raw and processed syllabuses.
*   Outline a processing workflow for syllabuses to extract key structured information.
*   Integrate syllabus information with existing course-specific indices.
*   Enable temporal organization of lectures and readings based on syllabus data.

## 3. Proposed Syllabus Integration Architecture

### 3.1. Location of Syllabuses

Syllabuses are inherently course-specific. Their storage will mirror this within the established `source_materials/` structure.

*   **Raw Syllabuses:**
    *   **Path:** `source_materials/raw/courses/[COURSE_CODE]/syllabuses/[FILENAME.ext]`
    *   **Example:** `source_materials/raw/courses/PHL316/syllabuses/PHL316_Syllabus_Fall2025.pdf`
    *   This location keeps original syllabus documents alongside other raw course materials.

*   **Processed Syllabuses:**
    *   **Path:** `source_materials/processed/courses/[COURSE_CODE]/syllabuses/[SYLLABUS_ID]/`
    *   `[SYLLABUS_ID]` will be a unique identifier for the processed syllabus, incorporating term and year to distinguish different offerings of the same course (e.g., `phl316_syllabus_fall2025_processed`, `phl316_syllabus_spring2026_processed`).
    *   This directory will contain:
        *   `index.md`: Contains metadata for the syllabus (course, term, year, instructor, link to raw version, processing date, `is_active_syllabus: true/false`, etc.) and can include a full Markdown version of the syllabus content if converted.
        *   `extracted_data.json`: A JSON file holding structured data extracted from the syllabus (see Section 3.2).
        *   `chunks/` (Optional): If the textual content of the syllabus itself is chunked for detailed NLP analysis, those chunks would reside here.
    *   **Identifying the Active Syllabus:** The `master_index.json` entry for a syllabus (and its own `index.md`) should include a boolean field like `is_active_syllabus` or a specific tag (e.g., `status:active_for_current_term`). The system (e.g., `philosophy-orchestrator` or a course-focused mode) would be responsible for ensuring only one syllabus per course offering (e.g., PHL316 Fall 2025) is marked as active. Alternatively, the most recent syllabus by `term` and `year` could be programmatically determined as active if an explicit flag is not set.

### 3.2. Processing of Syllabuses

The goal of processing syllabuses is to extract structured, actionable information that can be used by other system modes.

1.  **Initial Conversion (if needed):**
    *   Original syllabus documents (e.g., PDF, DOCX) should be converted to Markdown. This Markdown version can be stored as `source_materials/processed/courses/[COURSE_CODE]/syllabuses/[SYLLABUS_ID]/syllabus_content.md`.

2.  **Structured Data Extraction:**
    *   An AI agent (e.g., a dedicated `philosophy-syllabus-processor` mode or a general analysis mode) will be responsible for parsing the syllabus (Markdown, PDF, DOCX, etc., depending on the AI's capabilities). This AI agent will use its natural language processing and document understanding capabilities to intelligently interpret varied syllabus formats.
    *   **Information to Extract:**
        *   **Course Details:** Course code, title, instructor, term, contact information, office hours.
        *   **Weekly Schedule:** For each week/module:
            *   Week number/identifier.
            *   Dates.
            *   Topic(s).
            *   Assigned readings (titles, authors, specific sections/pages). The AI agent should attempt to match these readings to existing `material_id`s in the `master_index.json`.
            *   Associated lecture(s) (if dates/topics align).
        *   **Assignments:** Descriptions, due dates, weighting.
        *   **Grading Policy.**
        *   **Learning Outcomes.**
    *   **Output Format:** The extracted information will be stored in `extracted_data.json` within the processed syllabus directory (`source_materials/processed/courses/[COURSE_CODE]/syllabuses/[SYLLABUS_ID]/extracted_data.json`).

    ```json
    // Example: extracted_data.json snippet
    {
      "course_code": "PHL316",
      "course_title": "19th Century Philosophy",
      "term": "Fall 2025",
      "instructor": "Dr. Philosopher",
      "weekly_schedule": [
        {
          "week": 1,
          "dates": "2025-09-01 - 2025-09-05",
          "topic": "Introduction to German Idealism",
          "readings_assigned": [
            {"text": "Kant - Prolegomena, Introduction", "matched_material_id": "kant_prolegomena_intro_processed"}
          ],
          "assignments_due": []
        },
        {
          "week": 2,
          "dates": "2025-09-08 - 2025-09-12",
          "topic": "Hegel's Phenomenology: Core Concepts",
          "readings_assigned": [
            {"text": "Hegel - Phenomenology of Spirit, Preface", "matched_material_id": "hegel_phen_preface_processed"},
            {"text": "Hegel - Phenomenology of Spirit, Introduction", "matched_material_id": "hegel_phen_intro_processed"}
          ],
          "assignments_due": [
            {"name": "Reading Response 1", "due_date": "2025-09-12"}
          ]
        }
        // ... more weeks
      ],
      "grading_policy": { /* ... */ }
    }
    ```

3.  **Indexing:**
    *   An entry for the processed syllabus will be added to `source_materials/processed/master_index.json`.
    *   This entry will include `material_type: "syllabus"`, `course_code`, `term`, `year`, `is_active_syllabus` (boolean), relevant tags (e.g., `syllabus`, `[COURSE_CODE]`, `[TERM]`), and a path to its `index.md`.
    *   The `index.md` for the syllabus itself (`source_materials/processed/courses/[COURSE_CODE]/syllabuses/[SYLLABUS_ID]/index.md`) will contain metadata (including `term`, `year`, and `is_active_syllabus`) and link to the `extracted_data.json` and the `syllabus_content.md`.

### 3.3. Course Index Integration

Processed syllabus information should enrich the course-specific index file.

*   The `source_materials/processed/courses/[COURSE_CODE]/index.md` (as defined in V1 Source Material Architecture) should be updated based on the data extracted by the AI syllabus processor. This update might be proposed by the AI agent and executed by an orchestrator or another designated mode.
*   **Updates to Course `index.md`:**
    1.  Add a section listing all available syllabuses for the course, with links to their respective `.../[SYLLABUS_ID]/index.md` files.
    2.  Embed or summarize key information from the **currently active syllabus** (identified via `is_active_syllabus` flag or by selecting the most recent term/year), such as:
        *   A concise week-by-week topic list.
        *   A consolidated list of all required readings for the course, with links to their processed `material_id`s if matched.

### 3.4. Temporal Organization of Lectures and Readings

Syllabuses are key to temporally organizing course materials.

1.  **Syllabus as Primary Source:** The `extracted_data.json` from a processed syllabus provides the authoritative weekly schedule, including topics, lecture dates (implicitly or explicitly), and assigned readings for those dates/weeks.
2.  **Lecture Metadata:** Processed lectures (`.../lectures/[LECTURE_ID]/index.md`) must include a `lecture_date` in their YAML frontmatter.
3.  **Automated Tagging & Linking:**
    *   **Syllabus Tags:** The AI syllabus processor will identify and propose week-specific tags (e.g., `PHL316_Week_1`, `PHL316_Topic_GermanIdealism`) for the syllabus's entry in `master_index.json` and its own `index.md`.
    *   **Lecture Tagging:** When lectures are processed, their `lecture_date` can be used to cross-reference the relevant course syllabus's `extracted_data.json` (produced by the AI agent). The AI agent or another coordinating mode can then propose the corresponding week and topic tags for the lecture's metadata.
    *   **Reading Tagging:** Readings listed in the syllabus for a specific week can be similarly tagged by the AI agent or a coordinating mode (e.g., `PHL316_Week_1_Reading`). If a reading spans multiple weeks, it could receive multiple week tags.
    *   **Linking in `extracted_data.json`:** The `weekly_schedule` within the syllabus's `extracted_data.json` should store the `material_id`s of matched readings and lectures for each week (as shown in the example JSON above).
4.  **Discoverability:**
    *   Modes can query `master_index.json` using week-specific tags (e.g., `PHL316_Week_2`) to retrieve all associated lectures and readings.
    *   Modes can parse a syllabus's `extracted_data.json` to get a structured weekly plan, including direct links (`material_id`s) to assigned readings and relevant lectures.

## 4. Workflow Implications

*   **`philosophy-text-processor` (or new `philosophy-syllabus-processor`):**
    *   Handles conversion of raw syllabuses to Markdown (if necessary).
    *   Invokes/utilizes AI-driven logic to parse syllabus content, intelligently handling varied formats.
    *   Generates `extracted_data.json`.
    *   Creates/updates the syllabus's `index.md` in the `processed` directory.
    *   Adds/updates the syllabus entry in `master_index.json`.
    *   Updates the relevant `courses/[COURSE_CODE]/index.md` with syllabus information.
    *   Potentially re-processes or updates tags on existing lectures/readings if a new syllabus provides more accurate temporal context.
*   **Analysis Modes:**
    *   Can leverage the `extracted_data.json` to understand course structure, weekly topics, and reading sequences.
    *   Can use week-specific tags to retrieve all materials for a given week.

## 5. Conclusion

Integrating syllabuses as proposed will significantly enhance the organizational structure and temporal awareness of the Philoso-Roo system's source material management. It provides a clear pathway for extracting valuable structured data from syllabuses and using it to link lectures, readings, and topics within a course's timeline, ultimately benefiting all modes that consume and analyze these materials.