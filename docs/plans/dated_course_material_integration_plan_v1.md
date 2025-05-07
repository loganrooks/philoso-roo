# Plan: Dated Course Material & Workflow Integration V1

**Date:** 2025-05-07
**Author:** Architect Mode
**Version:** 1.0
**Status:** Draft

## 1. Introduction

This plan details the architectural and system modifications required to integrate dated course materials (lectures and readings) and support a typical course progression workflow. It builds upon the existing V18 architecture, the V1 Source Material Architecture, and the V1 Syllabus Integration Architecture. The primary goal is to enhance the system's ability to manage and utilize time-sensitive academic content.

This plan initially focuses on supporting a single "active" set of materials per course code, deferring more complex handling of multiple past offerings of the same course.

## 2. Core Objectives

1.  **Integrate Syllabus Architecture:** Fully incorporate the proposals from [`docs/proposals/syllabus_integration_architecture_v1.md`](docs/proposals/syllabus_integration_architecture_v1.md:1).
2.  **Support Dated Materials:** Enable storage, metadata handling, and association for dated lectures and assigned readings.
3.  **Support Course Workflow:** Facilitate a workflow including pre-lecture analysis of readings, lecture transcript processing, and use of secondary literature, all linked temporally.
4.  **Simplify Initial Scope:** Focus on a single "active" set of materials per course.

## 3. Detailed Plan

### 3.1. Source Material Structure Modifications

Building on [`docs/proposals/source_material_architecture_v1.md`](docs/proposals/source_material_architecture_v1.md:1) and [`docs/proposals/syllabus_integration_architecture_v1.md`](docs/proposals/syllabus_integration_architecture_v1.md:1):

*   **Raw Materials (`source_materials/raw/courses/[COURSE_CODE]/`)**:
    *   `lectures/[YYYY-MM-DD_LECTURE_TITLE_SLUG]/[FILENAME.ext]`: Store raw lecture materials (transcripts, notes, slides) in dated subdirectories. The `YYYY-MM-DD` prefix is crucial.
        *   Example: `source_materials/raw/courses/PHL316/lectures/2025-09-08_hegel_phenomenology_concepts/transcript.md`
    *   `readings/[YYYY-MM-DD_READING_TITLE_SLUG]/[FILENAME.ext]`: Store raw assigned readings similarly. If a reading spans multiple dates or is not tied to a specific lecture date but rather a week, the `YYYY-MM-DD` could represent the start of the week or the primary discussion date.
        *   Example: `source_materials/raw/courses/PHL316/readings/2025-09-08_hegel_phen_preface/Hegel_Phenomenology_Preface.pdf`
    *   `syllabuses/`: As defined in [`docs/proposals/syllabus_integration_architecture_v1.md`](docs/proposals/syllabus_integration_architecture_v1.md:29).

*   **Processed Materials (`source_materials/processed/courses/[COURSE_CODE]/`)**:
    *   `lectures/[LECTURE_ID]/`: `LECTURE_ID` should incorporate the date (e.g., `phl316_lec_2025-09-08_hegel_concepts`).
        *   `index.md`: YAML frontmatter will include `lecture_date: YYYY-MM-DD`.
    *   `readings/[READING_ID]/`: `READING_ID` should ideally incorporate the primary assigned date (e.g., `phl316_reading_2025-09-08_hegel_phen_preface`).
        *   `index.md`: YAML frontmatter will include `assigned_date: YYYY-MM-DD` (or `week_start_date`).
    *   `syllabuses/[SYLLABUS_ID]/`: As defined in [`docs/proposals/syllabus_integration_architecture_v1.md`](docs/proposals/syllabus_integration_architecture_v1.md:34).

### 3.2. Date Handling & Metadata

*   **Canonical Date Format:** `YYYY-MM-DD`.
*   **Storage in `master_index.json`**:
    *   For lectures: Add `lecture_date: "YYYY-MM-DD"`.
    *   For readings: Add `assigned_date: "YYYY-MM-DD"` (or `week_start_date`).
    *   For syllabuses: Add `term_start_date`, `term_end_date`, `year` as per syllabus proposal.
*   **Storage in individual `[ID]/index.md` YAML frontmatter**:
    *   Lectures: `lecture_date: YYYY-MM-DD`.
    *   Readings: `assigned_date: YYYY-MM-DD`.
*   **[`scripts/process_source_text.py`](scripts/process_source_text.py:1) Modifications**:
    *   Must be updated to parse the `YYYY-MM-DD` from the raw material path (e.g., from `source_materials/raw/courses/[COURSE_CODE]/lectures/[YYYY-MM-DD_...]/`).
    *   Must add the extracted date to the metadata it generates for `master_index.json` and the material's `index.md`.
    *   The script should derive the `LECTURE_ID` or `READING_ID` to include this date for clarity in the `processed` directory structure.

### 3.3. Association Logic (Lectures & Readings)

Leverage the processed syllabus as the primary source of association.

1.  **Syllabus Processing (AI-Driven):**
    *   An AI agent (e.g., a dedicated `philosophy-syllabus-processor` mode or a general analysis mode) will be responsible for parsing the raw syllabus Markdown file. Input to the AI agent will be the path to the syllabus file.
    *   The AI agent will leverage its understanding of natural language and document structure to intelligently interpret varied syllabus formats and extract structured data (weekly schedule, topics, readings, assignments, term dates) into `extracted_data.json`, as defined in [`docs/proposals/syllabus_integration_architecture_v1.md`](docs/proposals/syllabus_integration_architecture_v1.md:50).
    *   The AI agent will also be responsible for attempting to match listed readings/lectures to existing `material_id`s in `master_index.json` based on title, author, and potentially date proximity. Matched `material_id`s will be stored in the `extracted_data.json`.
    *   The AI agent will propose updates to `master_index.json` and the course `index.md` based on the processed syllabus content.
2.  **Date Matching as Fallback/Reinforcement:**
    *   If syllabus data is incomplete or matching fails, modes can associate lectures and readings by matching `lecture_date` and `assigned_date` for the same `COURSE_CODE`.
    *   A "week of" association can also be used (e.g., all readings with `assigned_date` within the week of a `lecture_date`).
3.  **Tagging for Temporal Grouping:**
    *   The AI-driven syllabus processing should also identify and propose week-specific tags (e.g., `PHL316_Week_2`, `PHL316_Topic_SelfConsciousness`) for `master_index.json` entries and individual `index.md` files for lectures and readings, facilitating temporal querying.

### 3.4. Course Progression Workflow Support

The system will support the following logical flow:

1.  **Syllabus Review (User/Mode):** User or `philosophy-orchestrator` reviews the active syllabus (`extracted_data.json`) for the upcoming week/topic.
2.  **Pre-Lecture Reading Analysis (`philosophy-pre-lecture` mode):**
    *   Identifies assigned readings for the upcoming lecture date/week from the syllabus data or by date/tag matching.
    *   Retrieves and analyzes these dated readings.
    *   Generates questions, summaries, and initial concepts, storing them in the KB with appropriate context tags (course, week, reading_id, date).
3.  **Lecture Processing (`philosophy-text-processor` mode):**
    *   Processes the lecture transcript for the specific date.
    *   Stores processed lecture chunks and metadata (including `lecture_date` and week/topic tags derived from syllabus).
4.  **Post-Lecture Analysis/Integration (`philosophy-class-analysis` mode):**
    *   Analyzes the processed lecture.
    *   Integrates lecture content with pre-lecture analysis of readings (retrieved from KB using date/week/topic tags).
    *   Identifies key concepts, arguments, and their development across readings and the lecture.
5.  **Secondary Literature Supplementation (`philosophy-secondary-lit` mode):**
    *   If needed, retrieves and analyzes relevant secondary literature based on topics/concepts identified from the lecture and primary readings for that date/week.
    *   Links secondary analysis back to primary materials in the KB.

### 3.5. Affected Components

*   **Architecture Documents:**
    *   [`docs/architecture/architecture_v18.md`](docs/architecture/architecture_v18.md:1): Update Section 3 (Source Material Org), Section 4 (Mode Responsibilities, esp. `text-processor`, `syllabus-processor`, analysis modes), Section 5 (Diagram), Section 6 (KB Entry Format - if date fields impact it beyond `master_index.json`).
    *   [`docs/proposals/source_material_architecture_v1.md`](docs/proposals/source_material_architecture_v1.md:1): Minor addendum or new version if dated subdirectory structure significantly alters V1 principles. (Likely an addendum is sufficient as V1 focuses on `processed` and this plan details `raw` and `processed` date integration).
    *   [`docs/guides/user_guide_material_processing_workflows.md`](docs/guides/user_guide_material_processing_workflows.md:1): Update to reflect new dated directory structures and workflows.
*   **Scripts:**
    *   [`scripts/process_source_text.py`](scripts/process_source_text.py:1): Updates to handle dated paths, extract dates, and include dates in metadata for lectures and readings. Its role in direct syllabus *parsing* is removed. It may still handle file system operations for syllabus entries if the AI agent only provides structured data.
    *   The previously planned `scripts/process_syllabus.py` for parsing is superseded by the AI-driven approach. Any remaining script for syllabus handling would focus on I/O or invoking the AI agent.
*   **Index Files:**
    *   `source_materials/processed/master_index.json`: Add date fields.
    *   `source_materials/processed/courses/[COURSE_CODE]/index.md`: Add syllabus section, list dated materials.
    *   Individual material `index.md` files: Add date fields in YAML.
*   **`.clinerules` Files:**
    *   `philosophy-syllabus-processor` (new or enhanced existing analysis mode): To perform AI-driven parsing of syllabus Markdown, extract structured data, and propose updates to `master_index.json` and course indices.
    *   `philosophy-text-processor`: Role in direct syllabus *parsing* is removed. May still be involved in managing syllabus file entries if not handled by the `philosophy-syllabus-processor` or orchestrator.
    *   `philosophy-orchestrator`: To manage the new course progression workflow, interpret syllabus data.
    *   Analysis Modes (`philosophy-pre-lecture`, `philosophy-class-analysis`, `philosophy-secondary-lit`): To query and utilize dated materials and syllabus-derived temporal context.
    *   Other modes interacting with source materials may need minor adjustments to recognize dated paths/metadata.

### 3.6. Simplification: Single Active Set of Materials

*   **Initial Focus:** The system will assume only one "active" version of a syllabus, lecture set, and reading list per `COURSE_CODE`.
*   **Syllabus:** The `is_active_syllabus: true` flag in the syllabus's `index.md` and `master_index.json` entry (or derivation by latest term/year) will identify the canonical syllabus for current operations.
*   **Lectures/Readings:** The system will primarily operate on lectures and readings associated with this active syllabus or those falling within the current/most recent term implied by the active syllabus.
*   **Deferral:** Advanced handling of multiple past offerings of the same course (e.g., PHL316 Fall 2024 vs. PHL316 Fall 2025) with differing syllabuses, lectures, and readings will be deferred. The proposed dated directory structure (`YYYY-MM-DD`) and `SYLLABUS_ID` (with term/year) provide a foundation for this future capability.

## 4. Next Steps

1.  Review and approve this plan.
2.  Delegate architectural document updates (to Architect mode).
3.  Delegate script modifications/creation (to Code mode).
4.  Delegate `.clinerules` updates (to relevant modes or Code mode).