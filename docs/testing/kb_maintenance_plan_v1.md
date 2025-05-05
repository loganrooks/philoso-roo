# philoso-roo KB Maintenance Test Plan V1

**Date:** 2025-05-05
**Version:** 1.0
**Status:** Draft
**Related Documents:**
*   `docs/architecture/architecture_v18.md` (V18.3.4)
*   `docs/testing/strategy_v1.md`

## 1. Objective

This plan details specific test scenarios and validation methods for the distributed Knowledge Base (KB) maintenance approach in `philoso-roo` V18.3.4, involving `Orchestrator`, `MetaReflector`, and `VerificationAgent`. The goal is to ensure this distributed system reliably maintains KB integrity (schema, links, rigor consistency).

## 2. Scope

*   Testing the triggering logic in `Orchestrator`.
*   Testing the analysis, validation, and reporting logic in `MetaReflector`.
*   Testing the validation logic in `VerificationAgent` during workflows.
*   Testing interactions between these modes and the KB/MB.
*   Testing handling of simulated failures and edge cases.

## 3. Test Environment & Setup

*   **Environment:** As defined in `docs/testing/strategy_v1.md` (ideally mirroring production).
*   **Data Setup:**
    *   Create a dedicated test KB directory (`philosophy-knowledge-base-test/`) populated with a representative sample of entries (concepts, arguments, references, etc.).
    *   Include entries with:
        *   Correct schema and links.
        *   Known schema errors (e.g., missing required fields).
        *   Broken links (`related_ids` pointing to non-existent entries).
        *   Missing rigor fields.
        *   Inconsistent rigor information (e.g., claim verified but lacks source link).
    *   Create corresponding mock MB files (`phil-memory-bank-test/`) with relevant context/logs if needed for specific scenarios.

## 4. Test Scenarios

### 4.1. `MetaReflector` - Scheduled/Triggered Checks

*   **Scenario MR-1: Basic Health Check (Scheduled)**
    *   **Trigger:** Simulate scheduled trigger for `MetaReflector`.
    *   **Action:** `MetaReflector` performs standard checks (schema validation, link integrity) on the test KB.
    *   **Expected Outcome:** `MetaReflector` logs findings (identifying known errors/broken links) to its operational log (`phil-memory-bank-test/mode-specific/philosophy-meta-reflector.md`) and generates a summary report in `philosophy-knowledge-base-test/_operational/reports/`. Report should accurately reflect the pre-defined errors.
*   **Scenario MR-2: Rigor Consistency Check (Triggered)**
    *   **Trigger:** `Orchestrator` delegates a specific rigor check task to `MetaReflector` (e.g., "Verify all 'Verified' arguments have valid `source_ref_keys`").
    *   **Action:** `MetaReflector` analyzes relevant KB entries.
    *   **Expected Outcome:** `MetaReflector` identifies entries failing the check, logs details, and reports findings back to `Orchestrator` (via `attempt_completion` or log update, depending on defined interaction).
*   **Scenario MR-3: Pattern Identification**
    *   **Trigger:** Simulate scheduled trigger. Populate test MB logs with patterns (e.g., frequent use of a specific vague term).
    *   **Action:** `MetaReflector` analyzes KB and MB logs.
    *   **Expected Outcome:** `MetaReflector` identifies the pattern, logs the finding, and potentially proposes a refinement (e.g., suggesting a new concept definition) to `Orchestrator`.
*   **Scenario MR-4: Failure During Check**
    *   **Trigger:** Simulate scheduled trigger. Introduce a condition causing `MetaReflector` to fail mid-process (e.g., mock file read error).
    *   **Action:** `MetaReflector` attempts checks.
    *   **Expected Outcome:** `MetaReflector` logs the failure clearly, potentially attempts retry/fallback if defined, and reports failure status to `Orchestrator` or logs appropriately without leaving system in inconsistent state.

### 4.2. `VerificationAgent` - Workflow Checks

*   **Scenario VA-1: Verify Valid Draft**
    *   **Trigger:** `EssayPrep` delegates verification of a draft essay that is consistent with the test KB (valid claims, correct citations, populated rigor fields).
    *   **Action:** `VerificationAgent` reads draft, relevant KB entries, and source chunks.
    *   **Expected Outcome:** `VerificationAgent` generates a positive verification report, logs success.
*   **Scenario VA-2: Verify Draft with Claim Contradiction**
    *   **Trigger:** `EssayPrep` delegates verification of a draft containing a claim contradicting a 'Verified' KB entry.
    *   **Action:** `VerificationAgent` performs checks.
    *   **Expected Outcome:** `VerificationAgent` identifies the contradiction, generates a report detailing the issue, flags relevant KB entry/draft section, logs the finding, and potentially triggers correction loop via `Orchestrator`.
*   **Scenario VA-3: Verify Draft with Missing Rigor**
    *   **Trigger:** `EssayPrep` delegates verification of a draft referencing a KB concept missing required rigor fields (e.g., `presuppositions`).
    *   **Action:** `VerificationAgent` performs checks.
    *   **Expected Outcome:** `VerificationAgent` identifies the missing rigor, notes it in the report, logs the finding.
*   **Scenario VA-4: Verify Draft with Broken Citation Link**
    *   **Trigger:** `EssayPrep` delegates verification of a draft citing a `source_ref_key` that doesn't exist in the KB `references/` directory.
    *   **Action:** `VerificationAgent` performs checks.
    *   **Expected Outcome:** `VerificationAgent` identifies the broken link, reports the error.

### 4.3. `Orchestrator` - Triggering & Coordination

*   **Scenario OR-1: Triggering Maintenance**
    *   **Trigger:** Simulate condition requiring KB maintenance (e.g., time-based schedule, specific user request forwarded to `Orchestrator`).
    *   **Action:** `Orchestrator` delegates appropriate check task (e.g., general health check, specific rigor validation) to `MetaReflector`.
    *   **Expected Outcome:** `MetaReflector` receives task, executes checks, `Orchestrator` correctly logs delegation and receives/processes completion status from `MetaReflector`.
*   **Scenario OR-2: Handling Verification Failure**
    *   **Trigger:** `VerificationAgent` reports a verification failure (e.g., Scenario VA-2).
    *   **Action:** `Orchestrator` receives failure report.
    *   **Expected Outcome:** `Orchestrator` logs the failure, potentially delegates a correction task (e.g., back to `DraftGen` or `ClassAnalysis`), or escalates to user based on defined rules.

## 5. Validation Methods

*   **File Content Verification:** Use `diff` or manual inspection to compare generated/modified KB and MB files against expected states.
*   **Log Analysis:** Check operational logs (`phil-memory-bank-test/mode-specific/`) for correct logging format, expected actions, and error reporting.
*   **Report Validation:** Verify the content and accuracy of reports generated by `MetaReflector` and `VerificationAgent`.
*   **Schema Validation:** Run schema validator against generated/modified KB entries.

## 6. Test Execution & Reporting

*   Tests will be executed manually or via automation scripts (as developed).
*   Results (pass/fail, logs, generated files) will be documented for each scenario.
*   Defects will be tracked and prioritized for resolution.