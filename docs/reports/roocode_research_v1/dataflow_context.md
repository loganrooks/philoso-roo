# RooCode Detailed Research: Data Flow & Context Management

Date: 2025-05-05
Source: RooCode Docs Crawl (Job ID: `0d438814-566c-402a-bd97-e9387ed5c9b4`), General RooCode Instructions, `philoso-roo` project structure & rules

This section analyzes how information flows between RooCode components (user, AI, modes, tools) and how context is managed during task execution.

## 1. Core Interaction Loop & Data Flow

The fundamental data flow follows the interaction loop described in [Core Concepts](./core_concepts_architecture.md):

1.  **User Input:** User provides a task request (prompt) via the chat interface.
2.  **Prompt Assembly:** RooCode (likely the core extension) assembles the full prompt for the AI model. This includes:
    *   The user's latest message.
    *   Relevant chat history.
    *   System information (OS, workspace path, etc.).
    *   Mode-specific rules and instructions (from `.clinerules`).
    *   Global/Workspace/User Custom Instructions.
    *   Information about available tools (standard and MCP).
    *   Potentially, relevant context retrieved from the Memory Bank (based on mode rules).
    *   (The exact composition is detailed in the "Prompt Structure" documentation, which was identified but not fully crawled/analyzed in this pass).
3.  **AI Processing:** The selected AI model processes the prompt and generates a response, which might be:
    *   A textual answer/explanation for the user.
    *   Code to be inserted/modified.
    *   A request to use one or more tools.
4.  **Tool Execution (if requested):**
    *   RooCode parses the tool use request.
    *   User approval is typically sought (unless auto-approval is configured).
    *   RooCode executes the tool (either built-in logic or via MCP).
    *   The tool's result (success/failure, output data, error messages) is captured.
5.  **Feedback to AI:** The tool result is formatted and added back into the chat history/AI context.
6.  **Iteration:** The AI processes the tool result and continues the task (steps 3-6 repeat) until it determines the task is complete.
7.  **Final Output:** The AI generates a final response for the user, often using `attempt_completion`.

## 2. Context Management Mechanisms

Managing the context provided to the AI model is critical due to the finite context windows of LLMs. RooCode appears to employ several mechanisms:

### a) Chat History

- **Function:** Provides immediate short-term memory of the current task's conversation flow, including user messages, AI responses, and tool results.
- **Limitations:** Subject to the AI provider's context window limits. Older parts of the conversation will eventually be excluded from the prompt.

### b) Memory Bank (Inferred & Based on `philoso-roo`)

- **Function:** Provides a mechanism for **persistent context storage** across interactions and potentially tasks/sessions. It allows modes to record and retrieve key information, decisions, progress, and feedback, mitigating the limitations of chat history.
- **Structure (Likely):** A directory (`memory-bank/`) containing structured markdown files (e.g., `activeContext.md`, `globalContext.md`, `mode-specific/*.md`, `feedback/*.md`).
- **Interaction:** Modes use standard file tools (`read_file`, `insert_content`, `apply_diff`) to interact with Memory Bank files, governed by rules in their `.clinerules` (e.g., `memory_bank_strategy`, `memory_bank_updates`).
- **Data Flow:**
    - **Reading:** Modes read relevant MB files at the start of a task or specific steps to gain context.
    - **Writing:** Modes write updates (status, decisions, findings, errors) to MB files at defined trigger points (e.g., before `attempt_completion`, on significant events). Reverse chronological order is a common pattern.
- **Importance:** Crucial for long-running tasks, complex projects requiring historical context, cross-task consistency, and collaborative workflows involving multiple modes or handovers.

### c) Checkpoints

- **Function:** Allows explicitly saving the entire state of a task (chat history, mode, potentially MB state) to be resumed later.
- **Usage:** Useful for interrupting long tasks, preserving work before potentially risky operations, or managing context limits by allowing a "fresh start" from a saved state.

### d) Task Delegation (`new_task`)

- **Function:** Creates a sub-task, passing initial instructions (`message` parameter). This implicitly transfers some context relevant to the sub-task.
- **Context Passing:** The parent task needs to formulate the `message` carefully to include necessary context. The sub-task might also read relevant Memory Bank entries upon initialization.
- **Return Flow:** The "Boomerang Tasks" feature suggests mechanisms exist for sub-tasks to return results or control to the parent task, likely involving `attempt_completion` by the sub-task and subsequent processing by the parent.

### e) Custom Instructions & `.clinerules`

- **Function:** Provide persistent, task-agnostic or mode-specific context and instructions that are included in the prompt automatically.
- **Usage:** Defining core principles, constraints, required output formats, or project-specific background information.

### f) Context Mentions (from Docs)

- **Function:** Allows explicitly including specific files or code snippets in the prompt context using `@` mentions (e.g., `@src/main.js`).
- **Usage:** Drawing the AI's attention to specific parts of the codebase relevant to the current request.

## 3. Managing Context Limits

- **Challenge:** LLMs have finite context windows. Exceeding the limit leads to loss of older information, potentially causing errors or degraded performance.
- **RooCode Strategies:**
    - **Memory Bank:** Offloads less immediate context to persistent storage.
    - **Checkpoints:** Allows resetting the active chat history while preserving the ability to resume.
    - **Task Delegation (`new_task`):** Breaks large tasks into smaller ones, each with its own (potentially smaller) context.
    - **Partial File Reads:** Using `read_file` with line ranges avoids loading entire large files into context unnecessarily.
    - **Summarization (Implicit):** Modes (especially Orchestrator or Architect) might be implicitly or explicitly tasked with summarizing progress or key information into the Memory Bank to condense context.
    - **Proactive Handover (Rule):** Some `.clinerules` (like those in this system) include rules to proactively suggest using `new_task` for handover if context limits are approached, preventing failures.

## 4. Relevance to `philoso-roo`

- **Memory Bank Usage:** The `philoso-roo` project heavily utilizes the Memory Bank pattern, with detailed strategies defined in `.clinerules` files. This aligns with the inferred purpose of MB for managing complex, multi-step philosophical analysis and writing tasks. Ensuring consistent and efficient MB updates (e.g., using batch operations via `apply_diff` or `insert_content` where possible) is crucial.
- **Task Delegation:** The complexity of philosophical research and writing suggests that leveraging `new_task` and potentially an `Orchestrator` mode (as defined in V18.3) is appropriate for breaking down workflows (e.g., source processing -> analysis -> drafting -> verification).
- **Context for Analysis:** Analysis modes need access to both the source material being analyzed and relevant context from the KB/Memory Bank (previous analyses, related concepts, decisions). Efficiently providing this context (e.g., via targeted `read_file` calls based on MB links, `search_files` on the KB, or context mentions) is key.
- **V18.3.3 Architecture:** The direct access pattern requires modes to manage their own context retrieval from the KB using file tools. The removal of `kb-doctor` means context related to KB health/structure might need to be inferred or checked periodically by `MetaReflector` or `VerificationAgent`.