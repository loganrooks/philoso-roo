# Hegel Philosophy RooCode Suite - V18.3 Requirements Specification

**Date:** 2025-05-02
**Version:** 1.0
**Status:** Draft
**Based On:**
*   `docs/architecture/architecture_v18.md` (Version 18.3)
*   `docs/specs/v14_requirements_spec_v1.md` (Detail Level Reference)

**Goal:** This document provides detailed functional requirements and specifications for the V18.3 architecture of the Hegel Philosophy RooCode Suite. It translates the design outlined in `docs/architecture/architecture_v18.md` into actionable specifications for implementation, focusing on philosophical rigor, direct knowledge base (KB) access, direct operational context access, and refined workflows.

## 1. Overview

V18.3 builds upon previous versions by integrating enhanced philosophical rigor mechanisms, simplifying access patterns, and detailing operational procedures. Key features include:

*   **Enhanced Philosophical Rigor:** Specific KB fields and mode responsibilities for tracking determinacy, presuppositions, counter-arguments, etc.
*   **Direct KB Access:** Modes interact directly with the `philosophy-knowledge-base/` using file system tools, following defined patterns.
*   **Direct Operational Context Access:** Modes interact directly with `phil-memory-bank/` for reading context and writing logs, removing the need for a dedicated manager mode.
*   **KB Doctor (Maintenance):** A non-gatekeeping mode (`philosophy-kb-doctor`) orchestrates KB maintenance and rigor validation scripts.
*   **Refined Workflows:** Detailed specifications for inquiry, analysis, verification, self-reflection, failure handling, and user interaction patterns.
*   **Strict Separation:** Maintained separation between domain knowledge (`philosophy-knowledge-base/`) and operational context (`phil-memory-bank/`).
*   **Source Context Handling:** Retained V14 mechanism for organizing source materials and tagging KB entries with context.

## 2. Source Material Handling Specifications (V14 Retained, V18.3 Paths)

### 2.1. Raw Source Material Organization

*   **Location:** All raw source materials MUST be placed within the `source_materials/raw/` directory.
*   **Structure:** The directory structure under `source_materials/raw/` MUST follow a hierarchical pattern using forward slashes (`/`) to define context. (See `docs/architecture/architecture_v18.md`, Section 3 for detailed structure).
*   This structure MUST be extensible.

### 2.2. Context Extraction (`philosophy-text-processor`)

*   The `philosophy-text-processor` mode (via its scripts) MUST:
    *   Accept file paths within `source_materials/raw/`.
    *   Parse the directory path relative to `source_materials/raw/` to extract context information (`context_type`, `context_id`, `context_subtype`).
    *   Format extracted context as `context:key:value` tags (e.g., `context:type:course`, `context:id:PHL316`, `context:subtype:reading`).
    *   Pass these tags along with processed chunks, index data, and citation data when interacting with the KB (see Section 6.4).

### 2.3. Context Storage (KB Entries)

*   When KB entries are created or updated based on processed source material, the generating mode (or `text-processor` via its output) MUST ensure the `context:key:value` tags are included in the `tags` list within the entry's YAML frontmatter.

### 2.4. Contextual Querying (Modes)

*   Modes querying the KB (directly via file tools like `search_files`) MUST be able to filter results based on `context:key:value` tags present in the YAML frontmatter.
*   Query logic (implemented within mode rules or helper functions) SHOULD support combinations (AND/OR) of context tags and other filters (e.g., keywords, `type`).
    *   `// Pseudocode Anchor: Function search_kb(filters: Dict) -> List[KBEntry]`
    *   `// TDD Anchor: Test search_kb with context:id filter`
    *   `// TDD Anchor: Test search_kb with multiple context tags (AND)`

## 3. Philosophy Knowledge Base (KB) Specifications (V18.3)

### 3.1. Purpose & Location

*   **Purpose:** Centralized, structured, persistent repository for philosophical domain knowledge, enhanced for rigor, separate from operational context.
*   **Location:** `philosophy-knowledge-base/`.

### 3.2. Management & Access (Direct Access Model)

*   **Read Access:** Modes MUST read KB data directly using file system tools (`read_file`, `search_files`). Modes are responsible for locating relevant files based on ID, type (subdirectory), tags, or index files.
*   **Write Access:** Modes responsible for creating/updating KB content MUST write directly to the appropriate subdirectory and file within `philosophy-knowledge-base/`, following defined naming conventions and the entry format specified below. Tools like `write_to_file` or `apply_diff` should be used.
    *   `// Pseudocode Anchor: Function write_kb_entry(entry: KBEntry)`
    *   `// TDD Anchor: Test writing a new Concept entry`
    *   `// TDD Anchor: Test updating an Argument entry using apply_diff`
*   **Maintenance:** Orchestrated by `philosophy-kb-doctor` via scripts within `philosophy-knowledge-base/_operational/maintenance_scripts/`. `kb-doctor` does NOT gate read/write access.

### 3.3. Structure

*   The KB SHALL be organized into subdirectories based on content type (e.g., `concepts/`, `arguments/`, `quotations/`, `references/`, `questions/`, `theses/`, `relationships/`, `methods/`, `meta-reflections/`, `indices/`, `processed_texts/`).
*   An `_operational/` subdirectory SHALL exist for maintenance scripts, logs, status files, reports, and templates. (See `docs/architecture/architecture_v18.md`, Section 6).

### 3.4. Content Types & Entry Format (V18.3 Rigor Enhanced)

*   Each entry SHALL be a Markdown file with YAML frontmatter.
*   **YAML Frontmatter Fields (Mandatory):**
    *   `id`: Unique identifier (e.g., UUID). Generating mode is responsible for ensuring uniqueness or coordinating with a potential future ID service/script.
    *   `type`: Specifies the content type (e.g., `Concept`, `Argument`). MUST match the subdirectory.
    *   `timestamp`: ISO 8601 timestamp (YYYY-MM-DD HH:MM:SS) of creation/last modification. Updated by the writing mode.
    *   `generating_mode`: The slug of the mode that originated/last significantly modified the data.
*   **YAML Frontmatter Fields (Rigor & Context - V18.3 Emphasis):**
    *   `positive_determination`: (String) What the concept/argument IS. (Primarily Concepts/Arguments)
    *   `negative_determination`: (String) What the concept/argument is NOT. (Primarily Concepts/Arguments)
    *   `ordinary_language_contrast`: (String) How it differs from everyday usage. (Primarily Concepts)
    *   `related_terms`: (List[String]) IDs of related concepts/arguments.
    *   `presuppositions`: (List[String]) Underlying assumptions identified.
    *   `ambiguities`: (List[String]) Identified areas of unclear meaning or potential contradiction within the source/concept itself.
    *   `counter_arguments`: (List[String]) IDs of opposing/challenging arguments.
    *   `secondary_source_links`: (List[String]) IDs of relevant `Reference` entries for secondary literature.
    *   `other_philosopher_views`: (List[String]) IDs of KB entries detailing related views of other philosophers.
    *   `verification_status`: (String Enum: `Unverified` | `Verified` | `Disputed`) Status set by `verification-agent` or `kb-doctor`. Default `Unverified`.
    *   `verification_notes`: (String) Details from verification process, including identified rigor gaps.
    *   `tags`: (List[String]) Keywords including `context:key:value` tags and standard tags.
    *   `source_ref_keys`: (List[String]) Keys linking to `Reference` entries.
    *   `extraction_markers`: (List[String]) Markers linking to specific source locations.
    *   `related_ids`: (List[String]) General links to other KB entries.
*   **YAML Frontmatter Fields (Type-Specific):** As needed (e.g., `definition`, `premises`, `conclusion`, `question_text`, `thesis_statement`, `reflection_summary`, `method_description`, `index_path`, `chunk_summary`).
*   **Markdown Content:** Detailed descriptions, analysis, text excerpts, etc., reflecting rigor elements.

### 3.5. Knowledge Evolution & Conflict Resolution

*   **Competing Interpretations:** MUST be stored as separate, linked KB entries. Generating modes are responsible for identifying and linking (`related_ids`).
*   **Contradiction Resolution:**
    *   Detection: Analysis modes or `verification-agent` identify contradictions, update `ambiguities` or `verification_notes` fields, and report to `Orchestrator`.
    *   Process: `Orchestrator` delegates resolution (e.g., to `dialectical-analysis`, `meta-reflector`, `questioning`, or User). Resolution may involve refining entries, creating synthesis entries, marking as `Disputed`, or user guidance.
*   **Versioning:** Primarily handled by Git at the file level. KB entries MUST include `timestamp`. Future versions MAY incorporate internal version history fields.

## 4. Operational Context Management (`phil-memory-bank/`) Specifications (V18.3)

### 4.1. Purpose & Location

*   **Purpose:** To store operational context, logs, status, and feedback related to the execution of the philosophy modes, separate from the domain knowledge KB.
*   **Location:** `phil-memory-bank/`.

### 4.2. Management & Access (Direct Access Model)

*   **Read Access:** All modes MUST read operational context directly from files within `phil-memory-bank/` using file system tools (`read_file`, `search_files`).
*   **Write Access:**
    *   `philosophy-orchestrator`: Primarily responsible for writing to global context files (`activeContext.md`, `globalContext.md`).
    *   All other modes: MUST write their own operational logs directly to their designated file within `phil-memory-bank/mode-specific/[mode-slug].md`.
    *   Feedback: User feedback MAY be logged by `Orchestrator` or relevant modes into `phil-memory-bank/feedback/`.
*   **Log Standardization:** Mode `.clinerules` MUST define and adhere to a standardized log entry format (e.g., `[Timestamp] - [ModeSlug] - [Action/Status] - [Details/Outcome/KB_IDs_Affected]`).
    *   `// Pseudocode Anchor: Function write_operational_log(mode_slug: String, status: String, details: String)`
    *   `// TDD Anchor: Test writing a log entry for class-analysis`
    *   `// TDD Anchor: Test reading the last 10 log entries for orchestrator`

### 4.3. Structure

*   `phil-memory-bank/activeContext.md`: Log of current high-level task status and recent actions (managed by `Orchestrator`).
*   `phil-memory-bank/globalContext.md`: Longer-term context, decisions, progress summaries (managed by `Orchestrator`).
*   `phil-memory-bank/mode-specific/`: Contains individual log files for each mode (e.g., `philosophy-class-analysis.md`).
*   `phil-memory-bank/feedback/`: Contains logs related to user feedback or interventions.
*   `phil-memory-bank/status/` (Optional): May contain temporary status files for coordination if needed (e.g., simple locking).

## 5. Workflow Specifications (V18.3)

### 5.1. Philosophical Inquiry & Analysis Workflow

*   **Specification:** Follows the steps outlined in `docs/architecture/architecture_v18.md`, Section 7.1.
*   **Key Requirements:**
    *   Modes MUST use direct file access for reading/writing KB (`philosophy-knowledge-base/`) and operational context (`phil-memory-bank/`).
    *   Analysis modes MUST explicitly identify, analyze, and store rigor elements in KB entries.
    *   Modes MUST write standardized logs to their respective files in `phil-memory-bank/mode-specific/`.
    *   Context tags MUST be used for querying and storing KB entries derived from sources.
*   **Failure Handling:**
    *   Source Contradictions: Flag in KB (`ambiguities`/`source_issues`), report to `Orchestrator`.
    *   Mode Failures: Log failure clearly in `phil-memory-bank/mode-specific/`, report to `Orchestrator`. `Orchestrator` handles retry/delegation/user query.

### 5.2. Verification Workflow

*   **Specification:** Follows the steps outlined in `docs/architecture/architecture_v18.md`, Section 7.2.
*   **Key Requirements:**
    *   `verification-agent` MUST use direct file access for reading draft, KB, source chunks, and operational context.
    *   Verification MUST explicitly check for presence and consistency of rigor elements defined in Section 3.4.
    *   Reports MUST detail verification results, including rigor checks.
    *   KB entries MUST be updated (`verification_status`, `verification_notes`).
    *   `verification-agent` MUST write standardized logs to `phil-memory-bank/mode-specific/`.
*   **Failure Handling:**
    *   Verification Failures (Claim Disputed): Mark claim, update KB status to `Disputed`, log failure, report to `Orchestrator`. `Orchestrator` initiates correction loop (may involve `questioning`, `dialectical-analysis`, `essay-prep`, or User).

### 5.3. System Self-Reflection Workflow

*   **Specification:** Follows the steps outlined in `docs/architecture/architecture_v18.md`, Section 7.3.
*   **Key Requirements:**
    *   `meta-reflector` MUST use direct file access to read operational context (`phil-memory-bank/`), docs/rules, and KB content.
    *   Analysis MUST include evaluation of rigor enforcement, philosophical quality/progress (against defined metrics), and system efficiency.
    *   Findings MUST be stored in KB (tagged `meta`) via direct write.
    *   `meta-reflector` MUST write standardized logs to `phil-memory-bank/mode-specific/`.
    *   Proposals MUST be routed through `Orchestrator` for User approval.
*   **Failure Handling:**
    *   Analysis Failures: Log error, report to `Orchestrator`. `Orchestrator` handles delegation/notification.
    *   Proposal Rejections: Logged by `Orchestrator`. `meta-reflector` informed, may refine or abandon.

### 5.4. User Interaction Patterns

*   **Specification:** Follows the patterns outlined in `docs/architecture/architecture_v18.md`, Section 7.4.
*   **Key Requirements:**
    *   User Feedback: Logged by `Orchestrator` in `phil-memory-bank/feedback/`. Triggers refinement task delegation.
    *   User Intervention: `Orchestrator` attempts halt, logs state, awaits instructions.
    *   Ambiguous Queries: `Orchestrator` delegates to `questioning` to generate clarification questions using `ask_followup_question`.

## 6. Mode Specifications (V18.3)

### 6.1. `philosophy-kb-doctor`

*   **Identity & Purpose:** Orchestrates KB maintenance and rigor validation via KB-internal scripts. Non-gatekeeping.
*   **Functional Requirements:**
    *   Triggered by `Orchestrator`.
    *   Executes scripts from `philosophy-knowledge-base/_operational/maintenance_scripts/` using `execute_command`.
    *   Scripts perform tasks like indexing, validation (including rigor checks), cleanup, linking.
    *   Reads script logs/status from `philosophy-knowledge-base/_operational/`.
    *   Writes summary reports (including rigor validation) to `philosophy-knowledge-base/_operational/reports/`.
    *   Reports status and summaries to `Orchestrator`.
    *   Writes its own operational logs directly to `phil-memory-bank/mode-specific/philosophy-kb-doctor.md`.
*   **Interfaces:** Input triggers from `Orchestrator`. Output reports/status to `Orchestrator`. Executes scripts. Reads/writes operational logs.
*   **Dependencies:** `philosophy-orchestrator`, KB operational structure, maintenance scripts, `execute_command`, file system tools.
    *   `// Pseudocode Anchor: Function trigger_kb_maintenance(task_type: String)`
    *   `// TDD Anchor: Test triggering index update script`
    *   `// TDD Anchor: Test triggering rigor validation script`

### 6.2. Text Processing & Analysis Modes (`text-processor`, `pre-lecture`, `class-analysis`, `secondary-lit`, `dialectical-analysis`, `questioning`)

*   **Identity & Purpose:** Process sources, analyze content, generate KB entries, ensure rigor.
*   **Functional Requirements (V18.3):**
    *   **Direct KB Access:** Read/Write KB files directly.
    *   **Direct OpCtx Access:** Read context / Write logs directly to `phil-memory-bank/`.
    *   **Rigor Generation/Analysis:** Explicitly handle rigor elements (determinacy, presuppositions, etc.) during analysis and KB writing.
    *   **Context Handling:** Extract/Use context tags.
    *   **Logging:** Write standardized logs.
*   **Interfaces:** Input task delegation. Direct file I/O for KB and `phil-memory-bank/`. Output completion status to `Orchestrator`. `text-processor` executes scripts.
*   **Dependencies:** `philosophy-orchestrator`, file system tools, KB structure, `phil-memory-bank/` structure. `text-processor` depends on external scripts.
    *   `// Pseudocode Anchor: Function analyze_concept(concept_id: String)`
    *   `// TDD Anchor: Test analyze_concept reads KB entry directly`
    *   `// TDD Anchor: Test analyze_concept writes updated rigor fields directly`
    *   `// TDD Anchor: Test analyze_concept writes log to phil-memory-bank`

### 6.3. Essay Generation & Verification Modes (`essay-prep`, `draft-generator`, `citation-manager`, `verification-agent`)

*   **Identity & Purpose:** Manage essay workflow, generate content, verify claims/rigor.
*   **Functional Requirements (V18.3):**
    *   **Direct KB Access:** Read KB files directly (thesis, evidence, refs). `essay-prep` writes thesis directly.
    *   **Direct OpCtx Access:** Read context / Write logs directly to `phil-memory-bank/`.
    *   **Rigor Verification (`verification-agent`):** Explicitly check rigor fields in KB entries referenced by draft.
    *   **Version Control (`essay-prep`):** Manage Git for `essay_prep/` via `execute_command`.
    *   **Logging:** Write standardized logs.
*   **Interfaces:** Input task delegation. Direct file I/O for KB and `phil-memory-bank/`. `essay-prep` uses `execute_command`. Output completion status/reports to `Orchestrator`.
*   **Dependencies:** `philosophy-orchestrator`, file system tools, KB structure, `phil-memory-bank/` structure, `execute_command`.
    *   `// Pseudocode Anchor: Function verify_draft_section(draft_path: String)`
    *   `// TDD Anchor: Test verify_draft_section reads KB rigor fields directly`
    *   `// TDD Anchor: Test verify_draft_section reports rigor gaps`

### 6.4. Orchestration & Meta-Reflection Modes (`orchestrator`, `meta-reflector`)

*   **Identity & Purpose:** Manage workflows, delegate tasks, handle system reflection/proposals.
*   **Functional Requirements (V18.3):**
    *   **Direct OpCtx Access:** Read context / Write logs directly to `phil-memory-bank/`. `Orchestrator` manages global files.
    *   **Direct KB Access (`meta-reflector`):** Read KB files directly for analysis. Write meta-reflections directly to KB.
    *   **Delegation:** Provide detailed context in delegation messages, referencing relevant KB IDs and `phil-memory-bank/` log entries/timestamps.
    *   **Workflow Management:** Implement logic for inquiry, verification, reflection, failure handling, user interaction as specified.
    *   **Rigor Evaluation (`meta-reflector`):** Analyze KB/logs for rigor consistency and philosophical quality.
    *   **Logging:** Write standardized logs.
*   **Interfaces:** Input User requests/feedback. Direct file I/O for `phil-memory-bank/`. `meta-reflector` uses direct file I/O for KB. Output delegations, user queries/results, proposal routing.
*   **Dependencies:** All modes, User, file system tools, KB structure, `phil-memory-bank/` structure.
    *   `// Pseudocode Anchor: Function delegate_task(mode_slug: String, task_details: String, context_refs: List[String])`
    *   `// TDD Anchor: Test delegate_task includes references to phil-memory-bank logs`
    *   `// TDD Anchor: Test meta_reflector reads KB entries tagged 'meta'`

## 7. Version Control Specifications (V14 Retained)

*   **Essay Versioning:** `philosophy-essay-prep` MUST manage Git version control for `essay_prep/` via `execute_command`.
*   **KB/System Versioning (Consideration):** Future implementation MAY include Git versioning for `philosophy-knowledge-base/` and `phil-memory-bank/`, potentially managed by `devops` or triggered by `Orchestrator`.

## 8. Configuration Specifications (V18.3)

*   **Mode Definition File (`.roo/.roomodes`):** MUST list all V18.3 modes and their `.clinerules` paths using forward slashes (`/`). `philosophy-operational-context-manager` MUST be removed. (See `docs/architecture/architecture_v18.md`, Section 9 for example).
*   **Rules Files (`.clinerules`):** MUST be updated for all modes to reflect V18.3 requirements:
    *   Direct KB read/write logic using file tools.
    *   Direct `phil-memory-bank/` read/write logic for context/logging.
    *   Handling/Generation of rigor elements where applicable.
    *   Interaction patterns with `Orchestrator` and `KBDoctor` (if applicable).
    *   Use of forward slashes (`/`) in paths.

## 9. Open Questions / Future Considerations

*   Mechanism for ensuring KB ID uniqueness during direct writes.
*   Detailed implementation of file-based locking for KB writes if concurrency becomes an issue.
*   Specific metrics for `meta-reflector`'s philosophical quality evaluation.
*   Granular KB versioning beyond Git file history.
*   Error handling details for file system operations (permissions, disk space, etc.).
*   Mechanism for `Orchestrator` to gracefully halt modes during user intervention.