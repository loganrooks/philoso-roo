# Architect Specific Memory
### [2025-05-02 21:16:32] Task: Enhance V18.2 Architecture (V18.3 - Feedback Integration)
- **Action**: Based on user critique [Feedback: 2025-05-02 21:09], updated `docs/architecture/architecture_v18.md` to V18.3. Integrated feedback regarding Knowledge Evolution (Sec 6.1), Failure Handling (Sec 7.1, 7.2, 7.3 notes), Cross-Mode Communication (Sec 4.2 notes), User Interaction (Sec 7.4), and Evaluation Framework (Sec 4.4, 7.3 enhancements).
- **Output**: Modified `docs/architecture/architecture_v18.md` with V18.3 design. Updated Memory Bank (`activeContext.md`, `globalContext.md`, `architect.md`).
- **Status**: V18.3 design complete and documented. Ready for final review. Cross-ref: [Global Decision Log: V18.3 - 2025-05-02 21:16:32], [Active Context: 2025-05-02 21:16:32]
### [2025-05-02 15:56:11] Task: Enhance V18 Architecture (V18.1 - Rigor & Linux Paths)
- **Action**: Based on user task [2025-05-02 15:48], updated `docs/architecture/architecture_v18.md` to V18.1. Incorporated philosophical rigor enhancements (KB schema, mode responsibilities, workflows) derived from analysis mode rules and user requirements. Standardized all file paths to use Linux conventions (`/`). Maintained V18 core principles (Direct KB Access, KB Doctor, KB/MB Separation) and V14 detail level.
- **Output**: Overwrote `docs/architecture/architecture_v18.md` with V18.1 design. Updated Memory Bank (`activeContext.md`, `globalContext.md`, `architect.md`).
- **Status**: V18.1 design complete and documented. Ready for review/implementation planning. Cross-ref: [Global Context System Patterns: V18.1 - 2025-05-02 15:54:35], [Global Decision Log: V18.1 - 2025-05-02 15:54:35], [Active Context: 2025-05-02 15:56:11]

### Component Specification: philosophy-kb-doctor (V18.1 Enhanced) - [2025-05-02 15:56:11]
- **Responsibility**: Orchestrates KB maintenance tasks (indexing, validation, cleanup, linking). Triggered by `philosophy-orchestrator`. Executes scripts located in `philosophy-knowledge-base/_operational/maintenance_scripts/`. **V18.1:** Scripts may include validation checks for rigor elements (e.g., presence of determinacy fields, links to counter-arguments, source validity checks). Reads KB operational logs/status from `philosophy-knowledge-base/_operational/`. Reports KB status and rigor validation summaries to `philosophy-orchestrator`. **Does NOT perform maintenance directly; orchestrates KB-internal processes. Does NOT gate read/write access for other modes.**
- **Dependencies**: `philosophy-orchestrator` (trigger), scripts within `philosophy-knowledge-base/_operational/maintenance_scripts/`, data within `philosophy-knowledge-base/_operational/`, `philosophy-evidence-manager` (for SPARC context).
- **Interfaces Exposed**: Accepts maintenance triggers. Executes KB-internal scripts via `execute_command`. Reads KB operational logs/status from `philosophy-knowledge-base/_operational/`. Reports status and rigor validation summaries to orchestrator.
- **Logs**: Its *SPARC mode execution logs* go to `memory-bank/mode-specific/philosophy-kb-doctor.md`. The logs *of the maintenance tasks it triggers* go to `philosophy-knowledge-base/_operational/logs/`.

### Component Specification: Analysis Modes (V18.1 Rigor Enhanced) - [2025-05-02 15:56:11]
- **Responsibility**: Analyze sources/KB content, generate concepts, arguments, questions, etc., **ensuring philosophical rigor**.
- **Interaction (V18.1):** Directly Read KB files (`philosophy-knowledge-base/`), query related context (linked entries, secondary sources). Explicitly analyze for rigor elements (determinacy, presuppositions, ambiguities, etc.). Directly Write findings to KB, **populating rigor-related fields** and ensuring links (`source_ref_keys`, `extraction_markers`, `related_ids`). Query `philosophy-evidence-manager` for SPARC context.
- **Focus:** `class-analysis` (determinacy, evidence standards), `dialectical-analysis` (contradictions, presuppositions), `secondary-lit` (comparing interpretations), `questioning` (refining based on rigor gaps).

### Component Specification: philosophy-verification-agent (V18.1 Rigor Enhanced) - [2025-05-02 15:56:11]
- **Responsibility**: Verifies claims, citations, and **rigor elements** within drafts against KB entries and processed source chunks. Checks consistency, source representation, presence of rigor fields, handling of counter-arguments.
- **Interaction (V18.1):** Directly Reads draft, KB entries (incl. rigor fields), source chunks. Generates verification reports highlighting rigor gaps. Triggers self-correction loop via `Orchestrator`. Queries `philosophy-evidence-manager` for SPARC context.

### Data Model: Philosophy KB Entry (V18.1 Rigor Enhanced) - [2025-05-02 15:56:11]
- **Purpose**: Standard structure for entries within `philosophy-knowledge-base/`, enhanced for rigor.
- **Structure**:
  ```yaml
  ---
  id: [UUID]
  type: [Concept | Argument | Quotation | Reference | Question | Thesis | Relationship | Method | Meta-Reflection | Index | ProcessedTextChunk]
  timestamp: [YYYY-MM-DD HH:MM:SS]
  generating_mode: [mode-slug]
  # --- Rigor & Context Fields (V18.1 Additions/Emphasis) ---
  positive_determination: "..."
  negative_determination: "..."
  ordinary_language_contrast: "..."
  related_terms: [[term_id_1, ...]]
  presuppositions: ["...", "..."]
  ambiguities: ["...", "..."]
  counter_arguments: [[arg_id_1, ...]]
  secondary_source_links: [[ref_id_1, ...]]
  other_philosopher_views: [[ref_id_3, concept_id_x]]
  verification_status: [Unverified | Verified | Disputed]
  verification_notes: "..."
  # --- V14 Context Tags (Retained) ---
  tags: ["context:type:...", "context:id:...", "context:subtype:...", "hegel", ...]
  # --- Linking & Source Fields (V11+, Emphasized V18.1) ---
  source_ref_keys: [[ref_key_1, ...]] # CRITICAL
  extraction_markers: [[marker_1, ...]] # CRITICAL
  related_ids: [[id_1, ...]]
  # --- Type-Specific Fields ---
  # ...
  ---
  # Main Content (Markdown)
  [Detailed description reflecting rigor elements.]
  ```
- **Relationships**: Managed via `related_ids` and `Relationship` entries.
- **Notes**: Key change is addition/emphasis of rigor fields. See `docs/architecture/architecture_v18.md` (V18.1).

### Diagram: Hegel Philosophy Suite V18.1 (Rigor Enhanced) - [2025-05-02 15:56:11]
- **Description:** Overall mode interaction for V18.1. Modes access KB directly, populate/check rigor fields. `KBDoctor` handles maintenance & rigor validation via internal scripts. `Verify` checks rigor. Strict KB/MB separation. Linux paths (`/`).
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
        subgraph SPARC Memory [SPARC Operational Context]
            style SPARCMem fill:#e0e0e0,stroke:#666,stroke-width:1px
            EvidMan(philosophy-evidence-manager)
            SPARCMB[(SPARC Memory Bank<br>memory-bank/)]
            EvidMan -- Manages --> SPARCMB
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
    MetaReflector -- Query MB --> EvidMan
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

    %% Evidence Manager Interactions (SPARC Context ONLY)
    EvidMan -- Access/Update --> SPARCMB
    Orchestrator -- Use SPARC Context --> EvidMan
    TextProc -- Use SPARC Context --> EvidMan
    PreLec -- Use SPARC Context --> EvidMan
    ClassAn -- Use SPARC Context --> EvidMan
    SecLit -- Use SPARC Context --> EvidMan
    DialAn -- Use SPARC Context --> EvidMan
    Quest -- Use SPARC Context --> EvidMan
    EssayPrep -- Use SPARC Context --> EvidMan
    DraftGen -- Use SPARC Context --> EvidMan
    CiteMan -- Use SPARC Context --> EvidMan
    Verify -- Use SPARC Context --> EvidMan
    MetaReflector -- Use SPARC Context --> EvidMan
    KBDoctor -- Use SPARC Context --> EvidMan


    %% Styling
    classDef kb fill:#f9f,stroke:#333,stroke-width:2px;
    class PhilKB_Data, PhilKB_Ops kb;
    classDef mode fill:#ccf,stroke:#333,stroke-width:1px;
    class Orchestrator,TextProc,PreLec,ClassAn,SecLit,DialAn,Quest,EssayPrep,DraftGen,CiteMan,Verify,EvidMan,MetaReflector,KBDoctor mode;
    classDef script fill:#f0ad4e,stroke:#333,stroke-width:1px;
    class Scripts, KB_Scripts script;
    classDef vcs fill:#d9edf7,stroke:#31708f,stroke-width:1px;
    class VCS vcs;
    classDef sparcmb fill:#e0e0e0,stroke:#666,stroke-width:1px;
    class SPARCMB sparcmb;
    classDef source fill:#dff0d8,stroke:#3c763d,stroke-width:1px;
    class RawSource,ProcessedSource source;
    classDef kbops fill:#add8e6,stroke:#00008b,stroke-width:1px,stroke-dasharray: 2 2;
    class KB_Indices,KB_Logs,KB_Status,KB_Reports,KB_Scripts kbops;
```
**Notes:** Reflects V18.1 architecture documented in `docs/architecture/architecture_v18.md`.
### [2025-05-02 15:25:15] Task: Design V18 Architecture (Direct KB Access + KB Doctor)
- **Action**: Based on user task [2025-05-02 15:22] and V14 reference (`docs/architecture/architecture_v14.md`), designed V18 architecture. Key changes: Removed `philosophy-kb-manager`, implemented direct KB read/write access for modes following defined patterns, introduced `philosophy-kb-doctor` for maintenance (non-gatekeeping), ensured strict KB/MB separation, retained V14 source context handling.
- **Output**: Created `docs/architecture/architecture_v18.md` with detailed V18 design. Updated Memory Bank (`activeContext.md`, `globalContext.md`, `architect.md`).
- **Status**: V18 design complete and documented. Ready for review/implementation planning. Cross-ref: [Global Context System Patterns: V18 - 2025-05-02 15:25:15], [Global Decision Log: 2025-05-02 15:25:15], [Active Context: 2025-05-02 15:25:15]

### Component Specification: philosophy-kb-doctor (V18 New) - [2025-05-02 15:25:15]
- **Responsibility**: Orchestrates KB maintenance tasks (indexing, validation, cleanup, linking). Triggered by `philosophy-orchestrator`. Executes scripts located in `philosophy-knowledge-base/_operational/maintenance_scripts/`. Reads KB operational logs/status from `philosophy-knowledge-base/_operational/`. Reports KB status to `philosophy-orchestrator`. **Does NOT perform maintenance directly; orchestrates KB-internal processes. Does NOT gate read/write access for other modes.**
- **Dependencies**: `philosophy-orchestrator` (trigger), scripts within `philosophy-knowledge-base/_operational/maintenance_scripts/`, data within `philosophy-knowledge-base/_operational/`, `philosophy-evidence-manager` (for SPARC context).
- **Interfaces Exposed**: Accepts maintenance triggers. Executes KB-internal scripts via `execute_command`. Reads KB operational logs/status from `philosophy-knowledge-base/_operational/`. Reports status to orchestrator.
- **Logs**: Its *SPARC mode execution logs* go to `memory-bank/mode-specific/philosophy-kb-doctor.md`. The logs *of the maintenance tasks it triggers* go to `philosophy-knowledge-base/_operational/logs/`.

### Component Specification: philosophy-text-processor (V18 Revised) - [2025-05-02 15:25:15]
- **Responsibility**: Pre-processes source texts from `source_materials/raw/` via external scripts (chunking, indexing, citation extraction). Parses input path to extract context (`type`, `id`, `subtype`). **V18:** Directly writes outputs (index/chunk info, citation data, context tags) to designated files/sections within `philosophy-knowledge-base/`.
- **Dependencies**: External scripts, `philosophy-orchestrator`, File system tools (`write_to_file`, `insert_content`), `philosophy-evidence-manager` (for SPARC context).
- **Interfaces Exposed**: Accepts task delegation. Outputs processed chunks to `source_materials/processed/`. Writes data directly to KB.

### Component Specification: Analysis Modes (V18 Revised) - [2025-05-02 15:25:15]
- **Responsibility**: Analyze sources/KB content, generate concepts, arguments, questions, etc.
- **Interaction (V18):** Directly Read KB files (`philosophy-knowledge-base/`) using file tools (`read_file`, `search_files`), applying context filters. Directly Write findings to designated KB files/sections using file tools (`write_to_file`, `insert_content`). Query `philosophy-evidence-manager` for SPARC context.

### Component Specification: Essay Modes (V18 Revised) - [2025-05-02 15:25:15]
- **Responsibility**: Manage essay writing, drafting, citation, verification.
- **Interaction (V18):** Directly Read relevant KB entries from `philosophy-knowledge-base/` using file tools, applying context filters. Directly Write thesis (`essay-prep`) to KB. Query `philosophy-evidence-manager` for SPARC context. `essay-prep` manages Git.

### Diagram: Hegel Philosophy Suite V18 (Direct KB Access + KB Doctor) - [2025-05-02 15:25:15]
- **Description:** Overall mode interaction for V18. Modes access KB directly. `KBDoctor` handles maintenance via internal scripts. Strict KB/MB separation.
```mermaid
graph TD
    subgraph User Interaction
        User(User)
    end

    subgraph Orchestration
        Orchestrator(philosophy-orchestrator)
    end

    subgraph KB Maintenance
        KBDoctor(philosophy-kb-doctor)
    end

    subgraph Text Processing
        TextProc(philosophy-text-processor) -- Runs --> Scripts((External Scripts))
    end

    subgraph Analysis & Inquiry
        PreLec(philosophy-pre-lecture)
        ClassAn(philosophy-class-analysis)
        SecLit(philosophy-secondary-lit)
        DialAn(philosophy-dialectical-analysis)
        Quest(philosophy-questioning)
    end

    subgraph Meta-Reflection
        MetaReflector(philosophy-meta-reflector)
    end

    subgraph Essay Generation & Verification
        EssayPrep(philosophy-essay-prep) -- Git Ops --> VCS[(Version Control System<br>(Git))]
        DraftGen(philosophy-draft-generator)
        CiteMan(philosophy-citation-manager)
        Verify(philosophy-verification-agent)
    end

    subgraph Data Layer
        subgraph SPARC Memory [SPARC Operational Context]
            style SPARCMem fill:#e0e0e0,stroke:#666,stroke-width:1px
            EvidMan(philosophy-evidence-manager)
            SPARCMB[(SPARC Memory Bank<br>memory-bank/)]
            EvidMan -- Manages --> SPARCMB
        end
        subgraph Philosophical Knowledge Base [Domain Knowledge & Domain Operations]
            style PhilKB fill:#f9f,stroke:#333,stroke-width:2px
            PhilKB_Data[(Philosophy KB Data<br>philosophy-knowledge-base/<br>concepts/, arguments/, etc.)]
            PhilKB_Ops[(KB Operational<br>philosophy-knowledge-base/_operational/)]

            subgraph KB_Ops_Details ["_operational/"]
                 style KBOps fill:#add8e6,stroke:#00008b,stroke-width:1px,stroke-dasharray: 2 2
                 KB_Indices("indices/")
                 KB_Logs("logs/")
                 KB_Status("status/")
                 KB_Reports("reports/")
                 KB_Scripts("maintenance_scripts/")
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
    Orchestrator -- Trigger KB Maintenance --> KBDoctor
    Orchestrator -- Route KB/System Mod Proposal --> User
    Orchestrator -- Relay Approval --> Architect
    Orchestrator -- Relay Approval --> DevOps
    Orchestrator -- Results --> User

    %% Text Processing Flow (V18 Direct Write)
    TextProc -- Reads --> RawSource
    TextProc -- Processed Chunks --> ProcessedSource
    TextProc -- Direct Write KB --> PhilKB_Data

    %% Analysis & Inquiry Flow (V18 Direct R/W)
    PreLec -- Direct Write KB --> PhilKB_Data
    ClassAn -- Direct Write KB --> PhilKB_Data
    SecLit -- Direct Write KB --> PhilKB_Data
    DialAn -- Direct Write KB --> PhilKB_Data
    Quest -- Direct Write KB --> PhilKB_Data

    PreLec -- Direct Read KB --> PhilKB_Data
    ClassAn -- Direct Read KB --> PhilKB_Data
    SecLit -- Direct Read KB --> PhilKB_Data
    DialAn -- Direct Read KB --> PhilKB_Data
    Quest -- Direct Read KB --> PhilKB_Data

    %% Essay Flow (V18 Direct R/W)
    EssayPrep -- Direct Read KB --> PhilKB_Data
    EssayPrep -- Direct Write KB --> PhilKB_Data
    EssayPrep -- Request Draft --> DraftGen
    EssayPrep -- Request Citation --> CiteMan
    EssayPrep -- Request Verification --> Verify
    EssayPrep -- Manage Files --> Workspace

    DraftGen -- Direct Read KB --> PhilKB_Data
    DraftGen -- Draft --> EssayPrep
    DraftGen -- Trigger Commit --> Orchestrator

    CiteMan -- Direct Read KB --> PhilKB_Data
    CiteMan -- Cited Draft/Biblio --> EssayPrep
    CiteMan -- Trigger Commit --> Orchestrator

    Verify -- Direct Read KB --> PhilKB_Data
    Verify -- Verification Report --> EssayPrep

    %% Meta-Reflection Flow (V18 Direct R/W)
    MetaReflector -- Direct Read KB --> PhilKB_Data
    MetaReflector -- Query MB --> EvidMan
    MetaReflector -- Read Docs/Rules --> Workspace/.roo/docs
    MetaReflector -- Direct Write KB --> PhilKB_Data
    MetaReflector -- Propose KB Mod --> Orchestrator
    MetaReflector -- Propose Arch Mod --> Orchestrator
    MetaReflector -- Propose Method/Git Mod --> Orchestrator

    %% KB Doctor Interactions (Maintenance Only)
    KBDoctor -- Triggers --> KB_Scripts
    KB_Scripts -- Read/Write --> PhilKB_Data
    KB_Scripts -- Read/Write --> KB_Indices
    KB_Scripts -- Write Logs --> KB_Logs
    KB_Scripts -- Write Status --> KB_Status
    KBDoctor -- Reads Status/Logs --> PhilKB_Ops
    KBDoctor -- Writes Reports --> KB_Reports

    %% Evidence Manager Interactions (SPARC Context ONLY)
    EvidMan -- Access/Update --> SPARCMB
    Orchestrator -- Use SPARC Context --> EvidMan
    TextProc -- Use SPARC Context --> EvidMan
    PreLec -- Use SPARC Context --> EvidMan
    ClassAn -- Use SPARC Context --> EvidMan
    SecLit -- Use SPARC Context --> EvidMan
    DialAn -- Use SPARC Context --> EvidMan
    Quest -- Use SPARC Context --> EvidMan
    EssayPrep -- Use SPARC Context --> EvidMan
    DraftGen -- Use SPARC Context --> EvidMan
    CiteMan -- Use SPARC Context --> EvidMan
    Verify -- Use SPARC Context --> EvidMan
    MetaReflector -- Use SPARC Context --> EvidMan
    KBDoctor -- Use SPARC Context --> EvidMan


    %% Styling
    classDef kb fill:#f9f,stroke:#333,stroke-width:2px;
    class PhilKB_Data, PhilKB_Ops kb;
    classDef mode fill:#ccf,stroke:#333,stroke-width:1px;
    class Orchestrator,TextProc,PreLec,ClassAn,SecLit,DialAn,Quest,EssayPrep,DraftGen,CiteMan,Verify,EvidMan,MetaReflector,KBDoctor mode;
    classDef script fill:#f0ad4e,stroke:#333,stroke-width:1px;
    class Scripts, KB_Scripts script;
    classDef vcs fill:#d9edf7,stroke:#31708f,stroke-width:1px;
    class VCS vcs;
    classDef sparcmb fill:#e0e0e0,stroke:#666,stroke-width:1px;
    class SPARCMB sparcmb;
    classDef source fill:#dff0d8,stroke:#3c763d,stroke-width:1px;
    class RawSource,ProcessedSource source;
    classDef kbops fill:#add8e6,stroke:#00008b,stroke-width:1px,stroke-dasharray: 2 2;
    class KB_Indices,KB_Logs,KB_Status,KB_Reports,KB_Scripts kbops;
```
**Notes:** Reflects V18 architecture documented in `docs/architecture/architecture_v18.md`.
### [2025-05-02 13:44:56] Task: Design V17 Architecture (KB Manager Revision)
- **Action**: Following user intervention [Architect Feedback Log: 2025-05-02 13:43:34] rejecting script-based V16, redesigned architecture to V17. Reintroduced `philosophy-kb-manager` responsible for internal KB logic (organization, validation, `_operational/` data management). Removed `kb-doctor` and `maintenance_scripts`. Maintained strict KB/MB separation.
- **Output**: Overwrote `docs/architecture/architecture_v16.md` with detailed V17 design. Updated Memory Bank (`activeContext.md`, `globalContext.md`, `architect.md`).
- **Status**: V17 design complete and documented. Ready for review/implementation planning. Cross-ref: [Global Context System Patterns: V17 - 2025-05-02 13:44:56], [Global Decision Log: 2025-05-02 13:13:23], [Active Context: 2025-05-02 13:44:56]

### Component Specification: philosophy-kb-manager (V17 Revised) - [2025-05-02 13:44:56]
- **Responsibility**: Sole gateway and manager for `philosophy-knowledge-base/`. Maintains structure, integrity, consistency, and operational metadata (`_operational/`). Handles CRUD, validation (schema, references), indexing, logging, status updates, reporting internally.
- **Dependencies**: All modes requiring KB access (requests), `philosophy-evidence-manager` (for SPARC context if needed), files within `philosophy-knowledge-base/`.
- **Interfaces Exposed**: Accepts structured requests from modes (e.g., "get concept", "store analysis"). Returns data or confirmation.
- **Internal Structure (High-Level)**: Logic for structure awareness, CRUD, validation (using `_operational/formatting_templates_rules/`), indexing (writing to `_operational/indices/`), logging (writing to `_operational/logs/`), status management (writing to `_operational/status/`), reporting (writing to `_operational/reports/`), querying.
- **Logs**: Its *SPARC mode execution logs* go to `memory-bank/mode-specific/philosophy-kb-manager.md`. The logs *of KB operations it performs* go to `philosophy-knowledge-base/_operational/logs/`.

### Diagram: Hegel Philosophy Suite V17 (KB Manager Revision) - [2025-05-02 13:44:56]
- **Description:** Overall mode interaction for V17. `kb-manager` mediates all access to `philosophy-knowledge-base/` (domain and `_operational` data). Strict KB/MB separation maintained.
```mermaid
graph TD
    subgraph SPARC System Context [memory-bank/]
        style SPARCMem fill:#e0e0e0,stroke:#666,stroke-width:1px
        MB_Active("activeContext.md")
        MB_Global("globalContext.md")
        MB_ModeSpecific("mode-specific/")
        MB_Feedback("feedback/")
    end

    subgraph Philosophy Domain & Operations [philosophy-knowledge-base/]
        style PhilKB fill:#f9f,stroke:#333,stroke-width:2px
        PKB_Domain["Domain Knowledge<br>(e.g., concepts/, arguments/)"]
        PKB_Operational["_operational/ (KB-Internal Management Data)"]

        subgraph PKB_Operational_Details ["_operational/"]
             style KBOps fill:#add8e6,stroke:#00008b,stroke-width:1px,stroke-dasharray: 2 2
             PKB_Indices("indices/")
             PKB_Logs("logs/")
             PKB_Status("status/")
             PKB_Reports("reports/")
             PKB_Templates("formatting_templates_rules/")
        end
        PKB_Operational --> PKB_Operational_Details
    end

    Modes["SPARC Modes"] -- "R/W SPARC Ops Context<br>(via EvidMan)" --> SPARC System Context
    Modes -- "Request/Submit Data" --> KB_Manager["philosophy-kb-manager"]

    KB_Manager -- "Reads/Writes ALL Data" --> Philosophy Domain & Operations
    KB_Manager -- "Manages/Generates" --> PKB_Operational_Details
    KB_Manager -- "Writes SPARC Mode Log" --> MB_ModeSpecific

    classDef mode fill:#ccf,stroke:#333,stroke-width:1px;
    class Modes, KB_Manager mode;
```
**Notes:** Reflects V17 architecture documented in `docs/architecture/architecture_v16.md`.
### [2025-05-02 13:19:52] Task: Design V16 Architecture (Strict Separation)
- **Action**: Analyzed V15 architecture, user constraint [Global Decision Log: 2025-05-02 13:13:23], and Memory Bank context. Designed V16 architecture enforcing strict separation between `memory-bank/` and `philosophy-knowledge-base/`.
- **Key Decisions**:
    - Redefined `philosophy-kb-doctor` to orchestrate KB-internal maintenance scripts/processes.
    - Mandated that all philosophy-specific operational data (indices, logs, status) reside within `philosophy-knowledge-base/operational/`.
    - Confirmed SPARC operational context (including `kb-doctor`'s own execution logs) remains in `memory-bank/`.
- **Output**: Created `docs/architecture/architecture_v16.md`. Updated Memory Bank (`activeContext.md`, `globalContext.md`, `architect.md`).
- **Status**: V16 design complete. Ready for review/implementation planning. Cross-ref: [Global Context System Patterns: 2025-05-02 13:19:52], [Global Context Decision Log: 2025-05-02 13:13:23], [Active Context: 2025-05-02 13:19:52]

### Component Specification: philosophy-kb-doctor (V16 Revised) - [2025-05-02 13:19:52]
- **Responsibility**: Orchestrates KB maintenance tasks. Triggers scripts/processes located in `philosophy-knowledge-base/operational/maintenance_scripts/` to perform indexing, validation, linking, etc. *within* the KB structure. Monitors KB health based on data within `philosophy-knowledge-base/operational/`. Reports KB status to `philosophy-orchestrator`. **Does NOT perform maintenance directly; orchestrates KB-internal processes.**
- **Dependencies**: `philosophy-orchestrator` (trigger), scripts within `philosophy-knowledge-base/operational/maintenance_scripts/`, data within `philosophy-knowledge-base/`, `philosophy-evidence-manager` (for SPARC context).
- **Interfaces Exposed**: Accepts maintenance triggers. Executes KB-internal scripts via `execute_command`. Reads KB operational logs/status from `philosophy-knowledge-base/operational/`. Reports status to orchestrator.
- **Logs**: Its *SPARC mode execution logs* go to `memory-bank/mode-specific/philosophy-kb-doctor.md`. The logs *of the maintenance tasks it triggers* go to `philosophy-knowledge-base/operational/logs/`.

### Diagram: Hegel Philosophy Suite V16 (Strict Separation) - [2025-05-02 13:19:52]
- **Description:** Overall mode interaction and data flow for V16. Enforces strict separation: `memory-bank/` for SPARC ops, `philosophy-knowledge-base/` for domain data AND domain ops (logs, indices, status within `operational/`). `kb-doctor` orchestrates KB-internal scripts.
```mermaid
graph TD
    subgraph User Interaction
        User(User)
    end

    subgraph Orchestration
        Orchestrator(philosophy-orchestrator)
    end

    subgraph KB Maintenance
        KBDoctor(philosophy-kb-doctor)
    end

    subgraph Text Processing
        TextProc(philosophy-text-processor) -- Runs --> KB_Scripts((KB Internal Scripts<br>e.g., process_source_text.py))
    end

    subgraph Analysis & Inquiry
        PreLec(philosophy-pre-lecture)
        ClassAn(philosophy-class-analysis)
        SecLit(philosophy-secondary-lit)
        DialAn(philosophy-dialectical-analysis)
        Quest(philosophy-questioning)
        MetaReflector(philosophy-meta-reflector)
    end

    subgraph Essay Generation & Verification
        EssayPrep(philosophy-essay-prep) -- Git Ops --> VCS[(Version Control System<br>(Git))]
        DraftGen(philosophy-draft-generator)
        CiteMan(philosophy-citation-manager)
        Verify(philosophy-verification-agent)
    end

    subgraph Data Layer
        subgraph SPARC Memory [SPARC Operational Context]
            style SPARCMem fill:#e0e0e0,stroke:#666,stroke-width:1px
            EvidMan(philosophy-evidence-manager)
            SPARCMB[(SPARC Memory Bank<br>memory-bank/)]
            EvidMan -- Manages --> SPARCMB
        end
        subgraph Philosophical Knowledge Base [Domain Knowledge & Domain Operations]
            style PhilKB fill:#f9f,stroke:#333,stroke-width:2px
            PhilKB[(Philosophy KB<br>philosophy-knowledge-base/)]
            subgraph KB Content
                style KBContent fill:#fffacd,stroke:#8a6d3b,stroke-width:1px,stroke-dasharray: 5 5
                Concepts(concepts/)
                Arguments(arguments/)
                Quotations(quotations/)
                References(references/)
                Questions(questions/)
                Theses(theses/)
                Relationships(relationships/)
                Methods(methods/)
                MetaReflections(meta-reflections/)
                ProcessedTexts(processed_texts/)
                Analyses(analyses/)
                Citations(citations/)
            end
            subgraph KB Operations [Internal]
                 style KBOps fill:#add8e6,stroke:#00008b,stroke-width:1px,stroke-dasharray: 2 2
                 Indices(indices/)
                 Operational(operational/)
                 OpLogs(operational/logs/)
                 OpStatus(operational/status/)
                 OpScripts(operational/maintenance_scripts/)
            end
            PhilKB --> KBContent
            PhilKB --> KBOps
        end
        Workspace(analysis_workspace / essay_prep / source_materials/processed)
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
    Orchestrator -- Trigger KB Maintenance? --> KBDoctor
    Orchestrator -- Results --> User

    %% Direct KB Interactions (Read/Write Domain Data)
    TextProc -- Write Domain Data --> ProcessedTexts
    TextProc -- Write Domain Data --> Citations
    PreLec -- Read/Write Domain Data --> PhilKB
    ClassAn -- Read/Write Domain Data --> PhilKB
    SecLit -- Read/Write Domain Data --> PhilKB
    DialAn -- Read/Write Domain Data --> PhilKB
    Quest -- Read/Write Domain Data --> PhilKB
    MetaReflector -- Read/Write Domain Data --> PhilKB
    EssayPrep -- Read/Write Domain Data --> PhilKB
    DraftGen -- Read Domain Data --> PhilKB
    CiteMan -- Read Domain Data --> PhilKB
    Verify -- Read Domain Data --> PhilKB

    %% KB Doctor Interactions (Triggers KB-Internal Ops)
    KBDoctor -- Triggers --> OpScripts
    OpScripts -- Read/Write --> Indices
    OpScripts -- Read/Write --> PhilKB
    OpScripts -- Write Logs --> OpLogs
    OpScripts -- Write Status --> OpStatus
    KBDoctor -- Reads Status/Logs --> KBOps

    %% Other Interactions
    TextProc -- Processed Chunks --> Workspace
    EssayPrep -- Manage Files --> Workspace
    MetaReflector -- Query MB --> EvidMan
    MetaReflector -- Read Docs/Rules --> Workspace/.roo/docs

    %% SPARC Memory Interactions (Operational Context)
    Orchestrator -- Use SPARC Context --> EvidMan
    TextProc -- Use SPARC Context --> EvidMan
    PreLec -- Use SPARC Context --> EvidMan
    ClassAn -- Use SPARC Context --> EvidMan
    SecLit -- Use SPARC Context --> EvidMan
    DialAn -- Use SPARC Context --> EvidMan
    Quest -- Use SPARC Context --> EvidMan
    EssayPrep -- Use SPARC Context --> EvidMan
    DraftGen -- Use SPARC Context --> EvidMan
    CiteMan -- Use SPARC Context --> EvidMan
    Verify -- Use SPARC Context --> EvidMan
    MetaReflector -- Use SPARC Context --> EvidMan
    KBDoctor -- Use SPARC Context --> EvidMan

    %% Styling
    classDef mode fill:#ccf,stroke:#333,stroke-width:1px;
    class Orchestrator,TextProc,PreLec,ClassAn,SecLit,DialAn,Quest,EssayPrep,DraftGen,CiteMan,Verify,EvidMan,MetaReflector,KBDoctor mode;
    classDef script fill:#f0ad4e,stroke:#333,stroke-width:1px;
    class KB_Scripts, OpScripts script;
    classDef vcs fill:#d9edf7,stroke:#31708f,stroke-width:1px;
    class VCS vcs;
    classDef sparcmb fill:#e0e0e0,stroke:#666,stroke-width:1px;
    class SPARCMB sparcmb;
    classDef kbcontent fill:#fffacd,stroke:#8a6d3b,stroke-width:1px,stroke-dasharray: 5 5;
    class Concepts,Arguments,Quotations,References,Questions,Theses,Relationships,Methods,MetaReflections,ProcessedTexts,Analyses,Citations kbcontent;
    classDef kbops fill:#add8e6,stroke:#00008b,stroke-width:1px,stroke-dasharray: 2 2;
    class Indices,Operational,OpLogs,OpStatus,OpScripts kbops;
```
**Notes:** Reflects V16 architecture documented in `docs/architecture/architecture_v16.md`.
### [2025-05-02 02:44:49] Task: Design V13 Architecture (Corrected Scope)
- **Action**: Analyzed V12 architecture (`docs/architecture/architecture_v12.md`), V13 requirements (KB, Philosophical Inquiry Workflow, System Self-Reflection Workflow), `architecture-questioning.md`, and Memory Bank context. Designed V13 architecture addressing the full scope.
- **Key Decisions**:
    - Introduced **Philosophy Knowledge Base (KB)** (`philosophy-knowledge-base/`) for domain knowledge.
    - Created new **`philosophy-kb-manager`** mode as sole KB interface.
    - Revised **`philosophy-evidence-manager`** scope to SPARC Memory Bank only.
    - Integrated distinct **Philosophical Inquiry Workflow**.
    - Integrated distinct **System Self-Reflection Workflow** using new **`philosophy-meta-reflector`** mode.
    - Defined KB/System **modification proposal/approval workflow** via `philosophy-orchestrator`.
- **Output**: Created `docs/architecture/architecture_v13.md` and `docs/plans/philosophy_mode_improvement_plan_v3.md`. Updated Memory Bank (`activeContext.md`, `globalContext.md`, `architect.md`).
- **Status**: V13 design complete. Ready for V3 implementation. Cross-ref: [Global Context System Patterns: 2025-05-02 02:44:49], [Global Context Decision Log: 2025-05-02 02:44:49], [Global Context Progress: 2025-05-02 02:44:49]
### [2025-05-02 00:45:10] Task: Design V13 Architecture
### Component Specification: philosophy-kb-manager (V13 New) - [2025-05-02 02:44:49]
- **Responsibility**: Sole interface for CRUD operations and querying on the `philosophy-knowledge-base/`. Manages internal linking and structure within the KB. Executes approved modifications. Ensures data integrity within the KB.
- **Dependencies**: `philosophy-orchestrator` (for modification approvals), All modes requiring philosophical knowledge (for data requests/submissions), `philosophy-evidence-manager` (for SPARC context if needed).
- **Interfaces Exposed**: Provides structured data (concepts, arguments, references, questions, theses, etc.) from `philosophy-knowledge-base/` upon request. Accepts structured data for storage. Accepts approved modification instructions.
- **Internal Structure (High-Level)**: Logic for parsing queries, managing file I/O for `philosophy-knowledge-base/` (Markdown initially), handling unique IDs, parsing/creating links, executing changes based on approved proposals.

### Component Specification: philosophy-meta-reflector (V13 New) - [2025-05-02 02:44:49]
- **Responsibility**: Performs meta-level analysis of the system (architecture, methods, biases, limitations) based on `architecture-questioning.md` principles. Analyzes MB logs, docs, rules, KB content. Stores reflections/questions in KB. Proposes KB/System modifications via orchestrator.
- **Dependencies**: `philosophy-orchestrator` (trigger, proposal routing), `philosophy-kb-manager` (store/query reflections/methods), `philosophy-evidence-manager` (query MB), potentially `architect`, `devops`.
- **Interfaces Exposed**: Accepts triggers. Outputs meta-reflections/questions to `kb-manager`. Outputs modification proposals to `orchestrator`.
- **Internal Structure (High-Level)**: Logic for reading/analyzing various system artifacts, applying reflective frameworks, generating structured reflections and proposals.

### Component Specification: philosophy-evidence-manager (V13 Revised) - [2025-05-02 02:44:49]
- **Responsibility**: Manages access **only** to the **SPARC Memory Bank** (`memory-bank/`) and potentially intermediate analysis files (`analysis_workspace/`). Handles SPARC context queries (active context, global context, feedback, mode-specific logs), progress logs, decision logs, etc. **Does NOT interact with `philosophy-knowledge-base/`.**
- **Dependencies**: All modes (for SPARC context), `memory-bank/` files.
- **Interfaces Exposed**: Provides SPARC context data upon request. Accepts SPARC context data for storage.
- **Internal Structure (High-Level)**: Logic for reading/writing/querying files within `memory-bank/`.
- **Action**: Analyzed V12 architecture (`docs/architecture/architecture_v12.md`), user requirements [Task: 2025-05-02 00:40:46], exploratory notes (`architecture-questioning.md`), and Memory Bank context. Designed V13 architecture.
- **Key Decisions**:
    - Introduced **Philosopher's Index** (`philosophers-index/`) as a dedicated KB for philosophical content (concepts, arguments, etc.), initially using structured Markdown files.
    - Created new **`philosophy-kb-manager`** mode as the sole interface to the Philosopher's Index.
    - Reduced scope of **`philosophy-evidence-manager`** to manage only the SPARC Memory Bank (`memory-bank/`).
    - Integrated a **Questioning/Thesis Workflow** involving analysis modes, `philosophy-questioning`, `philosophy-essay-prep`, and `philosophy-kb-manager`.
    - Defined a proposal/approval workflow for **self-modification** of the Philosopher's Index, managed by `philosophy-orchestrator`.
- **Output**: Created `docs/architecture/architecture_v13.md` with detailed design and updated diagrams. Updated Memory Bank (`activeContext.md`, `globalContext.md`, `architect.md`).
- **Status**: V13 design complete. Ready to propose V3 implementation plan. Cross-ref: [Global Context System Patterns: 2025-05-02 00:44:45], [Global Context Decision Log: 2025-05-02 00:44:45], [Global Context Progress: 2025-05-02 00:44:45]

## Component Specifications
### Component Specification: philosophy-kb-manager (V14 Enhanced) - [2025-05-02 05:20:19]
- **Responsibility**: Sole interface to `philosophy-knowledge-base/`. Handles CRUD, querying, linking, and integrity for structured philosophical data. **V14:** Accepts context tags list from `text-processor`, stores them in entry YAML `tags` list using `context:key:value` format, and supports querying/filtering based on these tags. Executes approved KB modifications.
- **Dependencies**: `philosophy-orchestrator` (for modification approvals), All modes requiring KB access, `philosophy-evidence-manager` (for SPARC context if needed).
- **Interfaces Exposed**: Provides structured data from `philosophy-knowledge-base/` upon request (supports context filters). Accepts structured data for storage (including context tags list). Accepts approved modification instructions.
- **Internal Structure (High-Level)**: Logic for parsing queries (including context tag filters), managing file I/O for `philosophy-knowledge-base/`, handling unique IDs, parsing/creating links, storing/merging tags, executing changes.

### Component Specification: philosophy-text-processor (V14 Enhanced) - [2025-05-02 05:20:19]
- **Responsibility**: Pre-processes source texts from `source_materials/raw/` via external scripts (chunking, indexing, citation extraction). **V14:** Parses input path relative to `source_materials/raw/` to extract context (`type`, `id`, `subtype`).
- **Dependencies**: External scripts, `philosophy-orchestrator`, `philosophy-kb-manager`.
- **Interfaces Exposed**: Accepts task delegation. Outputs processed chunks to `source_materials/processed/`. Outputs data package (index, citations, **list of context tags**) to `philosophy-kb-manager`.
- **Internal Structure (High-Level)**: Logic to invoke external scripts, parse file paths for context extraction, format context tags into a list, package outputs for `kb-manager`.
### Component Specification: philosophy-kb-manager (V13 New) - [2025-05-02 00:45:10]
- **Responsibility**: Sole interface for CRUD operations and querying on the `philosophers-index/`. Manages internal linking and structure within the Index. Executes approved modifications. Ensures data integrity within the Index.
- **Dependencies**: `philosophy-orchestrator` (for modification approvals), All modes requiring philosophical knowledge (for data requests/submissions), `philosophy-evidence-manager` (for SPARC context).
- **Interfaces Exposed**: Provides structured data (concepts, arguments, references, questions, theses, etc.) from `philosophers-index/` upon request. Accepts structured data for storage. Accepts approved modification instructions.
- **Internal Structure (High-Level)**: Logic for parsing queries, managing file I/O for `philosophers-index/` (Markdown initially), handling unique IDs, parsing/creating links, executing changes based on approved proposals.

### Component Specification: philosophy-evidence-manager (V13 Revised) - [2025-05-02 00:45:10]
- **Responsibility**: Manages access to the **SPARC Memory Bank** (`memory-bank/`) and potentially intermediate analysis files in `analysis_workspace/`. Handles SPARC context queries (active context, global context, feedback, mode-specific logs), progress logs, decision logs, etc. **Does NOT interact with `philosophers-index/`.**
- **Dependencies**: All modes (for SPARC context), `memory-bank/` files.
### Data Model: Philosophy KB Entry (V13 Initial) - [2025-05-02 02:44:49]
- **Purpose**: Standard structure for entries within the `philosophy-knowledge-base/` (using Markdown + YAML frontmatter).
- **Structure**:
  ```yaml
  ---
  id: [UUID]
  type: [Concept | Argument | Quotation | Reference | Question | Thesis | Relationship | Method | Meta-Reflection | Index]
  timestamp: [YYYY-MM-DD HH:MM:SS]
  generating_mode: [mode-slug]
  source_ref_keys: [[ref_key_1, ...]] # Link to references/
  extraction_markers: [[marker_1, ...]] # Optional, link to source_materials/processed/
  related_ids: [[id_1, ...]] # Links to other KB entries
  tags: [[tag1, tag2, e.g., 'meta', 'inquiry', 'hegel', 'critique']]
  # --- Type-specific fields ---
  # (Examples: definition, premises, conclusion, question_text, thesis_statement, reflection_summary, method_description, index_path, chunk_summary, etc.)
  ---

  # Main Content (Markdown)
  [Detailed description, analysis, text, etc.]
  ```
- **Relationships**: Managed via `related_ids` field and potentially dedicated `Relationship` type entries.
- **Interfaces Exposed**: Provides SPARC context data upon request. Accepts SPARC context data for storage.
### Diagram: Hegel Philosophy Suite V13 (Corrected Scope) - [2025-05-02 02:44:49]
- **Description:** Overall mode interaction and data flow for the enhanced Hegel suite (V13). Introduces `philosophy-kb-manager` as the gateway to the `philosophy-knowledge-base/` (PhilKB), separating it from the SPARC Memory Bank (SPARCMB) managed by `philosophy-evidence-manager`. Includes `philosophy-meta-reflector` for system self-reflection.
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
        TextProc(philosophy-text-processor) -- Runs --> Scripts((External Scripts))
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
        subgraph SPARC Memory
            EvidMan(philosophy-evidence-manager)
            SPARCMB[(SPARC Memory Bank<br>memory-bank/)]
        end
        subgraph Philosophical Knowledge Base
            KBMan(philosophy-kb-manager)
            PhilKB[(Philosophy KB<br>philosophy-knowledge-base/)]
        end
        Workspace(analysis_workspace / essay_prep / source_materials/processed)
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

    %% Text Processing Flow
    TextProc -- Processed Chunks --> Workspace
    TextProc -- Store Index/Chunk Info & Citations --> KBMan

    %% Analysis & Inquiry Flow
    PreLec -- Store Analysis/ProtoQs --> KBMan
    ClassAn -- Store Analysis/ProtoQs --> KBMan
    SecLit -- Store Analysis/ProtoQs --> KBMan
    DialAn -- Store Analysis/ProtoQs --> KBMan
    Quest -- Store RefinedQs --> KBMan

    PreLec -- Query KB --> KBMan
    ClassAn -- Query KB --> KBMan
    SecLit -- Query KB --> KBMan
    DialAn -- Query KB --> KBMan
    Quest -- Query KB --> KBMan

    %% Essay Flow
    EssayPrep -- Request KB Data/Develop Thesis --> KBMan
    EssayPrep -- Store Thesis --> KBMan
    EssayPrep -- Request Draft --> DraftGen
    EssayPrep -- Request Citation --> CiteMan
    EssayPrep -- Request Verification --> Verify
    EssayPrep -- Manage Files --> Workspace

    DraftGen -- Request KB Data --> KBMan
    DraftGen -- Draft --> EssayPrep
    DraftGen -- Trigger Commit --> Orchestrator

    CiteMan -- Request KB Data --> KBMan
    CiteMan -- Cited Draft/Biblio --> EssayPrep
    CiteMan -- Trigger Commit --> Orchestrator

    Verify -- Request KB Data/Chunks --> KBMan
    Verify -- Verification Report --> EssayPrep

    %% Meta-Reflection Flow
    MetaReflector -- Query KB --> KBMan
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

    %% Evidence Manager Interactions (SPARC Context)
    EvidMan -- Access/Update --> SPARCMB
    EvidMan -- Provide SPARC Context --> Orchestrator
    EvidMan -- Provide SPARC Context --> TextProc
    EvidMan -- Provide SPARC Context --> PreLec
    EvidMan -- Provide SPARC Context --> ClassAn
    EvidMan -- Provide SPARC Context --> SecLit
    EvidMan -- Provide SPARC Context --> DialAn
    EvidMan -- Provide SPARC Context --> Quest
    EvidMan -- Provide SPARC Context --> EssayPrep
    EvidMan -- Provide SPARC Context --> DraftGen
    EvidMan -- Provide SPARC Context --> CiteMan
    EvidMan -- Provide SPARC Context --> Verify
    EvidMan -- Provide SPARC Context --> KBMan
    EvidMan -- Provide SPARC Context --> MetaReflector


    %% Styling
    classDef kb fill:#f9f,stroke:#333,stroke-width:2px;
    class PhilKB kb;
    classDef mode fill:#ccf,stroke:#333,stroke-width:1px;
    class Orchestrator,TextProc,PreLec,ClassAn,SecLit,DialAn,Quest,EssayPrep,DraftGen,CiteMan,Verify,EvidMan,KBMan,MetaReflector mode;
    classDef script fill:#f0ad4e,stroke:#333,stroke-width:1px;
    class Scripts script;
    classDef vcs fill:#d9edf7,stroke:#31708f,stroke-width:1px;
    class VCS vcs;
    classDef sparcmb fill:#e0e0e0,stroke:#666,stroke-width:1px;
    class SPARCMB sparcmb;
```
**Notes:** Cross-references `docs/architecture/architecture_v13.md` for full details.
- **Internal Structure (High-Level)**: Logic for reading/writing/querying files within `memory-bank/`.

## Data Models
### Data Model: Philosophy KB Entry (V14 Context-Aware) - [2025-05-02 05:20:19]
- **Purpose**: Standard structure for entries within the `philosophy-knowledge-base/`, enhanced to include source context tags.
- **Structure**:
  ```yaml
  ---
  id: [UUID]
  type: [Concept | Argument | Quotation | Reference | Question | Thesis | Relationship | Method | Meta-Reflection | Index]
  timestamp: [YYYY-MM-DD HH:MM:SS]
  generating_mode: [mode-slug]
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
  ---

  # Main Content (Markdown)
  [Detailed description, analysis, text, etc.]
  ```
- **Relationships**: Managed via `related_ids` field and potentially dedicated `Relationship` type entries.
- **Notes**: Key change is the inclusion of `context:key:value` tags within the `tags` list for entries derived from source material. See `docs/specs/v14_requirements_spec_v1.md`.
### Data Model: Philosopher's Index Entry (V13 Initial) - [2025-05-02 00:45:10]
- **Purpose**: Standard structure for entries within the `philosophers-index/` (using Markdown + YAML frontmatter).
- **Structure**:
  ```yaml
  ---
  id: [UUID]
  type: [Concept | Argument | Quotation | Reference | Question | Thesis | Relationship]
  timestamp: [YYYY-MM-DD HH:MM:SS]
  generating_mode: [mode-slug]
  source_ref_keys: [[ref_key_1, ref_key_2, ...]] # Link to knowledge_base/references/
  extraction_markers: [[marker_1, marker_2, ...]] # Optional, link to source text
  related_ids: [[id_1, id_2, ...]] # Links to other Index entries
  tags: [[tag1, tag2, ...]]
  # --- Type-specific fields below ---
  # e.g., for Concept:
  # definition: "..."
  # key_texts: [...]
  # potential_issues: [...]
  # e.g., for Argument:
  # premises: ["...", "..."]
  # conclusion: "..."
  # supporting_texts: [...]
  # counter_arguments: [[arg_id_1, ...]]
  # e.g., for Quotation:
  # text: "..."
  # e.g., for Question:
  # question_text: "..."
  # context: "..."
  # potential_theses: [[thesis_id_1, ...]]
  # e.g., for Thesis:
  # thesis_statement: "..."
  # supporting_evidence_ids: [[arg_id_1, concept_id_2, ...]]
  ---

  # Main Content (Markdown)
  [Detailed description, analysis, quotation text, etc.]
  ```
- **Relationships**: Managed via `related_ids` field and potentially dedicated `Relationship` type entries.

## System Diagrams
### Diagram: Hegel Philosophy Suite V14 - [2025-05-02 05:20:19]
- **Description:** Overall mode interaction and data flow for V14. Integrates V13 KB/Workflows with V14 Source Context Handling (raw source structure, context extraction/tagging, context-aware querying).
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
        subgraph SPARC Memory
            EvidMan(philosophy-evidence-manager)
            SPARCMB[(SPARC Memory Bank<br>memory-bank/)]
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

    %% Evidence Manager Interactions (SPARC Context)
    EvidMan -- Access/Update --> SPARCMB
    EvidMan -- Provide SPARC Context --> Orchestrator
    EvidMan -- Provide SPARC Context --> TextProc
    EvidMan -- Provide SPARC Context --> PreLec
    EvidMan -- Provide SPARC Context --> ClassAn
    EvidMan -- Provide SPARC Context --> SecLit
    EvidMan -- Provide SPARC Context --> DialAn
    EvidMan -- Provide SPARC Context --> Quest
    EvidMan -- Provide SPARC Context --> EssayPrep
    EvidMan -- Provide SPARC Context --> DraftGen
    EvidMan -- Provide SPARC Context --> CiteMan
    EvidMan -- Provide SPARC Context --> Verify
    EvidMan -- Provide SPARC Context --> KBMan
    EvidMan -- Provide SPARC Context --> MetaReflector


    %% Styling
    classDef kb fill:#f9f,stroke:#333,stroke-width:2px;
    class PhilKB kb;
    classDef mode fill:#ccf,stroke:#333,stroke-width:1px;
    class Orchestrator,TextProc,PreLec,ClassAn,SecLit,DialAn,Quest,EssayPrep,DraftGen,CiteMan,Verify,EvidMan,KBMan,MetaReflector mode;
    classDef script fill:#f0ad4e,stroke:#333,stroke-width:1px;
    class Scripts script;
    classDef vcs fill:#d9edf7,stroke:#31708f,stroke-width:1px;
    class VCS vcs;
    classDef sparcmb fill:#e0e0e0,stroke:#666,stroke-width:1px;
    class SPARCMB sparcmb;
    classDef source fill:#dff0d8,stroke:#3c763d,stroke-width:1px;
    class RawSource,ProcessedSource source;
```
**Notes:** Reflects V14 architecture documented in `docs/architecture/architecture_v14.md`.
### Diagram: V14 Source Context Extraction & Tagging Flow - [2025-05-02 03:41:12]
- **Description:** Illustrates how context is extracted from the raw source file path by `philosophy-text-processor` and stored as tags within the corresponding KB entry by `philosophy-kb-manager`.
```mermaid
graph LR
    A[Raw Source File<br>`source_materials/raw/courses/PHL316/readings/Hegel_Work.md`] --> B(philosophy-text-processor);
    B -- Extracts Path --> C{Context Info<br>type: course<br>id: PHL316<br>subtype: reading};
    B -- Processed Chunks, Index, Citations --> D(philosophy-kb-manager);
    C -- Context Tags --> D;
    D -- Creates/Updates Entry --> E[KB Entry<br>`philosophy-knowledge-base/...`];
    E -- Contains YAML --> F{YAML Frontmatter<br>...<br>tags: [<br>  "context:type:course",<br>  "context:id:PHL316",<br>  "context:subtype:reading"<br>]<br>...};
```
**Notes:** This flow enables context-aware querying of the KB. See `docs/architecture/architecture_v14.md` and `docs/specs/v14_requirements_spec_v1.md`.
### Diagram: Hegel Philosophy Suite V13 - [2025-05-02 00:45:10]
- **Description:** Overall mode interaction and data flow for the enhanced Hegel suite (V13). Introduces `philosophy-kb-manager` as the gateway to the `Philosopher's Index`, separating it from the SPARC Memory Bank managed by `philosophy-evidence-manager`.
```mermaid
graph TD
    subgraph User Interaction
        User(User)
    end

    subgraph Orchestration
        Orchestrator(philosophy-orchestrator)
    end

    subgraph Text Processing
        TextProc(philosophy-text-processor) -- Runs --> Scripts((External Scripts))
    end

    subgraph Analysis & Questioning
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
        subgraph SPARC Memory
            EvidMan(philosophy-evidence-manager)
            SPARCMB[(SPARC Memory Bank<br>memory-bank/)]
        end
        subgraph Philosophical Knowledge
            KBMan(philosophy-kb-manager)
            PhilIndex[(Philosopher's Index<br>philosophers-index/)]
        end
        Workspace(analysis_workspace / essay_prep / source_materials/processed)
    end

    %% Core Flow
    User -- Request --> Orchestrator
    Orchestrator -- Delegate Tasks --> TextProc
    Orchestrator -- Delegate Tasks --> PreLec
    Orchestrator -- Delegate Tasks --> ClassAn
    Orchestrator -- Delegate Tasks --> SecLit
    Orchestrator -- Delegate Tasks --> DialAn
    Orchestrator -- Delegate Tasks --> Quest
    Orchestrator -- Delegate Tasks --> EssayPrep
    Orchestrator -- Coordinate Commit? --> EssayPrep
    Orchestrator -- Route Modification Proposal --> User
    Orchestrator -- Results --> User

    %% Text Processing Flow
    TextProc -- Processed Chunks --> Workspace
    TextProc -- Store Index/Chunk Info & Citations --> KBMan

    %% Analysis Flow
    PreLec -- Store Analysis/ProtoQs --> KBMan
    ClassAn -- Store Analysis/ProtoQs --> KBMan
    SecLit -- Store Analysis/ProtoQs --> KBMan
    DialAn -- Store Analysis/ProtoQs --> KBMan
    Quest -- Store RefinedQs/Mod Proposals --> KBMan

    PreLec -- Query Index --> KBMan
    ClassAn -- Query Index --> KBMan
    SecLit -- Query Index --> KBMan
    DialAn -- Query Index --> KBMan
    Quest -- Query Index --> KBMan

    %% Essay Flow
    EssayPrep -- Request Evidence/Develop Thesis --> KBMan
    EssayPrep -- Store Thesis --> KBMan
    EssayPrep -- Request Draft --> DraftGen
    EssayPrep -- Request Citation --> CiteMan
    EssayPrep -- Request Verification --> Verify
    EssayPrep -- Manage Files --> Workspace

    DraftGen -- Request Evidence --> KBMan
    DraftGen -- Draft --> EssayPrep
    DraftGen -- Trigger Commit --> Orchestrator

    CiteMan -- Request References/Citation Data --> KBMan
    CiteMan -- Cited Draft/Biblio --> EssayPrep
    CiteMan -- Trigger Commit --> Orchestrator

    Verify -- Request Evidence/Refs/Chunks --> KBMan
    Verify -- Verification Report --> EssayPrep

    %% KB Manager Interactions
    KBMan -- Access/Update --> PhilIndex
    KBMan -- Provide Data/Paths --> PreLec
    KBMan -- Provide Data/Paths --> ClassAn
    KBMan -- Provide Data/Paths --> SecLit
    KBMan -- Provide Data/Paths --> DialAn
    KBMan -- Provide Data/Paths --> Quest
    KBMan -- Provide Data/Paths --> EssayPrep
    KBMan -- Provide Data/Paths --> DraftGen
    KBMan -- Provide Data/Paths --> CiteMan
    KBMan -- Provide Data/Paths --> Verify
    KBMan -- Execute Approved Modification --> PhilIndex

    %% Evidence Manager Interactions (SPARC Context)
    EvidMan -- Access/Update --> SPARCMB
    EvidMan -- Provide SPARC Context --> Orchestrator
    EvidMan -- Provide SPARC Context --> TextProc
    EvidMan -- Provide SPARC Context --> PreLec
    EvidMan -- Provide SPARC Context --> ClassAn
    EvidMan -- Provide SPARC Context --> SecLit
    EvidMan -- Provide SPARC Context --> DialAn
    EvidMan -- Provide SPARC Context --> Quest
    EvidMan -- Provide SPARC Context --> EssayPrep
    EvidMan -- Provide SPARC Context --> DraftGen
    EvidMan -- Provide SPARC Context --> CiteMan
    EvidMan -- Provide SPARC Context --> Verify
    EvidMan -- Provide SPARC Context --> KBMan


    %% Styling
    classDef kb fill:#f9f,stroke:#333,stroke-width:2px;
    class PhilIndex kb;
    classDef mode fill:#ccf,stroke:#333,stroke-width:1px;
    class Orchestrator,TextProc,PreLec,ClassAn,SecLit,DialAn,Quest,EssayPrep,DraftGen,CiteMan,Verify,EvidMan,KBMan mode;
    classDef script fill:#f0ad4e,stroke:#333,stroke-width:1px;
    class Scripts script;
    classDef vcs fill:#d9edf7,stroke:#31708f,stroke-width:1px;
    class VCS vcs;
    classDef sparcmb fill:#e0e0e0,stroke:#666,stroke-width:1px;
    class SPARCMB sparcmb;
```
**Notes:** Cross-references `docs/architecture/architecture_v13.md` for full details.
### [2025-05-01 22:10:18] Task: Verify Reworked `.clinerules` Files (Post-Intervention)
- **Action**: Read reference docs (`architecture_v12.md`, `new_requirements_spec_v1.md`, `clinerules_review_report_v1.md`), feedback/intervention logs, and 6 target `.clinerules` files (`orchestrator`, `essay-prep`, `citation-manager`, `draft-generator`, `verification-agent`, `text-processor`). Compared files against V12 specs and feedback.
- **Findings**: Most files functionally implement V12 features (scripted text processor, Git workflow), contradicting earlier review report (`clinerules_review_report_v1.md`). **CRITICAL GAP:** All modes inheriting standard MB rules lack the mandatory user confirmation step for handover delegation required by feedback [2025-05-01 21:00:03]. `philosophy-text-processor` rules are minimal but functional, addressing user quality concern partially.
- **Output**: Created `clinerules_verification_report_v1.md`.
- **Status**: Task complete. Report generated. Cross-ref: [Progress Update 2025-05-01 22:10:18], [Decision Log 2025-05-01 22:10:18]
### Task: Review Intermediate Artifacts (Phase 0, Step 2) - [2025-05-01 19:41:49]
- **Action**: Reviewed `clinerules_revision_plan_v1.md`, `clinerules_template_v1.md`, and conceptual `philosophy-orchestrator.clinerules` against `architecture_v12.md` and `new_requirements_spec_v1.md`.
- **Findings**: Artifacts are inconsistent with V12 due to being based on V11. They lack specifications for the V12 `philosophy-text-processor` (script-based, detailed outputs) and the Git-based version control system.
- **Output**: Created `artifact_review_report_v1.md` detailing findings and recommending revision of plan/template before proceeding.
- **Status**: Task complete. Memory Bank updated. Ready for SPARC to proceed with next step in `philosophy_mode_improvement_plan_v2.md`.
### Task: Revise Architecture (V12) & Plan (V2) - [2025-05-01 19:30:56]
- **Action**: Analyzed `new_requirements_spec_v1.md`, `architecture_v11.md`, `philosophy_mode_improvement_plan.md`.
- **Details**: Created `architecture_v12.md` incorporating `philosophy-text-processor` (script-based chunking/indexing/citation extraction) and Git version control. Updated Mermaid diagram and mode responsibilities. Created `philosophy_mode_improvement_plan_v2.md` reflecting V12 architecture, adding text processor script implementation, version control setup, and a pre-implementation review step for potentially flawed artifacts.
- **Status**: Task complete. Architecture and plan updated. Memory Bank updated. Ready for SPARC to proceed with Plan V2, Phase 0.
### Phase 1, Step 2: Design New Architecture - [2025-05-01 14:43:50]
- **Description**: Designed the V11 architecture for the Hegel Philosophy RooCode Suite based on `philosophy_mode_improvement_plan.md` and `architecture_review_summary_v2.md`.
- **Key Decisions**:
    - Introduced `philosophy-orchestrator` for workflow management.
    - Defined `knowledge_base` structure and `philosophy-evidence-manager` for centralized data access.
    - Added specialized modes: `philosophy-draft-generator`, `philosophy-citation-manager`, `philosophy-verification-agent`.
    - Refactored roles of existing analysis modes to populate `knowledge_base`.
    - Defined verification procedures involving `philosophy-verification-agent`.
    - Specified `.roo/.roomodes` and `.roo/rules-[mode-slug]/` structure.
- **Output**: Created `architecture_v11.md` containing the full design.
- **Status**: Architecture design complete. Ready for Phase 1, Step 3 (Implementation Planning).

## System Diagrams
### Diagram: Hegel Philosophy Suite V11 - [2025-05-01 14:43:50]
- **Description:** Overall mode interaction and data flow for the enhanced Hegel suite (V11). Shows orchestration, knowledge base population, essay generation/verification, and the central knowledge base.
```mermaid
graph TD
### Diagram: Hegel Philosophy Suite V12 - [2025-05-01 19:30:56]
- **Description:** Overall mode interaction and data flow for the enhanced Hegel suite (V12). Includes `philosophy-text-processor` (with external scripts) and Git version control integration.
```mermaid
graph TD
    subgraph User Interaction
        User(User)
    end

    subgraph Orchestration
        Orchestrator(philosophy-orchestrator)
    end

    subgraph Text Processing
        TextProc(philosophy-text-processor) -- Runs --> Scripts((External Scripts))
    end

    subgraph Knowledge Base Population
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
        EvidMan(philosophy-evidence-manager)
        KB[(knowledge_base<br>+ Processed Indices/Citations)]
        Workspace(analysis_workspace / essay_prep / source_materials/processed)
    end

    User -- Request --> Orchestrator
    Orchestrator -- Delegate Tasks --> TextProc
    Orchestrator -- Delegate Tasks --> PreLec
    Orchestrator -- Delegate Tasks --> ClassAn
    Orchestrator -- Delegate Tasks --> SecLit
    Orchestrator -- Delegate Tasks --> DialAn
    Orchestrator -- Delegate Tasks --> Quest
    Orchestrator -- Delegate Tasks --> EssayPrep
    Orchestrator -- Coordinate Commit? --> EssayPrep
    Orchestrator -- Results --> User

    TextProc -- Processed Chunks/Indices --> Workspace
    TextProc -- Store Index/Chunk Info & Citations --> EvidMan

    PreLec -- Store Analysis --> EvidMan
    ClassAn -- Store Analysis --> EvidMan
    SecLit -- Store Analysis --> EvidMan
    DialAn -- Store Analysis --> EvidMan
    Quest -- Store Questions --> EvidMan

    PreLec -- Query Evidence/Indices --> EvidMan
    ClassAn -- Query Evidence/Indices --> EvidMan
    SecLit -- Query Evidence/Indices --> EvidMan
    DialAn -- Query Evidence/Indices --> EvidMan
    Quest -- Query Evidence/Indices --> EvidMan

    EssayPrep -- Request Evidence/Indices --> EvidMan
    EssayPrep -- Request Draft --> DraftGen
    EssayPrep -- Request Citation --> CiteMan
    EssayPrep -- Request Verification --> Verify
    EssayPrep -- Manage Files --> Workspace

    EvidMan -- Access/Update --> KB
    EvidMan -- Provide Data/Paths --> PreLec
    EvidMan -- Provide Data/Paths --> ClassAn
    EvidMan -- Provide Data/Paths --> SecLit
    EvidMan -- Provide Data/Paths --> DialAn
    EvidMan -- Provide Data/Paths --> Quest
    EvidMan -- Provide Data/Paths --> EssayPrep
    EvidMan -- Provide Data/Paths --> DraftGen
    EvidMan -- Provide Data/Paths --> CiteMan
    EvidMan -- Provide Data/Paths --> Verify

    DraftGen -- Request Evidence --> EvidMan
    DraftGen -- Draft --> EssayPrep
    DraftGen -- Trigger Commit --> Orchestrator

    CiteMan -- Request References/Citation Data --> EvidMan
    CiteMan -- Cited Draft/Biblio --> EssayPrep
    CiteMan -- Trigger Commit --> Orchestrator

    Verify -- Request Evidence/Refs/Chunks --> EvidMan
    Verify -- Verification Report --> EssayPrep

    %% Styling
    classDef kb fill:#f9f,stroke:#333,stroke-width:2px;
    class KB kb;
    classDef mode fill:#ccf,stroke:#333,stroke-width:1px;
    class Orchestrator,TextProc,PreLec,ClassAn,SecLit,DialAn,Quest,EssayPrep,DraftGen,CiteMan,Verify,EvidMan mode;
    classDef script fill:#f0ad4e,stroke:#333,stroke-width:1px;
    class Scripts script;
    classDef vcs fill:#d9edf7,stroke:#31708f,stroke-width:1px;
    class VCS vcs;
```
**Notes:** Cross-references `architecture_v12.md` for full details.
    subgraph User Interaction
        User(User)
    end

    subgraph Orchestration
        Orchestrator(philosophy-orchestrator)
    end

    subgraph Knowledge Base Population
        TextProc(philosophy-text-processing)
        PreLec(philosophy-pre-lecture)
        ClassAn(philosophy-class-analysis)
        SecLit(philosophy-secondary-lit)
        DialAn(philosophy-dialectical-analysis)
        Quest(philosophy-questioning)
### Component Specification: philosophy-text-processor - [2025-05-01 19:30:56]
- **Responsibility**: Pre-processes large Markdown source texts via external scripts. Performs recursive splitting by headers, enforces chunk size limits, generates hierarchical `index.md` files (with summaries, concepts, args, links, metadata), and extracts detailed citation information at the deepest levels. Handles potential formatting/ToC issues.
- **Dependencies**: External scripts (e.g., Python), `philosophy-orchestrator` (trigger), `philosophy-evidence-manager` (store index/citation data).
- **Interfaces Exposed**: Orchestrated via `philosophy-orchestrator`. Provides status updates. Outputs processed files to `source_materials/processed/` and structured data (index info, citations) to `philosophy-evidence-manager`.
- **Internal Structure (High-Level)**: Mode orchestrates calls to external scripts for parsing, splitting, indexing, citation extraction, and file I/O. May include logic for manifest generation/parsing for corrections.
    end

    subgraph Essay Generation & Verification
        EssayPrep(philosophy-essay-prep)
        DraftGen(philosophy-draft-generator)
### Plan: Hegel Philosophy Mode Enhancement V2 - [2025-05-01 19:30:56]
- **Description**: Created `philosophy_mode_improvement_plan_v2.md` based on `architecture_v12.md`.
- **Focus**: Incorporates implementation steps for `philosophy-text-processor` (including external scripts), Git version control integration, and adds a pre-implementation review phase (Phase 0) for potentially problematic artifacts identified in user feedback [2025-05-01 19:21:04].
- **Key Elements**: Phase 0 (VC Init, Artifact Review), Phase 1 (Architecture - Completed), Phase 2 (Mode & Script Implementation - including text processor scripts and VC commands), Phase 3 (Configuration & Integration), Phase 4 (Testing & Docs).
- **Status**: Plan created. Ready for SPARC to initiate Phase 0. Cross-references `philosophy_mode_improvement_plan_v2.md`.
        CiteMan(philosophy-citation-manager)
        Verify(philosophy-verification-agent)
    end

    subgraph Data Layer
        EvidMan(philosophy-evidence-manager)
        KB[(knowledge_base)]
        Workspace(analysis_workspace / essay_prep)
    end

    User -- Request --> Orchestrator
    Orchestrator -- Delegate Tasks --> TextProc
    Orchestrator -- Delegate Tasks --> PreLec
    Orchestrator -- Delegate Tasks --> ClassAn
    Orchestrator -- Delegate Tasks --> SecLit
    Orchestrator -- Delegate Tasks --> DialAn
    Orchestrator -- Delegate Tasks --> Quest
    Orchestrator -- Delegate Tasks --> EssayPrep
    Orchestrator -- Results --> User

    TextProc -- Processed Text --> Workspace
    TextProc -- Update Refs --> EvidMan

    PreLec -- Store Analysis --> EvidMan
    ClassAn -- Store Analysis --> EvidMan
    SecLit -- Store Analysis --> EvidMan
    DialAn -- Store Analysis --> EvidMan
    Quest -- Store Questions --> EvidMan

    PreLec -- Query Evidence --> EvidMan
    ClassAn -- Query Evidence --> EvidMan
    SecLit -- Query Evidence --> EvidMan
    DialAn -- Query Evidence --> EvidMan
    Quest -- Query Evidence --> EvidMan

    EssayPrep -- Request Evidence --> EvidMan
    EssayPrep -- Request Draft --> DraftGen
    EssayPrep -- Request Citation --> CiteMan
    EssayPrep -- Request Verification --> Verify
    EssayPrep -- Manage Files --> Workspace

    EvidMan -- Access/Update --> KB
    EvidMan -- Provide Data --> PreLec
    EvidMan -- Provide Data --> ClassAn
    EvidMan -- Provide Data --> SecLit
    EvidMan -- Provide Data --> DialAn
    EvidMan -- Provide Data --> Quest
    EvidMan -- Provide Data --> EssayPrep
    EvidMan -- Provide Data --> DraftGen
    EvidMan -- Provide Data --> CiteMan
    EvidMan -- Provide Data --> Verify

    DraftGen -- Request Evidence --> EvidMan
    DraftGen -- Draft --> EssayPrep

    CiteMan -- Request References --> EvidMan
    CiteMan -- Cited Draft/Biblio --> EssayPrep

    Verify -- Request Evidence/Refs --> EvidMan
    Verify -- Verification Report --> EssayPrep

    %% Styling
    classDef kb fill:#f9f,stroke:#333,stroke-width:2px;
    class KB kb;
    classDef mode fill:#ccf,stroke:#333,stroke-width:1px;
    class Orchestrator,TextProc,PreLec,ClassAn,SecLit,DialAn,Quest,EssayPrep,DraftGen,CiteMan,Verify,EvidMan mode;
```
**Notes:** Cross-references `architecture_v11.md` for full details.
### Phase 1, Step 1: Review Existing Assets (Re-run) - [2025-05-01 13:38:00]
- **Description**: Re-ran the review of existing assets (`architectureV10.md`, actual `.clinerules` files in root) as per `philosophy_mode_improvement_plan.md`, based on corrected file information.
- **Findings**: Confirmed strengths (modularity, evidence linking, concept frameworks) and weaknesses (basic essay generation, missing citation generation/verification, lack of essay draft verification, no orchestrator, non-optimal memory for essay research) in V10 architecture and existing rules regarding enhancement goals.
- **Output**: Created `architecture_review_summary_v2.md` detailing the updated findings.
- **Status**: Ready for Phase 1, Step 2: Design New Architecture.
## Architectural Plans
### Plan: Philosophy Mode `.clinerules` Revision V1 - [2025-05-01 17:41:59]
- **Description**: Created `clinerules_revision_plan_v1.md` to guide the revision of `.clinerules` for all 12 philosophy modes defined in `architecture_v11.md`.
- **Focus**: Addresses user feedback [2025-05-01 16:57:41] by defining a consistent structure, ensuring philosophical rigor, and integrating `philosophy-orchestrator` capabilities.
- **Key Elements**: Includes a standard template proposal, content tailoring strategy (philosophical methods, avoiding generic rules), orchestrator interaction details (`new_task`), and a multi-step revision process.
- **Status**: Plan created. Ready for implementation (e.g., template drafting). Cross-references `clinerules_revision_plan_v1.md`.
## Task Progress
### Task: Document New Requirements - [2025-05-01 19:26:40]
- **Action**: Analyzed user feedback [2025-05-01 19:21:04] and created `new_requirements_spec_v1.md`.
- **Details**: Documented detailed specifications for the new `philosophy-text-processor` mode (recursive Markdown splitting, indexing, summarization, citation extraction, script-based processing, token limits, generic leveling) and version control integration (Git-based, workflow integration).
- **Status**: Specification document created. This informs the next step: revising the architecture to V12.

### Task: Revise philosophy-orchestrator.clinerules - [2025-05-01 17:47:30]
- **Action**: Synthesized revised rules content for `philosophy-orchestrator` based on `architecture_v11`, `clinerules_revision_plan_v1`, and `clinerules_template_v1`.
- **Status**: Content generated, ready for review/implementation. Part of Corrective Step 3.2.1.
### Phase 1, Step 1: Review Existing Assets - [2025-05-01 13:21:59]
- **Description**: Completed the review of existing assets (`architectureV10.md`, inferred modes) as per `philosophy_mode_improvement_plan.md`.
- **Findings**: Identified strengths (rigorous principles, modularity, evidence linking) and weaknesses (lack of dynamic evidence retrieval for essays, missing citation generation, insufficient verification in essay context, lack of orchestration, non-optimal memory structure for essays) in V10 architecture regarding essay writing, referencing, and verification.
- **Output**: Created `architecture_review_summary.md` detailing the findings.
- **Status**: Ready for Phase 1, Step 2: Design New Architecture.
<!-- Append new plans using the format below -->

### Plan: Hegel Philosophy Mode Enhancement - [2025-05-01 13:10:42]
- **Description**: Created a detailed task prompt and implementation plan (`philosophy_mode_improvement_plan.md`) for refactoring and enhancing the custom Hegel philosophy RooCode suite.
- **Focus**: Improving essay writing, reference accuracy, hallucination prevention, and memory management.
- **Key Elements**: Defined new architecture (`architecture_v11.md` to be created), new `philosophy-orchestrator` mode, refactoring steps for existing modes, new `.roo` structure for configuration, memory system design, and verification procedures.
- **Status**: Plan ready for handover to SPARC Orchestrator.
<!-- Entries below should be added reverse chronologically (newest first) -->