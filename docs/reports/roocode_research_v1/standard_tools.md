# RooCode Detailed Research: Standard Tools

Date: 2025-05-05
Source: RooCode Docs Crawl (Job ID: `0d438814-566c-402a-bd97-e9387ed5c9b4`), General RooCode Instructions

This section details the standard, built-in tools available to RooCode modes for interacting with the user's workspace and managing tasks.

## 1. File System Tools

These tools allow RooCode to read, write, and manipulate files within the workspace. Paths are typically relative to the workspace root.

### `read_file`
- **Description:** Reads the content of a file. Can read specific line ranges, useful for large files. Automatically handles text extraction from PDF/DOCX.
- **Parameters:**
    - `path` (required): Path to the file.
    - `start_line` (optional): 1-based starting line number.
    - `end_line` (optional): 1-based ending line number (inclusive).
- **Usage:** Essential for examining existing code, configuration, or data. Partial reads are crucial for managing context window size with large files.
- **Limitations:** May struggle with non-text or unsupported binary files. Truncation notices (`Showing only X of Y lines...`) must be heeded, especially if full context is needed for subsequent operations (like `apply_diff`).

### `write_to_file`
- **Description:** Writes content to a file, overwriting if it exists or creating it if it doesn't. Automatically creates necessary directories.
- **Parameters:**
    - `path` (required): Path to the file.
    - `content` (required): The **complete** content to write.
    - `line_count` (required): The total number of lines in the provided `content`.
- **Usage:** Creating new files, or completely replacing the content of existing files.
- **Limitations:** **Requires the entire file content.** Cannot be used for partial updates. Prone to failure with very large content due to potential truncation issues during transmission or processing (as observed in `philoso-roo` feedback logs). Should be used cautiously for modifications, preferring `apply_diff` or `insert_content` where possible.

### `apply_diff`
- **Description:** Replaces specific blocks of existing code/text using a search/replace mechanism defined in a diff format. Maintains indentation.
- **Parameters:**
    - `path` (required): Path to the file to modify.
    - `diff` (required): The search/replace block(s). Format:
      ```
      <<<<<<< SEARCH
      :start_line:[line_number]
      -------
      [Exact content to find]
      =======
      [New content to replace with]
      >>>>>>> REPLACE
      ```
      (Multiple blocks can be included in one `diff` parameter).
- **Usage:** Preferred method for making targeted modifications to existing files, especially code. More efficient and less error-prone than `write_to_file` for edits.
- **Limitations:** The `SEARCH` block must *exactly* match the existing content, including whitespace and line breaks. Requires knowing the correct starting line number. Failures can occur due to context mismatches (if the file changed since it was last read) or if the search block isn't found exactly.

### `insert_content`
- **Description:** Inserts new lines of content into a file at a specified line number without modifying existing content.
- **Parameters:**
    - `path` (required): Path to the file.
    - `line` (required): 1-based line number to insert *before*. Use `0` to append to the end of the file.
    - `content` (required): The content to insert.
- **Usage:** Ideal for adding imports, functions, configuration blocks, log entries, or any multi-line text block without replacing existing lines. Useful alternative to `apply_diff` when only adding content.

### `search_files`
- **Description:** Performs a regex search across files in a specified directory (recursively), returning matches with surrounding context lines.
- **Parameters:**
    - `path` (required): Directory path to search within.
    - `regex` (required): Regular expression pattern (Rust regex syntax).
    - `file_pattern` (optional): Glob pattern to filter files (e.g., `*.py`, `*.md`). Defaults to `*`.
- **Usage:** Finding specific code patterns, function calls, TODO comments, configuration values, or any text across multiple files. Useful for impact analysis before refactoring or understanding where specific logic is used.

### `list_files`
- **Description:** Lists files and directories within a specified path.
- **Parameters:**
    - `path` (required): Directory path to list.
    - `recursive` (optional): `true` for recursive listing, `false` or omitted for top-level only.
- **Usage:** Exploring the project structure, finding specific files or directories.

### `search_and_replace`
- **Description:** Finds and replaces text strings or regex patterns within a single file. Shows a diff preview.
- **Parameters:**
    - `path` (required): Path to the file.
    - `search` (required): Text or regex pattern to find.
    - `replace` (required): Text to replace matches with.
    - `start_line` (optional): 1-based start line for search range.
    - `end_line` (optional): 1-based end line for search range.
    - `use_regex` (optional): `true` if `search` is regex (default: `false`).
    - `ignore_case` (optional): `true` for case-insensitive search (default: `false`).
- **Usage:** Targeted replacements within a file, like renaming a variable or updating a specific string literal across multiple occurrences.

## 2. Code Analysis Tools

### `list_code_definition_names`
- **Description:** Lists definition names (classes, functions, methods, etc.) from source code in a specific file or all top-level files in a directory.
- **Parameters:**
    - `path` (required): Path to the file or directory.
- **Usage:** Getting a high-level overview of the code structure, identifying key components, understanding relationships between different parts of the code without reading the full content initially.

## 3. Execution Tools

### `execute_command`
- **Description:** Executes a CLI command in the system's terminal.
- **Parameters:**
    - `command` (required): The command to execute.
    - `cwd` (optional): Working directory for the command (defaults to workspace root).
- **Usage:** Running build scripts, tests, linters, package managers (`npm`, `pip`), or any other necessary command-line operations. Can run interactive/long-running commands.
- **Considerations:** Commands should be tailored to the user's OS (provided in system info). Use relative paths where possible. Be mindful of the working directory.

## 4. Interaction & Task Management Tools

### `ask_followup_question`
- **Description:** Asks the user a clarifying question when more information is needed to proceed.
- **Parameters:**
    - `question` (required): The question for the user.
    - `follow_up` (required): List of 2-4 suggested answers (`<suggest>` tags).
- **Usage:** Resolving ambiguities, gathering missing parameters or requirements. Should be used judiciously to avoid excessive back-and-forth.

### `attempt_completion`
- **Description:** Signals that the AI believes the task is complete and presents the result to the user.
- **Parameters:**
    - `result` (required): Description of the completed work and final state.
    - `command` (optional): A CLI command to demonstrate the result (e.g., `open index.html`).
- **Usage:** Final step in a task workflow after all actions are completed and verified (based on tool results/user feedback). Requires confirmation of previous steps' success.

### `switch_mode`
- **Description:** Requests a switch to a different RooCode mode. Requires user approval.
- **Parameters:**
    - `mode_slug` (required): The slug of the target mode (e.g., `code`, `debug`).
    - `reason` (optional): Justification for the switch.
- **Usage:** Transitioning between different phases of a task that require different specializations (e.g., switching from `architect` to `code` for implementation).

### `new_task`
- **Description:** Creates a new sub-task, potentially assigned to a different mode. Establishes a parent-child task relationship.
- **Parameters:**
    - `mode` (required): The slug of the mode for the new task.
    - `message` (required): Initial instructions for the new task.
- **Usage:** Breaking down complex projects into smaller, manageable units. Delegating specific parts of a workflow to specialized modes (often orchestrated by an `Orchestrator` mode). Essential for managing large tasks and context.

## 5. MCP Interaction Tools

These tools facilitate interaction with external capabilities provided by MCP servers.

### `use_mcp_tool`
- **Description:** Executes a specific tool provided by a connected MCP server.
- **Parameters:**
    - `server_name` (required): Name of the MCP server.
    - `tool_name` (required): Name of the tool on that server.
    - `arguments` (required): JSON object containing parameters required by the MCP tool's schema.
- **Usage:** Accessing external functionality like web search (`brave-search`), web scraping (`firecrawl`, `fetcher`), GitHub operations (`github`), etc.

### `access_mcp_resource`
- **Description:** Accesses a data resource provided by a connected MCP server.
- **Parameters:**
    - `server_name` (required): Name of the MCP server.
    - `uri` (required): URI identifying the specific resource.
- **Usage:** Retrieving data streams or static information from MCP servers (e.g., browser console logs from `puppeteer`).

*(Note: Specific parameters and behavior for MCP tools depend on the respective MCP server's implementation and documentation.)*