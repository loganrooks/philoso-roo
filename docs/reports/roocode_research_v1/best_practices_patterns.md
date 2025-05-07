# RooCode Detailed Research: Best Practices & Patterns

Date: 2025-05-05
Source: RooCode Docs Crawl (Job ID: `0d438814-566c-402a-bd97-e9387ed5c9b4`), General RooCode Instructions, `philoso-roo` project structure & rules

This section outlines best practices and common patterns for using RooCode effectively, based on the documentation and observed project structures.

## 1. Prompt Engineering

Effective prompting is crucial for guiding RooCode.

- **Clarity & Specificity:** Provide clear, unambiguous instructions. Define the desired output format.
- **Context:** Use context mentions (`@file`) to point the AI to relevant code. Ensure necessary background is provided either in the prompt or accessible via Memory Bank/Custom Instructions.
- **Mode Alignment:** Frame requests according to the selected mode's specialization.
- **Iterative Refinement:** Start with a high-level request and refine it based on RooCode's responses or tool usage. Use follow-up messages to correct misunderstandings or provide more detail.
- **Enhance Prompt Feature:** The docs mention an "Enhance Prompt" feature, likely a UI button to help automatically improve prompt clarity or detail.
- **Footgun Prompting:** A documented feature allows overriding parts of the system prompt directly, offering powerful control but requiring caution.

## 2. Workflow Design & Task Management

- **Mode Specialization:** Assign tasks to the most appropriate mode (e.g., `code` for implementation, `architect` for design, `debug` for errors).
- **Task Decomposition (`new_task`):** Break large, complex tasks into smaller, manageable sub-tasks delegated to specific modes. This improves focus, manageability, and context control. An `Orchestrator` mode is often used to manage these delegations.
- **Boomerang Tasks:** This pattern likely involves designing sub-tasks (`new_task`) to perform a specific function and then explicitly return results or control to the parent task, enabling more complex, multi-stage workflows.
- **Checkpoints:** Use checkpoints to save progress on long-running tasks, allowing resumption later or recovery from errors/context limits.

## 3. Tool Usage

- **Prefer Specific Tools:** Use the most specific tool for the job (e.g., `apply_diff` or `insert_content` for edits over `write_to_file` when possible).
- **Verify Tool Inputs:** Ensure correct parameters (paths, line numbers, regex) are provided. Use `read_file` (potentially with line ranges) or `list_files` to confirm paths/line numbers before attempting modifications.
- **Anticipate Failures:** Be prepared for tool failures (e.g., `apply_diff` context mismatch, `write_to_file` truncation). Implement error handling logic (as seen in `philoso-roo` rules) to analyze failures and retry appropriately (e.g., re-read file before retrying `apply_diff`).
- **Use MCP for External Interactions:** Leverage MCP servers for interacting with external APIs, web services, or complex processing, rather than trying to use `execute_command` with `curl` or similar workarounds.

## 4. Context & Memory Management

- **Be Mindful of Limits:** Understand that LLM context windows are finite.
- **Leverage Memory Bank:** Utilize the Memory Bank structure (if implemented, as in `philoso-roo`) for persistent context. Follow defined update rules (frequency, format, reverse chronological order). Keep entries concise but informative. Use cross-referencing links between related MB entries.
- **Use Partial Reads:** Employ `read_file` with `start_line`/`end_line` to read only necessary portions of large files.
- **Proactive Handover:** Implement rules (like in this system's mode) to monitor context usage and trigger handovers (`new_task`) *before* critical limits are reached, ensuring smoother continuation.
- **Summarization:** Encourage modes (especially Orchestrator/Architect) to summarize key information, decisions, and progress into the Memory Bank periodically.

## 5. Configuration & Customization

- **Custom Modes:** Define custom modes for recurring, specialized tasks unique to the project (like the `philosophy-*` modes).
- **Custom Instructions:** Use global or mode-specific custom instructions to provide consistent guidance (style guides, project goals, terminology).
- **API Profiles:** Use API configuration profiles to manage different models or providers easily.
- **Auto-Approval:** Carefully configure auto-approval rules. While speeding up workflows, it increases the risk of unintended actions. It's often safer to require approval for destructive operations (file writes, command execution).
- **Temperature:** Adjust model temperature based on the task (lower for predictable code/edits, higher for creative brainstorming).

## 6. Error Handling & Debugging

- **Structured Protocol:** Follow a structured error handling protocol (Log -> Analyze -> Consult MB -> Propose Solution -> Escalate if needed). Avoid generic retries.
- **"Three Strikes" Rule:** Mandate a change in strategy after repeated failures of the same tool on the same target.
- **Memory Bank Errors:** Have specific procedures for handling failures when reading/writing to the Memory Bank, including potentially switching to an inactive state or delegating to a `memory-bank-doctor` mode.
- **Critical Evaluation:** When faced with persistent errors or contradictions, explicitly re-evaluate previous assumptions or diagnoses, especially if context usage was high.
- **User Intervention Logging:** Mandatorily log all user interventions and corrections in feedback logs for learning and traceability.

## 7. Relevance to `philoso-roo`

- **Existing Practices:** The `philoso-roo` project already incorporates many of these best practices, particularly regarding Memory Bank usage, structured error handling, custom modes, and detailed `.clinerules`.
- **Areas for Review:**
    - **Tool Efficiency:** Ensure file modifications consistently use `apply_diff`/`insert_content` over `write_to_file` where appropriate, given the documented issues with `write_to_file`. Optimize `read_file` usage with line ranges.
    - **Workflow Orchestration:** Review the `Orchestrator` mode's logic and `new_task` usage for clarity and efficiency in managing the philosophy workflows. Ensure Boomerang Task patterns are used effectively if applicable.
    - **MCP Usage:** Continue leveraging MCPs for external data. Consider if any complex script logic run via `execute_command` could be migrated to a custom MCP server for better abstraction and robustness.
    - **Context Monitoring:** Reinforce proactive context monitoring and handover rules in orchestrating modes.