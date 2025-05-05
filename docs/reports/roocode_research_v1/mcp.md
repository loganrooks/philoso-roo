# RooCode Detailed Research: Model Context Protocol (MCP)

Date: 2025-05-05
Source: RooCode Docs Crawl (Job ID: `0d438814-566c-402a-bd97-e9387ed5c9b4`), General RooCode Instructions

## 1. Overview

The Model Context Protocol (MCP) is a fundamental component of RooCode's architecture, designed for **extensibility**. It allows RooCode to connect with external "MCP servers" that provide additional tools and data resources beyond the standard built-in capabilities.

- **Purpose:** To augment RooCode's functionality by integrating external services, APIs, databases, or custom logic.
- **Analogy:** MCP acts like a plugin system, enabling developers to add new skills and knowledge sources to the RooCode agent.

## 2. MCP Servers

MCP Servers are external processes that RooCode communicates with.

- **Function:** Host custom tools and resources.
- **Types/Transports:**
    - **Stdio-based:** Local servers running on the user's machine, communicating via standard input/output. Often launched via `npx` or similar commands.
    - **SSE-based (Server-Sent Events):** Remote servers communicating over HTTP/HTTPS using SSE.
- **Discovery/Connection:** RooCode likely discovers and connects to these servers based on configuration within the VS Code extension settings or potentially project-specific settings.
- **Examples (from Docs/Crawl/System Info):** `puppeteer`, `brave-search`, `fetcher`, `github`, `filesystem`, `firecrawl`, `zlibrary-mcp`.

## 3. MCP Tools

MCP servers expose custom **Tools** that RooCode modes can invoke.

- **Definition:** Each MCP tool has a defined **input schema** (JSON Schema) specifying required and optional parameters.
- **Invocation:** Modes use the standard `use_mcp_tool` tool, providing the server name, tool name, and arguments conforming to the tool's schema.
    ```xml
    <use_mcp_tool>
      <server_name>example-server</server_name>
      <tool_name>example_tool</tool_name>
      <arguments>
        {
          "param1": "value1",
          "param2": 123
        }
      </arguments>
    </use_mcp_tool>
    ```
- **Execution:** RooCode sends the request to the appropriate MCP server, which executes the tool logic and returns the result.
- **Purpose:** Enables actions like searching the web (`brave_web_search`), interacting with GitHub (`create_issue`, `get_file_contents`), scraping web pages (`firecrawl_scrape`), controlling a browser (`puppeteer_navigate`), etc.

## 4. MCP Resources

MCP servers can also provide access to **Resources**.

- **Definition:** Represent data sources like files, API responses, system information, or data streams. Identified by a URI.
- **Access:** Modes use the standard `access_mcp_resource` tool, providing the server name and the resource URI.
    ```xml
    <access_mcp_resource>
      <server_name>example-server</server_name>
      <uri>resource://example/data</uri>
    </access_mcp_resource>
    ```
- **Purpose:** Allows RooCode to access dynamic or large datasets, logs, or other information managed by an external server without needing to pass all the data through the prompt context. Example: Accessing browser console logs (`console://logs`) from the `puppeteer` server.

## 5. MCP vs. Standard Tools/APIs

- **When to use MCP:**
    - Interacting with external web services or APIs (e.g., weather, search, specific SaaS products).
    - Accessing databases or other external data stores.
    - Performing complex operations requiring dedicated logic or libraries not available in the standard RooCode environment (e.g., advanced web scraping, specific file format processing).
    - Accessing real-time or large-scale data resources.
    - Encapsulating complex or sensitive operations (like API key management) within a secure server environment.
- **When to use Standard Tools:**
    - Basic file system operations within the workspace.
    - Running standard CLI commands.
    - Simple code analysis within the workspace.
    - Direct user interaction.
    - Basic task/mode management.
- **MCP vs. Direct API Calls:** While a mode could theoretically try to construct and execute an API call using `execute_command` (e.g., with `curl`), using a dedicated MCP server is generally preferred. MCP provides:
    - **Abstraction:** Hides implementation details from the AI model.
    - **Schema Enforcement:** Ensures correct parameters are passed.
    - **Security:** API keys/credentials can be managed securely within the server, not exposed in prompts or logs.
    - **Maintainability:** Easier to update the tool logic in the server without changing mode prompts.

## 6. Creating MCP Servers

The documentation mentions the ability to create custom MCP servers, likely involving:
- Choosing a transport (Stdio or SSE).
- Defining tool schemas (JSON Schema).
- Implementing the server logic to handle tool requests and resource access.
- Registering/configuring the server with RooCode.
- (Specific instructions can be fetched using `<fetch_instructions><task>create_mcp_server</task></fetch_instructions>`).

## 7. Security Considerations

- MCP servers, especially remote ones or those handling sensitive data/APIs, need careful implementation regarding authentication, authorization, and input validation to prevent misuse.
- Managing API keys and credentials securely within the MCP server is crucial. They should not be part of RooCode prompts or logs.

## 8. Relevance to `philoso-roo`

- **External Knowledge:** MCPs are essential for `philoso-roo`'s broadened scope. `brave-search`, `fetcher`, `firecrawl`, `zlibrary-mcp` can be used to find and ingest philosophical texts, articles, and secondary sources.
- **Version Control:** The `github` MCP could potentially be used for managing the `philoso-roo` project itself or interacting with external philosophy-related code/data repositories.
- **Custom Integrations:** If `philoso-roo` needed to interact with specific academic databases or APIs (e.g., PhilPapers), a custom MCP server would be the appropriate architectural solution.
- **Data Processing:** Complex text processing or analysis requiring specific libraries (beyond the capabilities of the current Python scripts run via `execute_command`) could be encapsulated in a custom MCP server.