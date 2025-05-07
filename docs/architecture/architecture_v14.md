# Hegel Philosophy RooCode Suite - Architecture V14

**Date:** 2025-05-02
**Version:** 14.0
**Status:** Draft (Self-Contained Re-attempt)
**Based On:**
*   `docs/architecture/architecture_v13.md` (Content Merged)
*   `docs/specs/v13_requirements_spec_v1.md` (Content Merged)
*   User Task & Feedback (V13 Architectural Gap - Source Context Handling, as of 2025-05-02 03:29)
*   User Feedback (V14 Docs Insufficient Detail, as of 2025-05-02 04:18)
*   Memory Bank Context (as of 2025-05-02 05:06)

**Goal:** Define the V14 architecture, integrating a dedicated **Philosophy Knowledge Base (KB)**, a **Philosophical Inquiry Workflow**, a **System Self-Reflection Workflow**, and **Source Material Context Handling** into the V12 structure. This version emphasizes a clear separation between domain knowledge (KB) and process memory (Operational Memory), introduces meta-reflective capabilities, standardizes source input, specifies context capture/storage/querying, and refines mode responsibilities accordingly. This document aims to be self-contained and detailed.

## 1. Core Principles (V14)

*   **Determinacy:** Concepts/arguments clearly defined within the KB. (V11+)
*   **Evidence Saturation:** Claims linked to sources via KB entries (`source_ref_keys`, `extraction_markers`). (V11+)
*   **Chronological Integrity:** Analysis respects temporal flow of sources and system operations. (V11+)
*   **Verification Rigor:** Inputs/outputs verified against KB & sources. (V11+)
*   **Modularity:** Encapsulated functionality in specialized modes with defined responsibilities. (V11+)
*   **Orchestration:** Complex workflows managed by `philosophy-orchestrator`. (V11+)
*   **Traceability:** Version control (Git) for key artifacts (essays, potentially KB/config). (V12+)
*   **Knowledge Separation:** Explicit distinction between philosophical domain knowledge (`philosophy-knowledge-base/`) and operational/process memory (`memory-bank/`). (V13+)
*   **Reflexivity:** Capacity for the system to question its own assumptions, methods, and architecture (`philosophy-meta-reflector`). (V13+)
*   **Controlled Evolution:** Mechanisms for proposing and approving modifications to the KB and potentially the system architecture itself. (V13+)
*   **Source Contextualization (New V14):** Raw source materials are organized by context (`source_materials/raw/`), and this context is explicitly captured, stored as tags in the KB, and queryable.

## 2. V14 Architecture Overview

V14 integrates several key components into the V12 baseline:

1.  **Philosophy Knowledge Base (KB):** A dedicated, structured repository (`philosophy-knowledge-base/`) for philosophical concepts, arguments, references, questions, theses, methods, meta-reflections, and indices. Managed exclusively by `philosophy-kb-manager`. (V13 Core)
2.  **Source Material Organization & Context Handling (V14 Refinement):**
    *   **Standardized Input Structure:** Raw source materials consolidated under `source_materials/raw/` and organized hierarchically by context (e.g., course, project, type).
    *   **Context Extraction:** `philosophy-text-processor` extracts context information (e.g., `type:course`, `id:PHL316`, `subtype:reading`) from the source file path.
    *   **Context Storage:** Context stored as structured tags (`context:key:value`) within the YAML frontmatter of corresponding KB entries by `philosophy-kb-manager`.
    *   **Contextual Querying:** `philosophy-kb-manager` enables filtering KB queries based on context tags.
3.  **Philosophical Inquiry Workflow:** Leverages analysis modes, `philosophy-questioning`, and `philosophy-essay-prep` to generate, refine, and store philosophical questions and theses within the context-aware KB. (V13 Core, Context-Aware V14)
4.  **System Self-Reflection Workflow:** Introduces `philosophy-meta-reflector` for meta-level analysis of the system, storing reflections in the context-aware KB and proposing changes. (V13 Core, Context-Aware V14)
5.  **Mode Refinements:** Responsibilities adjusted for KB interaction, context handling, and workflow participation. `philosophy-evidence-manager` scope limited to Operational Memory.

## 3. Source Material Organization (V14)

*   **Raw Input Location:** `source_materials/raw/`
*   **Purpose:** Centralized location for all original source materials before processing. Provides a clear, machine-parsable structure for determining source context.
*   **Structure:** Hierarchical directories define context. This structure allows `philosophy-text-processor` to derive context automatically from the file path. It is designed to be scalable for new courses, projects, or literature types.
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
    These are then formatted as tags: `context:type:course`, `context:id:PHL316`, `context:subtype:reading`.

## 4. Mode Structure & Responsibilities (V14)

### 4.1. Core Data Management Modes

*   **`philosophy-kb-manager` (V13, Enhanced for V14):**
    *   **Responsibility:** Sole interface to `philosophy-knowledge-base/`. Handles CRUD, querying, linking, and integrity for structured philosophical data. **V14:** Accepts context tags from `text-processor`, stores them in entry YAML (`tags` list using `context:key:value` format), and supports querying/filtering based on these tags. Executes approved KB modifications.
    *   **Input:** Structured queries (potentially with context filters), structured data for storage (potentially with context tags), approved modification instructions.
    *   **Output:** Formatted philosophical data packages, confirmations, errors.
    *   **Dependencies:** `philosophy-orchestrator`, All modes requiring KB access, `philosophy-evidence-manager` (for operational context if needed).
*   **`philosophy-evidence-manager` (V13 Revised Scope):**
    *   **Responsibility:** Manages access **only** to Operational Memory (`memory-bank/`) and potentially `analysis_workspace/`. Handles operational context queries. **Does NOT interact with `philosophy-knowledge-base/`.**
    *   **Input:** Queries for operational context, operational context data for storage.
    *   **Output:** operational context data, confirmations.
    *   **Dependencies:** All modes (for operational context), `memory-bank/` files.

### 4.2. Text Processing & Analysis Modes

*   **`philosophy-text-processor` (V12, Enhanced for V14):**
    *   **Responsibility:** Pre-processes source texts from `source_materials/raw/` via external scripts (chunking, indexing, citation extraction). **V14:** Parses input path to extract context (`type`, `id`, `subtype`).
    *   **Output:** Processed chunks to `source_materials/processed/`. Index/chunk info, citation data, **and extracted context tags** provided to `philosophy-kb-manager`.
    *   **Dependencies:** External scripts, `philosophy-orchestrator`, `philosophy-kb-manager`.
*   **Analysis Modes (`pre-lecture`, `class-analysis`, `secondary-lit`, `dialectical-analysis`, `questioning`):**
    *   **Responsibility:** Analyze sources/KB content, generate concepts, arguments, questions, etc.
    *   **Interaction (V14):** Query `philosophy-kb-manager` for processed texts/indices and existing KB entries, **optionally filtering by context tags**. Store findings (concepts, proto-questions, refined questions, analyses) via `philosophy-kb-manager` (context tags are implicitly associated via the source or explicitly added if generated without direct source). Query `philosophy-evidence-manager` for operational context if needed. `philosophy-questioning` focuses on refining *philosophical inquiry* questions.

### 4.3. Essay Generation & Verification Modes

*   **`philosophy-essay-prep` (V11+):**
    *   **Responsibility:** Manages essay writing process, including thesis development and outline. Manages Git for essays.
    *   **Interaction (V14):** Queries `philosophy-kb-manager` for relevant KB entries, **optionally filtering by context tags** (e.g., specific course or project). Stores developed thesis via `philosophy-kb-manager`. Coordinates other essay modes. Executes Git commands.
*   **`philosophy-draft-generator` (V11+):**
    *   **Responsibility:** Generates prose based on outline and evidence.
    *   **Interaction (V14):** Requests evidence package from `philosophy-kb-manager` (likely via `essay-prep`), potentially with context filters.
*   **`philosophy-citation-manager` (V11+):**
    *   **Responsibility:** Formats citations and bibliography.
    *   **Interaction (V14):** Requests reference details and citation location data from `philosophy-kb-manager`, potentially filtered by context.
*   **`philosophy-verification-agent` (V11+):**
    *   **Responsibility:** Verifies claims and citations.
    *   **Interaction (V14):** Requests evidence, references, and processed chunk paths/indices from `philosophy-kb-manager`, potentially filtered by context.

### 4.4. Orchestration & Meta-Reflection Modes

*   **`philosophy-orchestrator` (V11+):**
    *   **Responsibility:** Manages workflows (including V13 Inquiry & Reflection, now context-aware), delegates tasks, handles handoffs, routes proposals (KB/System mods) for user approval, relays approvals. Coordinates Git commits.
    *   **Dependencies:** All modes, User.
*   **`philosophy-meta-reflector` (V13, Context-Aware V14):**
    *   **Responsibility:** Performs meta-level analysis of the system (architecture, methods, biases) based on `architecture-questioning.md`. Analyzes MB logs, docs, rules, KB content. Stores reflections/questions in KB. Proposes KB/System modifications via orchestrator.
    *   **Interaction (V14):** Queries `philosophy-evidence-manager` for operational context. Queries `philosophy-kb-manager` for KB content, **optionally filtering by context tags** to perform context-specific analysis. Stores findings via `kb-manager`. Sends proposals to `Orchestrator`.
    *   **Dependencies:** `philosophy-orchestrator`, `philosophy-kb-manager`, `philosophy-evidence-manager`, potentially `architect`, `devops`.

## 5. V14 Mode Interaction Diagram (Mermaid)

```mermaid
graph TD
    subgraph User Interaction
        User(User)
    end

    subgraph Orchestration
        Orchestrator(philosophy-orchestrator)
    end

    subgraph Meta-Reflection
        MetaReflector(philosophy-meta-reflector)
    end

    subgraph Text Processing
        TextProc(philosophy-text-processor) -- Extracts Context & Runs --> Scripts((External Scripts))
    end

    subgraph Analysis & Inquiry
        PreLec(philosophy-pre-lecture)
        ClassAn(philosophy-class-analysis)
        SecLit(philosophy-secondary-lit)
        DialAn(philosophy-dialectical-analysis)
        Quest(philosophy-questioning)
    end

    subgraph Essay Generation & Verification
        EssayPrep(philosophy-essay-prep) -- Git Ops --> VCS[(Version Control System<br>(Git))]
        DraftGen(philosophy-draft-generator)
        CiteMan(philosophy-citation-manager)
        Verify(philosophy-verification-agent)
    end

    subgraph Data Layer
        subgraph Operational Memory
            EvidMan(philosophy-evidence-manager)
            OPERATIONALMB[(Operational Memory<br>memory-bank/)]
        end
        subgraph Philosophical Knowledge Base
            KBMan(philosophy-kb-manager <br> Context-Aware)
            PhilKB[(Philosophy KB<br>philosophy-knowledge-base/ <br> w/ Context Tags)]
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
    Orchestrator -- Route KB/System Mod Proposal --> User
    Orchestrator -- Relay Approval --> KBMan
    Orchestrator -- Relay Approval --> Architect
    Orchestrator -- Relay Approval --> DevOps
    Orchestrator -- Results --> User

    %% Text Processing Flow (V14 Update)
    TextProc -- Reads --> RawSource
    TextProc -- Processed Chunks --> ProcessedSource
    TextProc -- Store Index/Chunk Info, Citations & Context Tags --> KBMan

    %% Analysis & Inquiry Flow (Context-Aware Queries)
    PreLec -- Store Analysis/ProtoQs --> KBMan
    ClassAn -- Store Analysis/ProtoQs --> KBMan
    SecLit -- Store Analysis/ProtoQs --> KBMan
    DialAn -- Store Analysis/ProtoQs --> KBMan
    Quest -- Store RefinedQs --> KBMan

    PreLec -- Query KB w/ Context Filter? --> KBMan
    ClassAn -- Query KB w/ Context Filter? --> KBMan
    SecLit -- Query KB w/ Context Filter? --> KBMan
    DialAn -- Query KB w/ Context Filter? --> KBMan
    Quest -- Query KB w/ Context Filter? --> KBMan

    %% Essay Flow (Context-Aware Queries)
    EssayPrep -- Request KB Data w/ Context Filter? --> KBMan
    EssayPrep -- Store Thesis --> KBMan
    EssayPrep -- Request Draft --> DraftGen
    EssayPrep -- Request Citation --> CiteMan
    EssayPrep -- Request Verification --> Verify
    EssayPrep -- Manage Files --> Workspace

    DraftGen -- Request KB Data w/ Context Filter? --> KBMan
    DraftGen -- Draft --> EssayPrep
    DraftGen -- Trigger Commit --> Orchestrator

    CiteMan -- Request KB Data w/ Context Filter? --> KBMan
    CiteMan -- Cited Draft/Biblio --> EssayPrep
    CiteMan -- Trigger Commit --> Orchestrator

    Verify -- Request KB Data/Chunks w/ Context Filter? --> KBMan
    Verify -- Verification Report --> EssayPrep

    %% Meta-Reflection Flow (Context-Aware Queries)
    MetaReflector -- Query KB w/ Context Filter? --> KBMan
    MetaReflector -- Query MB --> EvidMan
    MetaReflector -- Read Docs/Rules --> Workspace/.roo/docs
    MetaReflector -- Store Meta-Reflections/Qs --> KBMan
    MetaReflector -- Propose KB Mod --> Orchestrator
    MetaReflector -- Propose Arch Mod --> Orchestrator
    MetaReflector -- Propose Method/Git Mod --> Orchestrator

    %% KB Manager Interactions
    KBMan -- Access/Update --> PhilKB
    KBMan -- Provide Data/Paths --> TextProc
    KBMan -- Provide Data/Paths --> PreLec
    KBMan -- Provide Data/Paths --> ClassAn
    KBMan -- Provide Data/Paths --> SecLit
    KBMan -- Provide Data/Paths --> DialAn
    KBMan -- Provide Data/Paths --> Quest
    KBMan -- Provide Data/Paths --> EssayPrep
    KBMan -- Provide Data/Paths --> DraftGen
    KBMan -- Provide Data/Paths --> CiteMan
    KBMan -- Provide Data/Paths --> Verify
    KBMan -- Provide Data/Paths --> MetaReflector
    KBMan -- Execute Approved Modification --> PhilKB

    %% Evidence Manager Interactions (Operational Context)
    EvidMan -- Access/Update --> OPERATIONALMB
    EvidMan -- Provide Operational Context --> Orchestrator
    EvidMan -- Provide Operational Context --> TextProc
    EvidMan -- Provide Operational Context --> PreLec
    EvidMan -- Provide Operational Context --> ClassAn
    EvidMan -- Provide Operational Context --> SecLit
    EvidMan -- Provide Operational Context --> DialAn
    EvidMan -- Provide Operational Context --> Quest
    EvidMan -- Provide Operational Context --> EssayPrep
    EvidMan -- Provide Operational Context --> DraftGen
    EvidMan -- Provide Operational Context --> CiteMan
    EvidMan -- Provide Operational Context --> Verify
    EvidMan -- Provide Operational Context --> KBMan
    EvidMan -- Provide Operational Context --> MetaReflector


    %% Styling
    classDef kb fill:#f9f,stroke:#333,stroke-width:2px;
    class PhilKB kb;
    classDef mode fill:#ccf,stroke:#333,stroke-width:1px;
    class Orchestrator,TextProc,PreLec,ClassAn,SecLit,DialAn,Quest,EssayPrep,DraftGen,CiteMan,Verify,EvidMan,KBMan,MetaReflector mode;
    classDef script fill:#f0ad4e,stroke:#333,stroke-width:1px;
    class Scripts script;
    classDef vcs fill:#d9edf7,stroke:#31708f,stroke-width:1px;
    class VCS vcs;
    classDef operationalmb fill:#e0e0e0,stroke:#666,stroke-width:1px;
    class OPERATIONALMB operationalmb;
    classDef source fill:#dff0d8,stroke:#3c763d,stroke-width:1px;
    class RawSource,ProcessedSource source;
```

**Diagram Notes:**
*   Shows `RawSource` as input to `TextProc`.
*   `TextProc` extracts context and sends data + context tags to `KBMan`.
*   `KBMan` manages `PhilKB`, which contains context tags.
*   Modes query `KBMan` with optional context filters.
*   `EvidMan` manages `OPERATIONALMB` (operational context).
*   `MetaReflector` interacts with `KBMan`, `EvidMan`, and `Orchestrator`.
*   Workflows (Inquiry, Reflection, Modification) operate via `Orchestrator`.

## 6. Philosophy Knowledge Base (KB) - V14 Design

*   **Location:** `philosophy-knowledge-base/`
*   **Purpose:** Centralized, structured, persistent repository for **philosophical domain knowledge**, distinct from operational memory.
*   **Management:** Exclusively managed via `philosophy-kb-manager` mode.
*   **Structure:** Subdirectories based on content type:
    *   `concepts/`, `arguments/`, `quotations/`, `references/`, `questions/`, `theses/`, `relationships/`, `methods/`, `meta-reflections/`, `indices/`
*   **Entry Format (Markdown + YAML):**
    ```yaml
    ---
    id: [UUID] # Generated by kb-manager
    type: [Concept | Argument | Quotation | Reference | Question | Thesis | Relationship | Method | Meta-Reflection | Index] # Matches subdirectory
    timestamp: [YYYY-MM-DD HH:MM:SS] # Creation/last modification
    generating_mode: [mode-slug] # Mode that originated the data
    # --- V14 Context Tags (if applicable) ---
    tags: [
      # Context Tags (Extracted by text-processor from source path):
      "context:type:[course|project|external_lit|personal_note]",
      "context:id:[course_code|project_name|general_topic]",
      "context:subtype:[reading|lecture|note|primary|secondary]",
      # Standard Tags (Added by analysis modes or kb-manager):
      "hegel", "logic", "critique", "meta", "inquiry", ...
    ]
    # --- Optional/Contextual Fields ---
    source_ref_keys: [[ref_key_1, ...]] # Link to Reference entries
    extraction_markers: [[marker_1, ...]] # Link to source_materials/processed/
    related_ids: [[id_1, ...]] # Links to other KB entries
    # --- Type-Specific Fields ---
    # (Examples: definition, premises, conclusion, question_text, thesis_statement, reflection_summary, method_description, index_path, chunk_summary, etc.)
    # Example for Reference type:
    # citation_data: { author: "...", title: "...", year: ..., etc. }
    # Example for Index type:
    # source_path: "source_materials/raw/..."
    # chunk_file_path: "source_materials/processed/..."
    # chunk_summary: "..."
    # chunk_concepts: [...]
    # chunk_arguments: [...]
    ---

    # Main Content (Markdown)
    [Detailed description, analysis, text, etc.]
    ```
*   **Self-Modification:** Modes propose changes -> `Orchestrator` -> User Approval -> `Orchestrator` -> `kb-manager` executes & logs change.

## 7. Workflow Designs (V14)

### 7.1. Philosophical Inquiry Workflow (Context-Aware)

1.  **Input:** User prompt OR Analysis modes identify potential questions/concepts.
2.  **Storage (Proto):** Analysis modes send proto-questions/concepts (with source context if applicable) to `kb-manager`.
3.  **Refinement:** `philosophy-questioning` retrieves proto-questions/related concepts from `kb-manager`, **optionally filtering by context**. Refines questions.
4.  **Storage (Refined):** `philosophy-questioning` sends refined questions (tagged `inquiry`) to `kb-manager`.
5.  **Thesis Development:** `philosophy-essay-prep` retrieves relevant refined questions/support material from `kb-manager`, **optionally filtering by context**. Develops thesis.
6.  **Storage (Thesis):** `philosophy-essay-prep` sends thesis to `kb-manager`.
7.  **Essay Cycle:** Essay modes query `kb-manager` for thesis/evidence, **optionally filtering by context**.

### 7.2. System Self-Reflection Workflow (Context-Aware)

1.  **Trigger:** User, Anomaly Detection, Schedule.
2.  **Activation:** `Orchestrator` delegates to `philosophy-meta-reflector`.
3.  **Analysis:** `meta-reflector` queries `philosophy-evidence-manager` (Operational Memory), reads docs/rules, queries `philosophy-kb-manager` (existing reflections/methods, **optionally filtering by context**).
4.  **Reflection:** `meta-reflector` generates meta-reflections/questions.
5.  **Storage (Reflection):** `meta-reflector` sends findings to `kb-manager` (tagged `meta`).
6.  **Proposal Generation (Optional):** `meta-reflector` formulates proposals (KB Change, Arch Change, Method Change).
7.  **Proposal Routing/Approval:** Proposals -> `Orchestrator` -> User -> `Orchestrator` -> `kb-manager`/`architect`/`devops`.
8.  **Reporting:** `meta-reflector` reports to `Orchestrator`/User.

## 8. Version Control (V14)

*   **Primary Scope:** `essay_prep/` managed by `philosophy-essay-prep` using Git via `execute_command`.
*   **Potential Expansion (Considerations):**
    *   KB Versioning (`philosophy-knowledge-base/`).
    *   System Evolution Branching (triggered by `meta-reflector` proposals).
*   **Implementation:** Via `execute_command`.

## 9. Configuration Structure (V14)

*   **Mode Definition File (`.roo/.roomodes`):** Defines all V13+ modes and their `.clinerules` paths.
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
      "philosophy-evidence-manager": ".roo/rules-philosophy-evidence-manager/philosophy-evidence-manager.clinerules", // Manages Operational MB
      "philosophy-kb-manager": ".roo/rules-philosophy-kb-manager/philosophy-kb-manager.clinerules", // Manages Phil KB
      "philosophy-draft-generator": ".roo/rules-philosophy-draft-generator/philosophy-draft-generator.clinerules",
      "philosophy-citation-manager": ".roo/rules-philosophy-citation-manager/philosophy-citation-manager.clinerules",
      "philosophy-verification-agent": ".roo/rules-philosophy-verification-agent/philosophy-verification-agent.clinerules",
      "philosophy-meta-reflector": ".roo/rules-philosophy-meta-reflector/philosophy-meta-reflector.clinerules"
      // Add other non-philosophy modes if they exist in the same config
    }
    ```
*   **Rules File Directory Structure:** `.roo/rules-[mode-slug]/[mode-slug].clinerules`. `.clinerules` for relevant modes must be updated per V14 specs.