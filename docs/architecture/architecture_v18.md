# Hegel Philosophy RooCode Suite - Architecture V18.3 (Feedback Integration)

**Date:** 2025-05-07
**Version:** 18.3.7 (Dated Material Integration)
**Status:** Draft
**Based On:**
*   `docs/architecture/architecture_v18.md` (V18.3.1 - Text Processor Workflow Correction)
*   User Feedback (re: Processed Root Index - 2025-05-04 02:09:28)
*   `docs/reviews/text_processing_conflict_analysis_v1.md` (V1.1 - Revised Post-Feedback)
*   Memory Bank Context (as of 2025-05-04) - Note: Refers to `phil-memory-bank/` structure.

**Goal:** Update V18.3.1 architecture to include the root `index.md` within the `source_materials/processed/` directory structure, clarifying its purpose and update mechanism, based on user feedback.

## 1. Core Principles (V18.3)

*   **Determinacy & Specificity:** Concepts/arguments clearly defined within the KB, including positive/negative determination, contrast with ordinary language, and identification of ambiguities. (V11+, Enhanced V18.1)
*   **Evidence Saturation & Rigorous Sourcing:** Claims linked to specific sources via KB entries (`source_ref_keys`, `extraction_markers`). Verification emphasizes source validity and relevance. (V11+, Enhanced V18.1)
*   **Argument Analysis:** Explicit analysis of presuppositions, contradictions, counter-arguments, and relationships between arguments within the KB. (New V18.1)
*   **Contextual Awareness:** Analysis considers related terms, secondary sources, and other philosophers' views via KB links and context tags. (V14+, Enhanced V18.1)
*   **Chronological Integrity:** Analysis respects temporal flow of sources and system operations. (V11+)
*   **Verification Rigor:** Inputs/outputs verified against KB & sources, including checks for rigor elements. (V11+, Enhanced V18.1)
*   **Modularity:** Encapsulated functionality in specialized modes with defined responsibilities. (V11+)
*   **Orchestration:** Complex workflows managed by `philosophy-orchestrator`. (V11+)
*   **Traceability:** Version control (Git) for key artifacts (essays, potentially KB/config). (V12+)
*   **Knowledge Separation (Strict):** Explicit and enforced distinction between philosophical domain knowledge (`philosophy-knowledge-base/`) and operational/process memory (`phil-memory-bank/`). **NO philosophy system interaction with `phil-memory-bank/` for KB operations.** (V13+, Reinforced V18, Renamed V18.2)
*   **Reflexivity:** Capacity for the system to question its own assumptions, methods, and architecture (`philosophy-meta-reflector`). (V13+)
*   **Controlled Evolution:** Mechanisms for proposing and approving modifications to the KB and potentially the system architecture itself. (V13+)
*   **Source Contextualization (Retained V14):** Raw source materials are organized by context (`source_materials/raw/`), and this context is explicitly captured, stored as tags in the KB, and queryable.
*   **Direct KB Read Access (V18):** Modes read data directly from `philosophy-knowledge-base/` using standard file tools (`read_file`, `search_files`), guided by their internal logic and `.clinerules`.
*   **Defined KB Write Patterns (V18, Refined V18.3.1):** Modes that write to the KB do so directly into designated files/sections within `philosophy-knowledge-base/` according to established conventions (e.g., analysis modes write to `concepts/`, `arguments/`, etc.), including rigor-related fields. **Exception:** `philosophy-text-processor` orchestrates an external script; the mode then parses the script's JSON output to perform direct KB writes.
*   **KB Doctor for Maintenance (V18):** A dedicated `philosophy-kb-doctor` mode handles KB maintenance tasks (indexing, validation, cleanup, potentially identifying missing rigor elements) by orchestrating scripts within the KB's `_operational/` directory. It is triggered by the `Orchestrator` and **does not gate** read/write access for other modes.
*   **Direct Operational Context Access (V18.2):** Modes directly read and write operational context (status, logs, decisions) to designated files within the `phil-memory-bank/` directory using standard file tools. `Orchestrator` primarily manages global context files; individual modes manage their specific logs. **Requires diligent logging/reading and detailed delegation messages.**

## 2. V18.3.2 Architecture Overview

V18.3.2 incorporates user feedback regarding the `source_materials/processed/` directory structure within the V18.3.1 framework.

1.  **Direct KB Access:** Modes interact directly with `philosophy-knowledge-base/` using file tools. Read access is open; write access follows conventions and includes rigor fields.
2.  **Direct Operational Context Access:** Modes interact directly with `phil-memory-bank/` using file tools. `Orchestrator` primarily manages global files (`activeContext.md`, `globalContext.md`). Each mode manages its own log file within `phil-memory-bank/mode-specific/`. All modes can read any file in `phil-memory-bank/` for context. **This places higher emphasis on diligent logging/reading practices and detailed delegation messages.**
3.  **KB Doctor (Maintenance & Rigor Support):** `philosophy-kb-doctor` handles maintenance via KB-internal scripts, including potential rigor validation checks. Reports findings to `Orchestrator`. Remains non-gatekeeping.
4.  **Strict KB/Operational Memory Separation:** Maintained between `philosophy-knowledge-base/` and `phil-memory-bank/`.
5.  **Source Context Handling (Retained V14):** Maintained.
6.  **Enhanced KB Schema:** KB entry formats include specific fields for rigor elements (see Section 6).
7.  **Updated Mode Responsibilities:** Analysis, questioning, and verification modes explicitly handle rigor elements (see Section 4). Modes are now also responsible for directly managing their operational context logging within `phil-memory-bank/`.
8.  **Rigor-Aware Workflows:** Analysis and verification workflows include rigor checks and self-correction loops (see Section 7).
9.  **Corrected Text Processing Workflow (V18.3.1):** `philosophy-text-processor` orchestrates `scripts/process_source_text.py`. The script generates hierarchical `index.md` files in `source_materials/processed/[source_id]/...` for navigation AND outputs structured JSON to stdout. The mode parses this JSON and performs direct writes to the KB.
10. **Processed Source Library Index (V18.3.2):** A root `index.md` file exists at `source_materials/processed/index.md`, providing an overview of all processed sources within the library.

## 3. Source Material Organization (V18.3.7 - Dated Material Integration)

*   **Raw Input Location:** `source_materials/raw/`
*   **Purpose:** Centralized location for all original source materials before processing. Provides a clear, machine-parsable structure for determining source context, including dates for course-specific materials.
*   **Structure:** Hierarchical directories define context. Paths use forward slashes (`/`).
    ```
    source_materials/
    ├── raw/
    │   ├── courses/
    │   │   ├── [COURSE_CODE]/        # e.g., PHL316, PHL400
    │   │   │   ├── lectures/         # Lecture transcripts/notes
    │   │   │   │   └── [YYYY-MM-DD_LECTURE_TITLE_SLUG]/
    │   │   │   │       └── [FILENAME.ext]  # e.g., transcript.md, slides.pdf
    │   │   │   ├── readings/         # Assigned readings
    │   │   │   │   └── [YYYY-MM-DD_READING_TITLE_SLUG]/
    │   │   │   │       └── [FILENAME.ext]  # e.g., Hegel_Phenomenology_Preface.pdf
    │   │   │   ├── syllabuses/       # Course syllabuses
    │   │   │   │   └── [SYLLABUS_FILENAME.ext] # e.g., PHL316_Fall2025_Syllabus.pdf
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
    └── processed/                    # Output location for processed chunks & navigational indices
        ├── index.md                  # Root index for the processed library
        ├── courses/
        │   └── [COURSE_CODE]/
        │       ├── index.md          # Course-specific index (lists materials, syllabus link)
        │       ├── lectures/
        │       │   └── [LECTURE_ID]/ # LECTURE_ID incorporates date (e.g., phl316_lec_2025-09-08_hegel_concepts)
        │       │       ├── index.md  # Nav index for this lecture (YAML: lecture_date)
        │       │       └── chunks/
        │       │           └── chunk_XXX.md
        │       ├── readings/
        │       │   └── [READING_ID]/ # READING_ID incorporates date (e.g., phl316_reading_2025-09-08_hegel_phen_preface)
        │       │       ├── index.md  # Nav index for this reading (YAML: assigned_date)
        │       │       └── chunks/
        │       │           └── chunk_XXX.md
        │       └── syllabuses/
        │           └── [SYLLABUS_ID]/ # SYLLABUS_ID incorporates term/year
        │               ├── index.md        # Syllabus metadata (term, year, active status)
        │               └── extracted_data.json # Structured syllabus data
        └── library/                  # For non-course specific processed materials (structure TBD or mirrors V1 generic [source_id])
            └── [SOURCE_ID]/
                ├── index.md
                └── chunks/
                    └── chunk_XXX.md
    ```
*   **Processed Root Index (`source_materials/processed/index.md`):**
    *   **Purpose:** Provides a top-level overview or manifest of all sources that have been processed and are available within the `source_materials/processed/` directory. Helps determine library content and identify potentially missing items.
    *   **Content:** Lists processed `source_id`s, potentially with links to their respective top-level `index.md` files (e.g., `[source_id]/index.md`), timestamps, or status indicators.
    *   **Update Mechanism:** Updated by `philosophy-text-processor` mode after successfully processing a new source and confirming the creation of its hierarchical structure.
*   **Context Extraction:** `philosophy-text-processor` (or a dedicated syllabus processor) MUST parse paths like `source_materials/raw/courses/PHL316/lectures/2025-09-08_hegel_phenomenology_concepts/transcript.md` relative to `source_materials/raw/` to extract:
    *   `context_type`: `course`
    *   `context_id`: `PHL316`
    *   `context_subtype`: `reading`
    These are then formatted as tags: `context:type:course`, `context:id:PHL316`, `context:subtype:reading` for storage in the KB entry YAML.

## 4. Mode Structure & Responsibilities (V18.3.7 - Dated Material Integration)

*   **MCP Integration (V18.3.4):** Modes requiring external data access (e.g., web search, URL fetching) will utilize the Model Context Protocol (MCP). The chosen strategy is **Distributed MCP Calls**, where relevant modes directly invoke MCP tools. This requires strict adherence to standardized call patterns, error handling, and security measures defined in `docs/standards/clinerules_standard_v1.md`. API keys MUST be managed via environment variables accessible only to the MCP servers. See `docs/blueprints/mcp_integration_v1.md` for the detailed strategy and implementation patterns.
### 4.2. Text Processing & Analysis Modes

*   **`philosophy-text-processor` (V18.3.7 Dated Material Handling):**
    *   **Responsibility:** Orchestrates the pre-processing of general source texts (lectures, readings) from `source_materials/raw/` by executing the `scripts/process_source_text.py` script. **Parses dates from raw material paths (e.g., `YYYY-MM-DD` in lecture/reading subdirectories)**. Ensures extracted dates are included in the metadata generated for `master_index.json` and the material's `index.md`. Parses the script's JSON output, performs direct writes to the `philosophy-knowledge-base/`, and updates the root processed library index (`source_materials/processed/index.md`).
    *   **Workflow (Updated for Dated Materials):**
        1.  Receives source file path from `Orchestrator`.
        2.  Parses input path relative to `source_materials/raw/` to extract context (`type`, `id`, `subtype`) **and date information from dated subdirectories for lectures/readings**.
        3.  Executes `scripts/process_source_text.py` via `execute_command`, passing input path, output directory (`source_materials/processed/`), **and extracted date metadata**.
        4.  The script performs hierarchical splitting, chunking, generates navigational `index.md` files (incorporating date into `LECTURE_ID` or `READING_ID` for processed paths and including `lecture_date` or `assigned_date` in YAML frontmatter), and outputs structured JSON to stdout containing metadata (including dates), summaries, concepts, arguments, citations, context tags, and paths to generated files.
        5.  The mode **parses the JSON output** received from the script execution.
        6.  The mode performs **direct writes** to the `philosophy-knowledge-base/` using the parsed JSON data (including date metadata). This aligns with the "Direct KB Write Pattern".
        7.  The mode **updates the root library index** `source_materials/processed/index.md`.
        8.  The mode **directly writes** operational logs to `phil-memory-bank/mode-specific/philosophy-text-processor.md`.
    *   **Dependencies:** `philosophy-orchestrator` (trigger), `scripts/process_source_text.py` (updated for date handling), `execute_command`, File system tools (for KB, `processed/`, and `phil-memory-bank/` access), JSON parsing library.
*   **`philosophy-syllabus-processor` (New V18.3.7 - AI-Driven Parsing):**
    *   **Responsibility:** Processes course syllabuses using AI-driven logic to handle high variability in formatting. Parses syllabus documents (e.g., PDF, Markdown) by leveraging natural language understanding and document structure analysis to extract structured data including weekly schedules, topics, assigned readings, lecture associations, and term dates. Populates `extracted_data.json` within the processed syllabus directory. Attempts to match listed readings/lectures to existing `material_id`s in `master_index.json`. Adds week-specific and topic-specific tags to relevant entries in `master_index.json` and individual material `index.md` files. Proposes updates to `master_index.json` and course-specific `index.md` with syllabus metadata.
    *   **Workflow:**
        1. Receives syllabus file path from `Orchestrator`.
        2. The mode (as an AI agent) directly parses the syllabus content, intelligently handling diverse formats.
        3. Extracts structured data and generates `extracted_data.json`.
        4. Proposes updates to `master_index.json` with syllabus metadata (term dates, active status) and potentially adds/updates tags for associated materials based on syllabus content.
        5. Proposes updates to the course-specific `index.md` in `source_materials/processed/courses/[COURSE_CODE]/`.
        6. Directly writes operational logs.
    *   **Dependencies:** `philosophy-orchestrator` (trigger), `master_index.json`, course/material `index.md` files, File system tools (for reading syllabus and potentially writing `extracted_data.json` or proposing changes).
*   **Analysis Modes (`pre-lecture`, `class-analysis`, `secondary-lit`, `dialectical-analysis`, `questioning`) (V18.3.7 Dated Material Usage):**
    *   **Responsibility:** Analyze sources/KB content, generate concepts, arguments, questions, etc., ensuring philosophical rigor. **Utilize dated materials and syllabus-derived temporal context.** Directly manage own operational logs.
    *   **Interaction (Updated for Dated Materials):**
        *   **Read KB & Syllabus Context:** Directly Read KB files. **Query and utilize `lecture_date` and `assigned_date` metadata from `master_index.json` or individual material `index.md` files.** Access and interpret `extracted_data.json` from processed syllabuses to understand weekly schedules, topic-reading-lecture associations, and overall course progression. Use date/week/topic tags for targeted querying.
        *   **Read Operational Context:** Directly Read relevant files within `phil-memory-bank/` for operational context.
        *   **Analyze for Rigor:** Explicitly identify and analyze determinacy, presuppositions, ambiguities, contradictions, related terms, ordinary language contrast, etc.
        *   **Write KB:** Directly Write findings to designated KB files/sections using file tools, **populating rigor fields** (see Section 6) and ensuring correct formatting and linking (including `source_ref_keys`, `extraction_markers`, `related_ids`).
        *   **Write Operational Log:** Directly Write detailed operational logs (process, decisions, inputs, outputs) to own file in `phil-memory-bank/mode-specific/`.
*   **Cross-Mode Communication Notes (V18.3):**
            *   **Log Discovery:** Modes primarily rely on context provided by `Orchestrator` during delegation. For broader context or historical data, modes can use `search_files` on specific logs within `phil-memory-bank/mode-specific/` or global files (`activeContext.md`, `globalContext.md`), guided by timestamps (e.g., regex `\[2025-05-04 \d{2}:\d{2}:\d{2}\]`) or keywords (e.g., regex `concept_id:\s*hegel_spirit_003`). Effective searching requires clear delegation context and standardized logging.
            *   **Log Standardization:** Mode `.clinerules` MUST define a standardized format for log entries within `phil-memory-bank/mode-specific/`. A recommended baseline includes: `[Timestamp] - [ModeSlug] - [Action/Status] - [Details/Outcome/KB_IDs_Affected]`. This ensures logs are machine-parsable and interpretable by `Orchestrator` and `meta-reflector`.
            *   **KB Write Conflicts (Race Conditions):** Direct KB writes by multiple modes simultaneously carry a risk of race conditions or overwrites.
                *   **Mitigation (Current):** Primarily relies on `Orchestrator` sequencing tasks to minimize simultaneous writes to the *same* KB file/section. Modes should use `apply_diff` where possible for targeted changes rather than `write_to_file`.
                *   **Mitigation (Future):** Consider implementing a simple file-based locking mechanism managed via `phil-memory-bank/status/` or introducing brief, targeted critical sections orchestrated by `Orchestrator` for sensitive KB updates. `KB Doctor` maintenance scripts run during designated low-activity periods or are triggered explicitly by `Orchestrator`.
    *   **Specific Mode Focus (Rigor):**
        *   `class-analysis`: Focus on conceptual determinacy, evidence standards from lectures/readings, identifying potential counter-interpretations.
        *   `dialectical-analysis`: Focus on identifying contradictions, moments, transitions, resolutions, presuppositions within arguments.
        *   `secondary-lit`: Focus on comparing interpretations, identifying secondary source claims/arguments, linking to primary source KB entries.
        *   `questioning`: Refine questions based on identified ambiguities, presuppositions, or gaps in KB rigor.
*   **Example (`dialectical-analysis`):**
            1.  **Input:** `Orchestrator` delegates task: "Analyze KB concept `concept_id: hegel_absolute_knowing_001` for internal contradictions and dialectical movement." Mode reads the concept entry from `philosophy-knowledge-base/concepts/hegel_absolute_knowing_001.md`.
            2.  **Process:**
                *   Reads `positive_determination`: "The unity of subject and object where consciousness knows itself as the totality of reality."
                *   Identifies potential contradiction: The concept implies both a final state ("absolute") and an ongoing process ("knowing").
                *   Searches KB for related arguments/concepts using `related_ids` or tags like `hegel`, `phenomenology`, `knowing`. Finds `argument_id: hegel_phen_ending_arg_005`.
                *   Analyzes how Hegel presents the resolution (e.g., Spirit's self-recognition through its historical manifestations).
                *   Identifies presuppositions: Assumes the validity of the phenomenological journey, assumes Spirit as the ultimate subject.
            3.  **Output (KB Write):** Updates `philosophy-knowledge-base/concepts/hegel_absolute_knowing_001.md` via `apply_diff` or `write_to_file`:
                *   Populates `presuppositions`: ["Validity of phenomenological method", "Spirit as ultimate subject/substance"].
                *   Populates `contradictions`: ["Tension between finality ('absolute') and process ('knowing')"].
                *   Adds analysis of the resolution to the main content body, linking to `argument_id: hegel_phen_ending_arg_005`.
                *   Sets `verification_status: Unverified` (as analysis is new).
            4.  **Output (Operational Log):** Writes detailed log to `phil-memory-bank/mode-specific/philosophy-dialectical-analysis.md`: "[Timestamp] - DialecticalAnalysis - Analyzed concept hegel_absolute_knowing_001. Identified contradiction (finality/process), presuppositions. Linked to arg_005. Updated KB entry."

### 4.3. Essay Generation & Verification Modes

*   **`philosophy-essay-prep` (V11+):**
    *   **Responsibility:** Manages essay writing process, including thesis development and outline, ensuring thesis is determinate and addresses relevant KB context. Manages Git for essays. **Directly manages** own operational logs in `phil-memory-bank/mode-specific/`.
    *   **Interaction (V18.2):** Directly Reads relevant KB entries and operational context from `phil-memory-bank/` using file tools. Directly Writes developed thesis to KB. Coordinates other essay modes. Executes Git commands. Directly Writes operational logs.
*   **`philosophy-draft-generator` (V11+):**
    *   **Responsibility:** Generates prose based on outline and evidence package, aiming for clarity and specificity. **Directly manages** own operational logs in `phil-memory-bank/mode-specific/`.
    *   **Interaction (V18.2):** Directly Reads evidence package from KB and operational context from `phil-memory-bank/` using file tools. Directly Writes operational logs.
*   **`philosophy-citation-manager` (V11+):**
    *   **Responsibility:** Formats citations and bibliography, ensuring accurate linking via `source_ref_keys`. **Directly manages** own operational logs in `phil-memory-bank/mode-specific/`.
    *   **Interaction (V18.2):** Directly Reads reference details from KB and operational context from `phil-memory-bank/` using file tools. Directly Writes operational logs.
*   **`philosophy-verification-agent` (V11+, Enhanced V18.1):**
    *   **Responsibility:** Verifies claims, citations, and **rigor elements** within drafts against KB entries and processed source chunks. Checks for consistency, accurate representation, presence of rigor fields, and handling of counter-arguments. **Directly manages** own operational logs in `phil-memory-bank/mode-specific/`.
    *   **Interaction (V18.2):** Directly Reads draft, KB entries, source chunks, and operational context from `phil-memory-bank/` using file tools. Generates verification reports. Triggers self-correction loop via `Orchestrator`. Directly Writes operational logs.

### 4.4. Orchestration & Meta-Reflection Modes

*   **`philosophy-orchestrator` (V11+, V18.2 Memory Access):**
    *   **Responsibility:** Manages workflows, delegates tasks (providing detailed context), handles handoffs, routes proposals, relays approvals. Coordinates Git commits. **Triggers KB validation/maintenance checks** (e.g., delegating to `meta-reflector` or `verification-agent` based on task). Manages self-correction loops based on validation reports. **Primarily responsible for maintaining global operational context files** (`phil-memory-bank/activeContext.md`, `phil-memory-bank/globalContext.md`). Reads other logs in `phil-memory-bank/` as needed for context.
    *   **Dependencies:** All modes, User, File system tools (for `phil-memory-bank/` access).
*   **`philosophy-meta-reflector` (V13, Context-Aware V14):**
    *   **Responsibility (V18.3.3 Enhanced):** Performs meta-level analysis of the system. This includes:
        *   Evaluating the effectiveness of rigor enforcement across modes and KB entries.
        *   Analyzing operational memory logs (`phil-memory-bank/`), docs, rules, and KB content for patterns, inefficiencies, or contradictions. **Performs KB consistency checks, validation, or cleanup tasks as delegated by `Orchestrator` or based on identified patterns.**
        *   **Evaluating the philosophical quality and progress** of analyses over time (e.g., assessing depth, coherence, handling of counter-arguments, comparison of alternative approaches). Defining/refining metrics for quality assessment is a key task.
        *   Storing meta-reflections, quality assessments, and identified issues/questions in the KB (tagged `meta`).
        *   Proposing KB structure modifications, system architecture changes, or rule updates via `Orchestrator`.
        *   **Directly manages** own operational logs in `phil-memory-bank/mode-specific/philosophy-meta-reflector.md`.
    *   **Interaction (V18.2):** Directly Reads operational context from `phil-memory-bank/`, docs/rules, and KB content using file tools. Directly Writes findings to KB. Sends proposals to `Orchestrator`. Directly Writes operational logs.
    *   **Dependencies:** `philosophy-orchestrator`, File system tools (for KB and `phil-memory-bank/` access), potentially `architect`, `devops`.

### 4.5 Utility & Data Access Modes

*   **`philosophy-evidence-manager` (New V18.3.6):**
    *   **Responsibility:** Retrieves evidence and associated rigor context (source links, extraction markers) directly from the Knowledge Base (`philosophy-knowledge-base/`) based on queries or specific markers. It acts as a specialized data retrieval interface for other modes needing precise information from the KB.
    *   **Interaction (V18.3.6):**
        *   **Read KB:** Directly Reads KB files (`philosophy-knowledge-base/`) using file tools (`read_file`, `search_files`) based on specific queries (ID, marker, keywords).
        *   **Read Operational Context:** Directly Reads relevant files within `phil-memory-bank/` for operational context as needed.
        *   **Output:** Provides structured evidence results (snippets, KB entry IDs, paths, rigor fields) to the requesting mode (typically via `Orchestrator`).
        *   **Write Operational Log:** Directly Writes detailed operational logs (query, results, errors) to its own file in `phil-memory-bank/mode-specific/philosophy-evidence-manager.md`.
    *   **Dependencies:** `philosophy-orchestrator` (for task delegation), File system tools (for KB and `phil-memory-bank/` access).

## 5. V18.3.7 Mode Interaction Diagram (Mermaid - Dated Material Integration)

```mermaid
graph TD
    subgraph User Interaction
        User(User)
    end

    subgraph Orchestration
        Orchestrator(philosophy-orchestrator)
    end

    subgraph Evidence Retrieval %% New Subgraph for clarity
        style EvidSubgraph fill:#f0e68c,stroke:#666,stroke-width:1px
        EvidMan(philosophy-evidence-manager)
        class EvidMan mode;
    end

    %% KB Maintenance & Rigor Validation (Responsibilities moved to Orchestrator/MetaReflector/Verify)
    %% KBDoctor subgraph removed

    subgraph Text & Syllabus Processing
        TextProc(philosophy-text-processor) -- Runs --> ScriptsTP((scripts/process_source_text.py))
        SyllabusProc(philosophy-syllabus-processor)
        class SyllabusProc mode;
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
        subgraph Operational Context [phil-memory-bank/]
             style OpCtx fill:#e0e0e0,stroke:#666,stroke-width:1px
             OpMemBank_Global[(Global Context<br>activeContext.md,<br>globalContext.md)]
             OpMemBank_ModeLogs[(Mode Logs<br>mode-specific/)]
             OpMemBank_Feedback[(Feedback<br>feedback/)]
             Orchestrator -- Manages --> OpMemBank_Global
             %% Individual modes manage their own logs
             TextProc -- Writes --> OpMemBank_ModeLogs
             SyllabusProc -- Writes --> OpMemBank_ModeLogs %% Added
             PreLec -- Writes --> OpMemBank_ModeLogs
             ClassAn -- Writes --> OpMemBank_ModeLogs
             SecLit -- Writes --> OpMemBank_ModeLogs
             DialAn -- Writes --> OpMemBank_ModeLogs
             Quest -- Writes --> OpMemBank_ModeLogs
             EssayPrep -- Writes --> OpMemBank_ModeLogs
             DraftGen -- Writes --> OpMemBank_ModeLogs
             CiteMan -- Writes --> OpMemBank_ModeLogs
             Verify -- Writes --> OpMemBank_ModeLogs
             MetaReflector -- Writes --> OpMemBank_ModeLogs
             EvidMan -- Writes Log --> OpMemBank_ModeLogs
             %% All modes can read all OpCtx files
             Orchestrator -- Reads --> OpMemBank_Global
             Orchestrator -- Reads --> OpMemBank_ModeLogs
             Orchestrator -- Reads --> OpMemBank_Feedback
             TextProc -- Reads --> OpMemBank_Global; TextProc -- Reads --> OpMemBank_ModeLogs
             SyllabusProc -- Reads --> OpMemBank_Global; SyllabusProc -- Reads --> OpMemBank_ModeLogs %% Added
             PreLec -- Reads --> OpMemBank_Global; PreLec -- Reads --> OpMemBank_ModeLogs
             ClassAn -- Reads --> OpMemBank_Global; ClassAn -- Reads --> OpMemBank_ModeLogs
             SecLit -- Reads --> OpMemBank_Global; SecLit -- Reads --> OpMemBank_ModeLogs
             DialAn -- Reads --> OpMemBank_Global; DialAn -- Reads --> OpMemBank_ModeLogs
             Quest -- Reads --> OpMemBank_Global; Quest -- Reads --> OpMemBank_ModeLogs
             EssayPrep -- Reads --> OpMemBank_Global; EssayPrep -- Reads --> OpMemBank_ModeLogs
             DraftGen -- Reads --> OpMemBank_Global; DraftGen -- Reads --> OpMemBank_ModeLogs
             CiteMan -- Reads --> OpMemBank_Global; CiteMan -- Reads --> OpMemBank_ModeLogs
             Verify -- Reads --> OpMemBank_Global; Verify -- Reads --> OpMemBank_ModeLogs
             MetaReflector -- Reads --> OpMemBank_Global; MetaReflector -- Reads --> OpMemBank_ModeLogs; MetaReflector -- Reads --> OpMemBank_Feedback
             EvidMan -- Reads OpCtx --> OpMemBank_Global
        end
        subgraph Philosophical Knowledge Base [Domain Knowledge & Domain Operations]
            style PhilKB fill:#f9f,stroke:#333,stroke-width:2px
            PhilKB_Data[(Philosophy KB Data<br>philosophy-knowledge-base/<br>concepts/, arguments/, etc.<br>+ Rigor Fields, Date Metadata)]
            PhilKB_Ops[(KB Operational<br>philosophy-knowledge-base/_operational/)]

            subgraph KB_Ops_Details ["_operational/"]
                 style KBOps fill:#add8e6,stroke:#00008b,stroke-width:1px,stroke-dasharray: 2 2
                 KB_Indices("indices/")
                 KB_Logs("logs/")
                 KB_Status("status/")
                 KB_Reports("reports/")
                 KB_Scripts("maintenance_scripts/<br>**DEPRECATED**")
            end
            PhilKB_Ops --> KB_Ops_Details
        end
        RawSource[(Raw Source Materials<br>source_materials/raw/<br>(Incl. dated lectures/readings, syllabuses))]
        ProcessedSource[(Processed Source<br>source_materials/processed/<br>(Incl. dated lectures/readings with date metadata, processed syllabuses with extracted_data.json))]
        Workspace(analysis_workspace / essay_prep)
    end

    %% Core Flow & Orchestration
    User -- Request --> Orchestrator
    Orchestrator -- Delegate Tasks --> TextProc
    Orchestrator -- Delegate Syllabus Processing --> SyllabusProc %% Added
    Orchestrator -- Delegate Tasks --> PreLec
    Orchestrator -- Delegate Tasks --> ClassAn
    Orchestrator -- Delegate Tasks --> SecLit
    Orchestrator -- Delegate Tasks --> DialAn
    Orchestrator -- Delegate Tasks --> Quest
    Orchestrator -- Delegate Tasks --> EssayPrep
    Orchestrator -- Delegate Tasks/Trigger --> MetaReflector
    Orchestrator -- Delegate Evidence Retrieval --> EvidMan
    Orchestrator -- Coordinate Commit? --> EssayPrep
    Orchestrator -- Trigger KB Maintenance/Validation --> MetaReflector
    Orchestrator -- Trigger KB Maintenance/Validation --> Verify
    Orchestrator -- Route KB/System Mod Proposal --> User
    Orchestrator -- Relay Approval --> Architect
    Orchestrator -- Relay Approval --> DevOps
    Orchestrator -- Manage Self-Correction Loop --> Verify/MetaReflector/AnalysisModes
    Orchestrator -- Results --> User

    %% Text Processing Flow (V18.3.7 Dated Materials)
    TextProc -- Reads Dated Lectures/Readings --> RawSource
    ScriptsTP -- Generates Dated Hierarchical Indices/Chunks --> ProcessedSource
    ScriptsTP -- JSON Output (incl. dates) --> TextProc
    TextProc -- Parses JSON & Direct Write KB (incl. dates) --> PhilKB_Data
    TextProc -- Updates Root Index --> ProcessedSource

    %% Syllabus Processing Flow (V18.3.7 New)
    SyllabusProc -- Reads Syllabus --> RawSource
    SyllabusProc -- AI Parses Syllabus, Generates extracted_data.json --> ProcessedSource
    SyllabusProc -- Proposes Updates (master_index, course_index, tags) --> PhilKB_Data

    %% Analysis & Inquiry Flow (V18.3.7 Dated Material Usage)
    PreLec -- Direct Write KB (Analysis + Rigor Fields) --> PhilKB_Data
    ClassAn -- Direct Write KB (Analysis + Rigor Fields) --> PhilKB_Data
    SecLit -- Direct Write KB (Analysis + Rigor Fields) --> PhilKB_Data
    DialAn -- Direct Write KB (Analysis + Rigor Fields) --> PhilKB_Data
    Quest -- Direct Write KB (Refined Qs + Rigor Fields) --> PhilKB_Data

    PreLec -- Direct Read KB (incl. Dates, Tags) --> PhilKB_Data
    ClassAn -- Direct Read KB (incl. Dates, Tags) --> PhilKB_Data
    SecLit -- Direct Read KB (incl. Dates, Tags) --> PhilKB_Data
    DialAn -- Direct Read KB (incl. Dates, Tags) --> PhilKB_Data
    Quest -- Direct Read KB (incl. Dates, Tags) --> PhilKB_Data

    PreLec -- Reads Nav Index & Syllabus Data --> ProcessedSource
    ClassAn -- Reads Nav Index & Syllabus Data --> ProcessedSource
    SecLit -- Reads Nav Index & Syllabus Data --> ProcessedSource
    DialAn -- Reads Nav Index & Syllabus Data --> ProcessedSource
    Quest -- Reads Nav Index & Syllabus Data --> ProcessedSource

    %% Essay Flow (V18.2 Direct R/W + Rigor - No change for dated materials directly, but benefits from better KB context)
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

    %% Meta-Reflection Flow (V18.2 Direct R/W)
    MetaReflector -- Direct Read KB --> PhilKB_Data
    MetaReflector -- Direct Read OpCtx --> OpMemBank_Global; MetaReflector -- Direct Read OpCtx --> OpMemBank_ModeLogs; MetaReflector -- Direct Read OpCtx --> OpMemBank_Feedback
    MetaReflector -- Read Docs/Rules --> Workspace/.roo/docs
    MetaReflector -- Direct Write KB (Reflections + Rigor) --> PhilKB_Data
    MetaReflector -- Propose KB Mod --> Orchestrator
    MetaReflector -- Propose Arch Mod --> Orchestrator
    MetaReflector -- Propose Method/Git Mod --> Orchestrator

    %% Evidence Manager Interactions
    EvidMan -- Direct Read KB --> PhilKB_Data

    %% KB Maintenance & Validation Interactions (V18.3.3 - Distributed)
    MetaReflector -- Performs KB Maintenance/Validation --> PhilKB_Data
    MetaReflector -- Performs KB Maintenance/Validation --> PhilKB_Ops
    Verify -- Performs Rigor Validation --> PhilKB_Data

    %% Styling
    classDef kb fill:#f9f,stroke:#333,stroke-width:2px;
    class PhilKB_Data, PhilKB_Ops kb;
    classDef mode fill:#ccf,stroke:#333,stroke-width:1px;
    class Orchestrator,TextProc,PreLec,ClassAn,SecLit,DialAn,Quest,EssayPrep,DraftGen,CiteMan,Verify,MetaReflector,EvidMan mode; %% Added EvidMan
    classDef script fill:#f0ad4e,stroke:#333,stroke-width:1px;
    class Scripts script;
    classDef vcs fill:#d9edf7,stroke:#31708f,stroke-width:1px;
    class VCS vcs;
    classDef opmembank fill:#e0e0e0,stroke:#666,stroke-width:1px;
    class OpMemBank_Global, OpMemBank_ModeLogs, OpMemBank_Feedback opmembank;
    classDef source fill:#dff0d8,stroke:#3c763d,stroke-width:1px;
    class RawSource,ProcessedSource source;
    classDef kbops fill:#add8e6,stroke:#00008b,stroke-width:1px,stroke-dasharray: 2 2;
    class KB_Indices,KB_Logs,KB_Status,KB_Reports kbops;
    classDef evidsubgraph fill:#f0e68c,stroke:#666,stroke-width:1px; %% Style for EvidMan subgraph
    class EvidSubgraph evidsubgraph;
```

**Diagram Notes:**
*   Reflects V18.3.7: Dated Material Integration.
*   Added `philosophy-syllabus-processor` (SyllabusProc) and its interactions.
*   Updated `TextProc` interactions for dated lectures/readings.
*   Analysis modes now show interaction with `ProcessedSource` for syllabus data and dated material indices.
*   Updated data layer node descriptions for clarity on dated content.
*   V18.3.6 (EvidMan) and other V18.3.x elements remain.

## 6. Philosophy Knowledge Base (KB) - V18.3.7 Design (Dated Material Context)

*   **Location:** `philosophy-knowledge-base/`
*   **Purpose:** Centralized, structured, persistent repository for **philosophical domain knowledge**, distinct from operational memory (`phil-memory-bank/`). Enhanced for philosophical rigor.
*   **Management (V18.1):**
    *   **Content:** Managed directly by relevant modes using file tools, following defined write patterns/locations and **populating rigor-related fields**. `philosophy-text-processor` writes data parsed from script JSON output.
    *   **Maintenance & Rigor Validation:** KB validation (schema checks, link integrity, rigor consistency) is performed by `verification-agent` during workflows and `meta-reflector` during periodic analysis or specific checks triggered by `Orchestrator`. Cleanup/indexing tasks are handled by `meta-reflector` or dedicated logic within modes as needed. The `_operational/` directory structure is retained for logs, status, reports, and rules generated/used by these modes.
*   **Structure:** Subdirectories based on content type, plus operational directories:
    *   `concepts/`, `arguments/`, `quotations/`, `references/`, `questions/`, `theses/`, `relationships/`, `methods/`, `meta-reflections/`, `indices/`, `processed_texts/` (or similar - holds data derived from text processor JSON)
    *   `_operational/`
        *   `logs/` (Logs from maintenance/validation scripts)
        *   `status/` (Status files for maintenance/validation tasks)
        *   `reports/` (Reports from KB Doctor/scripts, incl. rigor validation summaries)
        *   `maintenance_scripts/` (**DEPRECATED** - Functionality moved to modes like `meta-reflector`, `verification-agent`)
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
            # Temporal Tags (Added by syllabus/text processor for dated materials):
            "[COURSE_CODE]_Week_[N]", "[COURSE_CODE]_Topic_[TOPIC_SLUG]", "date_YYYY-MM-DD", ...
          ]
          # Note: Date-specific metadata for lectures/readings (lecture_date, assigned_date) is primarily stored in the
          #       corresponding processed material's index.md and master_index.json. KB entries derive temporal
          #       context through these tags and their link to the source material via source_ref_keys/extraction_markers.

    # --- Linking & Source Fields (V11+, Emphasized V18.1) ---
    source_ref_keys: [[ref_key_1, ...]] # CRITICAL: Links to `Reference` type KB entries. Each `Reference` entry contains metadata about an original source text, including the unique `source_id` used in `source_materials/processed/[source_id]/`. This identifies the overall source document(s).
    extraction_markers: [[marker_1, ...]] # CRITICAL: Pinpoints the specific location(s) within the processed source text from which this KB entry's content derives. Works *with* `source_ref_keys`. Markers should reference specific chunk files (e.g., `[source_id]/level_1/chunk_005.md`) and potentially finer-grained details like paragraph/section IDs or character offsets if provided by the text processing script's JSON output. Enables precise verification and traceability.
    related_ids: [[id_1, ...]] # General links to other KB entries (concepts, arguments, etc.).

    # --- Type-Specific Fields ---
    # (Examples: definition, premises, conclusion, question_text, thesis_statement, reflection_summary, method_description, index_path, chunk_summary, etc.)
    ---

    # Main Content (Markdown)
    [Detailed description, analysis, text, etc. reflecting rigor elements.]
    ```
*   **Self-Modification:** Proposals -> `Orchestrator` -> User Approval -> `Orchestrator` -> Implementation by modes/scripts.
### 6.1 Knowledge Evolution & Conflict Resolution (V18.3 Enhancements)

Addressing the dynamic nature of philosophical interpretation requires specific mechanisms:

*   **Competing Interpretations:**
    *   **Mechanism:** Competing interpretations of the same concept (e.g., different readings of Hegel's 'Being') should ideally be stored as separate KB entries (e.g., `hegel_being_interpretation_pippin_001`, `hegel_being_interpretation_taylor_001`).
    *   **Linking:** These entries MUST be linked using the `related_ids` field, potentially with a specific relationship type tag (e.g., `relation:competing_interpretation`).
    *   **Attribution:** The `generating_mode` and potentially `source_ref_keys` (if derived from secondary lit) are crucial for tracking the origin of each interpretation.
    *   **Analysis:** Modes like `secondary-lit` or `dialectical-analysis` are responsible for identifying and linking these competing views.

*   **Contradiction Resolution:**
    *   **Detection:** Contradictions can be identified by analysis modes (within a text/argument) or `verification-agent` (between KB entries or KB and draft). Identified contradictions should be noted in the `contradictions` field of relevant KB entries and flagged in `verification_notes`.
    *   **Process:**
        1.  `Verification-Agent` or analysis mode reports contradiction to `Orchestrator` via logs/status updates.
        2.  `Orchestrator` logs the issue in `phil-memory-bank/activeContext.md` and potentially `globalContext.md` (Decision Log if systemic).
        3.  `Orchestrator` delegates resolution task, potentially to:
            *   `dialectical-analysis`: To analyze the nature of the contradiction.
            *   `meta-reflector`: If the contradiction suggests a systemic issue or rule conflict.
            *   `questioning`: To formulate clarification questions for the user.
        4.  Resolution might involve:
            *   Refining KB entries to clarify scope/context.
            *   Creating new entries representing a synthesis or higher-level concept.
            *   Marking an interpretation as disputed (`verification_status: Disputed`).
            *   Presenting the contradiction and potential resolutions to the user for guidance via `Orchestrator`.

*   **Concept Versioning:**
    *   **Current:** File-level history is provided by Git (managed via `philosophy-essay-prep` for essays, potentially manually or via `devops` for KB/config). The `timestamp` field in KB entries provides last-modified information.
    *   **Future Considerations:** For more granular tracking, future versions might incorporate:
        *   A dedicated `version_history` field within KB entries, logging significant changes with timestamps and mode attribution.
        *   Separate `history/` subdirectory in the KB to store previous versions of entries, linked by ID. This would require more complex management by `kb-doctor` or dedicated scripts.

## 7. Workflow Designs (V18.3.2 - Processed Root Index Update)

### 7.1. Philosophical Inquiry & Analysis Workflow (Context-Aware, Direct Access, Rigor Focused)

1.  **Input:** User prompt OR Analysis modes identify potential questions/concepts from source material (processed by `text-processor`).
2.  **Context Gathering:** Analysis modes **directly read** relevant operational context from `phil-memory-bank/` (e.g., `activeContext.md`, previous logs).
3.  **Analysis & Rigor Check:** Analysis modes **directly read** source chunks (potentially located via `source_materials/processed/index.md` files, including the root index) and/or related KB entries. They analyze content, explicitly identifying/documenting **rigor elements**.
4.  **Storage (Analysis + Rigor):** Analysis modes **directly write** findings to KB, **populating rigor fields** and ensuring links.
5.  **Logging:** Analysis modes **directly write** detailed operational logs to their specific file in `phil-memory-bank/mode-specific/`.
6.  **Refinement:** `philosophy-questioning` reads KB and `phil-memory-bank/` context, refines questions.
*   **(MCP Integration):** If source material is external (e.g., web article, online database), the responsible mode (e.g., `pre-lecture`, `secondary-lit`) uses MCP tools (`fetcher`, `brave-search`, etc.) to retrieve it, following the patterns defined in `docs/blueprints/mcp_integration_v1.md`.
7.  **Storage (Refined Qs + Rigor):** `philosophy-questioning` writes refined questions to KB and logs to `phil-memory-bank/`.
8.  **Thesis Development:** `philosophy-essay-prep` reads KB and `phil-memory-bank/` context, develops thesis.
9.  **Storage (Thesis + Rigor):** `philosophy-essay-prep` writes thesis to KB and logs to `phil-memory-bank/`.
10. **Essay Cycle:** Essay modes read KB/`phil-memory-bank/` context and write logs.
*   **Example Workflow:**
    1.  **User Prompt:** "How does Hegel's concept of 'Spirit' differ from Kant's transcendental subject?"
    2.  **Orchestrator:** Receives prompt. Creates initial context entry in `phil-memory-bank/activeContext.md`: "[Timestamp] - Orchestrator - Received user query re: Hegel's Spirit vs Kant's Subject. Delegating to class-analysis." Delegates task to `class-analysis`.
    3.  **Class Analysis (Context):** Reads task from `Orchestrator`. Reads `phil-memory-bank/activeContext.md` for current focus. May read `source_materials/processed/index.md` to see available processed sources.
    4.  **Class Analysis (KB Read):** Uses `search_files` on `philosophy-knowledge-base/concepts/` with regex for "Hegel" AND "Spirit" AND "Kant" AND "Subject". Finds existing entries `concept_id: hegel_spirit_003` and `concept_id: kant_transcendental_subject_001`. Reads these files.
    5.  **Class Analysis (Analysis & Rigor):** Compares the `positive_determination` and `negative_determination` fields. Notes `hegel_spirit_003` lacks `ordinary_language_contrast`. Identifies potential ambiguity: "Spirit" used differently in *Phenomenology* vs. *Encyclopedia*. Searches KB for related context tags (`context:id:PHL316`, `context:subtype:reading`). Finds related arguments about historical development vs. logical structure.
    6.  **Class Analysis (KB Write):** Updates `philosophy-knowledge-base/concepts/hegel_spirit_003.md`:
        *   Adds to `ambiguities`: "Term 'Spirit' has distinct nuances in Phenomenology (historical journey) vs. Encyclopedia (logical system)."
        *   Adds `ordinary_language_contrast`: "Differs from common usage implying ghost or soul; for Hegel, it's collective, self-knowing reason."
        *   Adds `related_ids` linking to the relevant arguments found.
        *   Sets `verification_status: Unverified`.
    7.  **Class Analysis (Logging):** Writes log to `phil-memory-bank/mode-specific/philosophy-class-analysis.md`: "[Timestamp] - ClassAnalysis - Compared Hegel/Spirit vs Kant/Subject. Updated hegel_spirit_003 with ambiguity (Phenom vs Encyc), ordinary language contrast, related args. Status Unverified."
    8.  **Orchestrator:** Receives completion signal (or delegates further, e.g., to `verification-agent` if required by rules). Updates `phil-memory-bank/activeContext.md`. Presents summary/updated concept to user or next mode.
*   **Failure Handling Notes (V18.3):**
    *   **Source Contradiction:** If `text-processor` (via script) or analysis modes detect contradictions *within* a source text, this should be flagged in the KB entry's `ambiguities` or a dedicated `source_issues` field, and potentially reported to `Orchestrator` for user notification or `meta-reflector` analysis.
    *   **Mode Failure:** If an analysis mode fails (e.g., cannot parse input, hits resource limits), it MUST log the failure state clearly in its `phil-memory-bank/mode-specific/` log, **including the error message, the attempted action, relevant input data (e.g., KB IDs), and current operational context**. It must also report failure status to `Orchestrator`. `Orchestrator` then decides whether to retry, delegate to a different mode (e.g., `meta-reflector` to analyze the failure), or query the user.

### 7.2. Verification Workflow (Rigor Focused)

1.  **Trigger:** `EssayPrep` requests verification.
2.  **Activation:** `Orchestrator` delegates to `philosophy-verification-agent`.
3.  **Context Gathering:** `verification-agent` **directly reads** relevant operational context from `phil-memory-bank/`.
4.  **Evidence Gathering:** `verification-agent` **directly reads** draft, KB entries, and source chunks (potentially located via `source_materials/processed/index.md`).
5.  **Verification & Rigor Check:** `verification-agent` compares claim against evidence and **explicitly verifies rigor elements**.
6.  **Reporting:** `verification-agent` generates report, updates KB verification status.
7.  **Logging:** `verification-agent` **directly writes** detailed logs to `phil-memory-bank/mode-specific/`.
*   **Example Workflow:**
    1.  **Trigger:** `EssayPrep` completes draft section, requests verification via `Orchestrator`.
    2.  **Orchestrator:** Delegates task: "Verify claims and rigor in `essay_prep/drafts/Hegel-Being-Nothing_draft_v1_section1.md` against KB." Updates `phil-memory-bank/activeContext.md`.
    3.  **Verification Agent (Context):** Reads task. Reads `phil-memory-bank/activeContext.md`.
    4.  **Verification Agent (Evidence):** Reads `essay_prep/drafts/Hegel-Being-Nothing_draft_v1_section1.md`. Identifies claim: "Hegel's 'Being' is initially presented as pure indeterminacy." Finds citation marker linking to `source_ref_key: hegel_sol_pp59_82_chunk_002`.
    5.  **Verification Agent (KB Read):** Reads KB entry for `source_ref_key: hegel_sol_pp59_82_chunk_002`. Reads related concept `concept_id: hegel_being_001`.
    6.  **Verification Agent (Verification & Rigor Check):**
        *   Confirms chunk text supports "pure indeterminacy".
        *   Checks `concept_id: hegel_being_001` for rigor fields: Finds `positive_determination` ("Pure, unmediated immediacy"), `negative_determination` ("Not yet differentiated, not Nothing"), but `presuppositions` is empty.
    7.  **Verification Agent (Reporting):** Generates report: "Claim verified against source chunk. Rigor Check: Concept `hegel_being_001` is missing `presuppositions` field." Updates `verification_status` in `concept_id: hegel_being_001` to `Verified` but adds note to `verification_notes`: "Rigor field 'presuppositions' is missing."
    8.  **Verification Agent (Logging):** Writes log to `phil-memory-bank/mode-specific/philosophy-verification-agent.md`: "[Timestamp] - VerificationAgent - Verified claim re: Being/indeterminacy in draft section 1. Source match OK. Rigor issue: concept hegel_being_001 missing presuppositions. Reported to Orchestrator."
    9.  **Orchestrator Action:** Receives report. Reads log. Updates `phil-memory-bank/activeContext.md`: "[Timestamp] - Orchestrator - Verification report received for draft sec 1. Rigor issue found (concept hegel_being_001 missing presuppositions). Delegating correction to dialectical-analysis." Delegates task to `dialectical-analysis` to populate the missing field.
8.  **Correction Loop Trigger:** If issues found, notifies `Orchestrator`.
9.  **Orchestrator Action:** `Orchestrator` reads `verification-agent` log from `phil-memory-bank/`, initiates correction loop (delegating back to analysis/essay modes), potentially triggers `KBDoctor`. Updates `phil-memory-bank/activeContext.md`.
*   **Failure Handling Notes (V18.3):**
    *   **Verification Failure:** If `verification-agent` cannot verify a claim (no supporting evidence found, evidence contradicts claim), it MUST:
        1.  Mark the claim as `Disputed` in its report.
        2.  Update the relevant KB entry's `verification_status` to `Disputed` and add details to `verification_notes`.
        3.  Clearly log the failure and reason in its `phil-memory-bank/mode-specific/` log, **including the specific claim, the KB entry/source chunk checked, the reason for dispute, and relevant context**.
        4.  Report the failure to `Orchestrator`.
        5.  `Orchestrator` then initiates a correction loop, potentially involving `questioning` (to ask user for clarification/alternative sources), `dialectical-analysis` (to re-evaluate the claim/evidence), or `essay-prep` (to revise the draft).

### 7.3. System Self-Reflection Workflow (Context-Aware, Direct Access)

1.  **Trigger:** User, Anomaly Detection, Schedule.
2.  **Activation:** `Orchestrator` delegates to `philosophy-meta-reflector`.
3.  **Analysis & Evaluation (V18.3 Enhanced):** `meta-reflector` **directly reads** operational context from `phil-memory-bank/`, docs/rules, and KB content. Performs analysis including:
    *   Evaluating system performance and rigor consistency across workflows.
    *   Assessing philosophical quality of recent KB entries/analyses against defined metrics (e.g., depth, clarity, handling of counter-arguments).
    *   Comparing different approaches taken for similar philosophical questions (if data exists).
    *   Identifying patterns of failure, success, or inefficiency.
4.  **Reflection:** `meta-reflector` generates meta-reflections/questions.
5.  **Storage (Reflection):** `meta-reflector` **directly writes** findings to KB (tagged `meta`).
6.  **Logging:** `meta-reflector` **directly writes** detailed logs to `phil-memory-bank/mode-specific/`.
7.  **Proposal Generation (Optional):** `meta-reflector` formulates proposals.
8.  **Proposal Routing/Approval:** Proposals -> `Orchestrator` -> User -> `Orchestrator` -> Implementation. `Orchestrator` logs decision in `phil-memory-bank/globalContext.md`.
9.  **Reporting:** `meta-reflector` reports to `Orchestrator`/User.
*   **Example Workflow:**
    1.  **Trigger:** `Orchestrator` detects repeated `verification-agent` reports about missing `negative_determination` fields in `Concept` entries over the past week (by reading `phil-memory-bank/mode-specific/philosophy-verification-agent.md` and `phil-memory-bank/activeContext.md`).
    2.  **Activation:** `Orchestrator` delegates task: "Analyze pattern of missing 'negative_determination' fields. Evaluate relevant mode rules and propose solution." Updates `phil-memory-bank/activeContext.md`.
    3.  **Meta-Reflector (Analysis):** Reads task. Reads `phil-memory-bank/activeContext.md`, `phil-memory-bank/mode-specific/philosophy-verification-agent.md`, and potentially logs from analysis modes (`class-analysis`, `dialectical-analysis`). Reads `.clinerules` for analysis modes. Reads KB entries tagged `meta` related to rigor.
    4.  **Meta-Reflector (Reflection):** Identifies that analysis modes' rules don't explicitly mandate *generating* `negative_determination` during initial concept creation, only verifying its presence later. Notes a potential inefficiency.
    5.  **Meta-Reflector (Storage):** Writes reflection to KB: `meta_reflection_id: rigor_gap_neg_determination_001`, type `Meta-Reflection`, tagged `meta`, `rigor`, `workflow_inefficiency`. Content: "Analysis modes lack explicit rule to generate negative_determination, leading to downstream verification failures. Suggest rule update."
    6.  **Meta-Reflector (Logging):** Writes log to `phil-memory-bank/mode-specific/philosophy-meta-reflector.md`: "[Timestamp] - MetaReflector - Analyzed missing negative_determination pattern. Root cause: rule gap in analysis modes. Stored reflection rigor_gap_neg_determination_001. Proposing rule update."
    7.  **Meta-Reflector (Proposal):** Formulates proposal: "Update `.clinerules` for `class-analysis` and `dialectical-analysis` to mandate generation of `negative_determination` field during concept creation." Sends proposal to `Orchestrator`.
    8.  **Orchestrator Action:** Receives proposal. Routes to User for approval. Logs proposal in `phil-memory-bank/globalContext.md` (Decision Log). If approved, delegates implementation task (e.g., to `architect` or `devops` depending on permissions/setup).
*   **Failure Handling Notes (V18.3):**
    *   **Analysis Failure:** If `meta-reflector` fails to analyze logs or rules (e.g., due to parsing errors, excessive data volume), it MUST log the specific error clearly in its `phil-memory-bank/mode-specific/` log, **including the attempted analysis task, the target files/data, the error encountered, and relevant context**. It must also report the failure to `Orchestrator`. `Orchestrator` might delegate to `devops` (for resource issues) or `architect` (to simplify logging/rule formats), or notify the user.
    *   **Proposal Rejection:** If a user rejects a proposal generated by `meta-reflector`, `Orchestrator` logs the rejection in `phil-memory-bank/globalContext.md` (Decision Log) and informs `meta-reflector`. `meta-reflector` may then attempt to refine the proposal based on feedback (if provided) or abandon that line of inquiry.
### 7.4 User Interaction Patterns (V18.3)

Clarifying user interaction loops:

*   **User Feedback on Analysis:**
    1.  `Orchestrator` presents completed analysis (e.g., a generated concept, argument summary) to the User.
    2.  User provides feedback (e.g., "This interpretation seems incomplete," "Consider also Author X's view").
    3.  `Orchestrator` logs feedback in `phil-memory-bank/feedback/` (relevant mode file and potentially global feedback).
    4.  `Orchestrator` delegates a refinement task back to the relevant analysis mode (e.g., `secondary-lit`, `dialectical-analysis`), providing the original analysis ID and the user feedback as context.
    5.  Analysis mode reads context, refines KB entry, logs changes, and reports completion to `Orchestrator`.

*   **User Intervention in Workflow:**
    1.  User observes an ongoing process (via `activeContext.md` or mode logs) and wishes to intervene (e.g., "Stop the essay generation, I want to change the thesis").
    2.  User sends intervention command to `Orchestrator`.
    3.  `Orchestrator` MUST attempt to gracefully halt the relevant mode(s) (mechanism TBD - could involve signaling or relying on modes checking for halt commands periodically).
    4.  `Orchestrator` logs the intervention and workflow state in `phil-memory-bank/activeContext.md` and `feedback/`.
    5.  `Orchestrator` awaits further user instructions (e.g., new thesis direction).

*   **Handling Ambiguous User Queries:**
    1.  User provides an ambiguous query (e.g., "Tell me about Hegel and negativity").
    2.  `Orchestrator` delegates initial interpretation/scoping to `questioning` mode.
    3.  `Questioning` mode analyzes the query, searches KB for related concepts (`negativity`, `nothing`, `dialectic`, etc.), identifies potential ambiguities (e.g., "Negativity in which work? Logic? Phenomenology?").
    4.  `Questioning` mode formulates clarification questions with suggested options (using `ask_followup_question` tool via `Orchestrator`). Example: "Your query about 'Hegel and negativity' is broad. Could you specify which context you're interested in? <suggest>Negativity in the Science of Logic</suggest> <suggest>Negativity in the Phenomenology</suggest> <suggest>General overview</suggest>"
    5.  `Orchestrator` presents the question to the user.
    6.  User selects an option or provides clarification.
    7.  `Orchestrator` receives clarification and delegates a more focused task to the appropriate analysis mode.

### 7.5 Handling Missing or Incomplete Source Materials (V18.3.7)

The system must gracefully handle scenarios where expected source materials (e.g., a lecture transcript listed in a syllabus) are missing or incomplete.

*   **Identification:**
    *   The `philosophy-syllabus-processor`, through its `extracted_data.json`, provides a list of expected materials for a course, including lectures and readings associated with specific dates or topics.
    *   When the `philosophy-orchestrator` or an analysis mode (e.g., `philosophy-class-analysis`) attempts to retrieve a specific material (e.g., a lecture for a given date) based on the syllabus schedule, it will check `master_index.json` and the `source_materials/processed/` directory.
    *   If the material is not found, it's flagged as missing.

*   **Logging and Reporting:**
    *   The mode that identifies the missing material MUST log this event in its specific operational log within `phil-memory-bank/mode-specific/`.
    *   The `philosophy-orchestrator` should be informed (e.g., if a delegated task to process a specific lecture fails due to missing input) and should log this in `globalContext.md` (e.g., under a "Data Integrity Issues" or "Progress" section) and `activeContext.md`.
    *   The system may, as a future enhancement, provide a consolidated report of missing expected materials to the user.

*   **Workflow Adaptation (Detailed Alternative):**
    *   **`philosophy-orchestrator`**:
        *   Upon identifying a missing lecture transcript (expected from syllabus), the orchestrator logs the issue.
        *   It may trigger a sub-workflow to find alternative materials:
            *   Instruct `philosophy-text-processor` to check for and process any available raw class notes or lecture slides for the corresponding date/topic from `source_materials/raw/courses/[COURSE_CODE]/lectures/[YYYY-MM-DD_LECTURE_TITLE_SLUG]/notes/` or `slides/`.
            *   Instruct `philosophy-secondary-lit` to find or acquire relevant secondary literature (see below).
        *   It will adapt the main workflow:
            *   Skip tasks directly dependent on the full transcript (e.g., detailed lecture summarization).
            *   Prioritize analysis of assigned readings, available notes/slides, and supplementary secondary literature.
        *   Clearly logs all deviations and alternative steps taken.
    *   **Analysis Modes (e.g., `philosophy-class-analysis`, `philosophy-pre-lecture`):**
        *   If an expected lecture transcript is missing, these modes will:
            1.  Utilize any processed class notes or lecture slides for that date/topic.
            2.  Place greater emphasis on the pre-lecture analysis of assigned readings.
            3.  Actively incorporate analysis from relevant secondary literature (see "Proactive Secondary Literature Acquisition" below).
            4.  Explicitly state in their outputs (KB entries, reports) that the analysis is modified due to the missing transcript and specify the alternative materials used.
    *   **`philosophy-secondary-lit` (Enhanced Role for Missing Transcripts):**
        *   **Proactive Secondary Literature Acquisition:**
            1.  If a lecture transcript is missing, `philosophy-orchestrator` or `philosophy-class-analysis` can task `philosophy-secondary-lit` to find/acquire supplementary materials.
            2.  `philosophy-secondary-lit` first searches the existing `philosophy-knowledge-base/` for relevant processed secondary sources related to the primary readings or topic of the missing lecture.
            3.  If insufficient, it uses the `zlibrary-mcp` tool (via `use_mcp_tool` with `search_books` or `full_text_search`) to find relevant academic commentaries or secondary analyses on the primary readings for that week.
            4.  If suitable texts are found, it uses `zlibrary-mcp`'s `download_book_to_file` tool to download them to a designated subdirectory in `source_materials/raw/external_lit/secondary/` (e.g., `source_materials/raw/external_lit/secondary/commentaries_on_hegel_phenomenology/`).
            5.  It then informs `philosophy-orchestrator` of the newly downloaded raw material.
            6.  `philosophy-orchestrator` delegates processing of this new raw material to `philosophy-text-processor`.
            7.  Once processed, this new secondary literature becomes available for `philosophy-class-analysis` and other modes to use in lieu of or to supplement the missing lecture content.
    *   **Downstream Modes (e.g., `philosophy-draft-generator`):** These modes will consume the KB as is. The KB will reflect the alternative analysis based on readings, notes/slides, and supplementary secondary literature if the primary lecture transcript was missing.

*   **Handling Lecture Slides/Notes (as part of the alternative workflow):**
    *   As mentioned above, if lecture slides or instructor notes are available in `source_materials/raw/courses/[COURSE_CODE]/lectures/[YYYY-MM-DD_LECTURE_TITLE_SLUG]/` (e.g., in subfolders like `slides/` or `notes/`), `philosophy-text-processor` will process them.
    *   These processed materials (with their own `MATERIAL_ID`s) will be linked to the lecture date/topic, ideally via the syllabus `extracted_data.json` or by `philosophy-orchestrator` / analysis modes.
    *   Analysis modes will then use these as primary sources of information about the lecture if the transcript is absent.

*   **Data Integrity Principle:** The system prioritizes proceeding with available information while clearly flagging and logging any missing expected data to ensure transparency and manage expectations about the completeness of analyses or generated content.
## 8. Version Control & Release Strategy (V18.3.4)

*   **Tool:** Git, managed via `execute_command`.
*   **Primary Scope:** `essay_prep/` directory managed by `philosophy-essay-prep` mode for essay drafts and related artifacts.
*   **Branching Strategy:**
    *   **`main`:** Represents the stable, production-ready state of the system and documentation. Merges only occur after features/fixes are complete and verified.
    *   **Feature Branches:** All development (new features, bug fixes, architectural changes) MUST occur on separate feature branches (e.g., `feature/add-mcp-support`, `fix/kb-linking-bug`). Branches should be created from `main`.
    *   **Pull Requests:** Merges into `main` should ideally occur via Pull Requests (if using a platform like GitHub/GitLab) to facilitate review.
*   **Tagging Strategy:**
    *   Releases are marked on the `main` branch using annotated Git tags following Semantic Versioning (e.g., `v18.3.4`, `v19.0.0`).
*   **`.clinerules` Versioning:** Recommend adding a `version` metadata field to `.clinerules` files (e.g., `version: "1.2.0"`) to track compatibility with specific architecture versions or standards.
*   **Potential Expansion (Considerations):**
    *   Versioning for `philosophy-knowledge-base/` (complex, requires careful strategy).
    *   Versioning for `phil-memory-bank/` (potentially useful for debugging, but high churn).
    *   More complex branching models (e.g., `develop` branch) if team size/complexity increases.
*   **Note:** See Section 8.1 regarding RooCode Checkpoints for task-level rollback.

## 9. Configuration Structure (V18.2 - Linux Paths)

### 8.1 RooCode Checkpoints (Task-Level Rollback)

*   **Description:** RooCode provides a "Checkpoints" feature, which acts as a task-specific, temporary version control system, distinct from the main project Git history. It automatically creates snapshots (like lightweight commits in a shadow Git repository) at key points during a task execution (e.g., before/after tool use, before `attempt_completion`).
*   **Purpose:** Serves as a safety net, allowing users to easily revert the workspace to a previous state *within the current task* if an AI operation produces undesirable results or errors occur. This is particularly valuable for complex operations like large code refactoring or document generation.
*   **Mechanism:** Checkpoints are managed internally by the RooCode framework. Users can typically view, compare (diff), and restore checkpoints via the RooCode user interface.
*   **Isolation:** Checkpoint history is isolated to the specific task instance and does not pollute the main Git repository history (`main`, feature branches). This keeps the primary version control clean and focused on deliberate, verified changes.
*   **Status:** Enabled for the `philoso-roo` project (Decision Log approx. [2025-05-02 13:35:26]).
*   **UX Considerations:** Users should be aware of the Checkpoint feature and how to access it via the UI. Modes (like `EssayPrep` or `Code`) might suggest creating manual checkpoints before potentially risky operations. Clear UI indicators for checkpoint creation and restoration are important.
*   **Mode Definition File (`.roo/.roomodes`):** Defines all V18.2 modes and their `.clinerules` paths. Uses forward slashes (`/`). **`philosophy-operational-context-manager` removed.**
    ```json
    {
      "philosophy-orchestrator": ".roo/rules-philosophy-orchestrator/philosophy-orchestrator.clinerules",
      "philosophy-evidence-manager": ".roo/rules-philosophy-evidence-manager/philosophy-evidence-manager.clinerules",
      "philosophy-text-processor": ".roo/rules-philosophy-text-processor/philosophy-text-processor.clinerules",
      "philosophy-pre-lecture": ".roo/rules-philosophy-pre-lecture/philosophy-pre-lecture.clinerules",
      "philosophy-class-analysis": ".roo/rules-philosophy-class-analysis/philosophy-class-analysis.clinerules",
      "philosophy-secondary-lit": ".roo/rules-philosophy-secondary-lit/philosophy-secondary-lit.clinerules",
      "philosophy-dialectical-analysis": ".roo/rules-philosophy-dialectical-analysis/philosophy-dialectical-analysis.clinerules",
      "philosophy-questioning": ".roo/rules-philosophy-questioning/philosophy-questioning.clinerules",
      "philosophy-essay-prep": ".roo/rules-philosophy-essay-prep/philosophy-essay-prep.clinerules",
      "philosophy-kb-doctor": ".roo/rules-philosophy-kb-doctor/philosophy-kb-doctor.clinerules", // Manages KB Maintenance & Rigor Validation
      "philosophy-draft-generator": ".roo/rules-philosophy-draft-generator/philosophy-draft-generator.clinerules",
      "philosophy-citation-manager": ".roo/rules-philosophy-citation-manager/philosophy-citation-manager.clinerules",
      "philosophy-verification-agent": ".roo/rules-philosophy-verification-agent/philosophy-verification-agent.clinerules",
      "philosophy-meta-reflector": ".roo/rules-philosophy-meta-reflector/philosophy-meta-reflector.clinerules"
      // Add other non-philosophy modes if they exist in the same config
    }
    ```
*   **Rules File Directory Structure:** `.roo/rules-[mode-slug]/[mode-slug].clinerules`. `.clinerules` for relevant modes must be updated per V18.3.2 specs (direct KB access logic, direct `phil-memory-bank/` access logic, rigor element handling, KB Doctor interaction if applicable, corrected text processor workflow including root index update). Uses forward slashes (`/`).
## 10. Operational Context Management (Memory Bank) (V18.3.4)

*   **Purpose:** The `phil-memory-bank/` directory serves as the persistent storage mechanism for **operational context**, distinct from the `philosophy-knowledge-base/` which holds domain knowledge. It tracks the system's state, decisions, progress, and inter-mode communication logs during task execution.
*   **Structure:**
    *   `activeContext.md`: Chronological log of the currently active task's high-level steps, delegations, and status updates. Primarily managed by `Orchestrator`.
    *   `globalContext.md`: Stores system-wide decisions, progress summaries across tasks, definitions of established system patterns, and potentially long-term goals or constraints. Primarily managed by `Orchestrator`.
    *   `mode-specific/`: Contains individual log files for each mode (e.g., `philosophy-orchestrator.md`, `philosophy-dialectical-analysis.md`). Modes are responsible for writing detailed logs of their operations, inputs, outputs, and decisions to their respective files.
    *   `feedback/`: Stores user feedback, intervention logs, and error reports, typically organized by mode (e.g., `architect-feedback.md`).
    *   `locks/` (Optional/Potential): May contain temporary lock files to manage concurrent access to shared resources (e.g., critical KB files), if the locking mechanism (See Section 2.4) is implemented.
*   **Interaction Pattern (V18.2+):** Modes interact directly with files within `phil-memory-bank/` using standard file tools (`read_file`, `insert_content`, `apply_diff`, `search_files`).
    *   **Writes:** Modes MUST write logs to their own `mode-specific/` file. `Orchestrator` primarily writes to global files. New entries are typically added in reverse chronological order (newest first) using `insert_content` at line 1 or via `apply_diff` if updating specific sections. Batching multiple log entries into a single write operation is recommended for efficiency.
    *   **Reads:** All modes CAN read any file within `phil-memory-bank/` to gather necessary operational context, guided by information provided during task delegation or by searching logs based on timestamps or keywords.
*   **Persistence Mechanism:** Persistence relies entirely on the standard file system saving the Markdown (`.md`) files within the `phil-memory-bank/` directory. RooCode itself does not provide a separate database or specialized persistence layer for the Memory Bank beyond these file operations.
*   **Scalability & Maintenance:** As logs grow, performance for reading/searching may degrade. Future considerations include:
    *   **Log Rotation:** Periodically archiving older log entries from `activeContext.md` or mode-specific logs.
    *   **Summarization:** Implementing logic (potentially within `MetaReflector`) to summarize older log periods or completed tasks in `globalContext.md`.
*   **Cross-Reference:** Evaluation Report Rec 3.5.