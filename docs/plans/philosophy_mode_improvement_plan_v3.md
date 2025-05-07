# Hegel Philosophy Suite - Mode Improvement Plan V3

**Version:** 3.0
**Date:** 2025-05-02
**Status:** Draft
**Based On:**
*   `docs/architecture/architecture_v13.md`
*   `docs/plans/philosophy_mode_improvement_plan_v2.md` (Implicitly, as V3 builds upon V12 implementation)
*   Memory Bank Context (as of 2025-05-02 02:43)

**Goal:** Outline the implementation steps required to transition the Hegel Philosophy RooCode Suite from V12 to the V13 architecture. This involves establishing the Philosophy Knowledge Base (KB), implementing new modes (`philosophy-kb-manager`, `philosophy-meta-reflector`), refactoring existing modes to interact with the KB, integrating the Philosophical Inquiry and System Self-Reflection workflows, and ensuring robust testing and documentation.

---

## Phase 0: Pre-Implementation Setup & Review (V13)

*   **Objective:** Prepare the workspace and ensure alignment before major implementation.
*   **Steps:**
    1.  **Verify V12 Completion:** (System/Architect) Confirm all V12 implementation steps (per Plan V2 and subsequent fixes) are complete and verified. Review `clinerules_verification_report_v1.md` and related logs.
    2.  **Backup Current State:** (DevOps/User) Create a Git tag or branch representing the stable V12 state before starting V13 modifications. `git tag v12.0` or `git checkout -b v13-development`.
    3.  **Create KB Directory Structure:** (Architect/DevOps) Create the initial `philosophy-knowledge-base/` directory and its subdirectories as defined in `architecture_v13.md` (concepts, arguments, references, questions, theses, relationships, methods, meta-reflections, indices). Add placeholder `.gitkeep` files if needed. Add `philosophy-knowledge-base/` to `.gitignore` if KB versioning is deferred.
    4.  **Plan Review & Approval:** (User/Architect) Review and approve this V3 plan.

## Phase 1: Implement Core KB & Meta-Reflection Modes (V13)

*   **Objective:** Implement the foundational modes for the new KB and self-reflection capabilities.
*   **Steps:**
    1.  **Implement `philosophy-kb-manager`:** (Code)
        *   Create `.roo/rules-philosophy-kb-manager/philosophy-kb-manager.clinerules`.
        *   Define identity, description, and core logic for interacting with `philosophy-knowledge-base/` (CRUD operations, querying based on entry type/tags/IDs, managing links). Initially focus on Markdown file I/O. Include logic for executing approved modification instructions.
        *   Define interfaces for receiving queries/data and returning results.
    2.  **Implement `philosophy-meta-reflector`:** (Code)
        *   Create `.roo/rules-philosophy-meta-reflector/philosophy-meta-reflector.clinerules`.
        *   Define identity, description, and core logic for analyzing system components (MB via `evidence-manager`, KB via `kb-manager`, docs, rules).
        *   Implement logic for generating meta-reflections/questions based on `architecture-questioning.md` principles.
        *   Define interfaces for storing reflections/questions via `kb-manager` and proposing modifications via `orchestrator`.
    3.  **Update Configuration:** (Code) Add `philosophy-kb-manager` and `philosophy-meta-reflector` entries to `.roo/.roomodes`.

## Phase 2: Refactor Existing Modes for KB Integration (V13)

*   **Objective:** Update existing modes to utilize the new `philosophy-kb-manager` for philosophical data and decouple them from `philosophy-evidence-manager` for this purpose.
*   **Steps:** (Delegate each sub-step to Code mode sequentially or in parallel batches)
    1.  **Refactor `philosophy-evidence-manager`:** (Code) Remove any logic related to managing philosophical domain knowledge (concepts, arguments, etc.). Ensure it focuses solely on Operational Memory (`memory-bank/`) access. Update its `.clinerules`.
    2.  **Refactor `philosophy-text-processor`:** (Code) Modify output logic to send index/chunk info and citation data to `philosophy-kb-manager` instead of `philosophy-evidence-manager`. Update its `.clinerules`.
    3.  **Refactor Analysis Modes (`pre-lecture`, `class-analysis`, `secondary-lit`, `dialectical-analysis`):** (Code)
        *   Update query logic to use `philosophy-kb-manager` for accessing processed texts, concepts, arguments, etc.
        *   Update storage logic to send analysis outputs (concepts, arguments, proto-questions) to `philosophy-kb-manager`.
        *   Update `.clinerules` for each mode.
    4.  **Refactor `philosophy-questioning`:** (Code)
        *   Update query logic to use `philosophy-kb-manager` for retrieving proto-questions and related KB entries.
        *   Update storage logic to send refined philosophical questions to `philosophy-kb-manager`.
        *   Ensure focus is on *philosophical inquiry* questions, distinct from meta-questions. Update `.clinerules`.
    5.  **Refactor Essay Modes (`essay-prep`, `draft-generator`, `citation-manager`, `verification-agent`):** (Code)
        *   Update query logic in all modes to use `philosophy-kb-manager` for retrieving evidence, references, theses, questions, and processed chunk paths/indices.
        *   Update `essay-prep` storage logic to send developed theses to `philosophy-kb-manager`.
        *   Update `.clinerules` for each mode.

## Phase 3: Integrate Workflows & Orchestration (V13)

*   **Objective:** Ensure the new KB, modes, and workflows are correctly orchestrated.
*   **Steps:**
    1.  **Refactor `philosophy-orchestrator`:** (Code)
        *   Update delegation logic to correctly route tasks involving philosophical data to `philosophy-kb-manager` and operational context data to `philosophy-evidence-manager`.
        *   Implement logic for the `Philosophical Inquiry Workflow` (coordinating `kb-manager`, `questioning`, `essay-prep`).
        *   Implement logic for the `System Self-Reflection Workflow` (triggering `meta-reflector`, routing proposals to User, relaying approvals to `kb-manager`/`architect`/`devops`).
        *   Implement logic for the `KB Modification Workflow`.
        *   Update `.clinerules`.
    2.  **Integration Verification:** (Architect/QA Tester)
        *   Review updated `.clinerules` for all modes against `architecture_v13.md`.
        *   Verify data flow diagrams and sequence diagrams for the new workflows.
        *   Create an `integration_verification_report_v13.md`.

## Phase 4: Testing (V13)

*   **Objective:** Test the new KB functionality, refactored modes, and integrated workflows.
*   **Steps:**
    1.  **Develop Test Plan V2:** (QA Tester) Update the test plan to include specific scenarios for:
        *   Populating the KB via `text-processor` and analysis modes.
        *   Querying the KB via `kb-manager` from various modes.
        *   Executing the Philosophical Inquiry Workflow (question generation -> refinement -> thesis).
        *   Executing the System Self-Reflection Workflow (triggering reflection -> storing output -> proposing KB change -> user approval -> KB modification).
        *   Essay generation using the KB via `kb-manager`.
        *   Verification using KB data via `kb-manager`.
    2.  **Unit Testing:** (Code/TDD) Write/update unit tests for `kb-manager` and `meta-reflector` logic.
    3.  **Integration Testing:** (QA Tester/Integration) Execute test scenarios defined in the plan, focusing on interactions between modes and the `kb-manager`, and the correct functioning of the new workflows via the `orchestrator`.
    4.  **Workflow Testing:** (QA Tester/User) Perform end-to-end tests for key workflows (text processing, analysis, inquiry, reflection, essay writing).
    5.  **Bug Fixing:** (Debugger/Code) Address issues identified during testing.

## Phase 5: Documentation & Finalization (V13)

*   **Objective:** Update all relevant documentation and finalize the V13 release.
*   **Steps:**
    1.  **Update Architecture Document:** (Architect) Finalize `docs/architecture/architecture_v13.md` based on any changes during implementation.
    2.  **Update Mode Documentation:** (Docs Writer/Architect) Update READMEs or documentation for all modified/new modes, explaining their V13 roles and interactions, especially regarding `kb-manager` vs `evidence-manager`.
    3.  **Update User Guide:** (Docs Writer) Update any user-facing documentation explaining how to interact with the new workflows (Inquiry, Reflection).
    4.  **Final Review:** (Architect/User) Review all changes and documentation.
    5.  **Tag Release:** (DevOps/User) Create a Git tag for the V13 release (`git tag v13.0`).

---