# Hegel Philosophy RooCode Suite - Architecture V18.1 (Rigor Enhanced, No SPARC Ref)

**Date:** 2025-05-02
**Version:** 18.1 (Revised)
**Status:** Draft
**Based On:**
*   `docs/architecture/architecture_v18.md` (Original V18.1)
*   `docs/architecture/architecture_v14.md` (Structure & Detail Level Reference)
*   V15/V16 Principles (Direct Access, KB Doctor - derived from Memory Bank logs)
*   User Task & Feedback (V18 Requirements & Constraints, Rigor Enhancements, Linux Paths, No SPARC Ref - as of 2025-05-02 15:59)
*   Memory Bank Context (as of 2025-05-02 15:59)
*   Rigor Principles Sources: `.roo/rules-philosophy-class-analysis/`, `.roo/rules-philosophy-verification-agent/`, `.roo/rules-philosophy-dialectical-analysis/`

**Goal:** Update V18 architecture to incorporate enhanced principles of **philosophical rigor** (determinacy, specificity, verification, argument analysis), ensure all file paths use **Linux conventions** (`/`), while maintaining V18 core principles (Direct KB Access, KB Doctor) and V14 detail level. Remove system-specific terminology ("SPARC").

## 1. Core Principles (V18.1 Revised)

*   **Determinacy & Specificity:** Concepts/arguments clearly defined within the KB, including positive/negative determination, contrast with ordinary language, and identification of ambiguities. (V11+, Enhanced V18.1)
*   **Evidence Saturation & Rigorous Sourcing:** Claims linked to specific sources via KB entries (`source_ref_keys`, `extraction_markers`). Verification emphasizes source validity and relevance. (V11+, Enhanced V18.1)
*   **Argument Analysis:** Explicit analysis of presuppositions, contradictions, counter-arguments, and relationships between arguments within the KB. (New V18.1)
*   **Contextual Awareness:** Analysis considers related terms, secondary sources, and other philosophers' views via KB links and context tags. (V14+, Enhanced V18.1)
*   **Chronological Integrity:** Analysis respects temporal flow of sources and system operations. (V11+)
*   **Verification Rigor:** Inputs/outputs verified against KB & sources, including checks for rigor elements. (V11+, Enhanced V18.1)
*   **Modularity:** Encapsulated functionality in specialized modes with defined responsibilities. (V11+)
*   **Orchestration:** Complex workflows managed by `philosophy-orchestrator`. (V11+)
*   **Traceability:** Version control (Git) for key artifacts (essays, potentially KB/config). (V12+)
*   **Knowledge Separation (Strict):** Explicit and enforced distinction between philosophical domain knowledge (`philosophy-knowledge-base/`) and operational/process memory (`memory-bank/`). **NO philosophy system interaction with `memory-bank/` for KB operations.** (V13+, Reinforced V18)
*   **Reflexivity:** Capacity for the system to question its own assumptions, methods, and architecture (`philosophy-meta-reflector`). (V13+)
*   **Controlled Evolution:** Mechanisms for proposing and approving modifications to the KB and potentially the system architecture itself. (V13+)
*   **Source Contextualization (Retained V14):** Raw source materials are organized by context (`source_materials/raw/`), and this context is explicitly captured, stored as tags in the KB, and queryable.
*   **Direct KB Read Access (V18):** Modes read data directly from `philosophy-knowledge-base/` using standard file tools (`read_file`, `search_files`), guided by their internal logic and `.clinerules`.
*   **Defined KB Write Patterns (V18):** Modes that write to the KB do so directly into designated files/sections within `philosophy-knowledge-base/` according to established conventions (e.g., `text-processor` writes to `processed_texts/`, analysis modes write to `concepts/`, `arguments/`, etc.), including rigor-related fields.
*   **KB Doctor for Maintenance (V18):** A dedicated `philosophy-kb-doctor` mode handles KB maintenance tasks (indexing, validation, cleanup, potentially identifying missing rigor elements) by orchestrating scripts within the KB's `_operational/` directory. It is triggered by the `Orchestrator` and **does not gate** read/write access for other modes.

## 2. V18.1 Architecture Overview (Revised)

V18.1 builds upon V18 by explicitly integrating philosophical rigor requirements into the direct-access model.

1.  **Direct KB Access:** Modes interact directly with `philosophy-knowledge-base/` using file tools. Read access is open; write access follows conventions and includes rigor fields. Modes embed logic for locating, reading, interpreting, and *writing* KB data, including rigor elements.
2.  **KB Doctor (Maintenance & Rigor Support):** `philosophy-kb-doctor` handles maintenance via KB-internal scripts. Its role is expanded to potentially include running validation scripts that check for the presence and consistency of rigor elements (e.g., ensuring arguments link to counter-arguments, concepts have determinacy fields). It reports findings to the `Orchestrator`, potentially triggering corrective actions or analysis tasks. Remains non-gatekeeping.
3.  **Strict KB/Operational Memory Separation:** Maintained. `philosophy-operational-context-manager` used only for `memory-bank/` access.
4.  **Source Context Handling (Retained V14):** Maintained. Context tags enable rigor checks within specific contexts (e.g., comparing interpretations across different courses or secondary sources).
5.  **Enhanced KB Schema:** KB entry formats (esp. `Concept`, `Argument`) are expanded with specific fields to capture rigor elements (see Section 6).
6.  **Updated Mode Responsibilities:** Analysis, questioning, and verification modes are explicitly tasked with generating, refining, and checking rigor elements during their operations (see Section 4).
7.  **Rigor-Aware Workflows:** Analysis and verification workflows include steps to query related context (secondary sources, counter-arguments) and explicitly document rigor checks (see Section 7). A self-correction loop is formalized.

## 3. Source Material Organization (V14 - Retained, Linux Paths)

*   **Raw Input Location:** `source_materials/raw/`
*   **Purpose:** Centralized location for all original source materials before processing. Provides a clear, machine-parsable structure for determining source context.
*   **Structure:** Hierarchical directories define context. Paths use forward slashes (`/`).
    ```
    source_materials/
    ├── raw/
    │   ├── courses/
    │   │   ├── [COURSE_CODE]/        # e.g., PHL316, PHL400
    │   │   │   ├── readings/         # Assigned readings
    │   │   │   │   └── [filename.md | .pdf | .docx]
    │   │   │   ├── lectures/         # Lecture transcripts/notes
    │   │   │   │   └── [filename.md | .txt]
    │   │   │   └── notes/            # Personal notes specific to this course
    │   │   │       └── [filename.md]
    │   │   └── ... (other courses)
    │   ├── projects/
    │   │   ├── [PROJECT_NAME]/       # e.g., dissertation, hegel_paper
    │   │   │   ├── primary_sources/
    │   │   │   │   └── [filename.md | .pdf | .docx]
    │   │   │   ├── secondary_lit/
    │   │   │   │   └── [filename.md | .pdf | .docx]
    │   │   │   └── notes/
    │   │   │       └── [filename.md]
    │   │   └── ... (other projects)
    │   ├── external_lit/             # Literature not tied to a specific course/project
    │   │   ├── primary/              # Primary texts by author/topic
    │   │   │   └── [author_or_topic]/
    │   │   │       └── [filename.md | .pdf | .docx]
    │   │   └── secondary/            # Secondary texts by author/topic
    │   │       └── [author_or_topic]/
    │   │           └── [filename.md | .pdf | .docx]
    │   └── personal_notes/           # General notes not tied to course/project
    │       └── [filename.md]
    └── processed/                    # Existing location for processed chunks (output of text-processor)
        └── ...
    ```
*   **Context Extraction:** `philosophy-text-processor` MUST parse paths like `source_materials/raw/courses/PHL316/readings/Hegel_Work.md` relative to `source_materials/raw/` to extract:
    *   `context_type`: `course`
    *   `context_id`: `PHL316`
    *   `context_subtype`: `reading`
    These are then formatted as tags: `context:type:course`, `context:id:PHL316`, `context:subtype:reading` for storage in the KB entry YAML.

## 4. Mode Structure & Responsibilities (V18.1 Revised - Rigor Enhanced, Linux Paths)

### 4.1. Core Data Management Modes

*   **`philosophy-operational-context-manager` (V13 Revised Scope - Retained):**
    *   **Responsibility:** Manages access **only** to the Operational Memory Bank (`memory-bank/`) and potentially `analysis_workspace/`. Handles operational context queries. **Does NOT interact with `philosophy-knowledge-base/`.**
    *   **Input:** Queries for operational context, operational context data for storage.
    *   **Output:** Operational context data, confirmations.
    *   **Dependencies:** All modes (for operational context), `memory-bank/` files.
*   **`philosophy-kb-doctor` (V18, Enhanced V18.1):**
    *   **Responsibility:** Orchestrates KB maintenance tasks (indexing, validation, cleanup, linking). Triggered by `philosophy-orchestrator`. Executes scripts located in `philosophy-knowledge-base/_operational/maintenance_scripts/`. **V18.1:** Scripts may include validation checks for rigor elements (e.g., presence of determinacy fields, links to counter-arguments, source validity checks). Reads KB operational logs/status from `philosophy-knowledge-base/_operational/`. Reports KB status and rigor validation summaries to `philosophy-orchestrator`. **Does NOT perform maintenance directly; orchestrates KB-internal processes. Does NOT gate read/write access for other modes.**
    *   **Input:** Maintenance triggers from `Orchestrator`.
    *   **Output:** Status reports and rigor validation summaries to `Orchestrator`. Writes execution logs to its mode-specific log in `memory-bank/`. (Maintenance script logs are written within `philosophy-knowledge-base/_operational/logs/`).
    *   **Dependencies:** `philosophy-orchestrator` (trigger), scripts within `philosophy-knowledge-base/_operational/maintenance_scripts/`, data within `philosophy-knowledge-base/_operational/`, `philosophy-operational-context-manager` (for operational context).

### 4.2. Text Processing & Analysis Modes

*   **`philosophy-text-processor` (V12, V14 Context, V18 Write Pattern):**
    *   **Responsibility:** Pre-processes source texts from `source_materials/raw/` via external scripts (chunking, indexing, citation extraction). Parses input path to extract context (`type`, `id`, `subtype`). Emphasizes extraction of markers (`extraction_markers`) linking chunks to precise source locations.
    *   **Output (V18):** Processed chunks to `source_materials/processed/`. **Directly writes** index/chunk info, citation data (including `source_ref_keys`), and extracted context tags to designated files/sections within `philosophy-knowledge-base/`.
    *   **Dependencies:** External scripts, `philosophy-orchestrator`, File system tools (`write_to_file`, `insert_content`), `philosophy-operational-context-manager` (for operational context).
*   **Analysis Modes (`pre-lecture`, `class-analysis`, `secondary-lit`, `dialectical-analysis`, `questioning`):**
    *   **Responsibility:** Analyze sources/KB content, generate concepts, arguments, questions, etc., **ensuring philosophical rigor**.
    *   **Interaction (V18.1):**
        *   **Read:** Directly Read KB files (`philosophy-knowledge-base/`) using file tools, applying context filters. Query related context (linked entries like counter-arguments, secondary sources) via `related_ids` or context tags.
        *   **Analyze for Rigor:** Explicitly identify and analyze determinacy, presuppositions, ambiguities, contradictions, related terms, ordinary language contrast, etc.
        *   **Write:** Directly Write findings to designated KB files/sections using file tools, **populating rigor-related fields** (see Section 6) and ensuring correct formatting and linking (including `source_ref_keys`, `extraction_markers`, `related_ids`).
        *   **Operational Context:** Query `philosophy-operational-context-manager` for operational context if needed.
    *   **Specific Mode Focus (Rigor):**
        *   `class-analysis`: Focus on conceptual determinacy, evidence standards from lectures/readings, identifying potential counter-interpretations.
        *   `dialectical-analysis`: Focus on identifying contradictions, moments, transitions, resolutions, presuppositions within arguments.
        *   `secondary-lit`: Focus on comparing interpretations, identifying secondary source claims/arguments, linking to primary source KB entries.
        *   `questioning`: Refine questions based on identified ambiguities, presuppositions, or gaps in KB rigor.

### 4.3. Essay Generation & Verification Modes

*   **`philosophy-essay-prep` (V11+):**
    *   **Responsibility:** Manages essay writing process, including thesis development and outline, ensuring thesis is determinate and addresses relevant KB context. Manages Git for essays.
    *   **Interaction (V18.1):** Directly Reads relevant KB entries (questions, concepts, arguments, counter-arguments) using file tools, applying context filters. Directly Writes developed thesis (including its presuppositions/scope) to KB. Coordinates other essay modes. Executes Git commands. Queries `philosophy-operational-context-manager` for operational context.
*   **`philosophy-draft-generator` (V11+):**
    *   **Responsibility:** Generates prose based on outline and evidence package, aiming for clarity and specificity.
    *   **Interaction (V18.1):** Directly Reads evidence package (thesis, concepts, arguments, quotes, counter-arguments) from KB using file tools. Queries `philosophy-operational-context-manager` for operational context.
*   **`philosophy-citation-manager` (V11+):**
    *   **Responsibility:** Formats citations and bibliography, ensuring accurate linking via `source_ref_keys`.
    *   **Interaction (V18.1):** Directly Reads reference details and citation location data from KB using file tools. Queries `philosophy-operational-context-manager` for operational context.
*   **`philosophy-verification-agent` (V11+, Enhanced V18.1):**
    *   **Responsibility:** Verifies claims, citations, and **rigor elements** within drafts against KB entries and processed source chunks. Checks for consistency, accurate representation of sources/arguments, presence of required rigor fields (e.g., determinacy), and appropriate handling of counter-arguments.
    *   **Interaction (V18.1):** Directly Reads draft content, evidence, references, rigor fields, and processed chunk paths/indices from KB using file tools. Queries `philosophy-operational-context-manager` for operational context. Generates verification reports highlighting discrepancies, missing rigor, or unsupported claims. Triggers self-correction loop via `Orchestrator` if significant issues found.

### 4.4. Orchestration & Meta-Reflection Modes

*   **`philosophy-orchestrator` (V11+):**
    *   **Responsibility:** Manages workflows, delegates tasks, handles handoffs, routes proposals, relays approvals. Coordinates Git commits. Triggers `philosophy-kb-doctor` for maintenance and potentially for rigor validation checks based on `verification-agent` reports. Manages self-correction loops.
    *   **Dependencies:** All modes, User, `philosophy-operational-context-manager` (for operational context).
*   **`philosophy-meta-reflector` (V13, Context-Aware V14):**
    *   **Responsibility:** Performs meta-level analysis of the system, including evaluating the effectiveness of rigor enforcement. Analyzes operational memory logs, docs, rules, KB content. Stores reflections/questions in KB. Proposes KB/System modifications via orchestrator.
    *   **Interaction (V18.1):** Queries `philosophy-operational-context-manager` for operational context. Directly Reads KB content using file tools. Directly Writes findings to KB. Sends proposals to `Orchestrator`.
    *   **Dependencies:** `philosophy-orchestrator`, File system tools, `philosophy-operational-context-manager`, potentially `architect`, `devops`.

## 5. V18.1 Mode Interaction Diagram (Mermaid - Revised, Linux Paths)

```mermaid
graph TD
    subgraph User Interaction
        User(User)
    end

    subgraph Orchestration
        Orchestrator(philosophy-orchestrator)
    end

    subgraph KB Maintenance & Rigor Validation
        KBDoctor(philosophy-kb-doctor)
    end

    subgraph Text Processing
        TextProc(philosophy-text-processor) -- Runs --> Scripts((External Scripts))
    end

    subgraph Analysis & Inquiry (Rigor Focused)
        PreLec(philosophy-pre-lecture)
        ClassAn(philosophy-class-analysis)
        SecLit(philosophy-secondary-lit)
        DialAn(philosophy-dialectical-analysis)
        Quest(philosophy-questioning)
    end

    subgraph Meta-Reflection
        MetaReflector(philosophy-meta-reflector)
    end

    subgraph Essay Generation & Verification (Rigor Focused)
        EssayPrep(philosophy-essay-prep) -- Git Ops --> VCS[(Version Control System<br>(Git))]
        DraftGen(philosophy-draft-generator)
        CiteMan(philosophy-citation-manager)
        Verify(philosophy-verification-agent)
    end

    subgraph Data Layer
        subgraph Operational Context
             style OpCtx fill:#e0e0e0,stroke:#666,stroke-width:1px
             OpCtxMan(philosophy-operational-context-manager)
             OpMemBank[(Operational Memory Bank<br>memory-bank/)]
             OpCtxMan -- Manages --> OpMemBank
        end
        subgraph Philosophical Knowledge Base [Domain Knowledge & Domain Operations]
            style PhilKB fill:#f9f,stroke:#333,stroke-width:2px
            PhilKB_Data[(Philosophy KB Data<br>philosophy-knowledge-base/<br>concepts/, arguments/, etc.<br>+ Rigor Fields)]
            PhilKB_Ops[(KB Operational<br>philosophy-knowledge-base/_operational/)]

            subgraph KB_Ops_Details ["_operational/"]
                 style KBOps fill:#add8e6,stroke:#00008b,stroke-width:1px,stroke-dasharray: 2 2
                 KB_Indices("indices/")
                 KB_Logs("logs/")
                 KB_Status("status/")
                 KB_Reports("reports/")
                 KB_Scripts("maintenance_scripts/<br>+ Rigor Validation Scripts?")
            end
            PhilKB_Ops --> KB_Ops_Details
        end
        RawSource[(Raw Source Materials<br>source_materials/raw/)]
        ProcessedSource[(Processed Source<br>source_materials/processed/)]
        Workspace(analysis_workspace / essay_prep)
    end

    %% Core Flow & Orchestration
    User -- Request --> Orchestrator
    Orchestrator -- Delegate Tasks --> TextProc
    Orchestrator -- Delegate Tasks --> PreLec
    Orchestrator -- Delegate Tasks --> ClassAn
    Orchestrator -- Delegate Tasks --> SecLit
    Orchestrator -- Delegate Tasks --> DialAn
    Orchestrator -- Delegate Tasks --> Quest
    Orchestrator -- Delegate Tasks --> EssayPrep
    Orchestrator -- Delegate Tasks/Trigger --> MetaReflector
    Orchestrator -- Coordinate Commit? --> EssayPrep
    Orchestrator -- Trigger KB Maintenance/Validation --> KBDoctor
    Orchestrator -- Route KB/System Mod Proposal --> User
    Orchestrator -- Relay Approval --> Architect
    Orchestrator -- Relay Approval --> DevOps
    Orchestrator -- Manage Self-Correction Loop --> Verify/KBDoctor/AnalysisModes
    Orchestrator -- Results --> User

    %% Text Processing Flow (V18 Direct Write)
    TextProc -- Reads --> RawSource
    TextProc -- Processed Chunks --> ProcessedSource
    TextProc -- Direct Write KB (Index, Citations, Context) --> PhilKB_Data

    %% Analysis & Inquiry Flow (V18.1 Direct R/W + Rigor)
    PreLec -- Direct Write KB (Analysis + Rigor Fields) --> PhilKB_Data
    ClassAn -- Direct Write KB (Analysis + Rigor Fields) --> PhilKB_Data
    SecLit -- Direct Write KB (Analysis + Rigor Fields) --> PhilKB_Data
    DialAn -- Direct Write KB (Analysis + Rigor Fields) --> PhilKB_Data
    Quest -- Direct Write KB (Refined Qs + Rigor Fields) --> PhilKB_Data

    PreLec -- Direct Read KB (incl. Related Context) --> PhilKB_Data
    ClassAn -- Direct Read KB (incl. Related Context) --> PhilKB_Data
    SecLit -- Direct Read KB (incl. Related Context) --> PhilKB_Data
    DialAn -- Direct Read KB (incl. Related Context) --> PhilKB_Data
    Quest -- Direct Read KB (incl. Related Context) --> PhilKB_Data

    %% Essay Flow (V18.1 Direct R/W + Rigor)
    EssayPrep -- Direct Read KB (Thesis Context + Rigor) --> PhilKB_Data
    EssayPrep -- Direct Write KB (Thesis + Rigor) --> PhilKB_Data
    EssayPrep -- Request Draft --> DraftGen
    EssayPrep -- Request Citation --> CiteMan
    EssayPrep -- Request Verification --> Verify
    EssayPrep -- Manage Files --> Workspace

    DraftGen -- Direct Read KB (Evidence + Rigor) --> PhilKB_Data
    DraftGen -- Draft --> EssayPrep
    DraftGen -- Trigger Commit --> Orchestrator

    CiteMan -- Direct Read KB (Refs + Rigor) --> PhilKB_Data
    CiteMan -- Cited Draft/Biblio --> EssayPrep
    CiteMan -- Trigger Commit --> Orchestrator

    Verify -- Direct Read KB (Draft, Evidence, Rigor Fields) --> PhilKB_Data
    Verify -- Verification Report (incl. Rigor Check) --> EssayPrep
    Verify -- Trigger Correction Loop? --> Orchestrator

    %% Meta-Reflection Flow (V18.1 Direct R/W)
    MetaReflector -- Direct Read KB --> PhilKB_Data
    MetaReflector -- Query OpCtx --> OpCtxMan
    MetaReflector -- Read Docs/Rules --> Workspace/.roo/docs
    MetaReflector -- Direct Write KB (Reflections + Rigor) --> PhilKB_Data
    MetaReflector -- Propose KB Mod --> Orchestrator
    MetaReflector -- Propose Arch Mod --> Orchestrator
    MetaReflector -- Propose Method/Git Mod --> Orchestrator

    %% KB Doctor Interactions (Maintenance + Rigor Validation)
    KBDoctor -- Triggers --> KB_Scripts
    KB_Scripts -- Read/Write --> PhilKB_Data
    KB_Scripts -- Read/Write --> KB_Indices
    KB_Scripts -- Write Logs --> KB_Logs
    KB_Scripts -- Write Status --> KB_Status
    KB_Scripts -- Perform Rigor Validation --> PhilKB_Data
    KBDoctor -- Reads Status/Logs --> PhilKB_Ops
    KBDoctor -- Writes Reports (incl. Rigor Summary) --> KB_Reports
    KBDoctor -- Report Status/Rigor --> Orchestrator

    %% Operational Context Manager Interactions
    OpCtxMan -- Access/Update --> OpMemBank
    Orchestrator -- Use OpCtx --> OpCtxMan
    TextProc -- Use OpCtx --> OpCtxMan
    PreLec -- Use OpCtx --> OpCtxMan
    ClassAn -- Use OpCtx --> OpCtxMan
    SecLit -- Use OpCtx --> OpCtxMan
    DialAn -- Use OpCtx --> OpCtxMan
    Quest -- Use OpCtx --> OpCtxMan
    EssayPrep -- Use OpCtx --> OpCtxMan
    DraftGen -- Use OpCtx --> OpCtxMan
    CiteMan -- Use OpCtx --> OpCtxMan
    Verify -- Use OpCtx --> OpCtxMan
    MetaReflector -- Use OpCtx --> OpCtxMan
    KBDoctor -- Use OpCtx --> OpCtxMan


    %% Styling
    classDef kb fill:#f9f,stroke:#333,stroke-width:2px;
    class PhilKB_Data, PhilKB_Ops kb;
    classDef mode fill:#ccf,stroke:#333,stroke-width:1px;
    class Orchestrator,TextProc,PreLec,ClassAn,SecLit,DialAn,Quest,EssayPrep,DraftGen,CiteMan,Verify,OpCtxMan,MetaReflector,KBDoctor mode;
    classDef script fill:#f0ad4e,stroke:#333,stroke-width:1px;
    class Scripts, KB_Scripts script;
    classDef vcs fill:#d9edf7,stroke:#31708f,stroke-width:1px;
    class VCS vcs;
    classDef opmembank fill:#e0e0e0,stroke:#666,stroke-width:1px;
    class OpMemBank opmembank;
    classDef source fill:#dff0d8,stroke:#3c763d,stroke-width:1px;
    class RawSource,ProcessedSource source;
    classDef kbops fill:#add8e6,stroke:#00008b,stroke-width:1px,stroke-dasharray: 2 2;
    class KB_Indices,KB_Logs,KB_Status,KB_Reports,KB_Scripts kbops;
```

**Diagram Notes:**
*   Reflects V18.1 enhancements (Revised).
*   Modes directly Read/Write `PhilKB_Data`, including rigor fields.
*   `KBDoctor` triggers maintenance and rigor validation scripts.
*   `Verify` explicitly checks rigor elements and can trigger correction loop via `Orchestrator`.
*   Analysis modes query related context and write rigor fields.
*   All paths use forward slashes (`/`).
*   "SPARC" references removed; Operational Memory Bank (`memory-bank/`) managed by `philosophy-operational-context-manager`.

## 6. Philosophy Knowledge Base (KB) - V18.1 Design (Revised, Rigor Enhanced, Linux Paths)

*   **Location:** `philosophy-knowledge-base/`
*   **Purpose:** Centralized, structured, persistent repository for **philosophical domain knowledge**, distinct from operational memory. Enhanced for philosophical rigor.
*   **Management (V18.1):**
    *   **Content:** Managed directly by relevant modes using file tools, following defined write patterns/locations and **populating rigor-related fields**.
    *   **Maintenance & Rigor Validation:** Orchestrated by `philosophy-kb-doctor`, triggering scripts in `_operational/maintenance_scripts/` for indexing, validation, linking, cleanup, and **rigor consistency checks**.
*   **Structure:** Subdirectories based on content type, plus operational directories:
    *   `concepts/`, `arguments/`, `quotations/`, `references/`, `questions/`, `theses/`, `relationships/`, `methods/`, `meta-reflections/`, `indices/`, `processed_texts/` (or similar)
    *   `_operational/`
        *   `logs/` (Logs from maintenance/validation scripts)
        *   `status/` (Status files for maintenance/validation tasks)
        *   `reports/` (Reports from KB Doctor/scripts, incl. rigor validation summaries)
        *   `maintenance_scripts/` (Scripts for indexing, validation, rigor checks, etc.)
        *   `formatting_templates_rules/` (Schemas/rules for validation)
*   **Entry Format (Markdown + YAML - V18.1 Rigor Enhanced):**
    ```yaml
    ---
    id: [UUID] # Generated by mode creating the entry or maintenance script
    type: [Concept | Argument | Quotation | Reference | Question | Thesis | Relationship | Method | Meta-Reflection | Index | ProcessedTextChunk] # Matches subdirectory
    timestamp: [YYYY-MM-DD HH:MM:SS] # Creation/last modification
    generating_mode: [mode-slug] # Mode that originated the data

    # --- Rigor & Context Fields (V18.1 Additions/Emphasis) ---
    # For Concepts/Arguments primarily, adapt as needed for others:
    positive_determination: "..." # What the concept/argument IS or asserts.
    negative_determination: "..." # What the concept/argument is NOT or excludes.
    ordinary_language_contrast: "..." # How it differs from everyday usage.
    related_terms: [[term_id_1, term_id_2]] # Link to related concepts/arguments.
    presuppositions: ["...", "..."] # Underlying assumptions.
    ambiguities: ["...", "..."] # Identified areas of unclear meaning.
    counter_arguments: [[arg_id_1, arg_id_2]] # Link to opposing arguments.
    secondary_source_links: [[ref_id_1, ref_id_2]] # Link to relevant secondary literature Reference entries.
    other_philosopher_views: [[ref_id_3, concept_id_x]] # Link to KB entries on other philosophers' related views.
    verification_status: [Unverified | Verified | Disputed] # Set/updated by verification-agent or kb-doctor
    verification_notes: "..." # Details from verification process.

    # --- V14 Context Tags (Retained) ---
    tags: [
      # Context Tags (Extracted by text-processor from source path):
      "context:type:[course|project|external_lit|personal_note]",
      "context:id:[course_code|project_name|general_topic]",
      "context:subtype:[reading|lecture|note|primary|secondary]",
      # Standard Tags (Added by analysis modes):
      "hegel", "logic", "critique", "meta", "inquiry", ...
    ]

    # --- Linking & Source Fields (V11+, Emphasized V18.1) ---
    source_ref_keys: [[ref_key_1, ...]] # CRITICAL: Link to Reference entries for source texts.
    extraction_markers: [[marker_1, ...]] # CRITICAL: Link to specific locations in source_materials/processed/ or raw source.
    related_ids: [[id_1, ...]] # General links to other KB entries (concepts, arguments, etc.).

    # --- Type-Specific Fields ---
    # (Examples: definition, premises, conclusion, question_text, thesis_statement, reflection_summary, method_description, index_path, chunk_summary, etc.)
    ---

    # Main Content (Markdown)
    [Detailed description, analysis, text, etc. reflecting rigor elements.]
    ```
*   **Self-Modification:** Proposals -> `Orchestrator` -> User Approval -> `Orchestrator` -> Implementation by modes/scripts.

## 7. Workflow Designs (V18.1 Revised - Rigor Enhanced)

### 7.1. Philosophical Inquiry & Analysis Workflow (Context-Aware, Direct Access, Rigor Focused)

1.  **Input:** User prompt OR Analysis modes identify potential questions/concepts from source material (processed by `text-processor`).
2.  **Analysis & Rigor Check:** Analysis modes (`pre-lecture`, `class-analysis`, `secondary-lit`, `dialectical-analysis`) **directly read** source chunks/related KB entries (using context tags, `related_ids`). They analyze content, explicitly identifying/documenting **rigor elements** (determinacy, presuppositions, ambiguities, counter-arguments, related terms, secondary sources via KB links).
3.  **Storage (Analysis + Rigor):** Analysis modes **directly write** findings (concepts, arguments, proto-questions) to designated KB locations, **populating rigor fields** and ensuring links (`source_ref_keys`, `extraction_markers`, `related_ids`) are set.
4.  **Refinement:** `philosophy-questioning` **directly reads** proto-questions/concepts/arguments from KB, focusing on rigor elements (ambiguities, presuppositions). Refines questions for clarity and determinacy.
5.  **Storage (Refined Qs + Rigor):** `philosophy-questioning` **directly writes** refined questions (tagged `inquiry`) to KB, including analysis of their scope/presuppositions.
6.  **Thesis Development:** `philosophy-essay-prep` **directly reads** refined questions/support material (incl. counter-arguments, secondary views) from KB. Develops a determinate thesis addressing rigor context.
7.  **Storage (Thesis + Rigor):** `philosophy-essay-prep` **directly writes** thesis to KB, documenting its scope and relation to rigor elements.
8.  **Essay Cycle:** Essay modes **directly read** thesis/evidence (incl. rigor fields) from KB.

### 7.2. Verification Workflow (Rigor Focused)

1.  **Trigger:** `EssayPrep` requests verification of a draft section/claim.
2.  **Activation:** `Orchestrator` delegates to `philosophy-verification-agent`.
3.  **Evidence Gathering:** `verification-agent` **directly reads** the draft claim, cited KB entries (arguments, concepts, references, including their rigor fields), and linked source chunks (`extraction_markers`) from `philosophy-knowledge-base/` and `source_materials/processed/`.
4.  **Verification & Rigor Check:** `verification-agent` compares the claim against evidence, checks citation accuracy (`source_ref_keys`), evaluates source validity, and **explicitly verifies rigor elements**: Is the claim determinate? Are presuppositions acknowledged? Are counter-arguments addressed appropriately? Is evidence sufficient?
5.  **Reporting:** `verification-agent` generates a report detailing findings, including rigor gaps or inconsistencies. Updates `verification_status` and `verification_notes` in relevant KB entries.
6.  **Correction Loop Trigger:** If significant rigor issues or factual errors are found, `verification-agent` flags this in the report and notifies `Orchestrator`.
7.  **Orchestrator Action:** `Orchestrator` initiates a correction loop, potentially delegating back to analysis modes (`dialectical-analysis`, `class-analysis`) to refine KB entries or to `EssayPrep` to revise the draft based on the verification report. May trigger `KBDoctor` for broader consistency checks if systemic issues suspected.

### 7.3. System Self-Reflection Workflow (Context-Aware, Direct Access)

(Largely unchanged from V18, but analysis includes evaluation of rigor enforcement effectiveness)

1.  **Trigger:** User, Anomaly Detection, Schedule.
2.  **Activation:** `Orchestrator` delegates to `philosophy-meta-reflector`.
3.  **Analysis:** `meta-reflector` queries `philosophy-operational-context-manager` (Operational Memory), reads docs/rules, **directly reads** KB content (reflections, methods, rigor validation reports), applying context filters. Evaluates system performance, including rigor consistency.
4.  **Reflection:** `meta-reflector` generates meta-reflections/questions about system effectiveness, biases, limitations, including rigor handling.
5.  **Storage (Reflection):** `meta-reflector` **directly writes** findings to KB (tagged `meta`).
6.  **Proposal Generation (Optional):** `meta-reflector` formulates proposals (KB Change, Arch Change, Method Change, Rigor Rule Change).
7.  **Proposal Routing/Approval:** Proposals -> `Orchestrator` -> User -> `Orchestrator` -> Approved changes implemented.
8.  **Reporting:** `meta-reflector` reports to `Orchestrator`/User.

## 8. Version Control (V14 - Retained, Linux Paths)

*   **Primary Scope:** `essay_prep/` managed by `philosophy-essay-prep` using Git via `execute_command`.
*   **Potential Expansion (Considerations):**
    *   KB Versioning (`philosophy-knowledge-base/`). Requires careful strategy (e.g., Git LFS, dedicated KB versioning tools).
    *   System Evolution Branching (triggered by `meta-reflector` proposals).
*   **Implementation:** Via `execute_command`.

## 9. Configuration Structure (V18.1 Revised - Linux Paths)

*   **Mode Definition File (`.roo/.roomodes`):** Defines all V18.1 modes and their `.clinerules` paths. Uses forward slashes (`/`).
    ```json
    {
      "philosophy-orchestrator": ".roo/rules-philosophy-orchestrator/philosophy-orchestrator.clinerules",
      "philosophy-text-processor": ".roo/rules-philosophy-text-processor/philosophy-text-processor.clinerules",
      "philosophy-pre-lecture": ".roo/rules-philosophy-pre-lecture/philosophy-pre-lecture.clinerules",
      "philosophy-class-analysis": ".roo/rules-philosophy-class-analysis/philosophy-class-analysis.clinerules",
      "philosophy-secondary-lit": ".roo/rules-philosophy-secondary-lit/philosophy-secondary-lit.clinerules",
      "philosophy-dialectical-analysis": ".roo/rules-philosophy-dialectical-analysis/philosophy-dialectical-analysis.clinerules",
      "philosophy-questioning": ".roo/rules-philosophy-questioning/philosophy-questioning.clinerules",
      "philosophy-essay-prep": ".roo/rules-philosophy-essay-prep/philosophy-essay-prep.clinerules",
      "philosophy-operational-context-manager": ".roo/rules-philosophy-operational-context-manager/philosophy-operational-context-manager.clinerules", // Manages Operational Memory Bank
      "philosophy-kb-doctor": ".roo/rules-philosophy-kb-doctor/philosophy-kb-doctor.clinerules", // Manages KB Maintenance & Rigor Validation
      "philosophy-draft-generator": ".roo/rules-philosophy-draft-generator/philosophy-draft-generator.clinerules",
      "philosophy-citation-manager": ".roo/rules-philosophy-citation-manager/philosophy-citation-manager.clinerules",
      "philosophy-verification-agent": ".roo/rules-philosophy-verification-agent/philosophy-verification-agent.clinerules",
      "philosophy-meta-reflector": ".roo/rules-philosophy-meta-reflector/philosophy-meta-reflector.clinerules"
      // Add other non-philosophy modes if they exist in the same config
    }
    ```
*   **Rules File Directory Structure:** `.roo/rules-[mode-slug]/[mode-slug].clinerules`. `.clinerules` for relevant modes must be updated per V18.1 specs (direct KB access logic, rigor element handling, KB Doctor interaction if applicable). Uses forward slashes (`/`).