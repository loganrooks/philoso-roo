# Task Prompt: Enhance Hegel Philosophy RooCode Suite (V2)

**Goal:** Refactor and enhance the existing suite of custom RooCode modes (`.roomodes`) designed for processing PHL316 (Hegel philosophy course) materials. The primary focus is to significantly improve the system's capability for generating well-structured philosophical essays with accurate textual references, robust verification procedures, effective memory/knowledge management, integrated text processing, and version control.

**Deliverables:**

1.  **Updated Architecture Document:** `architecture_v12.md` (Completed).
2.  **New `.roomodes` Configuration:** A `.roo/.roomodes` file defining the complete suite of modes based on V12.
3.  **Refactored/New `.clinerules` Files:** Updated `.clinerules` files for all modes reflecting `architecture_v12.md`, placed in `.roo/rules-[mode-slug]/`.
4.  **New/Updated Scripts:** External scripts (e.g., Python) required by `philosophy-text-processor`.
5.  **Memory Management System Implementation:** Files and configurations defining the `knowledge_base` structure.
6.  **Version Control Setup:** Initialized Git repository (if needed) and `.gitignore`.

**Key Requirements (Updated):**

*   **Essay Writing Enhancement:** As per original plan.
*   **Reference Accuracy:** As per original plan, enhanced by `philosophy-text-processor`'s citation extraction.
*   **Hallucination Prevention:** As per original plan, leveraging the detailed `knowledge_base`.
*   **Knowledge Management:** Implement the `knowledge_base` structure as defined in `architecture_v12.md`, managed via `philosophy-evidence-manager`.
*   **Advanced Text Processing:** Implement the `philosophy-text-processor` mode and associated scripts for chunking, indexing, and citation extraction from large Markdown sources.
*   **Version Control:** Integrate Git for versioning key artifacts (essays, potentially processed sources, configurations) via mode interactions (`execute_command`).
*   **Modularity & Orchestration:** As per original plan, guided by `architecture_v12.md`.
*   **RooCode Standards:** As per original plan.
*   **New File Structure:** As per original plan.

**Inputs:**

*   Existing `.clinerules` files (to be refactored).
*   `architecture_v12.md`.
*   `new_requirements_spec_v1.md`.
*   User requirements outlined in the initial request and subsequent feedback [2025-05-01 19:21:04].

---

# Implementation Plan V2 for the System Orchestrator

This plan outlines the steps to refactor and enhance the Hegel Philosophy RooCode Suite based on `architecture_v12.md`.

**Phase 0: Pre-Implementation Setup & Review**

1.  **Initialize Version Control (if needed):**
    *   Delegate to `devops` or `architect`: Check if a Git repository exists in the workspace root.
    *   If not, execute `git init`.
    *   Ensure a suitable `.gitignore` file exists, adding entries for temporary files, logs, etc.
    *   **Output:** Initialized Git repository, updated `.gitignore`.

2.  **Review Potentially Problematic Artifacts (User Feedback):**
    *   Delegate to `holistic-reviewer` or `architect`: Review files potentially affected by the previous system instance's issues (approx. 17:33 - 17:49), specifically `clinerules_revision_plan_v1.md`, `clinerules_template_v1.md`, and any generated `.clinerules` content (like the draft `philosophy-orchestrator.clinerules` mentioned in logs).
    *   Cross-reference these artifacts against the *new* `architecture_v12.md` and `new_requirements_spec_v1.md`.
    *   Identify any inconsistencies or sections needing revision *before* proceeding with `.clinerules` implementation based on potentially flawed intermediate plans/templates.
    *   **Output:** Review report (`artifact_review_report_v1.md`) detailing necessary adjustments or confirming validity.

**Phase 1: Architecture & Design Definition (Completed)**

1.  **Review Existing Assets:** (Completed - Output: `architecture_review_summary_v2.md`)
2.  **Design New Architecture (V11):** (Completed - Output: `architecture_v11.md`)
3.  **Incorporate New Requirements (V12):** (Completed - Output: `architecture_v12.md`)

**Phase 2: Mode & Script Implementation**

1.  **Implement `philosophy-text-processor` Scripts:**
    *   Delegate task to `code` mode: Develop the external scripts (e.g., Python) required by `philosophy-text-processor` as defined in `architecture_v12.md` and `new_requirements_spec_v1.md`.
    *   Scripts should handle: Markdown parsing, recursive splitting based on headers, chunk size enforcement (token counting), `index.md` generation (summaries, concepts, args, links, metadata), detailed citation extraction, file I/O for the specified directory structure (`source_materials/processed/`), and potentially formatting correction based on a manifest.
    *   Place scripts in the `scripts/` directory (e.g., `scripts/process_source_text.py`). Include a `README.md` explaining usage.
    *   **Output:** Functional Python scripts, `scripts/README.md`.

2.  **Create/Refactor `.clinerules` Files:**
    *   Delegate task to `spec-pseudocode` or `code` mode (iteratively for each mode):
        *   **New Modes:** Create `.clinerules` for `philosophy-text-processor`, `philosophy-evidence-manager`, `philosophy-draft-generator`, `philosophy-citation-manager`, `philosophy-verification-agent`, `philosophy-orchestrator`.
        *   **Refactored Modes:** Update `.clinerules` for `philosophy-pre-lecture`, `philosophy-class-analysis`, `philosophy-secondary-lit`, `philosophy-dialectical-analysis`, `philosophy-questioning`, `philosophy-essay-prep`.
    *   **Implementation Details:**
        *   Base rules on `architecture_v12.md` and the findings from the Phase 0 artifact review.
        *   Implement interactions with `philosophy-evidence-manager` for `knowledge_base` access.
        *   Implement `philosophy-text-processor` orchestration logic (calling scripts).
        *   Implement Git command execution (`execute_command`) within relevant modes (`essay-prep`, `orchestrator`) for version control actions.
        *   Ensure adherence to RooCode standards and handoff protocols.
        *   Save files to `.roo/rules-[mode-slug]/[mode-slug].clinerules`.
    *   **Output:** New and refactored `.clinerules` files in the correct directory structure.

**Phase 3: Configuration & Integration**

1.  **Create `.roomodes` Configuration File:**
    *   Delegate task to `architect` or `code` mode: Create the `.roo/.roomodes` file based on `architecture_v12.md`.
    *   List all 12 philosophy modes and their `.clinerules` paths.
    *   **Output:** The `.roo/.roomodes` configuration file.

2.  **Verify Mode Integration:**
    *   Delegate task to `architect` or `qa-tester` mode: Review all `.clinerules` files and `.roomodes`.
    *   Verify consistency with `architecture_v12.md` (mode transitions, triggers, handoffs, KB interactions, text processor script calls, Git command usage).
    *   **Output:** Integration verification report (`integration_verification_report_v12.md`).

**Phase 4: Testing & Documentation Finalization**

1.  **Develop Test Plan:**
    *   Delegate task to `qa-tester` or `tdd` mode: Create a test plan (`testing/workflow_test_plan_v2.md`) focusing on:
        *   `philosophy-text-processor` workflow (chunking, indexing, citation extraction).
        *   Essay writing workflow, including version control actions (commit, log, checkout).
        *   Verification procedures.
        *   Knowledge base interactions.
    *   **Output:** `testing/workflow_test_plan_v2.md`.

2.  **Execute Tests (Simulated/Manual):**
    *   Delegate task to `qa-tester`: Execute the test plan.
    *   Document results (`testing/workflow_test_results_v2.md`).
    *   **Output:** Test execution report.

3.  **Bug Fixing (Iterative):**
    *   Delegate task to `debugger` or `code` mode: Address issues found during testing.
    *   Commit fixes using Git.
    *   Re-run tests.
    *   **Output:** Updated `.clinerules` files, scripts.

4.  **Finalize Documentation:**
    *   Delegate task to `architect` or `docs-writer` mode: Update `architecture_v12.md` and potentially script READMEs to reflect final implementation details.
    *   **Output:** Final `architecture_v12.md`, updated READMEs.

**Completion:** Successful completion results in an enhanced RooCode suite meeting V2 requirements, with all deliverables produced and verified.