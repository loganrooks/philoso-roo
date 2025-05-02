# Hegel Philosophy RooCode Suite - Architecture V15 (Direct KB Access)

**Version:** 1.0
**Date:** 2025-05-02
**Status:** Proposed

## 1. Overview

This document outlines the V15 architecture for the Hegel Philosophy RooCode Suite. This version represents a significant shift from V14, removing the `philosophy-kb-manager` gatekeeper mode and implementing a **Direct Knowledge Base (KB) Access** model. This change addresses user feedback regarding V14's potential inefficiencies and handover complexities [See Decision Log: 2025-05-02 12:46:20].

The core principle of V15 is to empower relevant modes with direct read and controlled write access to the `philosophy-knowledge-base/` directory using standard file system tools (`read_file`, `search_files`, `write_to_file`, `insert_content`). A new `philosophy-kb-doctor` mode is introduced for KB maintenance and integrity checks.

## 2. Goals

*   Improve efficiency by removing the `kb-manager` bottleneck.
*   Reduce handover frequency associated with KB interactions.
*   Simplify the interaction patterns for KB access.
*   Maintain KB organization and integrity through defined write access rules and a dedicated maintenance mode.
*   Ensure modes possess the necessary knowledge to interact directly with the KB structure.

## 3. Key Architectural Changes (V14 -> V15)

*   **Deprecated Mode:** `philosophy-kb-manager` is removed.
*   **Direct KB Read Access:** Modes requiring KB information will read directly from `philosophy-knowledge-base/` using file tools.
*   **Controlled KB Write Access:** Specific modes are granted write permissions to designated subdirectories within `philosophy-knowledge-base/`. Write operations must follow strict conventions defined in mode rules.
*   **New Mode:** `philosophy-kb-doctor` introduced for KB maintenance, indexing, and validation.
*   **Embedded KB Knowledge:** `.clinerules` for relevant modes updated to include detailed knowledge of the KB structure, file formats, and interaction protocols.

## 4. V15 System Diagram

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
        MetaReflector(philosophy-meta-reflector)
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
            style PhilKB fill:#f9f,stroke:#333,stroke-width:2px
            PhilKB[(Philosophy KB<br>philosophy-knowledge-base/)]
            PhilKB --- Concepts(concepts/)
            PhilKB --- Arguments(arguments/)
            PhilKB --- Quotations(quotations/)
            PhilKB --- References(references/)
            PhilKB --- Questions(questions/)
            PhilKB --- Theses(theses/)
            PhilKB --- Relationships(relationships/)
            PhilKB --- Methods(methods/)
            PhilKB --- MetaReflections(meta-reflections/)
            PhilKB --- Indices(indices/)
            PhilKB --- ProcessedTexts(processed_texts/)
            PhilKB --- Analyses(analyses/)
            PhilKB --- Citations(citations/)
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

    %% Direct KB Interactions (Read/Write)
    TextProc -- Write --> ProcessedTexts
    TextProc -- Write --> Indices
    TextProc -- Write --> Citations
    PreLec -- Read/Write --> PhilKB
    ClassAn -- Read/Write --> PhilKB
    SecLit -- Read/Write --> PhilKB
    DialAn -- Read/Write --> PhilKB
    Quest -- Read/Write --> PhilKB
    MetaReflector -- Read/Write --> PhilKB
    EssayPrep -- Read/Write --> PhilKB
    DraftGen -- Read --> PhilKB
    CiteMan -- Read --> PhilKB
    Verify -- Read --> PhilKB

    %% KB Doctor Interactions
    KBDoctor -- Read/Write --> Indices
    KBDoctor -- Read --> PhilKB

    %% Other Interactions
    TextProc -- Processed Chunks --> Workspace
    EssayPrep -- Manage Files --> Workspace
    MetaReflector -- Query MB --> EvidMan
    MetaReflector -- Read Docs/Rules --> Workspace/.roo/docs

    %% SPARC Memory Interactions (Unchanged)
    EvidMan -- Access/Update --> SPARCMB
    Orchestrator -- Use Context --> EvidMan
    TextProc -- Use Context --> EvidMan
    PreLec -- Use Context --> EvidMan
    ClassAn -- Use Context --> EvidMan
    SecLit -- Use Context --> EvidMan
    DialAn -- Use Context --> EvidMan
    Quest -- Use Context --> EvidMan
    EssayPrep -- Use Context --> EvidMan
    DraftGen -- Use Context --> EvidMan
    CiteMan -- Use Context --> EvidMan
    Verify -- Use Context --> EvidMan
    MetaReflector -- Use Context --> EvidMan

    %% Styling
    classDef mode fill:#ccf,stroke:#333,stroke-width:1px;
    class Orchestrator,TextProc,PreLec,ClassAn,SecLit,DialAn,Quest,EssayPrep,DraftGen,CiteMan,Verify,EvidMan,MetaReflector,KBDoctor mode;
    classDef script fill:#f0ad4e,stroke:#333,stroke-width:1px;
    class Scripts script;
    classDef vcs fill:#d9edf7,stroke:#31708f,stroke-width:1px;
    class VCS vcs;
    classDef sparcmb fill:#e0e0e0,stroke:#666,stroke-width:1px;
    class SPARCMB sparcmb;
    classDef kbdir fill:#fffacd,stroke:#8a6d3b,stroke-width:1px,stroke-dasharray: 5 5;
    class Concepts,Arguments,Quotations,References,Questions,Theses,Relationships,Methods,MetaReflections,Indices,ProcessedTexts,Analyses,Citations kbdir;

```

## 5. Knowledge Base Access Patterns (`philosophy-knowledge-base/`)

### 5.1. Base Directory Structure

The `philosophy-knowledge-base/` directory contains subdirectories for different types of knowledge artifacts.

```
philosophy-knowledge-base/
├── analyses/             # Output from analysis modes
├── arguments/            # Structured arguments
├── citations/            # Extracted citation data from sources
├── concepts/             # Definitions and explanations of concepts
├── indices/              # Master index, topic indices, etc. (Managed by kb-doctor)
├── meta-reflections/     # Output from meta-reflector mode
├── methods/              # Descriptions of philosophical methods
├── processed_texts/      # Processed chunks from source texts
├── questions/            # Refined questions from questioning mode
├── quotations/           # Direct quotations from sources
├── references/           # Bibliographic information
├── relationships/        # Links between concepts, arguments, etc.
└── theses/               # Thesis statements from essay-prep mode
```

### 5.2. Read Access

*   **Modes:** `philosophy-pre-lecture`, `philosophy-class-analysis`, `philosophy-secondary-lit`, `philosophy-dialectical-analysis`, `philosophy-questioning`, `philosophy-meta-reflector`, `philosophy-essay-prep`, `philosophy-draft-generator`, `philosophy-citation-manager`, `philosophy-verification-agent`, `philosophy-kb-doctor`.
*   **Mechanism:** Use `read_file` (for specific files) and `search_files` (for pattern matching across files/directories) directly on `philosophy-knowledge-base/` and its subdirectories.
*   **`.clinerules` Requirement:** Must contain knowledge of relevant subdirectories, file naming conventions, and expected content formats (e.g., Markdown with YAML frontmatter) to construct appropriate tool calls. Must specify how to handle file-not-found or search-no-results scenarios.

### 5.3. Write Access

Write access is restricted to specific modes and subdirectories to maintain organization. All write operations must follow strict naming conventions and formatting rules defined within the respective mode's `.clinerules`. Modes should use `write_to_file` (for new files) or `insert_content` / `apply_diff` (for updates, used cautiously).

*   **`philosophy-text-processor`:**
    *   Writes processed text chunks to `processed_texts/` (e.g., `processed_texts/[source_hash]/chunk_[N].md`).
    *   Writes index information to `indices/` (e.g., `indices/[source_hash]_index.md`).
    *   Writes extracted citation data to `citations/` (e.g., `citations/[source_hash]_citations.json`).
*   **Analysis Modes (`pre-lecture`, `class-analysis`, `secondary-lit`, `dialectical-analysis`):**
    *   Write analysis outputs to `analyses/` (e.g., `analyses/[mode_name]_[source_id]_[timestamp].md`).
    *   Write identified concepts to `concepts/` (e.g., `concepts/[concept_slug].md`).
    *   Write identified relationships to `relationships/` (e.g., `relationships/[relationship_type]_[timestamp].md`).
*   **`philosophy-questioning`:**
    *   Writes refined questions to `questions/` (e.g., `questions/question_[timestamp]_[slug].md`).
*   **`philosophy-essay-prep`:**
    *   Writes thesis statements to `theses/` (e.g., `theses/thesis_[essay_topic_slug]_[timestamp].md`).
*   **`philosophy-meta-reflector`:**
    *   Writes meta-reflections to `meta-reflections/` (e.g., `meta-reflections/reflection_[timestamp].md`).
*   **`philosophy-kb-doctor`:**
    *   Writes/updates index files in `indices/` (e.g., `indices/master_index.md`, `indices/topic_index.md`).

## 6. `philosophy-kb-doctor` Mode

*   **Purpose:** Maintain the health, organization, and accessibility of the `philosophy-knowledge-base/`.
*   **Responsibilities:**
    *   **Indexing:** Generate and update master index files (e.g., listing all concepts, arguments, etc.) and potentially topic-based indices within the `indices/` directory.
    *   **Validation:** Check KB structure against defined conventions. Verify internal links within KB files. Identify orphaned or potentially duplicate entries.
    *   **Cleanup (Optional/Future):** Implement rules for archiving or flagging outdated/redundant information.
*   **Triggers:**
    *   Manually invoked by the user.
    *   Scheduled execution triggered by the SPARC orchestrator (e.g., daily, weekly).
    *   Potentially triggered by `philosophy-orchestrator` after major KB updates.
*   **Interaction:** Reads extensively from all KB subdirectories. Writes primarily to the `indices/` subdirectory. Reports findings and potential issues to the user/orchestrator.

## 7. `.clinerules` KB Knowledge Embedding

To enable direct KB access, the `.clinerules` for each mode interacting with the KB must include a dedicated section specifying:

*   **KB Base Path:** `philosophy-knowledge-base/`
*   **Relevant Subdirectories:** List of subdirectories the mode reads from and/or writes to.
*   **File Naming Conventions:** Precise rules for naming files the mode reads or creates (e.g., using slugs, timestamps, source identifiers).
*   **File Format:** Expected structure of KB files (e.g., Markdown with specific YAML frontmatter keys: `id`, `title`, `type`, `tags`, `related_concepts`, `source_ref`).
*   **Interaction Protocols:** Specific instructions on how to use `read_file`, `search_files`, `write_to_file`, `insert_content` for interacting with the KB, including error handling (e.g., file not found). Example: "To retrieve a concept definition, use `read_file` on `philosophy-knowledge-base/concepts/[concept_slug].md`."

## 8. Data Flow Example (Analysis Mode storing a Concept)

1.  `philosophy-dialectical-analysis` identifies a new concept during analysis.
2.  Consults its `.clinerules` for KB write path (`concepts/`) and naming convention (`concept_[concept_slug].md`).
3.  Formats the concept definition in Markdown with required YAML frontmatter.
4.  Uses `write_to_file` to create `philosophy-knowledge-base/concepts/aufhebung.md` (assuming 'aufhebung' is the slug).
5.  Reports success/failure.

## 9. Data Flow Example (Essay Prep retrieving data)

1.  `philosophy-essay-prep` needs arguments related to 'Subjectivity'.
2.  Consults its `.clinerules` for KB read path (`arguments/`, `concepts/`, `relationships/`) and search strategy.
3.  Uses `search_files` with a regex pattern like `'Subjectivity|subjectivity'` on `philosophy-knowledge-base/arguments/` and potentially `philosophy-knowledge-base/concepts/`.
4.  Receives search results (list of matching files and context).
5.  Uses `read_file` on relevant files identified in search results.
6.  Processes the retrieved content.

## 10. Open Questions / Considerations

*   **Concurrency:** Direct file writes from multiple modes could potentially lead to conflicts if not carefully managed by unique naming conventions or locking mechanisms (though file system tools might handle basic locking). The `kb-doctor` can help identify inconsistencies arising from this.
*   **Scalability:** A pure file-based KB might face performance issues with a very large number of files. The `kb-doctor`'s indexing is crucial for mitigation. Future iterations (V16+) might consider migrating to a graph database or other structured storage, using V15's file structure as an intermediate step.
*   **Error Handling:** Mode `.clinerules` must robustly handle errors during file operations (e.g., file not found, permission denied, write failures).