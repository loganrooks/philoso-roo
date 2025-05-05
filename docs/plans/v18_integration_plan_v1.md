# V18.3.3 Architecture Evaluation Integration Plan (v1)

Date: 2025-05-05

## 1. Objective

This plan outlines the steps required to address the recommendations from the V18.3.3 architecture evaluation report (`docs/reports/architecture_v18_evaluation_v1.md` v6), prioritizing critical gaps and foundational improvements.

## 2. Summary of Key Evaluation Findings

The evaluation identified several key areas requiring attention:

*   **Critical Gap:** Undefined strategy for Model Context Protocol (MCP) integration, hindering access to external data.
*   **High Risk:** Distributed Knowledge Base (KB) maintenance complexity and lack of robust testing strategy.
*   **Need for Standardization:** Inconsistent patterns for cross-mode communication, error handling, Memory Bank (MB) updates, and `.clinerules` structure.
*   **Documentation Gaps:** Inaccurate architecture diagram, missing MB pattern description, lack of clarity on task delegation and Checkpoints.

## 3. Implementation Steps (Prioritized)

The following steps will be executed sequentially to address the evaluation recommendations. Steps marked with `[DELEGATE?]` may be suitable for delegation to other modes or require separate, dedicated tasks.

1.  **Correct Architecture Diagram (Rec 3.2)**
    *   **Action:** Modify Mermaid diagram in `docs/architecture/architecture_v18.md` (Sec 5) to remove `KBDoctor` and accurately reflect distributed maintenance roles (`Orchestrator`, `MetaReflector`, `VerificationAgent`).
    *   **Tools:** `read_file`, `apply_diff`.
    *   **Complexity:** Low.
    *   **Dependencies:** None.

2.  **Define MCP Integration Strategy & Blueprint (Rec 3.1, 3.11)**
    *   **Action:** Create a dedicated blueprint document `docs/blueprints/mcp_integration_v1.md`. Update `docs/architecture/architecture_v18.md` (Sec 4/7) to reference the blueprint and summarize the chosen strategy.
    *   **Details:** The blueprint should compare implementation alternatives (e.g., dedicated `Research` mode vs. distributed calls), define workflows, responsibilities, data formats, error handling, configuration (`settings.json`), and security (API keys via env vars).
    *   **Tools:** `write_to_file` (for blueprint), `read_file`, `apply_diff` (for Arch Doc).
    *   **Complexity:** High (Requires design decisions).
    *   **Dependencies:** None.
    *   **`[DELEGATE?]`**: Blueprint creation could be a separate task for Architect.

3.  **Define Testing Strategy (Rec 3.9, 3.13)**
    *   **Action:** Create `docs/testing/strategy_v1.md` and `docs/testing/kb_maintenance_plan_v1.md`.
    *   **Details:** Outline unit, integration, E2E tests. Include MCP mock strategy, validation metrics, Git rollback. Detail specific integration tests for distributed KB maintenance and E2E tests for MCP workflows. The KB maintenance plan should cover specific scenarios, data setup, and validation for `Orchestrator`, `MetaReflector`, `VerificationAgent` interactions.
    *   **Tools:** `write_to_file`.
    *   **Complexity:** Medium-High.
    *   **Dependencies:** MCP Strategy (Step 2).
    *   **`[DELEGATE?]`**: KB Maintenance Test Plan could be delegated to QA Tester.

4.  **Propose `.clinerules` Standard Enhancements (Rec 3.10, 3.15)**
    *   **Action:** Document proposed enhancements for `docs/standards/clinerules_standard_v1.md` within this plan or a temporary file. (Actual update to the standard is a separate task).
    *   **Details:** Propose standard patterns/snippets for MB I/O (batching), KB validation hooks, error logging, `apply_diff` handling, MCP interaction, rule inheritance mechanisms, and multi-mode coordination (locking, etc.).
    *   **Tools:** N/A (Documentation within this plan).
    *   **Complexity:** Medium.
    *   **Dependencies:** MCP Strategy (Step 2).

5.  **Formalize Task Delegation (Rec 3.3)**
    *   **Action:** Update `Orchestrator.clinerules`. Recommend creation of sequence diagrams (Rec 3.12 - separate task).
    *   **Details:** Define sub-task result handling, context passing strategy (MB refs vs. message content), and potentially reference sequence diagrams.
    *   **Tools:** `read_file`, `apply_diff`.
    *   **Complexity:** Medium.
    *   **Dependencies:** `.clinerules` Standard Enhancements (Step 4).

6.  **Strengthen Distributed Maintenance & Monitoring (Rec 3.7)**
    *   **Action:** Update `.clinerules` for `Orchestrator`, `MetaReflector`, `VerificationAgent`.
    *   **Details:** Implement scheduled/triggered health checks, rigor checks, health metrics, cross-checking logic. Add rule for `MetaReflector` to generate user reports.
    *   **Tools:** `read_file`, `apply_diff`.
    *   **Complexity:** High.
    *   **Dependencies:** Testing Strategy (Step 3), `.clinerules` Standard Enhancements (Step 4).

7.  **Enforce File Tool Best Practices (Rec 3.4)**
    *   **Action:** Update `general.error_handling_protocol` section in all relevant philosophy mode `.clinerules` files.
    *   **Details:** Add rules prioritizing `apply_diff`/`insert_content`, mandating partial reads, and providing specific `apply_diff` error handling examples.
    *   **Tools:** `read_file`, `apply_diff` (potentially `search_files` to find all relevant files).
    *   **Complexity:** Low-Medium (Repetitive).
    *   **Dependencies:** `.clinerules` Standard Enhancements (Step 4).

8.  **Document Memory Bank Pattern & Persistence (Rec 3.5)**
    *   **Action:** Add a new subsection to `docs/architecture/architecture_v18.md`.
    *   **Details:** Describe `phil-memory-bank/` structure, update format/order, file-based persistence, and scalability notes.
    *   **Tools:** `read_file`, `insert_content`.
    *   **Complexity:** Low.
    *   **Dependencies:** None.

9.  **Evaluate & Document Checkpoints (Rec 3.8)**
    *   **Action:** Add Decision Log entry to `memory-bank/globalContext.md`. Add subsection to `docs/architecture/architecture_v18.md`. Add rule suggestion to `EssayPrep.clinerules`.
    *   **Details:** Log decision to enable Checkpoints. Document feature, UX implications, and role in Arch Doc. Add rule for `EssayPrep` to suggest manual checkpoints.
    *   **Tools:** `read_file`, `insert_content` (for MB/Arch Doc), `apply_diff` (for `.clinerules`).
    *   **Complexity:** Low-Medium.
    *   **Dependencies:** None.

10. **Define Versioning Strategy (Rec 3.14)**
    *   **Action:** Add section to `docs/architecture/architecture_v18.md` or create `docs/project/versioning.md`.
    *   **Details:** Specify Git branch/tag strategy. Recommend `.clinerules` version metadata.
    *   **Tools:** `read_file`, `insert_content` or `write_to_file`.
    *   **Complexity:** Low.
    *   **Dependencies:** None.

11. **Define Rollback Procedures (Rec 3.16)**
    *   **Action:** Add section to `docs/testing/strategy_v1.md` (created in Step 3) or create `docs/project/operations.md`.
    *   **Details:** Clarify Git vs. Checkpoints for different rollback scenarios.
    *   **Tools:** `read_file`, `insert_content` or `write_to_file`.
    *   **Complexity:** Low.
    *   **Dependencies:** Testing Strategy (Step 3), Checkpoint Documentation (Step 9).

12. **Plan Script-to-MCP Migration (Rec 3.6)**
    *   **Action:** Add Decision Log entry to `memory-bank/globalContext.md`.
    *   **Details:** Log decision to schedule periodic review of `process_source_text.py` complexity and prioritize migration to MCP if needed.
    *   **Tools:** `read_file`, `insert_content`.
    *   **Complexity:** Low.
    *   **Dependencies:** None.

13. **Define Migration Strategy (Rec 3.17)**
    *   **Action:** Recommend creation of `docs/project/migration_strategy_v1.md` (separate task).
    *   **Details:** Log this recommendation in `memory-bank/activeContext.md`.
    *   **Tools:** `read_file`, `insert_content`.
    *   **Complexity:** Low (Logging recommendation only).
    *   **Dependencies:** Completion of other steps.
    *   **`[DELEGATE?]`**: Actual strategy creation is a separate task.

## 4. Dependencies & Sequencing

*   The **MCP Strategy/Blueprint (Step 2)** is foundational for several other steps, including Testing (Step 3) and `.clinerules` enhancements (Step 4).
*   The **Testing Strategy (Step 3)** should inform the detailed implementation of Distributed Maintenance (Step 6).
*   **`.clinerules` Standard Enhancements (Step 4)** should ideally precede detailed updates to individual mode rules (Steps 5, 6, 7).
*   Documentation updates (Steps 1, 8, 9, 10, 11) can largely proceed in parallel but should reflect decisions made in other steps (e.g., MCP strategy).

## 5. Next Steps

Begin execution with Step 1: Correct Architecture Diagram.