# Standard `.clinerules` Structures for Philosophy Modes (V2 - Based on V18.3.4 Arch)

## 1. Introduction

**Version:** 2.0
**Date:** 2025-05-05

**Purpose:** This document defines standard structures and guidelines for `.clinerules` files used by philosophy-focused modes within the `philoso-roo` system (formerly SPARC).

**Background:** This V2 standard supersedes V1 (`docs/standards/clinerules_standard_v1.md`). It incorporates enhancements proposed in `docs/proposals/clinerules_standard_enhancements_v1.md` and aligns with the V18.3.4 system architecture (`docs/architecture/architecture_v18.md`), which features direct KB/Memory Bank access, distributed KB maintenance (via `Orchestrator`, `MetaReflector`, `VerificationAgent`), MCP integration, and RooCode Checkpoints.

**Inspiration:** The structure and detail level remain inspired by robust mode examples (e.g., `.clinerules-philosophy-essay-prep`), adapted for the current orchestrated system.

**Core Principles:**
*   **Consistency:** Predictable structure for mode configuration.
*   **Rigor:** Embedded requirements for philosophical rigor.
*   **Reliability:** Strict protocols for critical workflows (KB interaction, verification, error handling, logging, concurrency).
*   **Orchestration Alignment:** Focus on interaction with `philosophy-orchestrator` and direct interaction with `philosophy-knowledge-base/` and `phil-memory-bank/`.
*   **Adaptability:** Flexibility where appropriate, strictness for critical operations.
*   **Explicitness:** Rules should be clear and unambiguous.

## 2. Standard Archetypes

Two primary archetypes are defined:

*   **Archetype A: Simple Orchestrated Task Mode:** Focused tasks, limited/well-defined KB interaction.
*   **Archetype B: Complex Analysis/Generation Mode:** Detailed analysis/synthesis/generation, significant KB interaction, potential workspace management, verification steps.

## 3. Common Sections (Applicable to All Archetypes)

These sections MUST be present and adhere to the central system standards.

### 3.1. `mode`
*   **Type:** `string`
*   **Description:** Unique mode slug (e.g., `philosophy-class-analysis`).
*   **Example:** `mode: philosophy-class-analysis`

### 3.2. `identity`
*   **Type:** `object`
*   **Fields:** `name` (string), `description` (string).
*   **Example:**
    ```yaml
    identity:
      name: "Philosophy Class Analysis"
      description: "Analyzes lecture transcripts/readings to identify key concepts, arguments, and questions, ensuring conceptual determinacy and adherence to evidence standards. Interacts directly with the Knowledge Base and Memory Bank."
    ```

### 3.3. `memory_bank_strategy`
*   **Type:** `object`
*   **Description:** Defines interaction with the central operational context repository (`phil-memory-bank/`).
*   **Implementation:** **STRICT:** Must adhere to standard rules defined centrally (likely in `.roo/rules-sparc/.clinerules-sparc` or shared config). Includes initialization, update frequency/process, feedback handling. Modes should NOT define custom MB strategies unless explicitly justified.
*   **Example (Reference Only):**
    ```yaml
    memory_bank_strategy:
      # --- INHERITED FROM CENTRAL CONFIGURATION ---
      # initialization: | ... standard checks ...
      # update_process: | ... standard update rules (reverse chrono, batching) ...
      # feedback_handling: | ... standard feedback logging ...
    ```

### 3.4. `general`
*   **Type:** `object`
*   **Description:** General operational rules.
*   **Implementation:** **STRICT:** Must adhere to standard rules defined centrally.
*   **Fields (Examples - Inherited):**
    *   `status_prefix`: Standard response prefix (e.g., `[MEMORY BANK: ACTIVE]`).
    *   `context_management`: Standard rules for proactive context handling and delegation (`new_task`).
    *   `error_handling_protocol`: Standard structured error handling, including tool-specific checks (read truncation), MB consultation, solution proposal, "Three Strikes" rule, and intervention logging. **V2 Enhancement:** Includes specific guidance for `apply_diff` context mismatch failures:
        > "If `apply_diff` fails with a context mismatch or low similarity: 1. Re-read the target file section using `read_file` with `start_line`/`end_line`. 2. Compare the expected `SEARCH` block with the actual content read. 3. If different, adjust the `SEARCH` block and retry `apply_diff`. 4. If identical, investigate other causes (tool bug?) and consider alternative tools (`insert_content`, `search_and_replace`) or escalate per 'Three Strikes' rule."
    *   `error_handling`: Standard Memory Bank operation error handling.
    *   `critical_evaluation`: Standard rule for re-evaluating assumptions on persistent failure.
*   **Example (Reference Only):**
    ```yaml
    general:
      # --- INHERITED FROM CENTRAL CONFIGURATION ---
      # status_prefix: | ... standard prefix ...
      # context_management: | ... standard delegation rules ...
      # error_handling_protocol: | ... standard error handling steps including V2 apply_diff guidance ...
      # ... etc ...
    ```

### 3.5. `operational_context_protocols` (New V2 Section)
*   **Type:** `object`
*   **Description:** **STRICT PROTOCOL** defining direct interaction with the operational context repository (`phil-memory-bank/`). Aligns with Arch V18.3.4 Section 10.
*   **Fields:**
    *   `write_access`: (string) **MUST** state: "Modes MUST write operational logs ONLY to their designated `phil-memory-bank/mode-specific/[mode_slug].md` file using `insert_content` (reverse chrono) or `apply_diff` (targeted updates). Batching recommended."
    *   `read_access`: (string) **MUST** state: "Modes CAN read any file within `phil-memory-bank/` (global context, other mode logs, feedback) using `read_file` or `search_files` as needed for operational context, guided by `Orchestrator` delegation."
    *   `separation_mandate`: (string) **MUST** state: "Strict separation MUST be maintained. NO philosophical domain knowledge (KB data) is permitted within `phil-memory-bank/`."
*   **Example:**
    ```yaml
    operational_context_protocols:
      write_access: "Modes MUST write operational logs ONLY to their designated `phil-memory-bank/mode-specific/[mode_slug].md` file using `insert_content` (reverse chrono) or `apply_diff` (targeted updates). Batching recommended."
      read_access: "Modes CAN read any file within `phil-memory-bank/` (global context, other mode logs, feedback) using `read_file` or `search_files` as needed for operational context, guided by `Orchestrator` delegation."
      separation_mandate: "Strict separation MUST be maintained. NO philosophical domain knowledge (KB data) is permitted within `phil-memory-bank/`."
    ```

### 3.6. `operational_logging`
*   **Type:** `object`
*   **Description:** **STRICT PROTOCOL** for logging operational steps to the mode's specific file within `phil-memory-bank/`.
*   **Fields:**
    *   `target_file`: (string) **MUST** be `phil-memory-bank/mode-specific/[mode_slug].md`.
    *   `format`: (string) Log entry format. **MUST** include Timestamp, Action/Status, Details, KB Interaction (IDs), Input/Output Summary, Cross-Refs. **MUST** be reverse chronological.
    *   `frequency`: (string) **MUST** log task start/end, sub-steps, KB R/W ops, script/MCP calls, verification, errors, interventions.
    *   `guidelines`: (string) Concise, operational focus, use KB IDs. **V2 Enhancement:** "Recommend batching log entries where feasible (e.g., buffer 3-5 entries related to a single sub-task) before performing a single `insert_content` operation to `target_file` to reduce I/O frequency."
*   **Example:**
    ```yaml
    operational_logging:
      target_file: "phil-memory-bank/mode-specific/philosophy-class-analysis.md"
      format: |
        ### [YYYY-MM-DD HH:MM:SS] - [Action/Status]
        - **Details:** [Brief description of the step, parameters used, files involved.]
        - **KB Interaction:** [Read KB ID: X, Y; Wrote KB ID: Z (Type: Concept)]
        - **Input:** [Summary of key input data]
        - **Output:** [Summary of key output data/result]
        - **Cross-ref:** [Link to relevant KB entry, feedback log, etc. if applicable]
      frequency: "Log task start/end, major sub-steps, all KB R/W ops, MCP calls, script calls, verification, errors, interventions."
      guidelines: "Maintain reverse chronological order. Be concise. Focus on operational actions, use KB IDs. Do not duplicate KB content. Recommend batching log entries before writing via `insert_content`."
    ```

### 3.7. `error_reporting_protocols`
*   **Type:** `object`
*   **Description:** **STRICT PROTOCOL** for reporting errors.
*   **Fields:**
    *   `reporting_target`: (string) **MUST** report errors primarily via the standard return mechanism to the calling orchestrator (`philosophy-orchestrator`).
    *   `error_codes`: (object) Define standard error codes the mode might emit. (Modes should aim to use centrally defined codes where possible). **V2 Additions:** `MCP_TOOL_FAIL`, `MCP_SERVER_UNAVAILABLE`, `CONCURRENCY_CONFLICT`.
        *   `KB_READ_FAIL`: Failed to read from Knowledge Base.
        *   `KB_WRITE_FAIL`: Failed to write to Knowledge Base.
        *   `KB_SCHEMA_VIOLATION`: Attempted write does not conform to KB schema.
        *   `VERIFICATION_FAIL`: Evidence/claim verification failed.
        *   `SCRIPT_EXEC_FAIL`: External script execution failed.
        *   `INPUT_VALIDATION_FAIL`: Input from orchestrator failed validation.
        *   `MISSING_DEPENDENCY`: Required file or KB entry not found.
        *   `CONFIG_ERROR`: Issue with `.clinerules` configuration.
        *   `MCP_TOOL_FAIL`: "MCP Tool Execution Failure"
        *   `MCP_SERVER_UNAVAILABLE`: "MCP Server Unavailable"
        *   `CONCURRENCY_CONFLICT`: "Concurrency Conflict Detected (e.g., lock file)"
    *   `error_message_format`: (string) Format for error messages returned to orchestrator. **MUST** include Error Code, Mode Slug, File/Resource Path (if applicable), KB ID (if applicable), Line Number (if applicable), and a concise description.
    *   `logging`: (string) **MUST** log all errors in the mode's operational log (`operational_logging.target_file`) and feedback log (`phil-memory-bank/feedback/[mode_slug]-feedback.md`) following standard formats.
    *   `escalation`: (string) Adhere to the standard SPARC `error_handling_protocol` regarding retries, strategy changes (Three Strikes Rule), delegation to `debug`, and invoking Early Return.
*   **Example:**
    ```yaml
    error_reporting_protocols:
      reporting_target: "Return structured error object to Orchestrator."
      error_codes:
        KB_READ_FAIL: "Knowledge Base Read Failure"
        KB_WRITE_FAIL: "Knowledge Base Write Failure"
        KB_SCHEMA_VIOLATION: "Knowledge Base Schema Violation"
        VERIFICATION_FAIL: "Verification Failure"
        SCRIPT_EXEC_FAIL: "Script Execution Failure"
        INPUT_VALIDATION_FAIL: "Input Validation Failure"
        MISSING_DEPENDENCY: "Missing Dependency"
        CONFIG_ERROR: "Configuration Error"
        MCP_TOOL_FAIL: "MCP Tool Execution Failure"
        MCP_SERVER_UNAVAILABLE: "MCP Server Unavailable"
        CONCURRENCY_CONFLICT: "Concurrency Conflict Detected (e.g., lock file)"
      error_message_format: "[ErrorCode] in [ModeSlug]: [Description]. Resource: [Path/ID], Line: [LineNum]."
      logging: "Log all errors with details in operational log and feedback log."
      escalation: "Follow standard SPARC error handling protocol (retries, three strikes, debug delegation, early return)."
    ```

### 3.8. `mcp_interaction_protocols` (New V2 Section)
*   **Type:** `object`
*   **Description:** Defines rules for interacting with external services via the Model Context Protocol (MCP). Aligns with Arch V18.3.4 Section 4.1 and `docs/blueprints/mcp_integration_v1.md`.
*   **Fields:**
    *   `strategy_reference`: (string) **MUST** state: "Adheres to 'Distributed MCP Calls' strategy defined in `docs/blueprints/mcp_integration_v1.md`."
    *   `allowed_tools`: (array) List of specific MCP tools the mode is permitted to use, including `server_name` and `tool_name`. Define structure: `{ server_name: string, tool_name: string }`.
    *   `security_mandate`: (string) **MUST** state: "API keys/secrets MUST NOT be included in `.clinerules` or code. Access MUST be managed via environment variables on the MCP server."
    *   `error_handling`: (string) **MUST** state: "Report MCP failures using `MCP_TOOL_FAIL` or `MCP_SERVER_UNAVAILABLE` via `error_reporting_protocols`. Follow standard escalation. Consider tool-specific retry logic if appropriate."
    *   `usage_guidelines`: (string) Mode-specific instructions on *when* and *how* to use allowed tools effectively and responsibly (e.g., query specificity, rate limits, data privacy considerations).
*   **Example:**
    ```yaml
    mcp_interaction_protocols:
      strategy_reference: "Adheres to 'Distributed MCP Calls' strategy defined in `docs/blueprints/mcp_integration_v1.md`."
      allowed_tools:
        - server_name: "brave-search"
          tool_name: "brave_web_search"
        - server_name: "fetcher"
          tool_name: "fetch_url"
      security_mandate: "API keys/secrets MUST NOT be included in `.clinerules` or code. Access MUST be managed via environment variables on the MCP server."
      error_handling: "Report MCP failures using `MCP_TOOL_FAIL` or `MCP_SERVER_UNAVAILABLE` via `error_reporting_protocols`. Follow standard escalation. Consider tool-specific retry logic if appropriate."
      usage_guidelines: |
        Use 'brave_web_search' for finding secondary sources or external definitions relevant to the current philosophical context.
        Use 'fetch_url' for retrieving content from specific URLs found via search or KB refs, ensuring relevance before processing.
        Handle timeouts/errors gracefully. Respect API limits. Avoid fetching sensitive or irrelevant content.
    ```

### 3.9. `concurrency_coordination_protocols` (New V2 Section)
*   **Type:** `object`
*   **Description:** Defines protocols to mitigate risks associated with concurrent file access by multiple modes, particularly to the shared Knowledge Base and Memory Bank.
*   **Fields:**
    *   `risk_acknowledgment`: (string) **MUST** state: "Direct file access by multiple modes introduces risks (race conditions, data corruption). These protocols aim to mitigate, but not eliminate, these risks. Adherence by all modes is critical."
    *   `locking_mechanism`: (object) Defines the recommended advisory file locking protocol.
        *   `type`: (string) "Advisory File Locking"
        *   `lock_file_location`: (string) "`phil-memory-bank/locks/`"
        *   `lock_file_naming`: (string) "`[file_path_hash].lock` (e.g., MD5 hash of the relative file path being locked, ensuring consistent hashing algorithm across modes)"
        *   `protocol`: (string)
            > "1. Before critical writes (`write_to_file`, `apply_diff` on shared files like KB entries or global MB files): Calculate hash of target file path. Check for `phil-memory-bank/locks/[hash].lock`.
            > 2. If lock file absent: Create the lock file (e.g., using `write_to_file` with minimal content like a timestamp/mode slug). Perform write operation on the target file. Delete the lock file.
            > 3. If lock file present: Wait briefly (e.g., 1-2 seconds), retry check 1-2 times. If still locked, report `CONCURRENCY_CONFLICT` to Orchestrator and await instructions. Do NOT proceed with write."
        *   `scope`: (string) "Recommended for writes to shared KB files or critical `phil-memory-bank/` files (e.g., `globalContext.md`) where simultaneous access by different modes is plausible."
    *   `orchestrator_role`: (string) "`Orchestrator` SHOULD sequence tasks targeting the same critical files whenever feasible to minimize potential conflicts proactively."
*   **Example:**
    ```yaml
    concurrency_coordination_protocols:
      risk_acknowledgment: "Direct file access by multiple modes introduces risks (race conditions, data corruption). These protocols aim to mitigate, but not eliminate, these risks. Adherence by all modes is critical."
      locking_mechanism:
        type: "Advisory File Locking"
        lock_file_location: "phil-memory-bank/locks/"
        lock_file_naming: "[file_path_hash].lock (e.g., MD5 hash of relative path)"
        protocol: |
          1. Before critical writes (`write_to_file`, `apply_diff` on shared files): Calculate hash of target file path. Check for `phil-memory-bank/locks/[hash].lock`.
          2. If lock file absent: Create the lock file. Perform write operation on the target file. Delete the lock file.
          3. If lock file present: Wait briefly (e.g., 1-2 seconds), retry check 1-2 times. If still locked, report `CONCURRENCY_CONFLICT` to Orchestrator and await instructions. Do NOT proceed with write.
        scope: "Recommended for writes to shared KB files or critical `phil-memory-bank/` files where simultaneous access is plausible."
      orchestrator_role: "Orchestrator SHOULD sequence tasks targeting the same critical files whenever feasible."
    ```

### 3.10. `rule_inheritance_guidelines` (New V2 Section)
*   **Type:** `object`
*   **Description:** Guidelines for managing rule reuse and inheritance to promote consistency and maintainability.
*   **Fields:**
    *   `yaml_anchors`: (string) "YAML anchors (`&`) and aliases (`*`) MAY be used within a single `.clinerules` file for defining and reusing common rule blocks (e.g., standard error codes, reusable schema snippets), *if supported by the current RooCode YAML parser*. Verify parser support before extensive use."
    *   `external_includes`: (string) "Current RooCode parser status regarding external file includes (e.g., `!include shared_rules.yaml`) is **Not Supported** [Verify/Update this status if RooCode changes]. This limits direct cross-file rule inheritance."
    *   `documentation_convention`: (string) "**Mandatory:** Due to limited direct inheritance, modes MUST explicitly state adherence to centrally defined standards within their `.clinerules` documentation (e.g., via comments). Example: `# Adheres to Standard SPARC Error Handling Protocol V2.0 defined in docs/standards/clinerules_standard_v2.md Section 3.4`."
*   **Example:**
    ```yaml
    rule_inheritance_guidelines:
      yaml_anchors: "YAML anchors (`&`) and aliases (`*`) MAY be used within a single `.clinerules` file for reusing common blocks, if supported by the parser. Verify support."
      external_includes: "Current RooCode parser status regarding external file includes (`!include`) is Not Supported." # Verify/Update
      documentation_convention: "Mandatory: Modes MUST explicitly state adherence to centrally defined standards via comments, referencing `docs/standards/clinerules_standard_v2.md` and relevant section numbers."
    ```

## 4. Archetype A: Simple Orchestrated Task Mode

Includes Common Sections (3.1-3.10) plus:

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
    *   `read_access`: (array) List allowed KB directory paths or entry types for reading. **STRICT:** Default is no read access. Use V18.3.4 direct access patterns (`read_file`, `search_files`). Paths MUST start with `philosophy-knowledge-base/`.
    *   `write_access`: (array) List allowed KB directory paths or entry types for writing. **STRICT:** Default is no write access. Writes MUST conform to V18.3.4 KB schema. Paths MUST start with `philosophy-knowledge-base/`.
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
*   **Description:** Defines rules for executing external scripts via `execute_command`.
*   **Fields:**
    *   `script_path`: (string) Path to the executable script (relative to workspace root).
    *   `input_format`: (string) Method for passing data (e.g., "stdin", "command_line_args", "temp_file").
    *   `output_parsing`: (string) How script output is captured and parsed (e.g., "stdout_json", "stdout_text", "output_file").
    *   `error_handling`: (string) How script errors (non-zero exit codes, stderr output) are detected and reported using `error_reporting_protocols` (e.g., `SCRIPT_EXEC_FAIL`).
*   **Example:**
    ```yaml
    script_execution:
      script_path: "scripts/format_text.py"
      input_format: "stdin"
      output_parsing: "stdout_text"
      error_handling: "Capture stderr, check exit code. Report using SCRIPT_EXEC_FAIL via error_reporting_protocols."
    ```

## 5. Archetype B: Complex Analysis/Generation Mode

Includes Common Sections (3.1-3.10) plus:

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
        rigor_focus: # Example V18.3.4 rigor parameter
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
    *   `read_access`: (array) List allowed KB directory paths or entry types. **STRICT:** Use V18.3.4 direct access patterns (`read_file`, `search_files`). Must specify how context tags are used for filtering. Paths MUST start with `philosophy-knowledge-base/`.
    *   `write_access`: (array) List allowed KB directory paths or entry types. **STRICT:** Writes MUST conform to the full V18.3.4 KB entry schema (YAML frontmatter + Markdown content, see Arch Doc Sec 6), including population of relevant rigor fields (`positive_determination`, `negative_determination`, `presuppositions`, `counter_arguments`, etc.). **MUST** generate and use unique IDs. **MUST** ensure critical linking fields (`source_ref_keys`, `extraction_markers`, `related_ids`) are accurately populated based on analysis. Use `write_to_file` or `insert_content` appropriately. Paths MUST start with `philosophy-knowledge-base/`.
    *   `querying`: (string) Guidelines for constructing KB queries using `search_files` or logic based on `read_file`. Emphasize using context tags and relationship links (`related_ids`) for efficient and relevant data retrieval. Avoid reading entire KB directories.
    *   `kb_maintenance_interaction`: (string) **V2 Update:** Define conditions under which the mode should flag potential KB inconsistencies (e.g., broken links, schema violations detected during read, conflicting information) to the `Orchestrator`. **Modes do NOT trigger maintenance directly.** `Orchestrator` delegates checks to `MetaReflector` or `VerificationAgent` as appropriate.
    *   `validation_hooks`: (string) **V2 Addition:** "Modes performing KB writes SHOULD attempt self-validation against schemas/rules in `philosophy-knowledge-base/_operational/formatting_templates_rules/` before writing. `VerificationAgent` performs mandatory post-write checks during workflows."
    *   `rigor_field_handling`: (string) **V2 Addition:** "Modes MUST explicitly populate relevant rigor fields (determinacy, presuppositions, etc.) as defined in the V18.3.4 KB Entry Format (Arch Doc Sec 6) when creating/updating KB entries."
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
      kb_maintenance_interaction: "If KB inconsistencies (broken links, schema violations, conflicts) detected during R/W, report details (e.g., KB_SCHEMA_VIOLATION, MISSING_DEPENDENCY) to Orchestrator, suggesting MetaReflector/VerificationAgent review."
      validation_hooks: "Modes performing KB writes SHOULD attempt self-validation against schemas in `philosophy-knowledge-base/_operational/formatting_templates_rules/`. `VerificationAgent` performs mandatory post-write checks."
      rigor_field_handling: "Modes MUST explicitly populate relevant rigor fields (determinacy, presuppositions, etc.) per Arch Doc Sec 6 when creating/updating KB entries."
    ```

### 5.5. `conceptual_determinacy` (Guideline Section - Adaptable)
*   **Type:** `object`
*   **Description:** Guidelines for ensuring philosophical rigor regarding concept clarity. Adapt requirements based on mode's function.
*   **Fields:**
    *   `requirements`: (object) Define expectations for generated concepts.
        *   `negative_definition`: (string) e.g., `required`, `recommended`, `optional`.
        *   `disambiguation_protocol`: (string) e.g., `required_if_ambiguous`, `optional`.
        *   `ordinary_language_contrast`: (string) e.g., `recommended`, `optional`.
    *   `implementation`: (string) Guidelines for how the mode should achieve these requirements during analysis/generation. Reference specific V18.3.4 KB schema fields (`positive_determination`, `negative_determination`, `ordinary_language_contrast`, `ambiguities`, `related_terms`).
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
*   **Description:** Defines integration with Git for modes managing versioned artifacts (e.g., essay drafts). References Arch V18.3.4 Section 8.
*   **Fields:**
    *   `integration`: (string) How Git is used (e.g., "Via `execute_command`").
    *   `commit_strategy`: (string) When commits should occur (e.g., "After each major section completion", "On explicit user command via orchestrator"). Define commit message format.
    *   `branching`: (string) Branching strategy, if applicable (e.g., "Work on feature branches coordinated by orchestrator").
    *   `checkpoint_awareness`: (string) "Be aware of RooCode Checkpoints (Arch Sec 8.1) for task-level rollback; Git is for persistent, verified changes."
*   **Example (for `philosophy-essay-prep`):**
    ```yaml
    version_control:
      integration: "Via `execute_command`"
      commit_strategy: "Commit after successful verification of a draft section, or on explicit 'commit' task from orchestrator. Message format: 'feat(essay): Update section X - [Brief Description]' or 'fix(essay): Correct citation in section Y'."
      branching: "Assumes working on a feature branch managed externally or by orchestrator."
      checkpoint_awareness: "Be aware of RooCode Checkpoints (Arch Sec 8.1) for task-level rollback; Git is for persistent, verified changes."
    ```

## 6. Conclusion

Adherence to these V2 standards is crucial for maintaining a consistent, reliable, and philosophically rigorous system aligned with the V18.3.4 architecture. Modes should be implemented following the common sections and the specific archetype that best fits their function. Deviations should be explicitly justified and approved. These standards should be reviewed and updated alongside major architectural changes.