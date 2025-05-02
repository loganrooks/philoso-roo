# Hegel Philosophy RooCode Suite - Architecture V12

**Date:** 2025-05-01
**Version:** 12.0
**Based On:**
*   `architecture_v11.md`
*   `new_requirements_spec_v1.md` (Incorporating `philosophy-text-processor` & Version Control)
*   User Feedback & Memory Bank Context (as of 2025-05-01 19:21)

**Goal:** Define the enhanced architecture for the Hegel Philosophy RooCode Suite, incorporating detailed text processing capabilities and version control, while maintaining focus on improved essay generation, robust reference/citation management, hallucination prevention, optimized knowledge management, and clear orchestration.

## 1. Core Principles (Inherited & Reinforced)

*   **Determinacy:** Concepts and arguments must be clearly defined and differentiated.
*   **Evidence Saturation:** Claims must be rigorously linked to source material via extraction markers (`[[EXTRACT:source_file:start_line-end_line]]`) and structured knowledge base entries.
*   **Chronological Integrity:** Analysis respects the temporal flow of lectures and readings.
*   **Verification Rigor:** Both analysis inputs and generated outputs (essays) undergo verification against the knowledge base and source texts.
*   **Modularity:** Functionality is encapsulated within specialized modes with clear responsibilities.
*   **Orchestration:** Complex workflows are managed by a dedicated orchestrator mode.
*   **Traceability:** Version control provides history and traceability for key artifacts.

## 2. Mode Structure & Responsibilities

The suite comprises refactored analysis modes, new specialized modes for text processing, essay generation, verification, and a central orchestrator.

### 2.1 Knowledge Base Population & Analysis Modes (Refactored & New Processor)

These modes focus on processing source materials and populating the `knowledge_base`.

*   **`philosophy-text-processor` (New/Replaces V11 `text-processing`):**
    *   **Responsibility:** Pre-processes large source texts (books, long essays, lectures) in Markdown format into a structured, indexed, and manageable format. Implemented primarily via **external scripts** orchestrated by the mode.
        *   Accepts path to a single Markdown file.
        *   Performs **recursive splitting** based on header structure (`#`, `##`, etc.), creating a hierarchical directory structure (e.g., `source_materials/processed/[source_id]/level_0/...`) with leaf Markdown files containing text chunks.
        *   Enforces **chunk size constraint** (e.g., < 20,000 tokens), subdividing further if necessary.
        *   Generates **`index.md` files** at each directory level, containing summaries, key concepts, arguments, links, and metadata.
        *   Performs **detailed citation extraction** (cited work, location in citation, location in source chunk, context) for `index.md` files at the deepest levels containing leaf chunks.
        *   Handles potential **formatting corrections** and **header/ToC discrepancies** (potentially via manifest files and script functions).
    *   **Input:** Path to source Markdown file, configuration (token limit, output path).
    *   **Output:** Hierarchical directory structure with processed text chunks (`.md`) and index files (`index.md`) in `source_materials/processed/`. Status updates to Orchestrator. Index/chunk structure information and extracted citation data provided to `philosophy-evidence-manager`.
    *   **Dependencies:** External scripts (e.g., Python) for parsing, splitting, token counting, file I/O.
*   **`philosophy-pre-lecture`:**
    *   **Responsibility:** Analyzes upcoming readings *before* the lecture using processed chunks/indices from `philosophy-evidence-manager`. Identifies key concepts, potential arguments, difficult passages, and generates preparatory questions. Stores findings via `philosophy-evidence-manager`.
    *   **Input:** Pointers to processed readings (via `evidence-manager`).
    *   **Output:** Structured analysis (concepts, arguments, questions) stored in `knowledge_base`. Handoff package for `class-analysis`.
*   **`philosophy-class-analysis`:**
    *   **Responsibility:** Analyzes lecture transcripts in conjunction with pre-lecture analysis and readings (using processed chunks/indices). Identifies core arguments, concept clarifications, connections, and discrepancies. Stores findings via `philosophy-evidence-manager`.
    *   **Input:** Processed transcripts, pre-lecture handoff, relevant processed readings (via `evidence-manager`).
    *   **Output:** Structured analysis (arguments, concept updates, connections) stored in `knowledge_base`. Handoff package.
*   **`philosophy-secondary-lit`:**
    *   **Responsibility:** Analyzes secondary literature (using processed chunks/indices). Identifies interpretations, critiques, comparisons to primary texts, and scholarly context. Stores findings via `philosophy-evidence-manager`.
    *   **Input:** Processed secondary literature texts (via `evidence-manager`).
    *   **Output:** Structured analysis (interpretations, arguments, concepts) stored in `knowledge_base`. Updates `knowledge_base/references/index.md`.
*   **`philosophy-dialectical-analysis`:**
    *   **Responsibility:** Performs deeper analysis focusing on dialectical structures, contradictions, and resolutions within specific arguments or across texts, drawing from the `knowledge_base`. Stores findings via `philosophy-evidence-manager`.
    *   **Input:** Queries to `philosophy-evidence-manager`, specific text segments/indices.
    *   **Output:** Detailed dialectical analyses stored in `knowledge_base/arguments/`.
*   **`philosophy-questioning`:**
    *   **Responsibility:** Generates clarifying questions based on analysis outputs or user prompts, interacts with the `knowledge_base` to identify ambiguities or areas needing further investigation.
    *   **Input:** Analysis outputs, user prompts, queries to `philosophy-evidence-manager`.
    *   **Output:** Questions stored in `knowledge_base/questions/`, potentially triggering further analysis tasks via the orchestrator.

### 2.2 Essay Generation & Verification Modes (New & Refactored)

These modes collaborate under the orchestrator to produce verified, well-cited, and version-controlled essays.

*   **`philosophy-essay-prep` (Refactored):**
    *   **Responsibility:** Manages the high-level essay writing process. Analyzes prompt, develops thesis, creates outline, identifies evidence requirements. Coordinates with `evidence-manager` to gather materials. Triggers other modes for drafting, citation, verification. Handles revisions. **Manages version control (Git) for essay artifacts** within `essay_prep/` using `execute_command` (initiating commits, viewing history, potentially branching).
    *   **Input:** Essay prompt, user guidance, feedback from `verification-agent`.
    *   **Output:** Essay outline, evidence package requests, draft requests, revision requests, final approved essay structure. Manages files and **Git commits** within `essay_prep/[essay_topic]/`.
*   **`philosophy-evidence-manager` (New):**
    *   **Responsibility:** Acts as the sole interface to the `knowledge_base`. Handles querying, retrieving, and formatting structured data (quotations, arguments, concepts, references, **processed text chunk indices/paths**, **extracted citation data**). Handles storing analysis outputs from other modes. Ensures data consistency.
    *   **Input:** Structured queries from other modes, analysis data to be stored.
    *   **Output:** Formatted data packages (e.g., Markdown snippets, JSON objects, file paths) containing requested evidence/metadata. Confirmation of data storage.
*   **`philosophy-draft-generator` (New):**
    *   **Responsibility:** Generates coherent philosophical prose based on an outline and evidence package. Focuses on structuring paragraphs, integrating evidence smoothly (using placeholders for citations), maintaining argumentative flow. **Triggers commit action** via `essay-prep` or `orchestrator` upon draft completion.
    *   **Input:** Detailed outline, evidence package.
    *   **Output:** Draft essay text (Markdown) with evidence integrated and citation placeholders (`[[CITE:ref_key]]`).
*   **`philosophy-citation-manager` (New):**
    *   **Responsibility:** Processes a draft essay with citation placeholders. Retrieves full reference details and **detailed citation location data (from text processor)** from the `knowledge_base` (via `evidence-manager`). Formats and inserts in-text citations and bibliography. **Triggers commit action** via `essay-prep` or `orchestrator`.
    *   **Input:** Draft essay with `[[CITE:ref_key]]` placeholders, citation style guide, access to `knowledge_base`.
    *   **Output:** Essay draft with formatted in-text citations, formatted bibliography.
*   **`philosophy-verification-agent` (New):**
    *   **Responsibility:** Verifies claims and citations within a generated essay draft against the `knowledge_base` and processed source chunks. Checks factual accuracy, unsupported claims, correct attribution, and citation format/accuracy.
    *   **Input:** Essay draft, evidence package used, access to `knowledge_base` (including processed chunk paths/indices).
    *   **Output:** Verification report detailing flagged issues for `essay-prep`.

### 2.3 Orchestration Mode (New)

*   **`philosophy-orchestrator`:**
    *   **Responsibility:** Manages complex, multi-step workflows. Interprets user requests, delegates tasks, manages handoffs, sequences operations. Handles error reporting. **May coordinate Git commits** at key workflow stages (e.g., after successful verification).
    *   **Key Workflows:**
        *   `process_source_text`: User Input (Path) -> `philosophy-text-processor` (Execute Scripts) -> `philosophy-evidence-manager` (Store Index/Refs).
        *   `analyze_material_cycle`: User Input (Source ID) -> (e.g., `pre-lecture` or `secondary-lit` querying `evidence-manager`) -> `evidence-manager` (Store Analysis).
        *   `analyze_lecture_cycle`: User Input (Transcript Path, Source IDs) -> `text-processing` (Transcript) -> `class-analysis` (using pre-lecture handoff & querying `evidence-manager`) -> `evidence-manager` (Store Analysis).
        *   `write_essay_cycle`: User Prompt -> `essay-prep` (Outline/Thesis, **Init Git?**) -> `evidence-manager` (Query KB) -> `draft-generator` (**Commit Draft**) -> `citation-manager` (**Commit Cited Draft**) -> `verification-agent` -> `essay-prep` (Review/Revise based on verification, **Commit Revisions**) -> [Loop if needed] -> Final Output.
    *   **Input:** User commands, handoff packages, verification reports.
    *   **Output:** Task delegations, workflow status updates, final results to user.

## 3. Mode Interaction Diagram (Mermaid)

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

**Diagram Notes:**
*   `philosophy-text-processor` relies on external scripts.
*   `EvidMan` manages access to the `knowledge_base`, which now includes indices, paths, and citation data from the text processor.
*   `EssayPrep` primarily drives Git operations via `execute_command`.
*   `Orchestrator` may coordinate commits at key workflow points.

## 4. Memory Management System: `knowledge_base`

This system centralizes curated knowledge derived from source materials.

*   **Structure:** A dedicated top-level directory `knowledge_base/` containing subdirectories:
    *   `knowledge_base/concepts/`: Definitions, analyses, relationships.
    *   `knowledge_base/arguments/`: Reconstructed arguments, dialectical analyses.
    *   `knowledge_base/quotations/`: Significant quotations linked via extraction markers.
    *   `knowledge_base/references/`: Bibliographic information, source metadata, **extracted citation details** (from `text-processor`). `index.md` tracks sources.
    *   `knowledge_base/questions/`: Generated questions.
    *   `knowledge_base/indices/`: Stores metadata about processed text chunks (paths, summaries, concepts - mirroring `index.md` files generated by `text-processor`) for quick lookups by `evidence-manager`.
*   **Entry Format:** Each entry (Markdown or JSON) includes content, Unique ID, Source Reference Key, Extraction Marker(s), Timestamp, Generating Mode, Tags/Keywords. Citation entries include detailed location info.
*   **Mode Interactions:**
    *   **Write:** Analysis modes and `TextProc` write structured data *only* via `philosophy-evidence-manager`. `TextProc` specifically provides chunk indices/paths and detailed citation data.
    *   **Read/Query:** All modes query *only* via `philosophy-evidence-manager`. `CiteMan` specifically queries for detailed citation data. Analysis modes query for relevant chunks/indices.
    *   **`philosophy-evidence-manager`:** Provides CRUD operations and querying. Manages the link between high-level concepts/arguments and the specific processed text chunks/indices.
*   **Integration:** Complements `analysis_workspace` and `source_materials/processed/`. Extraction markers link KB entries to processed source text chunks.

## 5. Verification Procedures

Verification occurs at multiple levels, focusing on preventing hallucinations and ensuring reference accuracy.

*   **Mechanism 1: Citation Generation & Formatting (`philosophy-citation-manager`)**
    *   Uses `[[CITE:ref_key]]` placeholders.
    *   Retrieves full reference data **and detailed citation location info** from `knowledge_base` via `Evidence Manager`.
    *   Applies citation style rules.
    *   Generates formatted citations and bibliography.
    *   **Accuracy Check:** Ensures `ref_key` exists, data is complete. Flags missing references/data.
*   **Mechanism 2: Essay Draft Verification (`philosophy-verification-agent`)**
    *   **Input:** Essay draft, evidence package, access to `knowledge_base` (including chunk paths/indices).
    *   **Process:**
        1.  **Claim-Evidence Cross-Reference:** Identify evidence for claims. Use extraction markers (via `Evidence Manager`) to locate **processed source text chunks**. Compare claim against source chunk. Flag discrepancies, unsupported claims.
        2.  **Citation Accuracy Check:** Verify citation details against bibliography and `knowledge_base/references/`. Check page numbers/locations against extraction markers and **detailed citation data from text processor**.
        3.  **Quotation Accuracy:** Compare quoted text against source chunk via extraction markers.
    *   **Output:** Detailed verification report for `EssayPrep`.
*   **Workflow for Flagging/Resolving Inaccuracies:** (As per V11, involving `Verification Agent`, `Orchestrator`, `Essay Prep`, potentially `Evidence Manager`, `Draft Generator`, or user). Revisions trigger new **Git commits** managed by `Essay Prep`.

## 6. Configuration Structure

*   **Mode Definition File (`.roo/.roomodes`):** JSON mapping `mode-slug` to `.clinerules` path. Includes all modes (e.g., `philosophy-text-processor`, `philosophy-orchestrator`, etc.).
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
      "philosophy-evidence-manager": ".roo/rules-philosophy-evidence-manager/philosophy-evidence-manager.clinerules",
      "philosophy-draft-generator": ".roo/rules-philosophy-draft-generator/philosophy-draft-generator.clinerules",
      "philosophy-citation-manager": ".roo/rules-philosophy-citation-manager/philosophy-citation-manager.clinerules",
      "philosophy-verification-agent": ".roo/rules-philosophy-verification-agent/philosophy-verification-agent.clinerules"
      // Add other non-philosophy modes if they exist in the same config
    }
    ```
*   **Rules File Directory Structure:** `.roo/rules-[mode-slug]/[mode-slug].clinerules`

## 7. Version Control Integration

*   **Goal:** Manage versions of key project artifacts, primarily essays, using Git.
*   **Mechanism:** Utilize Git via the `execute_command` tool within relevant modes. Assumes Git is installed.
*   **Scope:** Primarily `essay_prep/` directory. Consider for `source_materials/processed/` (if reprocessing occurs) and configuration files (`.clinerules`, `.roomodes`).
*   **Repository Structure:** Recommend a **single Git repository** for the entire workspace initially for simplicity. Initialize if needed.
*   **`.gitignore`:** Maintain a workspace `.gitignore` file to exclude temporary files, logs, potentially large unprocessed source files, etc.
*   **Mode Interactions:**
    *   `philosophy-essay-prep`: Primary driver. Executes `git add`, `git commit -m "..."`, `git log`, `git checkout`, potentially `git branch` commands. Responsible for crafting or prompting for commit messages (AI assistance encouraged).
    *   `philosophy-draft-generator`, `philosophy-citation-manager`: Trigger commit actions via `essay-prep` or `orchestrator` upon completing significant updates.
    *   `philosophy-orchestrator`: May coordinate commits at logical workflow milestones (e.g., post-verification).
*   **User Interaction:** User can request version control actions (view history, checkout specific version) via `orchestrator` or `essay-prep`.
*   **Error Handling:** Modes executing Git commands must handle potential errors (conflicts, etc.), potentially pausing and reporting to the user via the orchestrator or delegating to `debug`.
*   **Security:** Ensure no sensitive information (API keys, etc.) is committed. (Less relevant for this project scope, but good practice).