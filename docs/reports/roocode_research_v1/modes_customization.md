# RooCode Detailed Research: Modes & Customization

Date: 2025-05-05
Source: RooCode Docs Crawl (Job ID: `0d438814-566c-402a-bd97-e9387ed5c9b4`), General RooCode Instructions, `philoso-roo` project structure

This section details how RooCode Modes are defined, customized, and managed.

## 1. Modes: Specialized Personas

As outlined in [Core Concepts](./core_concepts_architecture.md), Modes are distinct AI personas tailored for specific tasks.

- **Function:** They define the AI's identity, core instructions, available tools (implicitly via rules), and operational guidelines.
- **Selection:** The user selects a mode when starting a task, or an `Orchestrator` mode can delegate sub-tasks to specific modes using `new_task`. The `switch_mode` tool allows changing modes mid-task (with user approval).

## 2. `.clinerules` Files: Mode Definition

Each mode is defined by a configuration file, typically named `<mode-slug>.clinerules` and located within a `.roo/rules-<mode-slug>/` directory (based on `philoso-roo` structure and other community examples).

- **Purpose:** To provide the core system prompt components and operational rules for a specific mode.
- **Structure (Inferred from Docs/Examples/`philoso-roo`):** `.clinerules` files often contain sections like:
    - `mode`: The unique slug for the mode.
    - `identity`:
        - `name`: User-facing name (e.g., "🏗️ Architect").
        - `description`: Brief explanation of the mode's purpose.
    - `memory_bank_strategy` (Common Pattern): Defines how the mode interacts with the Memory Bank (initialization checks, reading context, update triggers, error handling).
    - `general` (Common Pattern): General operational rules, status prefixes, context management guidelines, error handling protocols (like the "Three Strikes" rule), critical evaluation prompts.
    - `memory_bank_updates` (Common Pattern): Specifies update frequency, process, feedback handling, and potentially mode-specific update details (primary responsibilities, triggers, target files/formats).
    - `rules` / `custom_instructions` / Mode-Specific Sections: Contains the core "persona" instructions, defining the mode's goals, constraints, specific workflows, tool usage preferences, and expected output formats. This is where the specialization happens.
    - `umb` (Update Memory Bank Command): Defines trigger and instructions for manual MB updates.
- **Loading:** RooCode loads these rules when a mode is activated, incorporating them into the system prompt sent to the underlying AI model.

## 3. Custom Modes

RooCode allows users to create their own **Custom Modes**.

- **Process:**
    1.  Define the mode's identity, purpose, and specialized instructions.
    2.  Create the corresponding `.clinerules` file (e.g., `.roo/rules-my-custom-mode/my-custom-mode.clinerules`).
    3.  Register the mode in the central `.roomodes` configuration file (likely in the `.roo/` directory or workspace root), specifying its slug, name, description, and potentially the path to its rules file.
- **Benefits:** Enables tailoring RooCode for highly specific project needs, workflows, or coding standards (e.g., security reviewer, documentation writer, specific framework expert, test generator).
- **Example (`philoso-roo`):** The project utilizes numerous custom modes (e.g., `philosophy-class-analysis`, `philosophy-dialectical-analysis`, `philosophy-essay-prep`) defined in `.clinerules-*` files in the root and configured in `.roomodes`.

## 4. Custom Instructions

Beyond the mode-level rules in `.clinerules`, users can provide **Custom Instructions** to further tailor RooCode's behavior.

- **Scope:** Can be applied globally (via settings), per-workspace (potentially via a root `.clinerules` or similar config), or per-mode (within the `.clinerules` file itself). The documentation mentions a dedicated "Custom Instructions" feature, likely configured through the extension settings UI.
- **Purpose:** To provide persistent, high-level guidance or constraints that apply across tasks or within specific modes, without needing to repeat them in every prompt. Examples include language preferences, coding style guides, project-specific context, or persona refinements.
- **Interaction with Mode Rules:** Custom instructions likely augment or potentially override parts of the base mode rules, depending on how they are structured and loaded into the final prompt.

## 5. Configuration & Management

- **`.roomodes` File:** A central file (likely in `.roo/` or root) lists available modes, their slugs, names, and potentially paths to their `.clinerules` files. This allows RooCode to discover and load modes.
- **Settings Management:** RooCode provides UI options for managing settings, including API keys, model selection, temperature, auto-approval rules, and likely custom instructions. The docs mention features for importing, exporting, and resetting settings.
- **API Configuration Profiles:** Allows defining multiple profiles for different AI providers or model configurations, making it easy to switch between them.

## 6. Relevance to `philoso-roo`

- **Mode Structure:** The project's use of numerous custom philosophy modes defined in `.clinerules-*` files and registered in `.roomodes` aligns perfectly with RooCode's documented customization capabilities.
- **Rule Granularity:** The detailed rules within `philoso-roo`'s `.clinerules` files (e.g., specific Memory Bank strategies, error handling, update formats) demonstrate the intended use of these files for fine-grained control over mode behavior.
- **Architect Role:** The `Architect` mode's documented responsibility for managing Memory Bank initialization and documentation structure fits well within the RooCode paradigm.
- **Potential Improvements:** Ensure consistency across all `.clinerules` files, potentially leveraging a shared template or standard sections more effectively (as suggested by the `clinerules_standard_v1.md` effort noted in `philoso-roo`'s Memory Bank). Review if any logic currently in mode rules could be better encapsulated in custom MCP tools.