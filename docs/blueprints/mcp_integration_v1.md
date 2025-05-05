# MCP Integration Blueprint V1

**Date:** 2025-05-05
**Version:** 1.0
**Status:** Draft

## 1. Objective

This blueprint defines the strategy and patterns for integrating Model Context Protocol (MCP) servers and tools into the `philoso-roo` workflow. It addresses the critical gap identified in the V18.3.3 architecture evaluation (Rec 3.1), enabling access to external data sources crucial for philosophical research.

## 2. Context & Requirements

*   **Problem:** The current architecture lacks a defined method for leveraging MCP to access external resources like web articles (e.g., Stanford Encyclopedia of Philosophy), journal databases, or perform web searches.
*   **Goal:** Enable modes to securely and reliably utilize MCP tools for research tasks.
*   **Core Requirements:**
    *   Fetch content from URLs (e.g., using `fetcher` or `firecrawl`).
    *   Perform web searches (e.g., using `brave-search`).
    *   Secure handling of API keys/credentials (MUST NOT be in `.clinerules`).
    *   Robust error handling for external network calls and tool failures.
    *   Clear configuration and usage patterns.
*   **Available MCP Servers (Illustrative):** `fetcher`, `brave-search`, `firecrawl`, `github`, `zlibrary-mcp`, `puppeteer`, `filesystem`. (Actual available servers depend on user's environment).

## 3. Implementation Alternatives

Two primary approaches were considered:

### 3.1. Option A: Dedicated `Research` Mode

*   **Description:** A new mode (`philosophy-research`) would be created to handle all interactions with MCP tools related to external data gathering. Other modes would delegate research tasks to this mode.
*   **Pros:**
    *   Centralizes external interaction logic and dependencies.
    *   Simplifies `.clinerules` for other modes (they only need to know how to delegate to `Research`).
    *   Easier to standardize MCP call patterns, error handling, and security within one mode.
*   **Cons:**
    *   Adds another mode to the system, increasing overall complexity.
    *   Potential bottleneck if many modes require research simultaneously.
    *   Requires defining clear, standardized task formats for delegation to `Research` and result formats for completion.
*   **Example Workflow:**
    1.  `Orchestrator` delegates task (e.g., "Fetch SEP entry on 'Being'") to `PreLecture`.
    2.  `PreLecture` determines need for external data, delegates sub-task via `new_task` to `Research` mode with URL.
    3.  `Research` mode receives task, calls `use_mcp_tool` (`fetcher`, `fetch_url`).
    4.  `Research` processes result (e.g., extracts Markdown), calls `attempt_completion` with processed content.
    5.  `Orchestrator` receives completion, routes result back to `PreLecture` via `new_task`.
    6.  `PreLecture` uses fetched content.

### 3.2. Option B: Distributed MCP Calls

*   **Description:** Existing modes that require external data (e.g., `PreLecture`, `SecondaryLit`, `Questioning`) would be granted permission and contain the logic to directly call relevant MCP tools (`use_mcp_tool`).
*   **Pros:**
    *   Keeps external data gathering logic within the context of the mode that needs it.
    *   Potentially more flexible, avoids adding a new mode.
    *   Aligns with evaluation report's initial suggestion for flexibility.
*   **Cons:**
    *   Distributes MCP dependency knowledge across multiple modes.
    *   Requires **strict standardization** of MCP call patterns, error handling, and security considerations within the `.clinerules` of *every* mode using MCP.
    *   Harder to update or change MCP usage patterns consistently across all modes.
*   **Example Workflow:**
    1.  `Orchestrator` delegates task (e.g., "Fetch SEP entry on 'Being'") to `PreLecture`.
    2.  `PreLecture` determines need for external data, directly calls `use_mcp_tool` (`fetcher`, `fetch_url`) within its own rule logic.
    3.  `PreLecture` handles result/error, processes content.
    4.  `PreLecture` calls `attempt_completion` with its overall task result.
    5.  `Orchestrator` receives completion.

## 4. Chosen Strategy: Option B (Distributed Calls) with Strong Standardization

*   **Decision:** Implement Option B (Distributed Calls) as the initial strategy.
*   **Rationale:** This approach offers greater flexibility initially and avoids introducing a new mode immediately. However, its success is **critically dependent** on implementing rigorous standardization for MCP usage within `.clinerules`. This aligns with the evaluation report's recommendation while acknowledging the risks. If standardization proves insufficient or maintenance becomes overly complex, revisiting Option A (Dedicated Mode) should be considered.
*   **Key Requirement:** Updates to `docs/standards/clinerules_standard_v1.md` (Integration Plan Step 4) are essential to define mandatory patterns for MCP calls, error handling, and result formatting used by modes implementing this strategy.

## 5. Implementation Details

### 5.1. `.clinerules` Standardization (Requires Plan Step 4 Implementation)

*   **MCP Call Pattern:** Define a standard structure/function within `.clinerules` for invoking `use_mcp_tool`. This should include parameters for `server_name`, `tool_name`, and `arguments`.
*   **Error Handling:** Mandate a robust error handling block for every `use_mcp_tool` call, covering:
    *   Tool execution errors (e.g., server unavailable, invalid arguments).
    *   Network timeouts.
    *   API-specific errors returned by the tool.
    *   Content parsing errors.
    *   Define standard retry logic (e.g., retry once on timeout) and fallback strategies (e.g., if `fetcher` fails, try `brave-search` for the URL).
    *   Standard logging format for MCP errors.
*   **Result Formatting:** Define a standard structure for how modes package results obtained from MCP tools when reporting completion to `Orchestrator`.
*   **Documentation:** Each mode's `.clinerules` must clearly document which MCP tools it uses, the purpose, and expected arguments/results.

### 5.2. Configuration & Security

*   **MCP Server Configuration:** Assumed to be managed by the RooCode environment, potentially via `mcp_settings.json` or command-line arguments when starting servers. Modes do not need to manage server connection details.
*   **API Keys/Credentials:**
    *   **CRITICAL:** API keys (e.g., for `brave-search`) MUST NOT be stored in `.clinerules`, source code, or any version-controlled file.
    *   **Mechanism:** Keys should be provided as **environment variables** (e.g., `BRAVE_API_KEY`) accessible *only* by the corresponding MCP server process (e.g., `@modelcontextprotocol/server-brave-search` reads `process.env.BRAVE_API_KEY`).
    *   **Mode Interaction:** Modes call `use_mcp_tool` without needing access to the API key; the server handles authentication using its environment variable.
    *   **Documentation:** Project setup documentation must clearly state required environment variables for MCP servers needing API keys.

### 5.3. Example (Conceptual `.clinerules` Snippet for `PreLecture`)

```yaml
# Within PreLecture.clinerules

rules:
  - name: Process Reading URL
    # ... trigger conditions ...
    actions:
      # ... other actions ...
      - tool: use_mcp_tool
        args:
          server_name: fetcher
          tool_name: fetch_url
          arguments:
            url: {{ task.input.url }}
            extractContent: true # Example parameter
            timeout: 45000 # Example parameter
        # --- MANDATORY MCP ERROR HANDLING BLOCK ---
        on_error:
          - log: "[ERROR] MCP fetcher.fetch_url failed for {{ task.input.url }}. Error: {{ error.message }}"
          # Optional: Retry logic
          # Optional: Fallback (e.g., try brave-search)
          - tool: attempt_completion
            args:
              status: failed
              result: "Failed to fetch content from URL: {{ task.input.url }}. Error: {{ error.message }}"
        # --- END MCP ERROR HANDLING BLOCK ---
        on_success:
          - log: "[INFO] MCP fetcher.fetch_url succeeded for {{ task.input.url }}."
          # Process result.data.markdown or result.data.html
          # ... subsequent actions using fetched content ...
```

## 6. Architecture Document Update

*   Sections 4 (Mode Structure) and 7 (Workflows) of `docs/architecture/architecture_v18.md` will be updated to:
    *   Summarize the chosen Distributed MCP Call strategy.
    *   Reference this blueprint (`docs/blueprints/mcp_integration_v1.md`) for detailed implementation patterns.
    *   Emphasize the requirement for standardization via `docs/standards/clinerules_standard_v1.md`.
    *   Briefly mention API key security via environment variables.

## 7. Future Considerations

*   Monitor the complexity of distributed MCP calls. If standardization proves difficult or maintenance becomes burdensome, reconsider migrating to a dedicated `Research` mode (Option A).
*   Evaluate migrating complex internal scripts (e.g., `process_source_text.py`) to custom MCP servers for better abstraction and maintainability.