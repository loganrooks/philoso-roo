# RooCode Research Summary (v1)

Date: 2025-05-05

## 1. Overview

This report summarizes findings from researching RooCode documentation, primarily sourced from crawling `https://docs.roocode.com/` (Job ID: `0d438814-566c-402a-bd97-e9387ed5c9b4`) and reviewing related GitHub repositories (`RooVetGit/Roo-Code`, `RooVetGit/Roo-Code-Docs`). The focus was on understanding core concepts, tools, extensibility (MCP), mode interaction, data flow, and best practices relevant to the `philoso-roo` knowledge management and analysis system.

## 2. Core Concepts

*   **Autonomous Agent:** RooCode operates as an AI agent within the VS Code editor, capable of understanding natural language, interacting with the workspace, and performing tasks autonomously.
*   **Modes:** RooCode utilizes specialized "modes" (e.g., Code, Architect, Debug, Ask, Orchestrator) which are distinct personas with specific capabilities and instructions (`.clinerules`). This allows tailoring the agent's behavior for different tasks. Custom modes can be created for highly specialized roles.
*   **Tools:** Modes use a defined set of tools to interact with the environment. These include standard tools for file system operations, terminal execution, and potentially browser automation, as well as custom tools provided via MCP.
*   **Model Context Protocol (MCP):** A key extensibility mechanism allowing RooCode to connect to external "MCP servers." These servers provide additional tools (e.g., web search, API interaction, database access) and resources, significantly expanding RooCode's capabilities beyond its built-in tools.
*   **Task Management:** RooCode supports task delegation (`new_task`) to break down complex problems and potentially "Boomerang Tasks" for managing sub-task execution and results. Checkpoints allow saving and resuming task states.
*   **Memory Bank (Implied):** While not explicitly detailed in the crawled core docs, the presence of a `memory-bank/` structure in the `philoso-roo` project and community discussions (e.g., Memory Bank Project by GreatScottyMac) strongly suggests a mechanism for persistent context management across tasks and sessions, likely involving structured files (`activeContext.md`, `globalContext.md`, mode-specific files). This aligns with the observed behavior and rules within `philoso-roo`.
*   **Customization:** RooCode is highly customizable through `Custom Instructions` (per-task or per-mode), `Custom Modes`, support for various AI providers (including local models), and configurable settings (e.g., auto-approval).

## 3. Available Tools & Capabilities

*   **Standard Tools:**
    *   File System: `read_file`, `write_to_file`, `apply_diff`, `insert_content`, `search_files`, `list_files`, `search_and_replace`. Crucial for reading/writing code, documentation, and potentially structured knowledge data.
    *   Code Analysis: `list_code_definition_names`.
    *   Execution: `execute_command` (for running scripts, build tools, etc.).
    *   Interaction: `ask_followup_question`, `attempt_completion`, `switch_mode`, `new_task`.
*   **MCP Tools (via connected servers):** The available tools depend on the connected MCP servers. Examples found in docs/crawl results include:
    *   `puppeteer` (Browser automation: navigate, click, fill, screenshot, evaluate JS)
    *   `brave-search` (Web and local search)
    *   `fetcher` (Fetch URL content)
    *   `github` (Interact with GitHub: read files, create issues/PRs, search repos, etc.)
    *   `filesystem` (Mentioned by user, potentially offers alternative file operations)
    *   `firecrawl` (Web scraping and crawling)
    *   `zlibrary-mcp` (Book search and download)
*   **MCP Interaction:** `use_mcp_tool` (execute a tool provided by an MCP server), `access_mcp_resource` (access data provided by an MCP server).

## 4. Mode Interaction & Data Flow

*   **Delegation:** The `Orchestrator` mode and the `new_task` tool are central to managing complex workflows by delegating sub-tasks to appropriate modes.
*   **Context Passing:** Information is likely passed between modes via the Memory Bank and potentially through the arguments provided when using `new_task`. `Custom Instructions` also play a role in setting context for a mode. The `Prompt Structure` documentation (referenced in crawl results) likely contains specifics.
*   **Control Flow:** `switch_mode` allows changing the active mode within a task. `Boomerang Tasks` provide a pattern for sub-tasks returning control/results to the parent task. `attempt_completion` signals task finalization.

## 5. Best Practices & Considerations

*   **Mode Specialization:** Use the most appropriate mode for a given task. Create custom modes for recurring, specialized workflows.
*   **Tool Selection:** Choose tools judiciously. Leverage file tools for direct workspace interaction. Use `execute_command` for CLI tasks. Employ MCPs for external data/services.
*   **MCP for Extensibility:** Use MCP to integrate external APIs, databases, or custom logic, rather than trying to implement complex external interactions solely within mode prompts or standard tools.
*   **Task Decomposition:** Break down complex tasks using `new_task` and potentially an `Orchestrator` mode for better management and context control.
*   **Context Management:** Be mindful of context window limits. Leverage the Memory Bank (if confirmed structure/usage) for persistent context. Use `Custom Instructions` effectively.
*   **Configuration:** Utilize API Configuration Profiles, Auto-Approval settings, and Temperature settings to optimize performance, cost, and safety.
*   **Prompting:** Follow prompt engineering best practices. Use `Enhance Prompt` feature if needed. Be aware of "Footgun Prompting" to override system prompts carefully.

## 6. Relevance to `philoso-roo`

*   **Knowledge Base Interaction:** The standard file tools are well-suited for reading from and writing to the markdown/YAML-based `philosophy-knowledge-base`. `search_files` can be used for querying across the KB.
*   **External Data Acquisition:** MCPs like `brave-search`, `fetcher`, `firecrawl`, and potentially `zlibrary-mcp` are highly relevant for gathering philosophical texts, research papers, and secondary literature.
*   **Analysis Workflow:** The concept of specialized modes aligns perfectly with the existing `philosophy-*` modes. Data flow likely relies on modes reading/writing to the KB and potentially passing specific context via Memory Bank updates or `new_task` arguments.
*   **Architecture V18.3.3:**
    *   The direct KB access pattern aligns with RooCode's file system tools.
    *   Removing the `kb-doctor` script dependency and distributing maintenance tasks to modes (`Orchestrator`, `MetaReflector`, `VerificationAgent`) leverages RooCode's internal capabilities (modes, tools) over external processes, which seems consistent with RooCode's philosophy of integrating tasks within the agent. The effectiveness depends on the implementation details within those modes' rules.
    *   The broadened scope necessitates robust use of MCPs for data gathering and potentially custom modes for diverse philosophical inquiries.

## 7. Open Questions/Further Research

*   Confirm the official structure and intended usage patterns for the Memory Bank.
*   Investigate the `Prompt Structure` documentation for details on context passing.
*   Clarify the status and best practices for browser automation (older `browser_action` vs. `puppeteer` MCP).
*   Explore community projects like SPARC and Memory Bank for advanced patterns.