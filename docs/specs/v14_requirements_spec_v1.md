# Hegel Philosophy RooCode Suite - V14 Requirements Specification

**Date:** 2025-05-02
**Version:** 1.0 (Comprehensive)
**Status:** Draft
**Based On:**
*   `docs/architecture/architecture_v14.md`
*   `docs/specs/v13_requirements_spec_v1.md` (Content Merged)
*   User Feedback (V14 Docs Insufficient Detail, as of 2025-05-02 04:18)

**Goal:** This document provides detailed functional requirements and specifications for the V14 architecture of the Hegel Philosophy RooCode Suite. It translates the design outlined in `docs/architecture/architecture_v14.md` into actionable specifications for implementation, incorporating V13 features and the V14 refinements for source material organization and context handling. This document aims to be self-contained.

## 1. Overview

V14 integrates significant enhancements focused on knowledge management, system reflexivity, and source material handling:

*   **Philosophy Knowledge Base (KB):** A dedicated repository (`philosophy-knowledge-base/`) for structured philosophical domain knowledge, managed by `philosophy-kb-manager`. (V13 Core)
*   **Source Material Handling (V14 Refinement):**
    *   Standardized Input Structure: Defines a clear structure within `source_materials/raw/` for organizing inputs by context (course, project, type).
    *   Context Extraction & Storage: Specifies how `philosophy-text-processor` extracts context from source paths and how `philosophy-kb-manager` stores this context as tags within KB entries.
    *   Contextual Querying: Enables `philosophy-kb-manager` to filter queries based on source context tags.
*   **Philosophical Inquiry Workflow:** A structured process for generating, refining, and storing philosophical questions and theses within the context-aware KB. (V13 Core, Context-Aware V14)
*   **System Self-Reflection Workflow:** A mechanism for the system to analyze its own operations, methods, and architecture, facilitated by the `philosophy-meta-reflector` mode, storing findings in the context-aware KB. (V13 Core, Context-Aware V14)
*   **Mode Refinements:** Updates to existing modes to interact with the context-aware KB via `philosophy-kb-manager` and participate in the new workflows. Clear separation between KB (`kb-manager`) and Operational Memory (`evidence-manager`). (V13 Core, Context-Aware V14)

## 2. Source Material Handling Specifications (V14)

### 2.1. Raw Source Material Organization

*   **Location:** All raw source materials MUST be placed within the `source_materials/raw/` directory.
*   **Structure:** The directory structure under `source_materials/raw/` MUST follow a hierarchical pattern to define context. Recommended top-level contexts include:
    *   `courses/[COURSE_CODE]/[SUBTYPE]/[filename]` (e.g., `readings`, `lectures`, `notes`)
    *   `projects/[PROJECT_NAME]/[SUBTYPE]/[filename]` (e.g., `primary_sources`, `secondary_lit`, `notes`)
    *   `external_lit/[PRIMARY_OR_SECONDARY]/[filename]`
    *   `personal_notes/[filename]`
*   This structure MUST be extensible to accommodate new courses, projects, or types.

### 2.2. Context Extraction (`philosophy-text-processor`)

*   The `philosophy-text-processor` mode (specifically, the scripts it executes) MUST be updated to:
    *   Accept file paths pointing to files within `source_materials/raw/`.
    *   Parse the directory path of the input file to determine its context.
    *   Extract at least the following context information:
        *   `context_type`: The top-level category (e.g., `course`, `project`, `external_lit`, `personal_note`).
        *   `context_id`: The specific identifier within the type (e.g., `PHL316`, `dissertation`, `kant`, `general`).
        *   `source_subtype`: The nature of the material within its context (e.g., `reading`, `lecture`, `note`, `primary`, `secondary`).
    *   Pass this extracted context information (formatted as `context:key:value` tags) along with processed chunks, index data, and citation data to `philosophy-kb-manager`.

### 2.3. Context Storage (`philosophy-kb-manager`)

*   When creating KB entries derived from processed source material, `philosophy-kb-manager` MUST:
    *   Receive the extracted context information (as tags) from `philosophy-text-processor`.
    *   Store these context tags within the `tags` field of the KB entry's YAML frontmatter.
    *   Use the consistent format `context:key:value` (e.g., `context:type:course`, `context:id:PHL316`, `context:subtype:reading`).

### 2.4. Contextual Querying (`philosophy-kb-manager`)

*   The `philosophy-kb-manager` query functionality MUST be enhanced to support filtering based on the `context:key:value` tags.
*   Modes querying the KB MUST be able to specify one or more context tags as part of their query parameters to retrieve context-specific information.
*   Query logic SHOULD support combinations (AND/OR) of context tags and other filters.
*   Examples of supported queries:
    *   Retrieve entries with tag `context:id:PHL316`.
    *   Retrieve entries with tags `context:type:project` AND `context:subtype:primary_source`.
    *   Retrieve entries with tag `context:type:course`.

## 3. Philosophy Knowledge Base (KB) Specifications (V14)

### 3.1. Purpose & Location

*   **Purpose:** To serve as a centralized, structured, and persistent repository for philosophical domain knowledge, separate from the system's operational memory.
*   **Location:** A top-level directory: `philosophy-knowledge-base/`.

### 3.2. Management

*   The KB MUST be accessed and modified **exclusively** through the `philosophy-kb-manager` mode. No other mode should directly read from or write to the `philosophy-knowledge-base/` directory.

### 3.3. Structure

*   The KB SHALL be organized into subdirectories based on content type:
    *   `philosophy-knowledge-base/concepts/`
    *   `philosophy-knowledge-base/arguments/`
    *   `philosophy-knowledge-base/quotations/`
    *   `philosophy-knowledge-base/references/`
    *   `philosophy-knowledge-base/questions/`
    *   `philosophy-knowledge-base/theses/`
    *   `philosophy-knowledge-base/relationships/`
    *   `philosophy-knowledge-base/methods/`
    *   `philosophy-knowledge-base/meta-reflections/`
    *   `philosophy-knowledge-base/indices/`

### 3.4. Content Types & Entry Format

*   Each entry in the KB SHALL be a separate Markdown file.
*   Each entry MUST contain a YAML frontmatter block and Markdown content.
*   **YAML Frontmatter Fields (Mandatory):**
    *   `id`: Unique identifier (e.g., UUID) for the entry. MUST be generated by `kb-manager` upon creation.
    *   `type`: Specifies the content type (e.g., `Concept`, `Argument`, `Quotation`, `Reference`, `Question`, `Thesis`, `Relationship`, `Method`, `Meta-Reflection`, `Index`). MUST match the subdirectory.
    *   `timestamp`: ISO 8601 timestamp (YYYY-MM-DD HH:MM:SS) of creation/last modification.
    *   `generating_mode`: The slug of the mode that originated the data (e.g., `philosophy-pre-lecture`, `philosophy-meta-reflector`).
*   **YAML Frontmatter Fields (Optional/Contextual):**
    *   `source_ref_keys`: List of keys linking to entries in `philosophy-knowledge-base/references/`. Used to associate KB content with its source material.
    *   `extraction_markers`: List of specific markers (e.g., unique IDs, text snippets) linking to precise locations within processed source text files (e.g., in `source_materials/processed/`).
    *   `related_ids`: List of `id`s of other KB entries, establishing explicit links.
    *   `tags`: List of relevant keywords for categorization and querying.
        *   **Context Tags (V14):** MUST include tags in the format `context:key:value` (e.g., `context:type:course`, `context:id:PHL316`, `context:subtype:reading`) if the entry is derived from source material processed by `text-processor`.
        *   **Standard Tags:** Include other relevant keywords (e.g., `hegel`, `critique`, `logic`, `ethics`).
        *   **Workflow Tags:** `Question` types MUST be tagged as either `inquiry` (for philosophical inquiry) or `meta` (for system self-reflection).
    *   *Type-Specific Fields:* Additional fields relevant to the `type` (e.g., `definition` for Concept, `premises`/`conclusion` for Argument, `question_text` for Question, `thesis_statement` for Thesis, `index_path`/`chunk_summary` for Index).
*   **Markdown Content:** The main body of the entry, containing detailed descriptions, analysis, text excerpts, etc.

### 3.5. Interaction Methods (via `kb-manager`)

*   **Create:** Add new entries to the KB. `kb-manager` assigns `id` and `timestamp`. MUST accept and store context tags if provided.
*   **Read/Query:** Retrieve entries based on `id`, `type`, `tags` (including context tags), `related_ids`, keywords within content, or other metadata. `kb-manager` SHALL provide flexible query capabilities, including filtering by context tags.
*   **Update:** Modify existing entries. `kb-manager` MUST update the `timestamp`.
*   **Delete:** Remove entries (use with caution; consider archival instead).
*   **Link:** Create or update `related_ids` between entries.

### 3.6. Self-Modification

*   Modes MAY propose modifications to KB content or structure (e.g., adding relationships, refining definitions).
*   Proposals MUST be sent to `philosophy-orchestrator`.
*   `philosophy-orchestrator` MUST route the proposal to the User for approval.
*   Upon User approval, `philosophy-orchestrator` MUST instruct `philosophy-kb-manager` to execute the modification.
*   `philosophy-kb-manager` MUST log the modification (e.g., within the entry or a dedicated log).

## 4. Philosophical Inquiry Workflow Specifications (V14 Context-Aware)

### 4.1. Purpose

*   To provide a structured workflow for generating, refining, storing, and utilizing philosophical questions and theses within the KB, primarily supporting research and essay writing.

### 4.2. Steps & Mode Responsibilities

1.  **Input/Trigger:**
    *   User explicitly prompts for inquiry on a topic/text.
    *   Analysis modes (`pre-lecture`, `class-analysis`, `secondary-lit`, `dialectical-analysis`) identify potential questions or novel concepts during their analysis.
2.  **Proto-Storage (`kb-manager`):**
    *   Analysis modes send identified proto-questions or concepts (with source context if applicable) to `kb-manager`.
    *   `kb-manager` stores these as `Question` or `Concept` entries, including any provided context tags and potentially adding a `proto-question` tag.
3.  **Refinement (`philosophy-questioning`):**
    *   Triggered by `orchestrator` based on user request or availability of proto-questions.
    *   `philosophy-questioning` queries `kb-manager` for relevant proto-questions and related concepts/arguments, **optionally filtering by context tags**.
    *   It analyzes the questions for clarity, scope, relevance, and philosophical interest, potentially refining wording or breaking down complex questions.
4.  **Refined Storage (`kb-manager`):**
    *   `philosophy-questioning` sends the refined questions (linked to original proto-questions if applicable) back to `kb-manager`.
    *   `kb-manager` updates existing entries or creates new `Question` entries, tagged as `inquiry`.
5.  **Thesis Development (`philosophy-essay-prep`):**
    *   Triggered by `orchestrator` when an essay task begins.
    *   `philosophy-essay-prep` queries `kb-manager` for relevant refined `Question` entries and supporting `Concept`, `Argument`, `Quotation` entries, **optionally filtering by context tags** based on the essay prompt.
    *   It develops a specific, arguable thesis statement addressing a chosen question.
6.  **Thesis Storage (`kb-manager`):**
    *   `philosophy-essay-prep` sends the developed thesis statement to `kb-manager`.
    *   `kb-manager` stores it as a `Thesis` entry, linking it back to the corresponding `Question` entry (`related_ids`).
7.  **Essay Cycle:**
    *   The standard essay generation workflow proceeds, orchestrated by `essay-prep`.
    *   Modes (`draft-generator`, `citation-manager`, `verification-agent`) query `kb-manager` (via `essay-prep` or directly as needed) for the thesis, relevant questions, concepts, arguments, quotations, and references, **optionally filtering by context tags**, to support drafting, citation, and verification.

### 4.3. Data Flow

*   Proto-questions/concepts (with context tags) -> `kb-manager`
*   Refined questions -> `kb-manager`
*   Thesis statements -> `kb-manager`
*   KB queries (with optional context filters) -> `kb-manager`
*   KB data packages -> Requesting modes

## 5. System Self-Reflection Workflow Specifications (V14 Context-Aware)

### 5.1. Purpose

*   To enable the system to perform meta-level analysis on its own architecture, methods, assumptions, and outputs, identifying potential limitations, biases, or areas for improvement.

### 5.2. Steps & Mode Responsibilities

1.  **Trigger:**
    *   User explicitly requests system reflection.
    *   `philosophy-orchestrator` detects anomalies.
    *   A pre-defined schedule.
2.  **Activation (`orchestrator` -> `meta-reflector`):**
    *   `philosophy-orchestrator` delegates the reflection task to `philosophy-meta-reflector`, providing context.
3.  **Analysis (`meta-reflector`):**
    *   `meta-reflector` queries `philosophy-evidence-manager` for relevant Operational Memory data.
    *   `meta-reflector` reads relevant system documentation (`docs/`), mode rules (`.roo/`), and potentially configuration files.
    *   `meta-reflector` queries `philosophy-kb-manager` for existing `Meta-Reflection` entries, `Method` descriptions, or relevant philosophical concepts, **optionally filtering by context tags**.
    *   Analysis guided by principles in `architecture-questioning.md`.
4.  **Reflection Generation (`meta-reflector`):**
    *   Based on its analysis, `meta-reflector` generates:
        *   **Meta-Reflections:** Observations about system behavior, limitations, assumptions, etc.
        *   **Meta-Questions:** Questions directed at the system's own structure or process.
5.  **Storage (`kb-manager`):**
    *   `meta-reflector` sends generated reflections and questions to `philosophy-kb-manager`.
    *   `kb-manager` stores them as `Meta-Reflection` or `Question` entries (tagged as `meta`).
6.  **Proposal Generation (`meta-reflector`, Optional):**
    *   If the reflection identifies actionable improvements, `meta-reflector` formulates specific proposals (KB Change, Architectural Change, Methodological Change).
7.  **Proposal Routing (`orchestrator`):**
    *   `meta-reflector` sends proposals to `philosophy-orchestrator`.
    *   `philosophy-orchestrator` MUST route proposals to the User for review and approval.
8.  **Approval Handling (`orchestrator` -> `kb-manager`/`architect`/`devops`):**
    *   If User approves:
        *   KB Change: `orchestrator` instructs `kb-manager`.
        *   Architectural Change: `orchestrator` delegates to `architect`.
        *   Methodological Change: `orchestrator` instructs `kb-manager` (method description) and/or delegates to `devops`/`architect` (branching/tooling).
9.  **Reporting (`meta-reflector` -> `orchestrator` -> User):**
    *   `meta-reflector` provides a summary report to `philosophy-orchestrator`.
    *   `philosophy-orchestrator` relays the report to the User.

### 5.3. Data Flow

*   Operational Memory data -> `meta-reflector` (via `evidence-manager`)
*   Docs/Rules/Config -> `meta-reflector` (via file reads)
*   KB data (with optional context filters) -> `meta-reflector` (via `kb-manager`)
*   Generated reflections/meta-questions -> `kb-manager`
*   Proposals -> `orchestrator` -> User -> `orchestrator` -> `kb-manager`/`architect`/`devops`
*   Summary Report -> `orchestrator` -> User

## 6. Mode Specifications (V14)

### 6.1. `philosophy-kb-manager`

*   **Identity & Purpose:** Sole interface to `philosophy-knowledge-base/`. Manages CRUD, querying (including context filtering), linking, integrity, and executes approved modifications for philosophical domain knowledge.
*   **Functional Requirements:**
    *   Exclusive file access to `philosophy-knowledge-base/`.
    *   CRUD Operations: Create (handles `id`, `timestamp`, context tags), Read/Retrieve (supports context filters), Update (updates `timestamp`), Delete/Archive.
    *   Querying: By `id`, `type`, `tags` (including `context:key:value`), `related_ids`, keywords, metadata. Must support context filtering. Results in structured format.
    *   Linking: Manages `related_ids`. Validates IDs.
    *   Data Integrity: Validates entry structure, mandatory fields, `type`/subdirectory match, context tag format.
    *   Structure Management: Creates entries in correct subdirectory. May suggest tag consistency.
    *   Modification Execution: Accepts instructions from `orchestrator` post-User approval. Logs modifications.
    *   Error Handling: Reports errors clearly.
*   **Interfaces:** Input requests (may include context filters/tags), modification instructions. Output data packages, confirmations, errors.
*   **Dependencies:** `philosophy-knowledge-base/`, `philosophy-orchestrator`, modes requiring KB access.

### 6.2. `philosophy-meta-reflector`

*   **Identity & Purpose:** Performs meta-level analysis of the system, questioning assumptions, methods, architecture, outputs. Fosters reflexivity.
*   **Functional Requirements:**
    *   Triggering: Activates on delegation from `orchestrator`.
    *   Analysis Targets: Operational Memory (via `evidence-manager`), system docs (`docs/`), mode rules (`.roo/`), KB content (via `kb-manager`, with context filters), potentially workspace code.
    *   Reflection Generation: Generates textual reflections and meta-questions based on analysis and `architecture-questioning.md`.
    *   Storage: Stores reflections (`Meta-Reflection`) and questions (`Question`, tagged `meta`) in KB via `kb-manager`.
    *   Proposal Generation: May generate actionable proposals (KB, Arch, Methodological).
    *   Proposal Routing: Sends proposals to `orchestrator`.
    *   Reporting: Provides summary report to `orchestrator`.
*   **Interfaces:** Input delegation request, data from `evidence-manager`/`kb-manager`, file content. Output storage requests to `kb-manager`, proposals to `orchestrator`, report to `orchestrator`.
*   **Dependencies:** `philosophy-orchestrator`, `philosophy-kb-manager`, `philosophy-evidence-manager`, docs/rules access, `architecture-questioning.md`.

### 6.3. `philosophy-evidence-manager` (Revised Scope)

*   **Identity & Purpose:** Manages access **only** to Operational Memory (`memory-bank/`) and potentially `analysis_workspace/`. Provides operational context.
*   **Functional Requirements:** Data Access limited to `memory-bank/` and `analysis_workspace/`. Provides operational context data.
*   **Interfaces:** Input queries for operational context, data for storage. Output operational context data, confirmations.
*   **Dependencies:** All modes needing operational context, `memory-bank/` files.

### 6.4. `philosophy-text-processor`

*   **Identity & Purpose:** Pre-processes source texts via external scripts.
*   **Functional Requirements (V14 Enhancement):**
    *   Reads from `source_materials/raw/`.
    *   Executes scripts for chunking, indexing, citation extraction.
    *   **Context Extraction:** Implements logic to parse source file paths and extract `context:type`, `context:id`, `context:subtype`.
    *   **KB Interaction:** Sends index/chunk info, citation data, and extracted context tags (formatted `context:key:value`) to `philosophy-kb-manager`.
*   **Interfaces:** Input task delegation. Output data package (index, citations, context tags) to `kb-manager`, processed chunks to `source_materials/processed/`.
*   **Dependencies:** External scripts, `philosophy-orchestrator`, `philosophy-kb-manager`.

### 6.5. Analysis Modes (`pre-lecture`, `class-analysis`, `secondary-lit`, `dialectical-analysis`, `questioning`)

*   **Identity & Purpose:** Analyze sources/KB content, generate philosophical insights. `questioning` refines inquiry questions.
*   **Functional Requirements (V14 Update):**
    *   **KB Querying:** MUST query `philosophy-kb-manager` for KB content, **optionally using context tags** for filtering.
    *   **KB Storage:** MUST send findings (concepts, arguments, proto-questions, refined questions, analyses) to `philosophy-kb-manager`. Context tags are added by `kb-manager` based on source or explicitly if generated without source.
    *   **Operational Context:** MAY query `philosophy-evidence-manager` for operational context.
*   **Interfaces:** Input task delegation. Query `kb-manager` (with optional context filters), `evidence-manager`. Output findings to `kb-manager`.
*   **Dependencies:** `philosophy-orchestrator`, `philosophy-kb-manager`, `philosophy-evidence-manager`.

### 6.6. Essay Modes (`essay-prep`, `draft-generator`, `citation-manager`, `verification-agent`)

*   **Identity & Purpose:** Manage and execute essay writing workflow. `essay-prep` coordinates and handles Git.
*   **Functional Requirements (V14 Update):**
    *   **KB Querying:** MUST query `philosophy-kb-manager` for thesis, questions, concepts, arguments, quotations, references, **optionally using context tags** for filtering based on essay scope.
    *   **KB Storage:** `essay-prep` MUST store the developed thesis via `philosophy-kb-manager`.
    *   **Coordination:** `essay-prep` coordinates other modes, providing necessary data (potentially retrieved with context filters).
    *   **Version Control:** `essay-prep` manages Git for `essay_prep/` via `execute_command`.
*   **Interfaces:** Input task delegation. Query `kb-manager` (with optional context filters). Output thesis to `kb-manager`, draft/citations/reports between modes, Git commands via `execute_command`.
*   **Dependencies:** `philosophy-orchestrator`, `philosophy-kb-manager`, `execute_command`.

### 6.7. `philosophy-orchestrator`

*   **Identity & Purpose:** Manages workflows, delegates tasks, handles handoffs, routes proposals.
*   **Functional Requirements (V14 Context):**
    *   Manages `philosophical_inquiry` and `system_self_reflection` workflows, which now operate on a context-aware KB.
    *   Routes proposals (KB/System mods) for User approval.
    *   Relays approvals to `kb-manager`/`architect`/`devops`.
    *   Updates delegation logic for V13+ modes (`kb-manager`, `meta-reflector`, revised `evidence-manager`).
*   **Interfaces:** Input User requests, proposals from modes. Output task delegations, proposal routing to User, approval relays, results to User.
*   **Dependencies:** All modes, User.

## 7. Version Control Specifications (V14)

*   **Essay Versioning:** `philosophy-essay-prep` MUST manage Git version control for `essay_prep/` via `execute_command`.
*   **KB Versioning (Consideration):** Implementation MAY include Git versioning for `philosophy-knowledge-base/`, managed by `philosophy-kb-manager` or `devops` upon approved modifications.
*   **System Evolution Branching (Consideration):** Proposals from `meta-reflector` MAY trigger creation of separate Git branches by `devops`/`architect`.

## 8. Configuration Specifications (V14)

*   The `.roo/.roomodes` file MUST include entries for all V13+ modes (`philosophy-kb-manager`, `philosophy-meta-reflector`) pointing to their `.clinerules` files.
*   New `.clinerules` files MUST exist for `philosophy-kb-manager` and `philosophy-meta-reflector`.
*   Existing `.clinerules` files for modes interacting with the KB (`text-processor`, analysis modes, essay modes, `orchestrator`, `meta-reflector`) MUST be updated to reflect V14 requirements (context extraction, storage, querying capabilities).

### 6.7. `philosophy-orchestrator`

*   **Identity & Purpose:** Manages workflows, delegates tasks, handles handoffs, routes proposals.
*   **Functional Requirements (V14 Context):**
    *   Manages `philosophical_inquiry` and `system_self_reflection` workflows, which now operate on a context-aware KB.
    *   Routes proposals (KB/System mods) for User approval.
    *   Relays approvals to `kb-manager`/`architect`/`devops`.
    *   Updates delegation logic for V13+ modes (`kb-manager`, `meta-reflector`, revised `evidence-manager`) and ensures context filters are considered where applicable.
*   **Interfaces:** Input User requests, proposals from modes. Output task delegations, proposal routing to User, approval relays, results to User.
*   **Dependencies:** All modes, User.

## 7. Version Control Specifications (V14)

*   **Essay Versioning:** `philosophy-essay-prep` MUST manage Git version control for `essay_prep/` via `execute_command`.
*   **KB Versioning (Consideration):** Implementation MAY include Git versioning for `philosophy-knowledge-base/`, managed by `philosophy-kb-manager` or `devops` upon approved modifications.
*   **System Evolution Branching (Consideration):** Proposals from `meta-reflector` MAY trigger creation of separate Git branches by `devops`/`architect`.

## 8. Configuration Specifications (V14)

*   The `.roo/.roomodes` file MUST include entries for all V13+ modes (`philosophy-kb-manager`, `philosophy-meta-reflector`) pointing to their `.clinerules` files.
*   New `.clinerules` files MUST exist for `philosophy-kb-manager` and `philosophy-meta-reflector`.
*   Existing `.clinerules` files for modes interacting with the KB (`text-processor`, analysis modes, essay modes, `orchestrator`, `meta-reflector`) MUST be updated to reflect V14 requirements (context extraction, storage, querying capabilities via `kb-manager`).
