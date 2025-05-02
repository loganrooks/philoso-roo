# Task Prompt: Enhance Hegel Philosophy RooCode Suite

**Goal:** Refactor and enhance the existing suite of custom RooCode modes (`.roomodes`) designed for processing PHL316 (Hegel philosophy course) materials. The primary focus is to significantly improve the system's capability for generating well-structured philosophical essays with accurate textual references, robust verification procedures to prevent hallucinations, and an effective memory management system for research materials.

**Deliverables:**

1.  **Updated Architecture Document:** A revised architecture document (`architecture_v11.md`) detailing the new mode structure, interactions, memory management system, and verification processes.
2.  **New `.roomodes` Configuration:** A `.roo/.roomodes` file defining the complete suite of modes, including refactored existing modes and newly created ones.
3.  **Refactored `.clinerules` Files:** Updated `.clinerules` files for all existing and new modes, reflecting the enhanced capabilities and new architecture. These should be placed in a structured `.roo/rules-[mode-slug]/` directory.
4.  **New Orchestrator Mode:** A dedicated `philosophy-orchestrator` mode responsible for managing complex tasks like essay writing by delegating sub-tasks to specialized modes.
5.  **New Supporting Modes (as needed):** Any additional modes identified during the design phase to support specific functions like fact-checking, quotation management, or advanced research tasks.
6.  **Memory Management System Implementation:** Files and configurations defining the memory system for managing quotations, references, and research notes relevant to essay writing.

**Key Requirements:**

*   **Essay Writing Enhancement:** Modes involved in essay preparation must have improved capabilities for structuring arguments, integrating evidence, and generating coherent prose.
*   **Reference Accuracy:** Implement strict mechanisms for tracking the source of information (lecture, reading, secondary lit) and ensuring accurate citation generation (using extraction markers or similar).
*   **Hallucination Prevention:** Design and implement verification procedures within the workflow (potentially a dedicated mode or integrated checks) to cross-reference claims against source materials and flag potential inaccuracies or unsupported statements.
*   **Memory Management:** Develop a system (e.g., "Quotations Bank", "Evidence Locker") for collecting, organizing, and retrieving relevant quotations, arguments, and conceptual definitions during essay writing. This system should integrate with the existing `analysis_workspace` or a new dedicated structure.
*   **Modularity & Orchestration:** Define clear responsibilities for each mode and implement a new `philosophy-orchestrator` to manage the flow between modes for complex tasks.
*   **RooCode Standards:** Adhere to RooCode conventions for mode definition (`.roomodes`) and rules (`.clinerules`).
*   **New File Structure:** Implement the specified file structure:
    *   `.roo/.roomodes`
    *   `.roo/rules-[mode-slug]/[mode-slug].clinerules`

**Inputs:**

*   Existing `.clinerules` files for `philosophy-class-analysis`, `philosophy-dialectical-analysis`, `philosophy-essay-prep`, `philosophy-pre-lecture`, `philosophy-secondary-lit`.
*   Existing `architectureV10.md` (Note: Requires significant updates).
*   User requirements outlined in the initial request.

---

# Implementation Plan for SPARC Orchestrator

This plan outlines the steps to refactor and enhance the Hegel Philosophy RooCode Suite.

**Phase 1: Architecture & Design Definition**

1.  **Review Existing Assets:**
    *   Delegate to `architect` mode: Analyze the provided `.clinerules` files (`philosophy-class-analysis`, `philosophy-dialectical-analysis`, `philosophy-essay-prep`, `philosophy-pre-lecture`, `philosophy-secondary-lit`) and `architectureV10.md`.
    *   Identify current capabilities, limitations, and areas for improvement, especially regarding essay writing, referencing, and verification.
    *   **Output:** Summary report of existing system strengths and weaknesses.

2.  **Design New Architecture:**
    *   Delegate to `architect` mode: Based on the review and user requirements, design the enhanced architecture.
    *   **Define Mode Structure:**
        *   Specify the roles and responsibilities of existing modes after refactoring.
        *   Define the `philosophy-orchestrator` mode's role in managing workflows (e.g., `write_essay`, `analyze_lecture_cycle`).
        *   Propose any new necessary modes (e.g., `philosophy-fact-checker`, `philosophy-quotation-manager`, `philosophy-reference-validator`).
        *   Create a Mermaid diagram illustrating mode interactions and data flow.
    *   **Design Memory Management System:**
        *   Specify the structure for storing and retrieving quotations, arguments, concept definitions, and references (e.g., dedicated files/folders within `analysis_workspace` or a new `essay_evidence_bank`).
        *   Define how modes will interact with this memory system (read, write, query).
        *   Ensure integration with the existing chronological and conceptual tracking.
    *   **Design Verification Procedures:**
        *   Specify how reference accuracy will be checked (e.g., validating extraction markers, cross-referencing citations).
        *   Define the hallucination prevention mechanism (e.g., a dedicated `philosophy-fact-checker` mode, verification steps within `philosophy-essay-prep`).
        *   Outline the workflow for flagging and resolving potential inaccuracies.
    *   **Define Configuration Structure:**
        *   Specify the format for the new `.roo/.roomodes` file.
        *   Define the directory structure `.roo/rules-[mode-slug]/` for `.clinerules` files.
    *   **Output:** Updated architecture document (`architecture_v11.md`) including diagrams, mode definitions, memory system design, verification procedures, and configuration structure.

**Phase 2: Mode Refactoring & Creation**

1.  **Refactor Existing Modes:**
    *   Delegate task to `spec-pseudocode` or `code` mode (as appropriate for `.clinerules` modification): For each existing mode (`philosophy-class-analysis`, `philosophy-dialectical-analysis`, `philosophy-essay-prep`, `philosophy-pre-lecture`, `philosophy-secondary-lit`):
        *   Update the `.clinerules` file according to the new architecture (`architecture_v11.md`).
        *   Incorporate enhanced essay-writing support where applicable (especially `philosophy-essay-prep`).
        *   Integrate interactions with the new memory management system.
        *   Add calls or checks for the new verification procedures.
        *   Update mode switching logic and handoff protocols.
        *   Ensure adherence to RooCode standards.
        *   Save the updated file to the new location: `.roo/rules-[mode-slug]/[mode-slug].clinerules`.
    *   **Output:** Refactored `.clinerules` files in the correct directory structure.

2.  **Create New Orchestrator Mode:**
    *   Delegate task to `spec-pseudocode` or `code` mode: Create the `.clinerules` file for `philosophy-orchestrator`.
    *   Define its identity, capabilities (including `switch_mode`, `new_task`), and primary workflows (e.g., `initiate_essay`, `manage_analysis_cycle`).
    *   Implement logic for breaking down complex tasks and delegating to specialized modes based on `architecture_v11.md`.
    *   Define handoff protocols for receiving results and initiating subsequent steps.
    *   Save the file as `.roo/rules-philosophy-orchestrator/philosophy-orchestrator.clinerules`.
    *   **Output:** New `.clinerules` file for the orchestrator mode.

3.  **Create Other New Modes (if identified in Phase 1):**
    *   Delegate task to `spec-pseudocode` or `code` mode: For each new mode identified (e.g., `philosophy-fact-checker`, `philosophy-quotation-manager`):
        *   Create the corresponding `.clinerules` file.
        *   Define its specific responsibilities, capabilities, and workflows based on `architecture_v11.md`.
        *   Implement interactions with other modes and the memory management system.
        *   Save the file to `.roo/rules-[mode-slug]/[mode-slug].clinerules`.
    *   **Output:** New `.clinerules` files for any additional specialized modes.

**Phase 3: Configuration & Integration**

1.  **Create `.roomodes` Configuration File:**
    *   Delegate task to `architect` or `code` mode: Create the `.roo/.roomodes` file.
    *   List all modes (refactored and new).
    *   Specify the path to their respective `.clinerules` files within the `.roo/rules-[mode-slug]/` structure.
    *   Define any necessary mode parameters or configurations.
    *   **Output:** The `.roo/.roomodes` configuration file.

2.  **Verify Mode Integration:**
    *   Delegate task to `architect` or `qa-tester` mode: Review all `.clinerules` files and the `.roomodes` file.
    *   Verify that mode transitions, triggers, and handoff protocols are consistent across all modes as defined in `architecture_v11.md`.
    *   Check that interactions with the memory management system and verification procedures are correctly implemented.
    *   **Output:** Integration verification report, highlighting any inconsistencies to be resolved.

**Phase 4: Testing & Documentation Finalization**

1.  **Develop Test Plan:**
    *   Delegate task to `qa-tester` or `tdd` mode: Create a test plan focusing on the enhanced essay writing workflow.
    *   Include test cases for:
        *   Initiating an essay task via the orchestrator.
        *   Gathering research and quotations using the memory system.
        *   Drafting sections with accurate references.
        *   Running verification procedures (fact-checking, citation validation).
        *   Handling hallucinations or inaccuracies flagged by verification.
        *   Mode transitions and handoffs during the essay process.
    *   **Output:** `testing/essay_workflow_test_plan.md`.

2.  **Execute Tests (Simulated/Manual):**
    *   Delegate task to `qa-tester`: Execute the test plan, potentially involving manual steps or simulated mode interactions.
    *   Document results, identifying any bugs or deviations from expected behavior.
    *   **Output:** Test execution report (`testing/essay_workflow_test_results.md`).

3.  **Bug Fixing (Iterative):**
    *   Delegate task to `debugger` or `code` mode: Address any issues identified during testing by modifying the relevant `.clinerules` files.
    *   Re-run relevant tests until they pass.
    *   **Output:** Updated `.clinerules` files.

4.  **Finalize Documentation:**
    *   Delegate task to `architect` or `docs-writer` mode: Update `architecture_v11.md` to reflect any changes made during implementation and testing.
    *   Ensure all diagrams, mode descriptions, and workflows are accurate.
    *   Add usage examples or guidelines if necessary.
    *   **Output:** Final `architecture_v11.md`.

**Completion:** The successful completion of these phases will result in an enhanced RooCode suite for Hegel philosophy analysis, meeting the specified requirements for improved essay writing, referencing, and verification, along with the necessary configuration files and documentation.