# Standard `.clinerules` Structures for Philosophy Modes (V1 - Based on V18.3 Arch)

## 1. Introduction

**Purpose:** This document defines standard structures and guidelines for `.clinerules` files used by philosophy-focused modes within the SPARC-orchestrated system.

**Background:** Based on the decision logged at [2025-05-02 23:50:14 in `memory-bank/globalContext.md`], these standards aim to address inconsistencies in `.clinerules` detail and ensure alignment with the current V18.3 system architecture (Direct KB Access, KB Doctor for maintenance, Orchestrator-centric workflow).

**Inspiration:** The structure and detail level are inspired by the robust `.clinerules-philosophy-essay-prep` file, adapted to remove inter-mode handoff logic now managed by the central orchestrator (`philosophy-orchestrator` or `sparc`).

**Core Principles:**
*   **Consistency:** Provide a predictable structure for mode configuration.
*   **Rigor:** Embed requirements and guidelines for philosophical rigor.
*   **Reliability:** Define strict protocols for critical workflows (KB interaction, verification, error handling, logging).
*   **Orchestration Alignment:** Focus on interaction with the central orchestrator and direct interaction with the Knowledge Base (`philosophy-knowledge-base/`) and Memory Bank (`memory-bank/`).
*   **Adaptability:** Allow flexibility where appropriate (e.g., rigor guidelines) while enforcing strictness for critical operations.

## 2. Standard Archetypes

Two primary archetypes are defined:

*   **Archetype A: Simple Orchestrated Task Mode:** Modes performing focused, often self-contained tasks with limited, well-defined KB interaction (e.g., generating captions, running a specific formatting script).
*   **Archetype B: Complex Analysis/Generation Mode:** Modes performing detailed analysis, synthesis, or generation, requiring significant interaction with the KB (reading multiple sources, writing complex entries with rigor fields), potentially managing a workspace, and involving verification steps (e.g., `philosophy-class-analysis`, `philosophy-dialectical-analysis`, `philosophy-essay-prep`).

## 3. Common Sections (Applicable to All Archetypes)

These sections MUST be present and adhere to the central SPARC system standards.

### 3.1. `mode`

*   **Type:** `string`
*   **Description:** The unique slug identifying the mode (e.g., `philosophy-class-analysis`).
*   **Example:**
    ```yaml
    mode: philosophy-class-analysis
    ```

### 3.2. `identity`

*   **Type:** `object`
*   **Description:** Defines the mode's name and purpose.
*   **Fields:**
    *   `name`: (string) User-facing name.
    *   `description`: (string) Concise explanation of the mode's function.
*   **Example:**
    ```yaml
    identity:
      name: "Philosophy Class Analysis"
      description: "Analyzes lecture transcripts and readings to identify key concepts, arguments, and questions, ensuring conceptual determinacy and adherence to evidence standards. Interacts directly with the Knowledge Base."
    ```

### 3.3. `memory_bank_strategy`

*   **Type:** `object`
*   **Description:** Defines how the mode interacts with the central SPARC Memory Bank (`memory-bank/`).
*   **Implementation:** **STRICT:** Must adhere to the standard SPARC Memory Bank strategy rules defined centrally (likely in `.roo/rules-sparc/.clinerules-sparc` or a shared configuration). This includes initialization checks, update frequency/process, and feedback handling. Modes should NOT define custom MB strategies unless explicitly approved as a deviation.
*   **Example (Reference Only - Do Not Copy Verbatim):**
    ```yaml
    memory_bank_strategy:
      # --- INHERITED FROM CENTRAL SPARC CONFIGURATION ---
      # initialization: | ... standard checks ...
      # update_process: | ... standard update rules (reverse chrono, batching) ...
      # feedback_handling: | ... standard feedback logging ...
      # --- Mode-Specific Overrides (Use Sparingly & With Justification) ---
      # (e.g., specific files to read on init beyond standard global/active)
    ```

### 3.4. `general`

*   **Type:** `object`
*   **Description:** General operational rules.
*   **Implementation:** **STRICT:** Must adhere to the standard SPARC general rules defined centrally.
*   **Fields (Examples - Inherited):**
    *   `status_prefix`: Standard prefix for responses (e.g., `[MEMORY BANK: ACTIVE]`).
    *   `context_management`: Standard rules for proactive context handling and delegation (`new_task`).
    *   `error_handling_protocol`: Standard structured error handling, including tool-specific checks (read truncation, apply_diff context), MB consultation, solution proposal, "Three Strikes" rule, and intervention logging.
    *   `error_handling`: Standard Memory Bank operation error handling.
    *   `critical_evaluation`: Standard rule for re-evaluating assumptions on persistent failure.
*   **Example (Reference Only - Do Not Copy Verbatim):**
    ```yaml
    general:
      # --- INHERITED FROM CENTRAL SPARC CONFIGURATION ---
      # status_prefix: | ... standard prefix ...
      # context_management: | ... standard delegation rules ...
      # error_handling_protocol: | ... standard error handling steps ...
      # ... etc ...
    ```

### 3.5. `operational_logging`

*   **Type:** `object`
*   **Description:** **STRICT PROTOCOL** for logging mode's operational steps to its specific Memory Bank file. This is distinct from philosophical content stored in the KB.
*   **Fields:**
    *   `target_file`: (string) **MUST** be `memory-bank/mode-specific/[mode_slug].md`.
    *   `format`: (string) Log entry format. **MUST** include Timestamp, Action/Status, Key Details (e.g., files accessed, KB IDs queried/written, parameters used), Input/Output Summary (brief), and Cross-References (to KB entries, other logs if relevant). **MUST** be added reverse chronologically (newest first).
    *   `frequency`: (string) When to log. **MUST** log at minimum: Task start/end, significant sub-steps, each KB read/write operation (including IDs), script executions, verification steps, errors encountered, user interventions.
    *   `guidelines`: (string) Instructions for content. Be concise but informative. Focus on *what* the mode did operationally. Avoid duplicating large chunks of KB content. Use KB IDs for reference.
*   **Example:**
    ```yaml
    operational_logging:
      target_file: "memory-bank/mode-specific/philosophy-class-analysis.md"
      format: |
        ### [YYYY-MM-DD HH:MM:SS] - [Action/Status]
        - **Details:** [Brief description of the step, parameters used, files involved.]
        - **KB Interaction:** [Read KB ID: X, Y; Wrote KB ID: Z (Type: Concept)]
        - **Input:** [Summary of key input data]
        - **Output:** [Summary of key output data/result]
        - **Cross-ref:** [Link to relevant KB entry, feedback log, etc. if applicable]
      frequency: "Log task start/end, major sub-steps, all KB read/write operations, script calls, verification checks, errors, and user interventions."
      guidelines: "Maintain reverse chronological order. Be concise. Focus on operational actions, use KB IDs for reference. Do not duplicate KB content here."
    ```

### 3.6. `error_reporting_protocols`

*   **Type:** `object`
*   **Description:** **STRICT PROTOCOL** for how the mode reports errors internally and to the orchestrator.
*   **Fields:**
    *   `reporting_target`: (string) **MUST** report errors primarily via the standard return mechanism to the calling orchestrator (SPARC or `philosophy-orchestrator`).
    *   `error_codes`: (object) Define standard error codes the mode might emit. (Modes should aim to use centrally defined codes where possible).
        *   `KB_READ_FAIL`: Failed to read from Knowledge Base.
        *   `KB_WRITE_FAIL`: Failed to write to Knowledge Base.
        *   `KB_SCHEMA_VIOLATION`: Attempted write does not conform to KB schema.
        *   `VERIFICATION_FAIL`: Evidence/claim verification failed.
        *   `SCRIPT_EXEC_FAIL`: External script execution failed.
        *   `INPUT_VALIDATION_FAIL`: Input from orchestrator failed validation.
        *   `MISSING_DEPENDENCY`: Required file or KB entry not found.
        *   `CONFIG_ERROR`: Issue with `.clinerules` configuration.
    *   `error_message_format`: (string) Format for error messages returned to orchestrator. **MUST** include Error Code, Mode Slug, File/Resource Path (if applicable), KB ID (if applicable), Line Number (if applicable), and a concise description.
    *   `logging`: (string) **MUST** log all errors in the mode's operational log (`operational_logging.target_file`) and feedback log (`memory-bank/feedback/[mode_slug]-feedback.md`) following standard formats.
    *   `escalation`: (string) Adhere to the standard SPARC `error_handling_protocol` regarding retries, strategy changes (Three Strikes Rule), delegation to `debug`, and invoking Early Return.
*   **Example:**
    ```yaml
    error_reporting_protocols:
      reporting_target: "Return structured error object to Orchestrator."
      error_codes:
        KB_READ_FAIL: "Knowledge Base Read Failure"
        KB_WRITE_FAIL: "Knowledge Base Write Failure"
        VERIFICATION_FAIL: "Verification Failure"
        SCRIPT_EXEC_FAIL: "Script Execution Failure"
        # ... other mode-specific or standard codes
      error_message_format: "[ErrorCode] in [ModeSlug]: [Description]. Resource: [Path/ID], Line: [LineNum]."
      logging: "Log all errors with details in operational log and feedback log."
      escalation: "Follow standard SPARC error handling protocol (retries, three strikes, debug delegation, early return)."
    ```

## 4. Archetype A: Simple Orchestrated Task Mode

Includes Common Sections plus:

### 4.1. `input_schema`

*   **Type:** `object`
*   **Description:** Defines the expected input data structure received from the orchestrator. Use JSON schema or descriptive format.
*   **Example:**
    ```yaml
    input_schema:
      type: object
      properties:
        task_type:
          type: string
          enum: ["generate_caption", "format_text"]
        source_text:
          type: string
          description: "Text content to process."
        kb_concept_id:
          type: string
          description: "(Optional) ID of a relevant KB concept."
      required: ["task_type", "source_text"]
    ```

### 4.2. `output_schema`

*   **Type:** `object`
*   **Description:** Defines the structure of the result returned to the orchestrator.
*   **Example:**
    ```yaml
    output_schema:
      type: object
      properties:
        status:
          type: string
          enum: ["success", "failure"]
        result_text:
          type: string
          description: "The generated caption or formatted text."
        error_details: # Present only if status is failure
          type: object
          # ... follows error_reporting_protocols.error_message_format
      required: ["status"]
    ```

### 4.3. `kb_interaction_protocols` (Optional/Minimal for Archetype A)

*   **Type:** `object`
*   **Description:** Defines limited KB interaction rules, if any.
*   **Fields:**
    *   `read_access`: (array) List allowed KB directory paths or entry types for reading. **STRICT:** Default is no read access. Use V18.3 direct access patterns (`read_file`, `search_files`).
    *   `write_access`: (array) List allowed KB directory paths or entry types for writing. **STRICT:** Default is no write access. Writes MUST conform to V18.3 KB schema.
    *   `verification`: (string) Typically "N/A" for simple modes.
*   **Example:**
    ```yaml
    kb_interaction_protocols:
      read_access:
        - "philosophy-knowledge-base/concepts/" # Allowed to read concepts
      write_access: [] # No write access allowed
      verification: "N/A"
    ```

### 4.4. `script_execution` (If Applicable)

*   **Type:** `object`
*   **Description:** Defines rules for executing external scripts.
*   **Fields:**
    *   `script_path`: (string) Path to the executable script (relative to workspace root).
    *   `input_format`: (string) Method for passing data (e.g., "stdin", "command_line_args", "temp_file").
    *   `output_parsing`: (string) How script output is captured and parsed (e.g., "stdout_json", "stdout_text", "output_file").
    *   `error_handling`: (string) How script errors (non-zero exit codes, stderr output) are detected and reported using `error_reporting_protocols`.
*   **Example:**
    ```yaml
    script_execution:
      script_path: "scripts/format_text.py"
      input_format: "stdin"
      output_parsing: "stdout_text"
      error_handling: "Capture stderr, check exit code. Report using SCRIPT_EXEC_FAIL via error_reporting_protocols."
    ```

## 5. Archetype B: Complex Analysis/Generation Mode

Includes Common Sections plus:

### 5.1. `input_schema`

*   **Type:** `object`
*   **Description:** Defines the expected input data structure received from the orchestrator (often more complex, e.g., multiple KB IDs, source file paths, analysis parameters).
*   **Example:**
    ```yaml
    input_schema:
      type: object
      properties:
        analysis_target_ids:
          type: array
          items:
            type: string
          description: "List of KB entry IDs (concepts, arguments) to analyze."
        source_material_paths:
          type: array
          items:
            type: string
          description: "List of paths to relevant source materials (readings, transcripts)."
        analysis_depth:
          type: string
          enum: ["summary", "detailed", "comparative"]
        rigor_focus: # Example V18.3 rigor parameter
          type: array
          items:
            type: string
            enum: ["determinacy", "presuppositions", "evidence_links"]
      required: ["analysis_target_ids"]
    ```

### 5.2. `output_schema`

*   **Type:** `object`
*   **Description:** Defines the structure of the result returned to the orchestrator (often includes new KB entry IDs, verification status, etc.).
*   **Example:**
    ```yaml
    output_schema:
      type: object
      properties:
        status:
          type: string
          enum: ["success", "partial_success", "failure", "verification_pending"]
        new_kb_entry_ids:
          type: array
          items:
            type: string
          description: "IDs of new KB entries created during analysis."
        updated_kb_entry_ids:
          type: array
          items:
            type: string
          description: "IDs of existing KB entries updated."
        analysis_summary:
          type: string
          description: "Brief summary of the analysis performed."
        verification_report_id: # If verification was performed
          type: string
          description: "ID of the KB entry containing the verification report."
        error_details: # Present only if status includes failure
          type: object
          # ... follows error_reporting_protocols.error_message_format
      required: ["status"]
    ```

### 5.3. `workspace_management` (Optional)

*   **Type:** `object`
*   **Description:** Defines rules if the mode requires a dedicated temporary workspace (e.g., for complex draft generation).
*   **Fields:**
    *   `root`: (string) Path relative to workspace root (e.g., `essay_prep/temp_drafts/`).
    *   `structure`: (array) List of expected subdirectories within the root.
    *   `cleanup`: (string) Rules for cleanup (e.g., "Delete on task completion", "Keep intermediate files").
*   **Example:**
    ```yaml
    workspace_management:
      root: "essay_prep/active_draft/"
      structure: ["sections", "notes", "verification_reports"]
      cleanup: "Keep intermediate files until explicit cleanup command."
    ```

### 5.4. `kb_interaction_protocols` (Mandatory & Detailed for Archetype B)

*   **Type:** `object`
*   **Description:** **STRICT PROTOCOL** defining all interactions with the `philosophy-knowledge-base/`.
*   **Fields:**
    *   `read_access`: (array) List allowed KB directory paths or entry types. **STRICT:** Use V18.3 direct access patterns (`read_file`, `search_files`). Must specify how context tags are used for filtering.
    *   `write_access`: (array) List allowed KB directory paths or entry types. **STRICT:** Writes MUST conform to the full V18.3 KB entry schema (YAML frontmatter + Markdown content), including population of relevant rigor fields (`positive_determination`, `negative_determination`, `presuppositions`, `counter_arguments`, etc.). **MUST** generate and use unique IDs. **MUST** ensure critical linking fields (`source_ref_keys`, `extraction_markers`, `related_ids`) are accurately populated based on analysis. Use `write_to_file` or `insert_content` appropriately.
    *   `querying`: (string) Guidelines for constructing KB queries using `search_files` or logic based on `read_file`. Emphasize using context tags and relationship links (`related_ids`) for efficient and relevant data retrieval. Avoid reading entire KB directories.
    *   `kb_doctor_interaction`: (string) Define conditions under which the mode should flag potential KB inconsistencies (e.g., broken links, schema violations detected during read, conflicting information) to the orchestrator, suggesting a `philosophy-kb-doctor` review. **Modes do NOT trigger `kb-doctor` directly.**
*   **Example:**
    ```yaml
    kb_interaction_protocols:
      read_access:
        - "philosophy-knowledge-base/concepts/"
        - "philosophy-knowledge-base/arguments/"
        - "philosophy-knowledge-base/processed_texts/" # Source chunks
        - "philosophy-knowledge-base/references/"
      write_access:
        - "philosophy-knowledge-base/concepts/" # Creating new concepts
        - "philosophy-knowledge-base/arguments/" # Creating new arguments
        - "philosophy-knowledge-base/relationships/" # Linking entries
      querying: |
        Use `search_files` with regex targeting YAML frontmatter fields (id, type, tags) for initial discovery.
        Use `read_file` for specific KB entry IDs identified via search or `related_ids`.
        Filter reads/searches using `context:key:value` tags based on input parameters.
        Follow relationship links (`related_ids`) to gather related context.
      kb_doctor_interaction: "If persistent KB read errors occur, or if schema violations / broken links are detected during analysis, report KB_READ_FAIL or KB_SCHEMA_VIOLATION to orchestrator with details, suggesting KB Doctor review."
    ```

### 5.5. `conceptual_determinacy` (Guideline Section - Adaptable)

*   **Type:** `object`
*   **Description:** Guidelines for ensuring philosophical rigor regarding concept clarity. Adapt requirements based on mode's function.
*   **Fields:**
    *   `requirements`: (object) Define expectations for generated concepts.
        *   `negative_definition`: (string) e.g., `required`, `recommended`, `optional`.
        *   `disambiguation_protocol`: (string) e.g., `required_if_ambiguous`, `optional`.
        *   `ordinary_language_contrast`: (string) e.g., `recommended`, `optional`.
    *   `implementation`: (string) Guidelines for how the mode should achieve these requirements during analysis/generation. Reference specific V18.3 KB schema fields (`positive_determination`, `negative_determination`, `ordinary_language_contrast`, `ambiguities`, `related_terms`).
*   **Example:**
    ```yaml
    conceptual_determinacy:
      requirements:
        negative_definition: recommended # Encourage defining what a concept is NOT
        disambiguation_protocol: required_if_ambiguous # Mandate clarification if term has multiple senses
        ordinary_language_contrast: recommended # Encourage contrasting with everyday usage
      implementation: |
        When generating 'Concept' entries:
        1. Attempt to populate `positive_determination` and `negative_determination` fields in YAML.
        2. If term is potentially ambiguous (based on KB search or source analysis), populate `ambiguities` field and clearly state the intended sense in the main content.
        3. Consider adding notes to `ordinary_language_contrast` field.
        4. Link related concepts via `related_terms` and `related_ids`.
        5. Log steps taken to ensure determinacy in operational log.
    ```

### 5.6. `evidence_standards` (Guideline Section + Strict Workflow)

*   **Type:** `object`
*   **Description:** Guidelines and strict workflow for handling and verifying evidence.
*   **Fields:**
    *   `requirements`: (object) General standards for evidence.
        *   `source_preference`: (string) e.g., "Prefer primary sources, use secondary critically".
        *   `citation_format`: (string) e.g., "Use KB reference IDs (`source_ref_keys`) and `extraction_markers`".
        *   `quotation_accuracy`: (string) e.g., "Must match source chunk exactly".
    *   `verification_workflow`: **STRICT PROTOCOL**
        *   `enabled`: (boolean) `true` if the mode performs verification.
        *   `trigger`: (string) Conditions under which verification MUST be performed (e.g., "Before finalizing essay section", "Before storing argument with external claims").
        *   `steps`: (string) Detailed, sequential steps for verification.
            1.  Identify claims/citations requiring verification within the input (e.g., draft text).
            2.  Extract `source_ref_keys` and `extraction_markers` associated with the claim/citation.
            3.  Query KB (`read_file`) for the specific source text chunk(s) using markers/keys.
            4.  Compare the claim/citation against the retrieved source text chunk for accuracy and faithful representation.
            5.  (Optional) Query KB for related arguments/concepts (`related_ids`) to check for consistency or known counter-arguments.
            6.  (Optional) Check relevant rigor fields in source/related KB entries.
            7.  Generate a verification result (`Pass`, `Fail`, `Disputed`) with detailed notes explaining the findings.
            8.  Log the verification attempt and outcome in the operational log (`operational_logging.target_file`), including claim, source IDs, and result.
            9.  Report the verification status (and failures) to the orchestrator via the standard output schema and `error_reporting_protocols`.
        *   `failure_handling`: (string) How verification failures are handled (e.g., "Report failure to orchestrator", "Attempt self-correction by querying KB for alternative evidence", "Flag claim as unverified"). **MUST** report failures.
*   **Example:**
    ```yaml
    evidence_standards:
      requirements:
        source_preference: "Prefer primary sources linked via `source_ref_keys`. Use secondary sources critically, noting potential biases."
        citation_format: "Link claims to KB source chunks using `source_ref_keys` and `extraction_markers`."
        quotation_accuracy: "Direct quotations must exactly match the text in the referenced KB source chunk."
      verification_workflow:
        enabled: true # This mode performs verification
        trigger: "Before finalizing any essay section containing claims linked to specific evidence."
        steps: |
          1. Identify claims/citations with `source_ref_keys`/`extraction_markers`.
          2. Use `read_file` to retrieve specific source chunk(s) from `philosophy-knowledge-base/processed_texts/` based on keys/markers.
          3. Compare claim/citation text against source chunk. Check for accuracy, context preservation, and potential misrepresentation.
          4. Query KB for entries linked via `related_ids` to check for known contradictions or alternative interpretations.
          5. Generate result (Pass/Fail/Disputed) with notes.
          6. Log verification attempt (claim, source IDs, result) in operational log.
          7. Report status/failures to orchestrator. If Fail/Disputed, include detailed notes.
        failure_handling: "Report Fail/Disputed status and notes to orchestrator via output schema. Flag claim in draft."
    ```

### 5.7. `version_control` (If Applicable)

*   **Type:** `object`
*   **Description:** Defines integration with Git for modes managing versioned artifacts (e.g., essay drafts).
*   **Fields:**
    *   `integration`: (string) How Git is used (e.g., "Via `execute_command`").
    *   `commit_strategy`: (string) When commits should occur (e.g., "After each major section completion", "On explicit user command via orchestrator"). Define commit message format.
    *   `branching`: (string) Branching strategy, if applicable (e.g., "Work on feature branches coordinated by orchestrator").
*   **Example (for `philosophy-essay-prep`):**
    ```yaml
    version_control:
      integration: "Via `execute_command`"
      commit_strategy: "Commit after successful verification of a draft section, or on explicit 'commit' task from orchestrator. Message format: 'feat(essay): Update section X - [Brief Description]' or 'fix(essay): Correct citation in section Y'."
      branching: "Assumes working on a feature branch managed externally or by orchestrator."
    ```

## 6. Conclusion

Adherence to these standards is crucial for maintaining a consistent, reliable, and philosophically rigorous system. Modes should be implemented following the common sections and the specific archetype that best fits their function. Deviations should be explicitly justified and approved. These standards should be reviewed and updated alongside major architectural changes (e.g., V19+).