# Standard `.clinerules` Structures for Philosophy Modes (V2.1 - Based on V18.3.4 Arch)

**Version:** 2.1
**Date:** 2025-05-05

**Purpose:** This document defines standard structures and guidelines for `.clinerules` files used by philosophy-focused modes within the `philoso-roo` system (formerly SPARC).

**Background:** This V2.1 standard supersedes V2.0. It addresses feedback regarding implicit inheritance comments and wasteful headers identified in V2.0 [See Feedback Log: 2025-05-05 14:12:11]. It incorporates enhancements proposed in `docs/proposals/clinerules_standard_enhancements_v1.md` and aligns with the V18.3.4 system architecture (`docs/architecture/architecture_v18.md`), which features direct KB/Memory Bank access, distributed KB maintenance (via `Orchestrator`, `MetaReflector`, `VerificationAgent`), MCP integration, and RooCode Checkpoints.

**Inspiration:** The structure and detail level remain inspired by robust mode examples (e.g., `.clinerules-philosophy-essay-prep`), adapted for the current orchestrated system.

**Core Principles:**
*   **Consistency:** Predictable structure for mode configuration.
*   **Rigor:** Embedded requirements for philosophical rigor.
*   **Reliability:** Strict protocols for critical workflows (KB interaction, verification, error handling, logging, concurrency).
*   **Orchestration Alignment:** Focus on interaction with `philosophy-orchestrator` and direct interaction with `philosophy-knowledge-base/` and `phil-memory-bank/`.
*   **Adaptability:** Flexibility where appropriate, strictness for critical operations.
*   **Explicitness:** Rules MUST be clear, unambiguous, and self-contained within the `.clinerules` file. No implicit inheritance via comments.

## Standard Archetypes

Two primary archetypes are defined:

*   **Archetype A: Simple Orchestrated Task Mode:** Focused tasks, limited/well-defined KB interaction.
*   **Archetype B: Complex Analysis/Generation Mode:** Detailed analysis/synthesis/generation, significant KB interaction, potential workspace management, verification steps.

## Common Sections (Applicable to All Archetypes)

These sections MUST be present and adhere to the standards defined below.

`mode`:
  type: string
  description: Unique mode slug (e.g., `philosophy-class-analysis`).
  example: `mode: philosophy-class-analysis`

`identity`:
  type: object
  fields: `name` (string), `description` (string).
  example:
    ```yaml
    identity:
      name: "Philosophy Class Analysis"
      description: "Analyzes lecture transcripts/readings to identify key concepts, arguments, and questions, ensuring conceptual determinacy and adherence to evidence standards. Interacts directly with the Knowledge Base and Memory Bank."
    ```

`memory_bank_strategy`:
  type: object
  description: Defines interaction with the central operational context repository (`phil-memory-bank/`). **STRICT:** Modes MUST adhere to this standard structure.
  fields:
    initialization: |
      # Standard Memory Bank Initialization Protocol
      - **CHECK FOR MEMORY BANK:**
          <thinking> * Check if memory-bank/ exists. Read if yes, suggest creation if no. </thinking>
          <list_files> <path>phil-memory-bank</path> <recursive>false</recursive> </list_files>
    if_no_memory_bank: |
      # Standard Protocol if No Memory Bank Found
      1. Inform User: "No Memory Bank found at `phil-memory-bank/`..."
      2. Conditional Actions: Offer switch to Architect to create MB structure or proceed in [MEMORY BANK: INACTIVE] state.
    if_memory_bank_exists: |
      # Standard Protocol if Memory Bank Exists
      1. Read Global & Active Files: `phil-memory-bank/activeContext.md`, `phil-memory-bank/globalContext.md` (WAIT after each)
      2. Read Mode-Specific & Feedback: `phil-memory-bank/mode-specific/[mode_slug].md`, `phil-memory-bank/feedback/[mode_slug]-feedback.md` (WAIT after each, if exists)
      3. Activation: Set status '[MEMORY BANK: ACTIVE]', inform user, apply feedback. **Verify reverse chronological order of logs.**
    update_frequency: |
      # Standard Memory Bank Update Frequency
      UPDATE MEMORY BANK AT THESE POINTS:
      1. At the beginning of each task (read)
      2. **Before calling attempt_completion (perform MANDATORY pre-completion checks: Verification: Ensure the `attempt_completion` message provides a *detailed* summary including: 1) Specific actions taken, 2) Files/resources affected (with paths), 3) Verification steps performed (doc accuracy), 4) Clear status/next steps. The summary must be sufficient for SPARC/user validation without needing to re-read extensive logs. Then write MB updates using batch operations)**
      3. When significant new information is discovered or decisions are made
      4. On explicit "Update Memory Bank" or "UMB" command
    update_process: |
      # Standard Memory Bank Update Process
      1. For all updates: Include timestamp, descriptive titles, maintain structure. **ALWAYS add new entries to the TOP (reverse chronological order).** Use insert_content/apply_diff appropriately (prefer batching). Avoid overwriting logs, keep concise. Minimize API calls.
      2. File-Specific Updates: Update `phil-memory-bank/activeContext.md` (using standard format) and relevant sections in `phil-memory-bank/globalContext.md`. Update `phil-memory-bank/mode-specific/[mode_slug].md` under appropriate headers (**newest first**). Cross-reference if needed.
    feedback_handling: |
      # Standard Feedback Handling Process
      Save feedback to `phil-memory-bank/feedback/[mode_slug]-feedback.md` (**newest first**), document source/issue/action, apply learnings. **IMMEDIATELY log user interventions, explicit corrections, or significant deviations from instructions using the format in the mode-specific Intervention Log (if applicable) or within the feedback file. Include: Trigger, Context, Action Taken, Rationale, Outcome, Follow-up.**

`general`:
  type: object
  description: General operational rules. **STRICT:** Modes MUST adhere to this standard structure.
  fields:
    status_prefix: |
      # Standard Status Prefix Rule
      "Begin EVERY response with either '[MEMORY BANK: ACTIVE]' or '[MEMORY BANK: INACTIVE]', according to the current state of the Memory Bank."
    context_management: |
      # Standard Context Management Rule
      **Proactive Context Management:** During complex or long-running tasks, be mindful of context window limitations. If you notice degraded performance, repeated errors, or difficulty recalling previous steps, **proactively suggest using `new_task` to delegate the remaining work with a clear handover**, rather than waiting for critical failure or user intervention. Explicitly state context concerns as the reason for suggesting delegation.
    error_handling_protocol: |
      # Standard Error Handling Protocol (Includes V2.1 Enhancements)
      # --- EARLY RETURN CLAUSE (Placeholder - Specific modes might override) ---
      # If intractable issues arise OR context limits (~40-50%) are approached, STOP IMMEDIATELY.
      # 1. Document Thoroughly in `phil-memory-bank/feedback/[mode_slug]-feedback.md` (Blocker, Progress, Attempts, Analysis, Self-Correction, Context %, Recommendations).
      # 2. Use `attempt_completion`: Summarize blocker, state Early Return invoked, reference feedback log.
      # 3. Return Control: Await instructions.

      **Structured Error Handling:** If a tool use fails or an unexpected error occurs:
      1. **Log:** Clearly state the error encountered.
      2. **Analyze:** Briefly analyze the potential cause (e.g., incorrect parameters, file access issue, API error, context mismatch). Check tool documentation/schema if applicable.
          *   **For `read_file`:** Explicitly check the result for the truncation notice (`Showing only X of Y lines...`). If found, and if the task might require full context (e.g., applying diffs, comprehensive analysis), mandate either re-reading with specific line ranges covering the needed area or asking the user for confirmation before proceeding with potentially incomplete data.
          *   **For `apply_diff` failures:** Mandate checking for context mismatch (due to truncation/prior edits) or "identical content" errors *first*. Suggest specific actions like re-reading the section or using `search_files` to verify context before retrying. **V2.1 Enhancement:** If `apply_diff` fails with a context mismatch or low similarity: 1. Re-read the target file section using `read_file` with `start_line`/`end_line`. 2. Compare the expected `SEARCH` block with the actual content read. 3. If different, adjust the `SEARCH` block and retry `apply_diff`. 4. If identical, investigate other causes (tool bug?) and consider alternative tools (`insert_content`, `search_and_replace`) or escalate per 'Three Strikes' rule.
      3. **Consult MB:** Check `phil-memory-bank/activeContext.md` and relevant mode-specific logs (e.g., `debug.md`) for recent similar errors or known issues.
      4. **Propose Solution:** Based on analysis, propose a *specific* next step:
          - Retry the tool with corrected parameters (if analysis suggests parameter error).
          - Use a different tool to gather more info (e.g., `read_file`, `list_files`).
          - Ask the user a *targeted* question via `ask_followup_question` if specific information is missing.
          - Suggest delegating to `debug` mode if the cause is unclear.
      5. **"Three Strikes" Rule:** After 2-3 *consecutive* failures of the *same tool* on the *same target*, mandate a strategy change. Choose one: attempt an alternative tool (`insert_content`, `search_and_replace`, cautious `write_to_file`), use MCPs (`fetcher`, `brave-search`) for research, ask the user a targeted question, delegate to `debug`, or invoke Early Return. Explicitly forbid further simple retries.
      6. **Intervention Handling:** If an error leads to user intervention, ensure the intervention is logged according to the updated `feedback_handling` rule *before* proceeding with the user's correction or the next step.
      **Avoid generic retries or immediately asking the user "What should I do?" without performing this analysis.**
    error_handling: |
      # Standard Memory Bank Error Handling Rule
      **Memory Bank Error Handling:** If any Memory Bank operation (`list_files`, `read_file`, `insert_content`, `apply_diff`) fails:
      1. Log the error clearly in the chat.
      2. Inform the user about the failure and potential impact on context.
      3. Consider switching to `[MEMORY BANK: INACTIVE]' if context is severely compromised.
      4. Suggest running `memory-bank-doctor` if corruption is suspected.
      5. If corruption is confirmed, delegate repair to `memory-bank-doctor` mode using `new_task`.
    critical_evaluation: |
      # Standard Critical Evaluation Rule
      **Rule: Critical Evaluation.** When encountering contradictory evidence or persistent failures, *critically evaluate prior diagnoses or assumptions*, especially those made under high context (>40%). State this evaluation explicitly in `<thinking>` before proceeding.

`operational_context_protocols`:
  type: object
  description: **STRICT PROTOCOL** defining direct interaction with the operational context repository (`phil-memory-bank/`). Aligns with Arch V18.3.4 Section 10.
  fields:
    write_access: (string) **MUST** state: "Modes MUST write operational logs ONLY to their designated `phil-memory-bank/mode-specific/[mode_slug].md` file using `insert_content` (reverse chrono) or `apply_diff` (targeted updates). Batching recommended."
    read_access: (string) **MUST** state: "Modes CAN read any file within `phil-memory-bank/` (global context, other mode logs, feedback) using `read_file` or `search_files` as needed for operational context, guided by `Orchestrator` delegation."
    separation_mandate: (string) **MUST** state: "Strict separation MUST be maintained. NO philosophical domain knowledge (KB data) is permitted within `phil-memory-bank/`."
  example:
    ```yaml
    operational_context_protocols:
      write_access: "Modes MUST write operational logs ONLY to their designated `phil-memory-bank/mode-specific/[mode_slug].md` file using `insert_content` (reverse chrono) or `apply_diff` (targeted updates). Batching recommended."
      read_access: "Modes CAN read any file within `phil-memory-bank/` (global context, other mode logs, feedback) using `read_file` or `search_files` as needed for operational context, guided by `Orchestrator` delegation."
      separation_mandate: "Strict separation MUST be maintained. NO philosophical domain knowledge (KB data) is permitted within `phil-memory-bank/`."
    ```

`operational_logging`:
  type: object
  description: **STRICT PROTOCOL** for logging operational steps to the mode's specific file within `phil-memory-bank/`.
  fields:
    target_file: (string) **MUST** be `phil-memory-bank/mode-specific/[mode_slug].md`.
    format: (string) Log entry format. **MUST** include Timestamp, Action/Status, Details, KB Interaction (IDs), Input/Output Summary, Cross-Refs. **MUST** be reverse chronological.
    frequency: (string) **MUST** log task start/end, sub-steps, KB R/W ops, script/MCP calls, verification, errors, interventions.
    guidelines: (string) Concise, operational focus, use KB IDs. **V2 Enhancement:** "Recommend batching log entries where feasible (e.g., buffer 3-5 entries related to a single sub-task) before performing a single `insert_content` operation to `target_file` to reduce I/O frequency."
  example:
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

`error_reporting_protocols`:
  type: object
  description: **STRICT PROTOCOL** for reporting errors.
  fields:
    reporting_target: (string) **MUST** report errors primarily via the standard return mechanism to the calling orchestrator (`philosophy-orchestrator`).
    error_codes: (object) Define standard error codes the mode might emit. (Modes should aim to use centrally defined codes where possible). **V2 Additions:** `MCP_TOOL_FAIL`, `MCP_SERVER_UNAVAILABLE`, `CONCURRENCY_CONFLICT`.
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
    error_message_format: (string) Format for error messages returned to orchestrator. **MUST** include Error Code, Mode Slug, File/Resource Path (if applicable), KB ID (if applicable), Line Number (if applicable), and a concise description.
    logging: (string) **MUST** log all errors in the mode's operational log (`operational_logging.target_file`) and feedback log (`phil-memory-bank/feedback/[mode_slug]-feedback.md`) following standard formats.
    escalation: (string) Adhere to the standard SPARC `error_handling_protocol` regarding retries, strategy changes (Three Strikes Rule), delegation to `debug`, and invoking Early Return.
  example:
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

`mcp_interaction_protocols`:
  type: object
  description: Defines rules for interacting with external services via the Model Context Protocol (MCP). Aligns with Arch V18.3.4 Section 4.1 and `docs/blueprints/mcp_integration_v1.md`.
  fields:
    strategy_reference: (string) **MUST** state: "Adheres to 'Distributed MCP Calls' strategy defined in `docs/blueprints/mcp_integration_v1.md`."
    allowed_tools: (array) List of specific MCP tools the mode is permitted to use, including `server_name` and `tool_name`. Define structure: `{ server_name: string, tool_name: string }`.
    security_mandate: (string) **MUST** state: "API keys/secrets MUST NOT be included in `.clinerules` or code. Access MUST be managed via environment variables on the MCP server."
    error_handling: (string) **MUST** state: "Report MCP failures using `MCP_TOOL_FAIL` or `MCP_SERVER_UNAVAILABLE` via `error_reporting_protocols`. Follow standard escalation. Consider tool-specific retry logic if appropriate."
    usage_guidelines: (string) Mode-specific instructions on *when* and *how* to use allowed tools effectively and responsibly (e.g., query specificity, rate limits, data privacy considerations).
  example:
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

`concurrency_coordination_protocols`:
  type: object
  description: Defines protocols to mitigate risks associated with concurrent file access by multiple modes, particularly to the shared Knowledge Base and Memory Bank.
  fields:
    risk_acknowledgment: (string) **MUST** state: "Direct file access by multiple modes introduces risks (race conditions, data corruption). These protocols aim to mitigate, but not eliminate, these risks. Adherence by all modes is critical."
    locking_mechanism: (object) Defines the recommended advisory file locking protocol.
        *   `type`: (string) "Advisory File Locking"
        *   `lock_file_location`: (string) "`phil-memory-bank/locks/`"
        *   `lock_file_naming`: (string) "`[file_path_hash].lock` (e.g., MD5 hash of the relative file path being locked, ensuring consistent hashing algorithm across modes)"
        *   `protocol`: (string)
            > "1. Before critical writes (`write_to_file`, `apply_diff` on shared files like KB entries or global MB files): Calculate hash of target file path. Check for `phil-memory-bank/locks/[hash].lock`.
            > 2. If lock file absent: Create the lock file (e.g., using `write_to_file` with minimal content like a timestamp/mode slug). Perform write operation on the target file. Delete the lock file.
            > 3. If lock file present: Wait briefly (e.g., 1-2 seconds), retry check 1-2 times. If still locked, report `CONCURRENCY_CONFLICT` to Orchestrator and await instructions. Do NOT proceed with write."
        *   `scope`: (string) "Recommended for writes to shared KB files or critical `phil-memory-bank/` files (e.g., `globalContext.md`) where simultaneous access by different modes is plausible."
    orchestrator_role: (string) "`Orchestrator` SHOULD sequence tasks targeting the same critical files whenever feasible to minimize potential conflicts proactively."
  example:
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

`rule_inheritance_guidelines`:
  type: object
  description: Guidelines for managing rule reuse and inheritance to promote consistency and maintainability. **V2.1 Update:** Emphasizes explicitness.
  fields:
    yaml_anchors: (string) "YAML anchors (`&`) and aliases (`*`) MAY be used within a single `.clinerules` file for defining and reusing common rule blocks (e.g., standard error codes, reusable schema snippets), *if supported by the current RooCode YAML parser*. Verify parser support before extensive use."
    external_includes: (string) "Current RooCode parser status regarding external file includes (e.g., `!include shared_rules.yaml`) is **Not Supported** [Verify/Update this status if RooCode changes]. This limits direct cross-file rule inheritance."
    explicitness_mandate: (string) "**Mandatory (V2.1):** All rules MUST be explicitly defined within the `.clinerules` file. Placeholder comments indicating inheritance (e.g., `# --- INHERITED...`) are FORBIDDEN. Modes MUST copy the full standard rule content into their file."
    documentation_convention: (string) "**Optional:** While rules must be explicit, modes MAY include comments referencing the source standard section for clarity. Example: `# Standard Error Handling Protocol - See docs/standards/clinerules_standard_v2.1.md Section: general`."
  example:
    ```yaml
    rule_inheritance_guidelines:
      yaml_anchors: "YAML anchors (`&`) and aliases (`*`) MAY be used within this file for reusing common blocks, if supported by the parser. Verify support."
      external_includes: "Current RooCode parser status regarding external file includes (`!include`) is Not Supported." # Verify/Update
      explicitness_mandate: "Mandatory (V2.1): All rules MUST be explicitly defined within the `.clinerules` file. Placeholder comments indicating inheritance (e.g., `# --- INHERITED...`) are FORBIDDEN. Modes MUST copy the full standard rule content into their file."
      documentation_convention: "Optional: Modes MAY include comments referencing the source standard section for clarity. Example: `# Standard Error Handling Protocol - See docs/standards/clinerules_standard_v2.1.md Section: general`."
    ```

## Archetype A: Simple Orchestrated Task Mode

Includes Common Sections plus:

`input_schema`:
  type: object
  description: Defines the expected input data structure received from the orchestrator. Use JSON schema or descriptive format.
  example:
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

`output_schema`:
  type: object
  description: Defines the structure of the result returned to the orchestrator.
  example:
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

`kb_interaction_protocols`: (Optional/Minimal for Archetype A)
  type: object
  description: Defines limited KB interaction rules, if any.
  fields:
    read_access: (array) List allowed KB directory paths or entry types for reading. **STRICT:** Default is no read access. Use V18.3.4 direct access patterns (`read_file`, `search_files`). Paths MUST start with `philosophy-knowledge-base/`.
    write_access: (array) List allowed KB directory paths or entry types for writing. **STRICT:** Default is no write access. Writes MUST conform to V18.3.4 KB schema. Paths MUST start with `philosophy-knowledge-base/`.
    verification: (string) Typically "N/A" for simple modes.
  example:
    ```yaml
    kb_interaction_protocols:
      read_access:
        - "philosophy-knowledge-base/concepts/" # Allowed to read concepts
      write_access: [] # No write access allowed
      verification: "N/A"
    ```

`script_execution`: (If Applicable)
  type: object
  description: Defines rules for executing external scripts via `execute_command`.
  fields:
    script_path: (string) Path to the executable script (relative to workspace root).
    input_format: (string) Method for passing data (e.g., "stdin", "command_line_args", "temp_file").
    output_parsing: (string) How script output is captured and parsed (e.g., "stdout_json", "stdout_text", "output_file").
    error_handling: (string) How script errors (non-zero exit codes, stderr output) are detected and reported using `error_reporting_protocols` (e.g., `SCRIPT_EXEC_FAIL`).
  example:
    ```yaml
    script_execution:
      script_path: "scripts/format_text.py"
      input_format: "stdin"
      output_parsing: "stdout_text"
      error_handling: "Capture stderr, check exit code. Report using SCRIPT_EXEC_FAIL via error_reporting_protocols."
    ```

## Archetype B: Complex Analysis/Generation Mode

Includes Common Sections plus:

`input_schema`:
  type: object
  description: Defines the expected input data structure received from the orchestrator (often more complex, e.g., multiple KB IDs, source file paths, analysis parameters).
  example:
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

`output_schema`:
  type: object
  description: Defines the structure of the result returned to the orchestrator (often includes new KB entry IDs, verification status, etc.).
  example:
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

`workspace_management`: (Optional)
  type: object
  description: Defines rules if the mode requires a dedicated temporary workspace (e.g., for complex draft generation).
  fields:
    root: (string) Path relative to workspace root (e.g., `essay_prep/temp_drafts/`).
    structure: (array) List of expected subdirectories within the root.
    cleanup: (string) Rules for cleanup (e.g., "Delete on task completion", "Keep intermediate files").
  example:
    ```yaml
    workspace_management:
      root: "essay_prep/active_draft/"
      structure: ["sections", "notes", "verification_reports"]
      cleanup: "Keep intermediate files until explicit cleanup command."
    ```

`kb_interaction_protocols`: (Mandatory & Detailed for Archetype B)
  type: object
  description: **STRICT PROTOCOL** defining all interactions with the `philosophy-knowledge-base/`.
  fields:
    read_access: (array) List allowed KB directory paths or entry types. **STRICT:** Use V18.3.4 direct access patterns (`read_file`, `search_files`). Must specify how context tags are used for filtering. Paths MUST start with `philosophy-knowledge-base/`.
    write_access: (array) List allowed KB directory paths or entry types. **STRICT:** Writes MUST conform to the full V18.3.4 KB entry schema (YAML frontmatter + Markdown content, see Arch Doc Sec 6), including population of relevant rigor fields (`positive_determination`, `negative_determination`, `presuppositions`, `counter_arguments`, etc.). **MUST** generate and use unique IDs. **MUST** ensure critical linking fields (`source_ref_keys`, `extraction_markers`, `related_ids`) are accurately populated based on analysis. Use `write_to_file` or `insert_content` appropriately. Paths MUST start with `philosophy-knowledge-base/`.
    querying: (string) Guidelines for constructing KB queries using `search_files` or logic based on `read_file`. Emphasize using context tags and relationship links (`related_ids`) for efficient and relevant data retrieval. Avoid reading entire KB directories.
    kb_maintenance_interaction: (string) **V2 Update:** Define conditions under which the mode should flag potential KB inconsistencies (e.g., broken links, schema violations detected during read, conflicting information) to the `Orchestrator`. **Modes do NOT trigger maintenance directly.** `Orchestrator` delegates checks to `MetaReflector` or `VerificationAgent` as appropriate.
    validation_hooks: (string) **V2 Addition:** "Modes performing KB writes SHOULD attempt self-validation against schemas/rules in `philosophy-knowledge-base/_operational/formatting_templates_rules/` before writing. `VerificationAgent` performs mandatory post-write checks during workflows."
    rigor_field_handling: (string) **V2 Addition:** "Modes MUST explicitly populate relevant rigor fields (determinacy, presuppositions, etc.) as defined in the V18.3.4 KB Entry Format (Arch Doc Sec 6) when creating/updating KB entries."
  example:
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

`conceptual_determinacy`: (Guideline Section - Adaptable)
  type: object
  description: Guidelines for ensuring philosophical rigor regarding concept clarity. Adapt requirements based on mode's function.
  fields:
    requirements: (object) Define expectations for generated concepts.
        *   `negative_definition`: (string) e.g., `required`, `recommended`, `optional`.
        *   `disambiguation_protocol`: (string) e.g., `required_if_ambiguous`, `optional`.
        *   `ordinary_language_contrast`: (string) e.g., `recommended`, `optional`.
    implementation: (string) Guidelines for how the mode should achieve these requirements during analysis/generation. Reference specific V18.3.4 KB schema fields (`positive_determination`, `negative_determination`, `ordinary_language_contrast`, `ambiguities`, `related_terms`).
  example:
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

`evidence_standards`: (Guideline Section + Strict Workflow)
  type: object
  description: Guidelines and strict workflow for handling and verifying evidence.
  fields:
    requirements: (object) General standards for evidence.
        *   `source_preference`: (string) e.g., "Prefer primary sources, use secondary critically".
        *   `citation_format`: (string) e.g., "Use KB reference IDs (`source_ref_keys`) and `extraction_markers`".
        *   `quotation_accuracy`: (string) e.g., "Must match source chunk exactly".
    verification_workflow: **STRICT PROTOCOL**
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
  example:
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

`version_control`: (If Applicable)
  type: object
  description: Defines integration with Git for modes managing versioned artifacts (e.g., essay drafts). References Arch V18.3.4 Section 8.
  fields:
    integration: (string) How Git is used (e.g., "Via `execute_command`").
    commit_strategy: (string) When commits should occur (e.g., "After each major section completion", "On explicit user command via orchestrator"). Define commit message format.
    branching: (string) Branching strategy, if applicable (e.g., "Work on feature branches coordinated by orchestrator").
    checkpoint_awareness: (string) "Be aware of RooCode Checkpoints (Arch Sec 8.1) for task-level rollback; Git is for persistent, verified changes."
  example (for `philosophy-essay-prep`):
    ```yaml
    version_control:
      integration: "Via `execute_command` tool to interact with Git."
      commit_strategy: |
        Commits should occur after significant milestones (e.g., thesis finalized, outline approved, major draft section completed), typically triggered by the Orchestrator based on workflow state.
        Commit Message Format: "feat(essay-prep): [Action] for [Essay Topic/ID] - [Brief Description]" (e.g., "feat(essay-prep): Finalize thesis for Hegel Spirit Essay - Stored KB ID: thesis_hegel_spirit_001")
      branching: "Work MAY occur on feature branches (e.g., `feature/essay-hegel-spirit`) coordinated by Orchestrator, merging back to main/develop after verification."
      checkpoint_awareness: "Be aware of RooCode Checkpoints (Arch Sec 8.1) for task-level rollback; Git is for persistent, verified changes to essay artifacts (potentially stored in `workspace_management.root`)."
      tool_usage: |
        Use `execute_command` for standard Git operations (`git add [file]`, `git commit -m "[message]"`, `git push`, `git checkout`, `git merge`). Ensure commands are executed in the correct directory (likely workspace root or `workspace_management.root`). Report `GIT_COMMAND_FAIL` on errors.