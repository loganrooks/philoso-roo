# Hegel Philosophy RooCode Suite - V15 Implementation Plan (V4)

**Version:** 1.0
**Date:** 2025-05-02
**Status:** Proposed
**Architecture Reference:** `docs/architecture/architecture_v15.md`

## 1. Overview

This plan outlines the steps required to implement the V15 architecture for the Hegel Philosophy RooCode Suite. The primary goal is to transition from the V14 `kb-manager`-centric model to the V15 Direct Knowledge Base (KB) Access model, involving the removal of `philosophy-kb-manager`, the introduction of `philosophy-kb-doctor`, and the refactoring of existing modes to interact directly with the `philosophy-knowledge-base/`.

## 2. Prerequisites

*   Final approval of the V15 architecture defined in `docs/architecture/architecture_v15.md`.
*   Workspace is under version control (Git), and a dedicated branch (e.g., `v15-direct-kb-access`) is created for this implementation.

## 3. Implementation Phases

### Phase 0: Preparation

**Goal:** Set up the basic structure for the new mode and update configuration.

*   **Step 0.1: Create `philosophy-kb-doctor` Mode Structure**
    *   **Mode:** `devops` / `architect`
    *   **Action:**
        *   Create directory: `.roo/rules-philosophy-kb-doctor/`
        *   Create placeholder file: `.roo/rules-philosophy-kb-doctor/philosophy-kb-doctor.clinerules` with basic identity section.
        *   Create feedback file: `memory-bank/feedback/philosophy-kb-doctor-feedback.md` with standard header.
*   **Step 0.2: Update `.roomodes` Configuration**
    *   **Mode:** `code`
    *   **Action:**
        *   Edit the relevant `.roomodes` file (e.g., `.roo/.roomodes` or a philosophy-specific one if it exists).
        *   Remove the entry for `philosophy-kb-manager`.
        *   Add an entry for `philosophy-kb-doctor` pointing to its new `.clinerules` file.

### Phase 1: Refactor Existing Modes for Direct KB Access

**Goal:** Update all modes previously reliant on `philosophy-kb-manager` to use direct file system access tools according to V15 specifications.

*   **Step 1.X (Iterate for each mode): Refactor [Mode Name]**
    *   **Mode:** `code`
    *   **Target Modes:**
        *   `philosophy-text-processor`
        *   `philosophy-pre-lecture`
        *   `philosophy-class-analysis`
        *   `philosophy-secondary-lit`
        *   `philosophy-dialectical-analysis`
        *   `philosophy-questioning`
        *   `philosophy-meta-reflector`
        *   `philosophy-essay-prep`
        *   `philosophy-draft-generator`
        *   `philosophy-citation-manager`
        *   `philosophy-verification-agent`
    *   **Action (for each target mode):**
        1.  **Read `.clinerules`:** Load the current `.clinerules` file for the target mode.
        2.  **Remove `kb-manager` Dependency:** Delete any instructions, prompts, or logic related to calling or interacting with `philosophy-kb-manager`.
        3.  **Embed KB Knowledge:** Add/update a dedicated section in the `.clinerules` detailing:
            *   KB Base Path (`philosophy-knowledge-base/`).
            *   Relevant subdirectories for read/write access (per `architecture_v15.md`, Section 5).
            *   File naming conventions for reading/writing.
            *   Expected file formats (Markdown + YAML).
            *   Specific protocols for using `read_file`, `search_files`, `write_to_file`, `insert_content`.
        4.  **Implement Direct Access Logic:** Modify the mode's workflow and instructions to use the appropriate file system tools (`read_file`, `search_files`, etc.) directly on the `philosophy-knowledge-base/` path, following the embedded KB knowledge and V15 write access rules.
        5.  **Update Error Handling:** Ensure robust error handling is implemented for file operations (file not found, permissions issues, write failures).
        6.  **Write Updated `.clinerules`:** Save the modified `.clinerules` file.
        7.  **Memory Bank Update:** Log the refactoring action in `activeContext.md` and potentially `globalContext.md` Progress section.

### Phase 2: Implement `philosophy-kb-doctor` Mode

**Goal:** Implement the core functionality of the new KB maintenance mode.

*   **Step 2.1: Implement `kb-doctor` Logic**
    *   **Mode:** `code`
    *   **Action:**
        1.  **Read Placeholder `.clinerules`:** Load `.roo/rules-philosophy-kb-doctor/philosophy-kb-doctor.clinerules`.
        2.  **Define Responsibilities:** Implement the core logic based on `architecture_v15.md`, Section 6:
            *   **Indexing:** Logic to scan relevant KB directories (e.g., `concepts/`, `arguments/`) and generate/update index files in `indices/` (e.g., `master_index.md`). Use `list_files`, `read_file`, `write_to_file`.
            *   **Validation:** Logic to check file naming conventions, YAML structure, and potentially internal link validity within the KB. Use `list_files`, `read_file`, `search_files`.
            *   **Reporting:** Logic to report findings (success, errors, validation issues) to the user/orchestrator.
        3.  **Embed KB Knowledge:** Include necessary knowledge about KB structure for scanning and indexing.
        4.  **Write Updated `.clinerules`:** Save the implemented `.clinerules` file.
        5.  **Memory Bank Update:** Log the implementation in `activeContext.md`.

### Phase 3: Integration & Testing

**Goal:** Verify that the refactored modes interact correctly with the KB and that the `kb-doctor` functions as expected.

*   **Step 3.1: Test Direct KB Access Workflow**
    *   **Mode:** `qa-tester` / `integration`
    *   **Action:** Design and execute test cases simulating common workflows that involve multiple modes reading from and writing to the KB (e.g., processing a source text, analyzing it, generating questions, using the analysis in an essay draft). Verify data consistency and correct file operations.
*   **Step 3.2: Test `kb-doctor` Functionality**
    *   **Mode:** `qa-tester` / `devops`
    *   **Action:** Trigger `philosophy-kb-doctor` manually. Verify that index files are created/updated correctly in `indices/`. Verify that validation checks run and report expected results (introduce deliberate errors to test detection).

### Phase 4: Documentation Update

**Goal:** Update project documentation to reflect the V15 architecture.

*   **Step 4.1: Update Mode Documentation**
    *   **Mode:** `docs-writer`
    *   **Action:** Review and update any existing READMEs or documentation for the refactored modes to reflect the removal of `kb-manager` and the new direct KB interaction patterns. Create documentation for `philosophy-kb-doctor`.
*   **Step 4.2: Update Overall System Documentation**
    *   **Mode:** `docs-writer` / `architect`
    *   **Action:** Ensure any high-level system documentation accurately reflects the V15 architecture.

## 4. Rollback Plan

*   In case of critical issues during implementation, revert changes using Git version control by checking out the commit before the V15 implementation started (or the last stable commit within the `v15-direct-kb-access` branch).
*   Re-introduce the `philosophy-kb-manager` `.clinerules` and update `.roomodes` if reverting fully to V14.
*   Analyze failure points documented in Memory Bank feedback files before attempting re-implementation.