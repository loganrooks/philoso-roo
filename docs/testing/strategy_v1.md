# philoso-roo Testing Strategy V1

**Date:** 2025-05-05
**Version:** 1.0
**Status:** Draft
**Related Documents:**
*   `docs/architecture/architecture_v18.md` (V18.3.4)
*   `docs/blueprints/mcp_integration_v1.md`
*   `docs/testing/kb_maintenance_plan_v1.md` (To be created)
*   `docs/project/operations.md` (To be created - for Rollback Procedures)

## 1. Objective

This document outlines the testing strategy for the `philoso-roo` system, focusing on ensuring the reliability, correctness, and robustness of its components and workflows, particularly considering the V18.3.4 architecture (Direct KB/MB Access, Distributed Maintenance, MCP Integration).

## 2. Scope

This strategy covers:
*   Unit testing for individual mode logic (where feasible).
*   Integration testing for interactions between modes, Memory Bank (MB), Knowledge Base (KB), and MCP servers.
*   End-to-End (E2E) testing for key user workflows.
*   Specific testing for critical components like distributed KB maintenance and MCP interactions.

## 3. Testing Levels & Approaches

### 3.1. Unit Testing

*   **Focus:** Testing individual functions or rules within a mode's `.clinerules` in isolation.
*   **Approach:** Due to the nature of `.clinerules` (declarative YAML), traditional unit testing is challenging. Focus will be on:
    *   **Schema Validation:** Automatically validating `.clinerules` files against a defined JSON schema (part of `docs/standards/clinerules_standard_v1.md` enhancements).
    *   **Rule Logic Review:** Manual or semi-automated review of rule logic for correctness, completeness, and adherence to standards.
    *   **Mocking (Conceptual):** For complex internal logic (if any develops beyond simple tool calls), consider if helper functions/scripts could be unit tested separately.
*   **Tools:** JSON Schema validators, Linters, Manual review checklists.

### 3.2. Integration Testing

*   **Focus:** Verifying interactions between components:
    *   Mode-to-Mode delegation (`Orchestrator` -> Mode -> `Orchestrator`).
    *   Mode-to-MB interactions (reading/writing logs, context).
    *   Mode-to-KB interactions (direct reads/writes, schema adherence, link integrity).
    *   Mode-to-MCP interactions (tool calls, error handling, result parsing).
    *   Distributed KB Maintenance interactions (`Orchestrator`, `MetaReflector`, `VerificationAgent`).
*   **Approach:**
    *   Define specific test scenarios simulating common interaction patterns.
    *   Use mock KB/MB states (pre-populated files) for predictable inputs.
    *   Use mock MCP servers or record/replay mechanisms (e.g., Polly.js concept adapted for MCP) to simulate external responses and failures.
    *   Assert expected state changes in MB/KB files and expected outcomes (e.g., task completion status, generated content).
    *   **Crucially, test distributed KB maintenance scenarios:** See `docs/testing/kb_maintenance_plan_v1.md` for details.
*   **Tools:** Test runner framework (potentially custom script orchestrating RooCode CLI runs), File comparison tools (`diff`), Mock MCP servers (custom or using mocking libraries if applicable to server implementation).

### 3.3. End-to-End (E2E) Testing

*   **Focus:** Validating complete user workflows from initial prompt to final output.
*   **Approach:**
    *   Define key user scenarios (e.g., "Analyze a new reading", "Generate essay draft on topic X", "Perform meta-reflection on KB consistency").
    *   Execute these scenarios using the full system stack (potentially with mock MCPs for external dependencies).
    *   Validate final outputs (e.g., generated KB entries, essay drafts, reports) against expected quality and correctness criteria.
    *   Validate MB/KB state consistency after workflow completion.
*   **Tools:** RooCode CLI, Manual review, File comparison tools.

## 4. Specific Component Testing

### 4.1. MCP Integration

*   **Focus:** Testing interactions with MCP servers (`fetcher`, `brave-search`, etc.).
*   **Approach:**
    *   **Mocking:** Develop mock MCP servers that return predefined successful responses, error conditions (timeouts, API errors, invalid data), and edge cases.
    *   **Contract Testing:** Ensure mode calls (`use_mcp_tool` arguments) match the MCP tool's input schema.
    *   **Error Handling Tests:** Verify that modes correctly handle various MCP errors according to standardized `.clinerules` patterns.
*   **Tools:** Mock MCP servers, JSON Schema validators.

### 4.2. Distributed KB Maintenance

*   **Focus:** Ensuring the combined actions of `Orchestrator`, `MetaReflector`, and `VerificationAgent` maintain KB integrity (link validation, schema checks, rigor consistency).
*   **Approach:** Detailed in `docs/testing/kb_maintenance_plan_v1.md`. Includes scenarios simulating concurrent edits (if applicable via locking), mode failures during maintenance tasks, and validation of KB health reports.
*   **Tools:** As defined in the KB Maintenance Test Plan.

## 5. Validation Metrics

*   **KB Consistency:** Percentage of KB entries passing schema validation; Number of broken links detected/resolved; Consistency of rigor field population.
*   **Task Success Rate:** Percentage of E2E workflows completing successfully without critical errors.
*   **Rigor Coverage:** Percentage of relevant KB entries with populated rigor fields; Qualitative assessment of rigor analysis depth.
*   **Error Handling Effectiveness:** Percentage of simulated MCP/internal errors handled gracefully according to defined patterns.
*   **Test Coverage:** (Difficult to quantify for `.clinerules`) Focus on coverage of key workflows, interaction patterns, and error conditions.

## 6. Rollback Procedures

*   **Git:** Used for managing changes to architecture documents, `.clinerules`, scripts, and potentially KB schema/templates. Standard Git workflows (feature branches, PRs, reverts) apply. Used for rolling back *design* or *code-level* changes.
*   **Checkpoints:** Used for task-level rollback within the RooCode environment. Allows reverting unwanted AI-generated changes or recovering from errors *during* a specific task run without affecting the main Git history. Primarily a development/debugging aid.
*   **Procedure:**
    1.  **Identify Issue:** Determine if the issue requires code/design rollback (Git) or task state rollback (Checkpoint).
    2.  **Checkpoint Rollback:** Use RooCode UI/CLI to revert to a previous checkpoint for the affected task. Re-run task from that point.
    3.  **Git Rollback:** Use standard Git commands (`git revert`, `git reset`, branch switching) to undo changes in the workspace. Requires careful coordination if KB/MB state is affected.
*   **Note:** Detailed procedures to be added to `docs/project/operations.md` (See Plan Step 11).

## 7. Test Environment

*   Testing should ideally occur in an environment mirroring production (same RooCode version, same available MCP servers).
*   Use separate Git branches for testing significant changes.
*   Consider dedicated KB/MB directories for specific test runs to avoid polluting main data.

## 8. Automation

*   Automate schema validation and linting for `.clinerules`.
*   Explore automation of integration tests using a test runner and mock servers.
*   E2E tests may remain partially manual initially due to the complexity of validating AI output quality.