# Standard `.clinerules` Structures for Philosophy Modes (V2.5 - Based on V18.3.4 Arch)

**Version:** 2.5
**Date:** 2025-05-06

**Purpose:** This document defines standard structures and guidelines for `.clinerules` files used by philosophy-focused modes within the `philoso-roo` system (formerly SPARC).

**Background:** This V2.5 standard supersedes V2.4. It restores specific details and adds examples to sections like `conceptual_determinacy_guidelines` and `evidence_standards` based on user feedback [See Feedback Log: 2025-05-06 01:45:00], ensuring critical rigor guidelines are explicit while maintaining the flexible formatting for `mode_specific_workflows` examples introduced in V2.4. It retains the V2.3 introduction of the `mode_specific_workflows` section and the V2.2 removal of the `rule_inheritance_guidelines` section. It addresses feedback regarding implicit inheritance comments and wasteful headers identified in V2.0. It incorporates enhancements proposed in `docs/proposals/clinerules_standard_enhancements_v1.md` and aligns with the V18.3.4 system architecture (`docs/architecture/architecture_v18.md`), which features direct KB/Memory Bank access, distributed KB maintenance, MCP integration, and RooCode Checkpoints. **Note:** During updates, modes MUST check for the presence of the optional `mode_specific_workflows` section and preserve its content if it exists.

**Inspiration:** The structure and detail level remain inspired by robust mode examples (e.g., `.clinerules-philosophy-essay-prep`), adapted for the current orchestrated system.

**Core Principles:**
*   **Consistency:** Predictable structure for mode configuration.
*   **Rigor:** Embedded requirements for philosophical rigor.
*   **Reliability:** Strict protocols for critical workflows (KB interaction, verification, error handling, logging, concurrency).
*   **Orchestration Alignment:** Focus on interaction with `philosophy-orchestrator` and direct interaction with `philosophy-knowledge-base/` and `phil-memory-bank/`.
*   **Adaptability:** Flexibility where appropriate, strictness for critical operations.
*   **Explicitness:** Rules MUST be clear, unambiguous, and self-contained within the `.clinerules` file. No implicit inheritance via comments.
*   **Preservation:** Custom, mode-specific operational logic should be preserved during standard updates via the `mode_specific_workflows` section.

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
          <thinking> * Check if phil-memory-bank/ exists. Read if yes, suggest creation if no. </thinking>
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
      # Example Log Entry:
      # ### [2025-05-06 01:50:00] - KB Concept Identified
      # - **Details:** Identified 'Being' as a key concept in Hegel_SoL_pp59-82.md analysis.
      # - **KB Interaction:** Preparing to write new Concept entry.
      # - **Input:** Analysis results from reading.
      # - **Output:** Draft Concept entry content.
      # - **Cross-ref:** [Hegel_SoL_pp59-82.md]
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
      # Example Error Message:
      # "[KB_SCHEMA_VIOLATION] in philosophy-class-analysis: Attempted to write Concept entry without required 'definition' field. Resource: philosophy-knowledge-base/concepts/new_concept_xyz.md, Line: N/A."
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
        - server_name: "zlibrary-mcp" # Example for a different mode
          tool_name: "search_books"
      security_mandate: "API keys/secrets MUST NOT be included in `.clinerules` or code. Access MUST be managed via environment variables on the MCP server."
      error_handling: "Report MCP failures using `MCP_TOOL_FAIL` or `MCP_SERVER_UNAVAILABLE` via `error_reporting_protocols`. Follow standard escalation. Consider tool-specific retry logic if appropriate."
      usage_guidelines: |
        Use 'brave_web_search' for finding secondary sources or external definitions relevant to the current philosophical context. Formulate specific queries.
        Use 'fetch_url' for retrieving content from specific academic URLs found via search or KB refs. Prioritize fetching from reputable domains.
        Use 'search_books' (if allowed) to find relevant monographs or edited volumes based on keywords or author searches.
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
      # Example Lock File Name Calculation (Conceptual):
      # Target Path: philosophy-knowledge-base/concepts/being.md
      # MD5 Hash (example): d41d8cd98f00b204e9800998ecf8427e
      # Lock File Path: phil-memory-bank/locks/d41d8cd98f00b204e9800998ecf8427e.lock
    ```

`mode_specific_workflows`: (**Optional**)
  type: object
  description: |
    This OPTIONAL section allows modes to define detailed, step-by-step operational logic or procedures unique to their function that are not adequately captured by the standard protocol sections (e.g., `kb_interaction_protocols`, `conceptual_determinacy`).
    It serves as a persistent record of complex, custom workflows, ensuring this logic is not lost during `.clinerules` updates or refactoring.
    Use clear, descriptive keys for each workflow.
    **Formatting Flexibility:** Define steps using a list. For each step:
    - Use `action:` for a narrative description of the step's purpose or process.
    - **Optionally**, include `tools:`, `input:`, `output:`, `input_schema:`, `output_schema:` **only when specifying the exact tool, data structure, or parameters is critical for clarity or correctness.** For simpler internal processing or transitions, a narrative `action:` description is sufficient. Avoid ambiguous terms like "Internal Logic"; describe the actual processing.
    **IMPORTANT:** Modes performing `.clinerules` updates (e.g., `code`, `system-modifier`) MUST check for this section and preserve its content if present.
  example:
    ```yaml
    mode_specific_workflows:
      evidence_retrieval_and_linking:
        description: "Workflow for finding, verifying, and linking evidence to a specific claim in an essay draft."
        steps:
          - step: 1
            action: "Parse input essay section text to identify claims needing evidence."
            # Simple internal analysis, no specific tool/schema needed here.
          - step: 2
            action: "For each claim, extract keywords and search KB for relevant arguments/concepts."
            tools: ["search_files"] # Tool is critical here
            input: "Keywords, KB paths (`philosophy-knowledge-base/arguments/`, `philosophy-knowledge-base/concepts/`)"
            output: "List of potential KB entry file paths"
          - step: 3
            action: "Read content of potential KB entries."
            tools: ["read_file"] # Tool is critical
            input: "List of KB entry file paths"
            output: "Content of KB entries"
          - step: 4
            action: "Analyze KB entry content for relevance and strength as evidence for the claim."
            # Internal analysis, narrative description is sufficient.
          - step: 5
            action: "If strong evidence found, retrieve `source_ref_keys` and `extraction_markers` from the KB entry's YAML frontmatter."
            # Internal parsing, narrative description is sufficient.
          - step: 6
            action: "Format citation using retrieved keys/markers for insertion into draft, adhering to the specified citation style guide."
            # Internal formatting, narrative description is sufficient.
          - step: 7
            action: "If no strong KB evidence found, formulate a targeted search query for external sources based on the claim and related keywords."
            # Internal query generation, narrative description is sufficient.
          - step: 8
            action: "Execute web search using MCP."
            tools: ["use_mcp_tool"] # Tool and arguments are critical
            input: "{ server_name: 'brave-search', tool_name: 'brave_web_search', arguments: { query: [query string] } }"
            output: "Search results object"
          - step: 9
            action: "Analyze search results for promising secondary sources."
            # Internal analysis, narrative description is sufficient.
          - step: 10
            action: "Fetch content from relevant URLs using MCP."
            tools: ["use_mcp_tool"] # Tool and arguments are critical
            input: "{ server_name: 'fetcher', tool_name: 'fetch_url', arguments: { url: [URL] } }"
            output: "Fetched content (Markdown)"
          - step: 11
            action: "Analyze fetched content for evidence. If found, delegate KB update task to the appropriate mode (e.g., `philosophy-text-processor` or `philosophy-secondary-lit`)."
            tools: ["new_task"] # Tool is critical for delegation
            input: "Fetched content analysis, claim text, delegation instructions"
            output: "Delegation task ID or confirmation"
          - step: 12
            action: "Log all actions, findings, KB interactions, and delegations in the operational log."
            tools: ["insert_content"] # Tool is critical for logging
            input: "Formatted log entry, target_file path"
            output: "Confirmation of log update"

      dialectical_contradiction_resolution:
        description: "Workflow for analyzing and attempting to resolve contradictions between two KB arguments."
        steps:
          - step: 1
            action: "Read the content of both input KB argument entries."
            tools: ["read_file"] # Tool is critical
            input: "File paths for Argument ID 1, Argument ID 2"
            output: "Content of both arguments"
          - step: 2
            action: "Analyze argument structures, premises, conclusions, and linked evidence (`source_ref_keys`, `extraction_markers`) by parsing YAML frontmatter and Markdown content."
            # Internal analysis/parsing, narrative description is sufficient.
          - step: 3
            action: "Identify specific points of contradiction (e.g., conflicting premises, differing interpretations of evidence, incompatible conclusions)."
            # Internal analysis, narrative description is sufficient.
          - step: 4
            action: "Search KB for related concepts, methods, or meta-reflections that might offer a resolution."
            tools: ["search_files"] # Tool and paths are critical
            input: "Keywords related to contradiction points, KB paths (`philosophy-knowledge-base/concepts/`, `philosophy-knowledge-base/methods/`, `philosophy-knowledge-base/meta-reflections/`)"
            output: "List of potentially relevant KB entry file paths"
          - step: 5
            action: "Read and analyze potentially relevant KB entries for resolution strategies."
            tools: ["read_file"] # Tool is critical
            input: "List of KB entry file paths"
            output: "Analysis of potential resolutions"
          - step: 6
            action: "If a resolution is identified (e.g., a mediating concept, a necessary distinction): Draft a new KB 'Relationship' entry detailing the resolution."
            # Internal drafting, narrative description is sufficient.
          - step: 7
            action: "Populate rigor fields (`resolution_attempts`, `synthesis_level`) in the new Relationship entry's YAML frontmatter. Link the original arguments via `related_ids`."
            # Internal YAML editing, narrative description is sufficient.
          - step: 8
            action: "Write the new Relationship entry to the KB, applying advisory lock if necessary."
            tools: ["write_to_file"] # Tool and concurrency check are critical
            input: "File path (`philosophy-knowledge-base/relationships/`), updated Relationship entry content"
            output: "Confirmation of write"
          - step: 9
            action: "If no resolution is found: Draft a new KB 'Question' entry or update an existing one detailing the unresolved contradiction."
            # Internal drafting/searching/updating, narrative description is sufficient. May use search_files, read_file, write_to_file, apply_diff.
          - step: 10
            action: "Populate rigor fields (`contradiction_points`, `unresolved_tension`, `scope_of_question`) in the Question entry's YAML frontmatter."
            # Internal YAML editing, narrative description is sufficient.
          - step: 11
            action: "Write/Update the Question entry in the KB, applying advisory lock if necessary."
            tools: ["write_to_file", "apply_diff"] # Tools and concurrency check are critical
            input: "File path (`philosophy-knowledge-base/questions/`), updated Question entry content"
            output: "Confirmation of write/update"
          - step: 12
            action: "If resolution seems possible but requires broader context or different expertise, report findings and suggest delegation to Orchestrator (e.g., to MetaReflector)."
            # Internal analysis and reporting, narrative description is sufficient.
          - step: 13
            action: "Log all analysis steps, findings, KB interactions (reads/writes), and any recommendations in the operational log."
            tools: ["insert_content"] # Tool is critical for logging
            input: "Formatted log entry, target_file path"
            output: "Confirmation of log update"
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
          description: "List of paths to relevant source materials (e.g., processed readings)."
        analysis_parameters:
          type: object
          properties:
            depth:
              type: string
              enum: ["surface", "deep", "exhaustive"]
            focus:
              type: string
              description: "Specific aspect to focus analysis on (e.g., 'presuppositions', 'evidence_links')."
      required: ["analysis_target_ids"]
    ```

`output_schema`:
  type: object
  description: Defines the structure of the result returned to the orchestrator (often includes analysis summaries, generated content, new KB entry IDs, verification status).
  example:
    ```yaml
    output_schema:
      type: object
      properties:
        status:
          type: string
          enum: ["success", "partial_success", "failure"]
        analysis_summary:
          type: string
          description: "Summary of the analysis performed."
        generated_content_path:
          type: string
          description: "(Optional) Path to newly generated file (e.g., essay draft section)."
        new_kb_entry_ids:
          type: array
          items:
            type: string
          description: "(Optional) List of IDs for newly created KB entries."
        verification_status:
          type: string
          enum: ["verified", "unverified", "verification_failed"]
        rigor_assessment:
          type: object
          # ... structure defined by rigor_fields
        error_details: # Present only if status is failure
          type: object
          # ... follows error_reporting_protocols.error_message_format
      required: ["status"]
    ```

`kb_interaction_protocols`: (**STRICT PROTOCOL** for Archetype B)
  type: object
  description: Defines rules for direct interaction with the Knowledge Base (`philosophy-knowledge-base/`). Aligns with Arch V18.3.4 Section 11.
  fields:
    read_access: (array) List allowed KB directory paths or entry types for reading. **STRICT:** Use V18.3.4 direct access patterns (`read_file`, `search_files`). Paths MUST start with `philosophy-knowledge-base/`.
    write_access: (array) List allowed KB directory paths or entry types for writing. **STRICT:** Use V18.3.4 direct access patterns (`write_to_file`, `apply_diff`, `insert_content`). Writes MUST conform to V18.3.4 KB schema. Paths MUST start with `philosophy-knowledge-base/`. Apply concurrency protocols.
    schema_enforcement: (string) **MUST** state: "All writes MUST strictly adhere to the KB entry schemas defined in Arch V18.3.4 Appendix A. Validate structure before writing."
    relationship_mandate: (string) **MUST** state: "New KB entries (concepts, arguments, etc.) MUST be linked to existing entries via the `related_ids` field or by creating/updating Relationship entries. Orphaned entries are prohibited."
    rigor_fields_population: (string) **MUST** state: "Modes MUST populate relevant rigor fields (e.g., `conceptual_determinacy`, `evidence_strength`, `presuppositions`, `contradiction_points`, `resolution_attempts`) based on analysis, as defined in Arch V18.3.4 Appendix A."
    verification_hooks: (string) **MUST** state: "Modes MUST check for and respect verification status flags (`verification_status`, `verified_by`, `verification_date`) in KB entries. Trigger re-verification via `Orchestrator` if significant changes are made to verified entries."
    maintenance_reporting: (string) **MUST** state: "Report suspected KB inconsistencies, schema violations, or maintenance needs (e.g., outdated links, conflicting info) to `Orchestrator` for potential delegation to `MetaReflector` or `VerificationAgent`."
  example:
    ```yaml
    kb_interaction_protocols:
      read_access: # Example for a mode analyzing arguments and concepts
        - "philosophy-knowledge-base/concepts/"
        - "philosophy-knowledge-base/arguments/"
        - "philosophy-knowledge-base/questions/"
        - "philosophy-knowledge-base/relationships/"
        - "philosophy-knowledge-base/processed_sources/"
        - "philosophy-knowledge-base/references/"
      write_access: # Example for a mode creating arguments and questions
        - "philosophy-knowledge-base/arguments/"
        - "philosophy-knowledge-base/questions/"
        - "philosophy-knowledge-base/relationships/" # To link new args/questions
      schema_enforcement: "All writes MUST strictly adhere to the KB entry schemas defined in Arch V18.3.4 Appendix A. Validate structure before writing."
      relationship_mandate: "New KB entries (concepts, arguments, etc.) MUST be linked to existing entries via the `related_ids` field or by creating/updating Relationship entries. Orphaned entries are prohibited."
      rigor_fields_population: "Modes MUST populate relevant rigor fields (e.g., `conceptual_determinacy`, `evidence_strength`, `presuppositions`, `contradiction_points`, `resolution_attempts`) based on analysis, as defined in Arch V18.3.4 Appendix A."
      verification_hooks: "Modes MUST check for and respect verification status flags (`verification_status`, `verified_by`, `verification_date`) in KB entries. Trigger re-verification via `Orchestrator` if significant changes are made to verified entries."
      maintenance_reporting: "Report suspected KB inconsistencies, schema violations, or maintenance needs to `Orchestrator` for potential delegation to `MetaReflector` or `VerificationAgent`."
    ```

`conceptual_determinacy_guidelines`:
  type: object
  description: Defines rules for ensuring clarity, precision, and consistency in concepts and arguments. **V2.5 Enhancement:** Restored specific methods and added sense tracking.
  fields:
    definition_standard: (string) Requirement for clear, unambiguous definitions.
    scope_management: (string) Guidelines for defining and respecting the scope of concepts/arguments.
    ambiguity_identification: (string) How to identify potential ambiguities.
    disambiguation_methods: (string) Specific methods for resolving identified ambiguities.
    marking_ambiguity: (string) Protocol for marking persistent ambiguities in the KB.
    sense_tracking: (string) Protocol for tracking changes in a concept's meaning.
    consistency_checks: (string) How to check for internal consistency and consistency with related KB entries.
  example:
    ```yaml
    conceptual_determinacy_guidelines:
      definition_standard: "Define concepts using necessary and sufficient conditions where possible. Avoid circularity. Use consistent terminology aligned with KB conventions."
      scope_management: "Clearly state the intended scope and limitations of arguments and concepts (e.g., specific text, author, historical period). Avoid overgeneralization."
      ambiguity_identification: "Identify potential ambiguities in terms or phrasing within the text or across related KB entries by comparing definitions, usage contexts, and relationships."
      disambiguation_methods: |
        Employ methods like:
        - **Negative Definition:** Define what the concept *is not* to narrow its meaning.
        - **Ordinary Language Contrast:** Compare the philosophical usage with its common usage to highlight specific technical meanings.
        - **Contextual Analysis:** Examine how the term is used within the specific text, author's corpus, or related KB entries.
        - **KB Search:** Look for existing definitions, distinctions, or relationship entries in the KB.
        - **External Resources:** Use MCP tools (e.g., `brave-search`) to consult philosophical dictionaries or secondary literature if necessary.
        Document the methods used and the resulting clarifications.
      marking_ambiguity: "If ambiguity persists after analysis, explicitly mark the concept/term as ambiguous in the KB entry (e.g., using `ambiguity_status: 'persistent'` or `conceptual_determinacy: 'low'`) and detail the nature of the ambiguity in the entry's body or a dedicated rigor field. Suggest generating a KB Question entry if the ambiguity warrants further investigation."
      sense_tracking: "Track subtle changes in a concept's sense across different works, authors, or within a single text. Document these shifts in relevant KB entries (e.g., in a dedicated 'sense_evolution' field, notes, or via linked Relationship entries connecting different conceptualizations)."
      consistency_checks: "Cross-reference new/modified entries with related KB entries (`related_ids`) to ensure logical consistency. Report unresolved inconsistencies via `maintenance_reporting`."
      # Example Application:
      # When analyzing 'Being' in Hegel vs. Heidegger:
      # 1. Identify ambiguity (different core meanings).
      # 2. Use contextual analysis (within each philosopher's work), negative definition (what 'Being' is *not* for each), and ordinary language contrast.
      # 3. Track sense changes: Create separate KB Concept entries (e.g., 'Being_Hegel', 'Being_Heidegger') or use Relationship entries to link a general 'Being' concept to specific interpretations, noting the evolution/differences.
      # 4. Mark ambiguity: If a specific passage remains ambiguous after analysis, add `ambiguity_status: 'passage_specific'` to the relevant Argument or Extraction entry.
    ```

`evidence_standards`:
  type: object
  description: Defines rules for sourcing, evaluating, and linking evidence. **V2.5 Enhancement:** Added example for linking mechanism.
  fields:
    source_preference: (string) Preferred order of evidence sources (e.g., KB primary sources, KB secondary sources, external academic sources).
    evaluation_criteria: (string) Criteria for evaluating evidence strength (e.g., relevance, authoritativeness, logical connection, verification status).
    linking_mechanism: (string) **STRICT:** How evidence is linked. **MUST** state: "Use `source_ref_keys` (linking to KB Reference entries) and `extraction_markers` (linking to specific locations in processed source files) in KB entries to ensure precise traceability back to source material paragraphs/sections within the hierarchical `source_materials/processed/` structure."
    verification_requirement: (string) When evidence requires verification by `VerificationAgent`.
  example:
    ```yaml
    evidence_standards:
      source_preference: "1. Verified KB Primary Source extractions. 2. Verified KB Secondary Source analyses. 3. External academic sources (via MCP search/fetch). 4. Unverified KB entries (use with caution, flag for verification)."
      evaluation_criteria: "Assess relevance to claim, authoritativeness of source (consider author, publication venue, date), logical strength of connection, verification status in KB, potential biases."
      linking_mechanism: |
        Use `source_ref_keys` (linking to KB Reference entries) and `extraction_markers` (linking to specific locations in processed source files) in KB entries to ensure precise traceability back to source material paragraphs/sections within the hierarchical `source_materials/processed/` structure.
        # Example: An Argument entry supporting a claim about Hegel's concept of 'Nothing' might have:
        # source_ref_keys: [hegel_sol_1812] # Links to the KB Reference entry for Science of Logic
        # extraction_markers: ["Hegel_ScienceOfLogic_pp59-82.md#section-1-paragraph-5"] # Points to a specific paragraph in the processed source file
      verification_requirement: "Claims based on unverified KB entries or newly fetched external sources MUST be flagged for verification by `VerificationAgent` via `Orchestrator`."
    ```

`version_control`: (Optional, if mode manages workspace files like drafts)
  type: object
  description: Defines protocols for interacting with Git via `execute_command`.
  fields:
    branching_strategy: (string) Recommended branching model (e.g., "feature branches", "main only").
    commit_frequency: (string) When commits should ideally occur (e.g., "after each significant change", "end of task").
    commit_message_format: (string) Standard format for commit messages (e.g., Conventional Commits).
    conflict_resolution: (string) How merge conflicts should be handled (e.g., "report to Orchestrator", "attempt automatic resolve").
  example:
    ```yaml
    version_control:
      branching_strategy: "Work on 'main' branch unless otherwise directed by Orchestrator."
      commit_frequency: "Commit significant changes to drafts or outlines at logical breakpoints or end of task."
      commit_message_format: "feat: [Short description]\n\n[Optional longer description]\nKB-Refs: [KB IDs]"
      conflict_resolution: "Report merge conflicts immediately to Orchestrator. Do not force push."
    ```

## Change Log
*   **V2.5 (2025-05-06):** Restored specific details to `conceptual_determinacy_guidelines` (negative definition, ordinary language contrast, sense tracking, marking ambiguity) and `evidence_standards`. Added more examples throughout for clarity, per user feedback. Maintained flexible formatting for `mode_specific_workflows`.
*   **V2.4 (2025-05-05):** Refined `mode_specific_workflows` examples for flexible formatting (narrative vs. detailed steps). Updated section description.
*   **V2.3 (2025-05-05):** Added optional `mode_specific_workflows` section with examples and preservation note.
*   **V2.2 (2025-05-05):** Removed `rule_inheritance_guidelines` section entirely. Enforced absolute explicitness.
*   **V2.1 (2025-05-05):** Removed implicit inheritance comments and wasteful headers. Mandated explicit rules. Added batching recommendation to `operational_logging`. Enhanced `apply_diff` error handling.
*   **V2.0 (2025-05-05):** Aligned with Arch V18.3.4. Added `mcp_interaction_protocols` and `concurrency_coordination_protocols`. Refined KB/MB interaction for direct access. Added rigor fields and verification hooks. Added `script_execution` section. Defined Archetypes A & B.
*   **V1.0 (2025-05-03):** Initial version based on analysis of existing `.clinerules` and user feedback.