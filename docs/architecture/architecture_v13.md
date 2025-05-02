# Hegel Philosophy RooCode Suite - Architecture V13

**Date:** 2025-05-02
**Version:** 13.0
**Status:** Draft
**Based On:**
*   `docs/architecture/architecture_v12.md`
*   `docs/specs/new_requirements_spec_v1.md`
*   `architecture-questioning.md` (System Self-Reflection concepts)
*   User Task & Feedback (as of 2025-05-02 02:28)
*   Memory Bank Context (as of 2025-05-02 02:41)

**Goal:** Define the V13 architecture, integrating a dedicated **Philosophy Knowledge Base (KB)**, a **Philosophical Inquiry Workflow**, and a **System Self-Reflection Workflow** into the V12 structure. This version emphasizes a clear separation between domain knowledge (KB) and process memory (SPARC Memory Bank), introduces meta-reflective capabilities, and refines mode responsibilities.

## 1. Core Principles (Inherited & Extended)

*   **Determinacy:** Concepts/arguments clearly defined. (V11+)
*   **Evidence Saturation:** Claims linked to sources via KB entries & extraction markers. (V11+)
*   **Chronological Integrity:** Analysis respects temporal flow. (V11+)
*   **Verification Rigor:** Inputs/outputs verified against KB & sources. (V11+)
*   **Modularity:** Encapsulated functionality in specialized modes. (V11+)
*   **Orchestration:** Complex workflows managed by `philosophy-orchestrator`. (V11+)
*   **Traceability:** Version control (Git) for key artifacts (essays, potentially KB/config). (V12+)
*   **Knowledge Separation (New V13):** Explicit distinction between philosophical domain knowledge (`philosophy-knowledge-base/`) and SPARC operational/process memory (`memory-bank/`).
*   **Reflexivity (New V13):** Capacity for the system to question its own assumptions, methods, and architecture (`philosophy-meta-reflector`).
*   **Controlled Evolution (New V13):** Mechanisms for proposing and approving modifications to the KB and potentially the system architecture itself.

## 2. V13 Architecture Overview

V13 introduces three major components integrated into the V12 structure:

1.  **Philosophy Knowledge Base (KB):** A dedicated, structured repository (`philosophy-knowledge-base/`) for philosophical concepts, arguments, references, questions, theses, etc., managed exclusively by the new `philosophy-kb-manager` mode.
2.  **Philosophical Inquiry Workflow:** Leverages analysis modes, `philosophy-questioning`, and `philosophy-essay-prep` to generate, refine, and store philosophical questions and theses within the KB.
3.  **System Self-Reflection Workflow:** Introduces the `philosophy-meta-reflector` mode to enable meta-level analysis and questioning of the system's own structure, methods, and potential biases, storing reflections in the KB and proposing changes.

## 3. Mode Structure & Responsibilities (V13)

### 3.1. Core Data Management Modes (Revised/New)

*   **`philosophy-kb-manager` (New):**
    *   **Responsibility:** Acts as the **sole interface** to the `philosophy-knowledge-base/`. Handles CRUD operations and querying for structured philosophical data (concepts, arguments, quotations, references, questions, theses, relationships, methods). Manages internal linking, structure, and data integrity within the KB. Executes approved KB modification proposals received via the orchestrator.
    *   **Input:** Structured queries from other modes, structured data for storage, approved modification instructions.
    *   **Output:** Formatted philosophical data packages (e.g., Markdown snippets, JSON). Confirmation of data storage/modification.
    *   **Dependencies:** `philosophy-orchestrator` (for modification approvals), All modes requiring philosophical knowledge, `philosophy-evidence-manager` (for SPARC context if needed for cross-referencing).
*   **`philosophy-evidence-manager` (Revised Scope):**
    *   **Responsibility:** Manages access **only** to the **SPARC Memory Bank** (`memory-bank/`) and potentially intermediate analysis files (`analysis_workspace/`). Handles queries for SPARC context (active context, global context, feedback, mode-specific logs), progress logs, decision logs, etc. **Does NOT interact with `philosophy-knowledge-base/`.**
    *   **Input:** Queries for SPARC context data, SPARC context data for storage.
    *   **Output:** SPARC context data packages. Confirmation of data storage.
    *   **Dependencies:** All modes (for SPARC context), `memory-bank/` files.

### 3.2. Text Processing & Analysis Modes (Interactions Updated)

*   **`philosophy-text-processor` (V12):**
    *   **Responsibility:** Pre-processes source texts via external scripts (chunking, indexing, citation extraction).
    *   **Output:** Processed chunks/indices to `source_materials/processed/`. Index/chunk structure info and extracted citation data provided to **`philosophy-kb-manager`** (changed from V12 `evidence-manager`) for storage in the KB.
    *   **Dependencies:** External scripts, `philosophy-orchestrator`, **`philosophy-kb-manager`**.
*   **`philosophy-pre-lecture` (V11+):**
    *   **Responsibility:** Analyzes upcoming readings using processed chunks/indices. Generates concepts, arguments, questions.
    *   **Interaction:** Queries **`philosophy-kb-manager`** for processed readings/indices. Stores findings (concepts, proto-questions, etc.) via **`philosophy-kb-manager`**.
*   **`philosophy-class-analysis` (V11+):**
    *   **Responsibility:** Analyzes lecture transcripts alongside readings. Identifies arguments, clarifications, connections.
    *   **Interaction:** Queries **`philosophy-kb-manager`** for relevant processed texts/indices/concepts. Stores findings via **`philosophy-kb-manager`**.
*   **`philosophy-secondary-lit` (V11+):**
    *   **Responsibility:** Analyzes secondary literature. Identifies interpretations, critiques, context.
    *   **Interaction:** Queries **`philosophy-kb-manager`** for processed texts/indices. Stores findings via **`philosophy-kb-manager`**. Updates reference data in KB via **`philosophy-kb-manager`**.
*   **`philosophy-dialectical-analysis` (V11+):**
    *   **Responsibility:** Performs deep dialectical analysis using KB content.
    *   **Interaction:** Queries **`philosophy-kb-manager`** for arguments, concepts, texts. Stores detailed analyses via **`philosophy-kb-manager`**.
*   **`philosophy-questioning` (V11+, Role Refined for Inquiry Workflow):**
    *   **Responsibility:** Focuses on **refining philosophical questions** for inquiry (essays, research). Interacts with the KB to identify ambiguities, develop lines of inquiry based on existing concepts/arguments. Distinguishes these from system/meta questions handled by `meta-reflector`.
    *   **Interaction:** Queries **`philosophy-kb-manager`** for proto-questions, concepts, arguments. Stores refined philosophical questions via **`philosophy-kb-manager`**.

### 3.3. Essay Generation & Verification Modes (Interactions Updated)

*   **`philosophy-essay-prep` (V11+):**
    *   **Responsibility:** Manages essay writing process (prompt analysis, thesis development, outline, evidence gathering coordination). Manages Git version control for essays.
    *   **Interaction:** Queries **`philosophy-kb-manager`** for relevant concepts, arguments, questions, theses to develop outline and evidence requirements. Stores developed thesis via **`philosophy-kb-manager`**. Coordinates with other essay modes. Executes Git commands.
*   **`philosophy-draft-generator` (V11+):**
    *   **Responsibility:** Generates prose based on outline and evidence. Triggers commit.
    *   **Interaction:** Requests evidence package (concepts, arguments, quotes) from **`philosophy-kb-manager`** (via `essay-prep` or directly).
*   **`philosophy-citation-manager` (V11+):**
    *   **Responsibility:** Formats citations and bibliography using KB data. Triggers commit.
    *   **Interaction:** Requests reference details and detailed citation location data from **`philosophy-kb-manager`**.
*   **`philosophy-verification-agent` (V11+):**
    *   **Responsibility:** Verifies claims and citations against KB and processed source chunks.
    *   **Interaction:** Requests evidence, references, and processed chunk paths/indices from **`philosophy-kb-manager`**.

### 3.4. Orchestration & Meta-Reflection Modes (Updated/New)

*   **`philosophy-orchestrator` (V11+):**
    *   **Responsibility:** Manages workflows, delegates tasks, handles handoffs, sequences operations. **Routes KB/System modification proposals** from modes like `meta-reflector` or `kb-manager` to the user for approval before relaying approval back to `kb-manager` or `architect`/`code`. Coordinates Git commits.
    *   **Key Workflows:** Includes V12 workflows plus:
        *   `philosophical_inquiry`: User Prompt/Analysis Output -> `kb-manager` (Store Proto-Q) -> `philosophy-questioning` (Refine Q) -> `kb-manager` (Store Refined Q) -> `philosophy-essay-prep` (Develop Thesis) -> `kb-manager` (Store Thesis).
        *   `system_self_reflection`: Trigger (User/Error/Schedule) -> `philosophy-meta-reflector` (Analyze System/MB/Docs/Rules) -> `kb-manager` (Store Meta-Reflections/Questions) -> `Orchestrator` (Route Proposals: KB Mod -> `kb-manager` via User; Arch Mod -> `architect` via User; Method Mod -> `kb-manager` via User).
        *   `kb_modification`: Proposal (e.g., from `meta-reflector`) -> `Orchestrator` -> User (Approval) -> `Orchestrator` -> `philosophy-kb-manager` (Execute Change).
*   **`philosophy-meta-reflector` (New):**
    *   **Responsibility:** Performs meta-level analysis of the system itself. Questions assumptions, methods, architecture, potential biases, and limitations based on `architecture-questioning.md` principles. Analyzes `memory-bank` logs, architecture documents, `.clinerules`, and potentially code structure. Proposes improvements or modifications.
    *   **Input:** Trigger (User, Orchestrator), Read access to `memory-bank/`, `docs/`, `.roo/`, potentially workspace code. Access to KB via `kb-manager`.
    *   **Output:** Meta-reflections and meta-questions stored in KB via `kb-manager` (tagged appropriately). Proposals for KB modifications (e.g., refining method descriptions) sent to Orchestrator. Proposals for architectural changes sent to Orchestrator (for routing to Architect). Proposals for methodological shifts (potentially involving Git branching for system evolution exploration) sent to Orchestrator (for routing to DevOps/Architect).
    *   **Dependencies:** `philosophy-orchestrator`, `philosophy-kb-manager`, `philosophy-evidence-manager` (for MB access), potentially `architect`, `devops`.

## 4. V13 Mode Interaction Diagram (Mermaid)

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

**Diagram Notes:**
*   Introduces `philosophy-kb-manager` as the gateway to the `philosophy-knowledge-base/` (PhilKB).
*   `philosophy-evidence-manager` now solely manages the SPARC Memory Bank (SPARCMB).
*   Introduces `philosophy-meta-reflector` interacting with Orchestrator, KBMan, EvidMan, and potentially proposing changes.
*   Analysis/Essay modes now query `KBMan` for philosophical content and `EvidMan` for SPARC context.
*   Orchestrator routes modification proposals (KB, System) for approval.

## 5. Philosophy Knowledge Base (KB) - V13 Design

*   **Location:** `philosophy-knowledge-base/` (New top-level directory).
*   **Purpose:** Centralized, structured repository for **philosophical domain knowledge**, distinct from SPARC operational memory. Aims for long-term persistence and potential evolution.
*   **Management:** Exclusively managed via `philosophy-kb-manager` mode.
*   **Initial Structure:** Subdirectories mirroring content types:
    *   `philosophy-knowledge-base/concepts/`
    *   `philosophy-knowledge-base/arguments/`
    *   `philosophy-knowledge-base/quotations/`
    *   `philosophy-knowledge-base/references/` (Includes detailed citation data from text processor)
    *   `philosophy-knowledge-base/questions/` (Includes philosophical inquiry Qs and meta-reflective Qs, distinguished by tags/metadata)
    *   `philosophy-knowledge-base/theses/`
    *   `philosophy-knowledge-base/relationships/` (Explicit links between entries)
    *   `philosophy-knowledge-base/methods/` (Descriptions/critiques of methods used/encountered)
    *   `philosophy-knowledge-base/meta-reflections/` (Outputs from `philosophy-meta-reflector`)
    *   `philosophy-knowledge-base/indices/` (Metadata about processed text chunks from `text-processor`)
*   **Entry Format (Initial - Markdown + YAML):**
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
*   **Self-Modification:**
    *   Modes (esp. `meta-reflector`, `dialectical-analysis`) can propose modifications (e.g., adding relationships, updating method descriptions, correcting concepts).
    *   Proposals are sent to `philosophy-orchestrator`.
    *   Orchestrator presents proposal to User for approval.
    *   If approved, Orchestrator instructs `philosophy-kb-manager` to execute the change.
    *   Changes are logged within the KB entry or a dedicated log.

## 6. Workflow Designs (V13)

### 6.1. Philosophical Inquiry Workflow

1.  **Input:** User prompt for inquiry OR Analysis modes (`pre-lecture`, `class-analysis`, etc.) identify potential questions/concepts during their process.
2.  **Storage (Proto):** Analysis modes send proto-questions/concepts to `philosophy-kb-manager` for storage (tagged appropriately).
3.  **Refinement:** `philosophy-questioning` mode retrieves proto-questions/related concepts from `kb-manager`. It refines questions based on KB context, logical structure, and philosophical relevance.
4.  **Storage (Refined):** `philosophy-questioning` sends refined questions to `kb-manager` for storage/update.
5.  **Thesis Development:** `philosophy-essay-prep`, when tasked with writing an essay, retrieves relevant refined questions and supporting material (concepts, arguments) from `kb-manager`. It develops a thesis statement.
6.  **Storage (Thesis):** `philosophy-essay-prep` sends the developed thesis to `kb-manager` for storage, linked to the relevant question(s).
7.  **Essay Cycle:** The standard essay generation cycle proceeds, using the thesis and querying `kb-manager` for evidence.

### 6.2. System Self-Reflection Workflow

1.  **Trigger:** User explicitly invokes reflection OR `philosophy-orchestrator` detects anomalies (e.g., persistent errors, contradictions flagged by `verification-agent`) OR scheduled task.
2.  **Activation:** Orchestrator delegates to `philosophy-meta-reflector`.
3.  **Analysis:** `meta-reflector` queries `philosophy-evidence-manager` for relevant SPARC Memory Bank logs (active context, feedback, global context). It reads relevant `docs/` (architecture, specs), `.roo/` files (`.clinerules`), and potentially queries `philosophy-kb-manager` for existing meta-reflections or method descriptions.
4.  **Reflection:** Based on analysis and `architecture-questioning.md` principles, `meta-reflector` generates questions and reflections about the system's assumptions, limitations, architecture, mode interactions, potential biases, or methodological blind spots.
5.  **Storage (Reflection):** `meta-reflector` sends generated reflections/questions to `philosophy-kb-manager` for storage in `philosophy-knowledge-base/meta-reflections/` or `philosophy-knowledge-base/questions/` (tagged as 'meta').
6.  **Proposal Generation (Optional):** If analysis suggests specific improvements, `meta-reflector` generates proposals:
    *   *KB Content/Structure Change:* Proposal sent to Orchestrator -> User Approval -> Orchestrator -> `kb-manager`.
    *   *Architectural Change:* Proposal sent to Orchestrator -> User Approval -> Orchestrator -> `architect`.
    *   *Methodological Change/Exploration:* Proposal sent to Orchestrator -> User Approval -> Orchestrator -> `kb-manager` (to update method description) AND/OR `devops`/`architect` (to potentially set up Git branch for exploring alternative system configuration).
7.  **Reporting:** `meta-reflector` reports findings and any proposals made back to the Orchestrator/User.

## 7. Version Control (V13 Refinements)

*   **Primary Scope:** `essay_prep/` remains the primary focus for Git versioning, managed by `philosophy-essay-prep`.
*   **Potential Expansion:**
    *   **KB Versioning:** Consider versioning the `philosophy-knowledge-base/` directory itself using Git, managed perhaps by `philosophy-kb-manager` or `devops` upon approved modifications. This tracks the evolution of the system's understanding.
    *   **System Evolution Branching:** `philosophy-meta-reflector` proposals for significant methodological or architectural shifts could trigger the creation of separate Git branches (managed by `devops`/`architect`) to explore these alternatives without disrupting the main workflow, inspired by `architecture-questioning.md`.
*   **Implementation:** Continue using `execute_command` via relevant modes (`essay-prep`, potentially `kb-manager`, `devops`, `architect`).

## 8. Configuration Structure (V13)

*   **Mode Definition File (`.roo/.roomodes`):** Updated to include `philosophy-kb-manager` and `philosophy-meta-reflector`.
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
      "philosophy-evidence-manager": ".roo/rules-philosophy-evidence-manager/philosophy-evidence-manager.clinerules", // Manages SPARC MB
      "philosophy-kb-manager": ".roo/rules-philosophy-kb-manager/philosophy-kb-manager.clinerules", // Manages Phil KB (New)
      "philosophy-draft-generator": ".roo/rules-philosophy-draft-generator/philosophy-draft-generator.clinerules",
      "philosophy-citation-manager": ".roo/rules-philosophy-citation-manager/philosophy-citation-manager.clinerules",
      "philosophy-verification-agent": ".roo/rules-philosophy-verification-agent/philosophy-verification-agent.clinerules",
      "philosophy-meta-reflector": ".roo/rules-philosophy-meta-reflector/philosophy-meta-reflector.clinerules" // New
      // Add other non-philosophy modes if they exist in the same config
    }
    ```
*   **Rules File Directory Structure:** `.roo/rules-[mode-slug]/[mode-slug].clinerules` (Includes new modes).