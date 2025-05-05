# Proposal: `.clinerules` Standard Enhancements (V1 -> V2)

**Date:** 2025-05-05
**Based On:**
*   `docs/standards/clinerules_standard_v1.md`
*   `docs/architecture/architecture_v18.md` (V18.3.4)
*   `docs/reports/architecture_v18_evaluation_v1.md` (V7 - Rec 3.10, 3.15)
*   `docs/blueprints/mcp_integration_v1.md`

## 1. Introduction

This document proposes enhancements to the `clinerules_standard_v1.md` to create Version 2. The goal is to align the standard with the V18.3.4 architecture, incorporate feedback from the V7 evaluation report, and provide clearer, more robust guidelines for mode developers.

## 2. Proposed Enhancements

### 2.1. General Updates

*   **Update Version References:** Change all references from V18.3 to V18.3.4 throughout the document.
*   **Remove KB Doctor References:** Replace mentions of `philosophy-kb-doctor` with the current distributed maintenance roles (`philosophy-orchestrator`, `philosophy-meta-reflector`, `philosophy-verification-agent`) where appropriate (e.g., in `kb_interaction_protocols.kb_doctor_interaction`). Rename the section if necessary (e.g., `kb_maintenance_interaction`).
*   **Add Operational Context Section:** Introduce a new common section (e.g., `operational_context_protocols`) detailing rules for direct interaction with `phil-memory-bank/`.
    *   Specify that modes MUST write logs to their designated `phil-memory-bank/mode-specific/[mode_slug].md` file.
    *   Specify that modes CAN read global context (`activeContext.md`, `globalContext.md`) and other mode logs as needed, guided by `Orchestrator` context.
    *   Reinforce strict separation: NO KB data in `phil-memory-bank/`.

### 2.2. MCP Integration (New Section 3.x)

*   **Title:** `mcp_interaction_protocols`
*   **Reference Blueprint:** Explicitly reference `docs/blueprints/mcp_integration_v1.md` for the "Distributed MCP Calls" strategy.
*   **Mode Responsibility:** Modes requiring external data MUST use appropriate MCP tools (`use_mcp_tool`).
*   **Security:** Mandate that API keys/secrets are NEVER included in `.clinerules` or code; they MUST be accessed only by the MCP server via environment variables.
*   **Error Handling:** Define standard error reporting codes (e.g., `MCP_TOOL_FAIL`, `MCP_SERVER_UNAVAILABLE`) and require modes to follow `error_reporting_protocols` when MCP calls fail (e.g., log error, report structured error to Orchestrator). Include retry logic guidelines if appropriate for the tool.
*   **Example Snippet:** Provide a YAML example within `.clinerules` showing how a mode might define its MCP tool usage:
    ```yaml
    mcp_interaction_protocols:
      allowed_tools:
        - server_name: "brave-search"
          tool_name: "brave_web_search"
        - server_name: "fetcher"
          tool_name: "fetch_url"
      usage_guidelines: |
        Use 'brave_web_search' for general philosophical queries or finding secondary sources.
        Use 'fetch_url' to retrieve content from specific article URLs identified via search or KB references.
        Handle potential timeouts and API errors gracefully, reporting failures via standard protocols.
        Ensure queries are specific and respect API usage limits.
    ```

### 2.3. KB Interaction Protocols (Section 5.4 Enhancements)

*   **Update Maintenance Interaction:** Replace `kb_doctor_interaction` with `kb_maintenance_interaction`. Describe how modes should report inconsistencies or trigger checks via `Orchestrator` for `MetaReflector` or `VerificationAgent`.
*   **Validation Hooks:** Add guideline: Modes performing KB writes SHOULD attempt self-validation against schemas defined in `philosophy-knowledge-base/_operational/formatting_templates_rules/` before writing. `VerificationAgent` performs mandatory post-write checks during workflows.
*   **Rigor Field Handling:** Add guideline: Modes MUST explicitly populate relevant rigor fields (determinacy, presuppositions, etc.) as defined in the V18.x KB Entry Format (Arch Doc Sec 6) when creating/updating KB entries.

### 2.4. Memory Bank / Operational Logging (Section 3.5 Enhancements)

*   **Batching Guideline:** Add to `operational_logging.guidelines`: "Recommend batching log entries where feasible (e.g., buffer 3-5 entries related to a single sub-task) before performing a single `insert_content` operation to `target_file` to reduce I/O frequency."

### 2.5. Error Handling / File Tools (Section 3.4 / General Enhancements)

*   **`apply_diff` Context Mismatch:** Add specific guidance to `general.error_handling_protocol`: "If `apply_diff` fails with a context mismatch or low similarity: 1. Re-read the target file section using `read_file` with `start_line`/`end_line`. 2. Compare the expected `SEARCH` block with the actual content read. 3. If different, adjust the `SEARCH` block and retry `apply_diff`. 4. If identical, investigate other causes (tool bug?) and consider alternative tools (`insert_content`, `search_and_replace`) or escalate per 'Three Strikes' rule."

### 2.6. Multi-Mode Coordination & Concurrency (New Section 3.x)

*   **Title:** `concurrency_coordination_protocols`
*   **Risk Acknowledgment:** Explicitly state the risk of race conditions/data corruption with direct file access by multiple modes.
*   **Locking Mechanism:** Recommend a simple advisory file locking mechanism:
    *   **Protocol:** Before critical write operations (especially `write_to_file` or `apply_diff` on shared KB/MB files), check for a lock file `phil-memory-bank/locks/[file_path_hash].lock`. If absent, create it. Perform write. Delete lock file. If present, wait briefly and retry, or report conflict to `Orchestrator`.
    *   **Implementation:** Define this protocol clearly. Note its advisory nature (requires mode cooperation).
*   **Orchestrator Sequencing:** Recommend that `Orchestrator` should sequence tasks known to target the same critical KB files/sections whenever possible to minimize potential conflicts.

### 2.7. Rule Inheritance (New Section or Guideline)

*   **Title:** `rule_inheritance_guidelines` (or integrate into relevant sections)
*   **YAML Anchors:** Explain the use of YAML anchors (`&`) and aliases (`*`) for defining reusable rule blocks within a single `.clinerules` file, if supported by the parser. Provide a simple example.
*   **External Includes:** State whether the current RooCode `.clinerules` parser supports external file includes (e.g., `!include shared_rules.yaml`). If not, state this limitation.
*   **Documentation Convention:** If direct inheritance is limited, recommend a documentation convention where modes explicitly state which standard rules (e.g., "Standard SPARC Error Handling Protocol V1.2") they adhere to, referencing a central standards document.

## 3. Implementation

These enhancements should be incorporated into a new version of the standards document, `docs/standards/clinerules_standard_v2.md`. Existing `.clinerules` files will need to be reviewed and updated for compliance with V2 as part of subsequent integration tasks.