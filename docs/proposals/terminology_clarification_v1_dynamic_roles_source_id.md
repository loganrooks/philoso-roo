# Proposal: Terminology Clarification V1 - `dynamic_roles` & `material_id`

**Date:** 2025-05-07
**Author:** Architect Mode
**Version:** 1.0
**Status:** Proposed

## 1. Introduction

This document addresses specific findings from the V1 Source Material Architecture QA report ([`docs/testing/verification_report_source_material_v1.md`](docs/testing/verification_report_source_material_v1.md:1)) concerning the `dynamic_roles` update mechanism and the terminology used for source material identifiers (referred to variously as `source_id`, `MATERIAL_ID`, or `id`).

The objective is to provide clear, consistent definitions and usage guidelines for these terms and to propose necessary updates to existing documentation to reflect these clarifications.

## 2. Summary of QA Findings

The QA report highlighted two key areas needing attention:

1.  **`dynamic_roles` Update Mechanism:** While the architecture allows analysis modes to update `dynamic_roles`, the precise mechanism and coordination (e.g., via Orchestrator, direct writes with locking) needs to be robustly implemented and reflected in the `.clinerules` of modes that will perform these updates. (See QA Report Sections 2.3, 3)
2.  **Terminological Consistency (`source_id` vs. `MATERIAL_ID` vs. `id`):** Inconsistent terminology for the unique identifier of processed source materials was noted across different documents. (See QA Report Sections 2.3, 3)

## 3. Analysis of Current State

A review of the V1 Source Material Architecture proposal ([`docs/proposals/source_material_architecture_v1.md`](docs/proposals/source_material_architecture_v1.md:1)), Navigation Guidelines ([`docs/standards/source_material_navigation_guidelines_v1.md`](docs/standards/source_material_navigation_guidelines_v1.md:1)), and the `.clinerules` Modification Specification ([`docs/specs/clinerules_source_material_v1_updates.md`](docs/specs/clinerules_source_material_v1_updates.md:1)) confirms these points:

*   **Identifier Terminology:**
    *   The architecture proposal uses `[MATERIAL_ID]` (and variants like `[LECTURE_ID]`) as placeholders in directory structures and `id` as the actual field name in `master_index.json` and individual `index.md` YAML.
    *   The navigation guidelines also use `id` as the field name and `[MATERIAL_ID]` as a placeholder.
    *   The `.clinerules` specification consistently uses the term `source_id` in its descriptive text when referring to these unique identifiers, even though the data field is `id`.
    *   This creates potential confusion.

*   **`dynamic_roles` Update Mechanism:**
    *   The architecture proposal and navigation guidelines state that analysis modes can update `dynamic_roles`, possibly via the `philosophy-orchestrator` or direct writes if rules permit and consistency mechanisms are in place.
    *   However, none of the documents provide a detailed specification for *how* these updates should be managed to ensure data integrity, avoid conflicts, and how the `philosophy-orchestrator` would facilitate this. The `.clinerules` specification focuses on read access for navigation rather than the update protocol for `dynamic_roles`.

## 4. Proposed Definitions and Usage Guidelines

To address these findings, the following precise definitions and usage guidelines are proposed:

### 4.1. Term: `material_id`

*   **Definition:** `material_id` is the canonical **conceptual term** for the unique, human-readable identifier assigned to each processed source material within the `source_materials/processed/` V1 architecture. It serves as the primary key for a processed material.
*   **Format:** A string, typically derived from key attributes of the source (e.g., `hegel_phenomenology_spirit_introduction_processed`, `PHL316_lecture_2025-01-15_hegel_being`).
*   **Usage:**
    *   **Directory Naming:** Used as the directory name for the specific material (e.g., `source_materials/processed/library/[material_id]/`).
    *   **Field Name in Data Structures:** The actual field name representing this identifier in `master_index.json` and the YAML frontmatter of individual `[material_id]/index.md` files **SHALL BE `id`**.
    *   **Internal System Reference & Documentation:**
        *   When modes or documentation (including `.clinerules` descriptive text, comments, logs) refer to this identifier **conceptually**, the term `material_id` should be preferred for clarity and to distinguish it from other types of IDs (e.g., `inquiry_id`, `concept_id`).
        *   When referring to the **actual data field** being accessed or manipulated in `master_index.json` or `index.md` YAML, the term `id` **MUST** be used.
    *   **Example Clarification:**
        *   Correct conceptual reference: "The `philosophy-text-processor` generates a unique `material_id` for each new source."
        *   Correct data field reference: "Query `master_index.json` where the `id` field matches the target `material_id`."

### 4.2. Term: `dynamic_roles`

*   **Definition:** An array of objects associated with a `material_id` (via its `id` field in data structures). Each object defines the role of that material (e.g., "primary_source", "secondary_source", "critique") within a specific, identified context (e.g., a particular research inquiry, essay, or conceptual analysis).
*   **Structure (per object in the array):**
    *   `context_id`: (String) A unique identifier for the context to which this role applies (e.g., `inquiry:hegel_being_sol`, `essay:kant_ethics_overview`). The prefix (e.g., `inquiry:`, `essay:`, `concept:`) should indicate the type of context.
    *   `role`: (String) The role assigned to the material within that specific `context_id` (e.g., `primary_source`, `secondary_source`, `key_text`, `supporting_evidence`, `critique_of`).
*   **Location:** Present as a field named `dynamic_roles` in:
    *   Entries within `master_index.json`.
    *   The YAML frontmatter of individual `[material_id]/index.md` files.
*   **Usage Guidelines & Update Mechanism:**
    *   **Read Access:** Any mode can read the `dynamic_roles` array to understand a material's relevance in various contexts.
    *   **Write Access (Responsibility):** Analysis modes (e.g., `philosophy-pre-lecture`, `philosophy-class-analysis`, `philosophy-secondary-lit`) are primarily responsible for identifying and assigning appropriate `dynamic_roles` to materials based on their current analytical task.
    *   **Update Protocol (MANDATORY):**
        1.  **Proposal by Analysis Mode:** When an analysis mode determines a new `dynamic_role` for a material, it **MUST** formulate this as a proposed update (e.g., "Propose adding `{'context_id': 'current_inquiry_XYZ', 'role': 'primary_source'}` to `dynamic_roles` for material with `id`: `hegel_phen_intro_processed`").
        2.  **Delegation to Orchestrator:** This proposed update **MUST** be sent to the `philosophy-orchestrator` mode. Direct modification of `master_index.json` or individual `index.md` files by analysis modes for `dynamic_roles` is **PROHIBITED**.
        3.  **Orchestrator Responsibility:** The `philosophy-orchestrator` is solely responsible for managing and applying updates to the `dynamic_roles` field in both `master_index.json` and the relevant individual `[material_id]/index.md` file. This centralized management is crucial to prevent race conditions, ensure data integrity, and maintain consistency between the master index and individual indexes.
        4.  **Update Implementation by Orchestrator:** The `philosophy-orchestrator` **SHALL**:
            *   Atomically (or as near as possible) read the current `master_index.json`.
            *   Locate the entry for the target `material_id` (using its `id` field).
            *   Append the new role object to its `dynamic_roles` array. If a role for the exact same `context_id` already exists, the orchestrator should decide on an update strategy (e.g., overwrite, or require clarification – this needs further specification in the orchestrator's `.clinerules`). For now, appending distinct `context_id` entries is the primary expectation.
            *   Atomically (or as near as possible) write the updated `master_index.json` back to disk.
            *   Perform an equivalent atomic read-modify-write operation for the `dynamic_roles` array in the YAML frontmatter of the corresponding individual `[material_id]/index.md` file.
            *   Log the update action, including the requesting mode, the `material_id`, and the added/updated role.
    *   **Consistency:** The `dynamic_roles` array in `master_index.json` is the definitive source of truth. The `philosophy-orchestrator` ensures the array in the individual `[material_id]/index.md` file is kept in sync.
    *   **`.clinerules` Reflection:**
        *   Analysis modes' `.clinerules` (e.g., in `mode_specific_workflows` or `kb_interaction_protocols`) **MUST** specify their capability to *propose* `dynamic_roles` updates *to the `philosophy-orchestrator`*. They **MUST NOT** specify direct write access to these fields for `dynamic_roles`.
        *   The `philosophy-orchestrator.clinerules` **MUST** define a detailed workflow for:
            *   Receiving `dynamic_roles` update proposals from other modes.
            *   Validating these proposals (optional, based on future requirements).
            *   Performing the synchronized, atomic (or near-atomic) updates to both `master_index.json` and the relevant individual `[material_id]/index.md` file.
            *   Handling potential errors during the update process (e.g., file not found, write errors).
            *   Logging the successful or failed update.

## 5. Recommendations for Document Updates

Based on the clarifications above, the following updates are recommended:

### 5.1. [`docs/proposals/source_material_architecture_v1.md`](docs/proposals/source_material_architecture_v1.md:1)

*   **Section 3.1 Directory Structure (and throughout):**
    *   Consistently use `[material_id]` as the placeholder for unique material identifiers in directory paths (e.g., `library/[material_id]/`, `courses/[COURSE_CODE]/lectures/[material_id]/`).
*   **Section 3.2.1 `master_index.json`:**
    *   Change field description for `id` (line 102) to: `"id": "hegel_phenomenology_spirit_intro_processed", // Unique material_id matching directory name`.
    *   Update the description of `dynamic_roles` (line 139) to reference the centralized update mechanism via `philosophy-orchestrator` as defined in Section 4.2 of this proposal.
*   **Section 3.2.2 Individual Material `index.md` Files:**
    *   Change field description for `id` in YAML frontmatter (line 148) to: `id: [material_id] # Unique material_id`.
    *   Update the description of `dynamic_roles` (line 158) to note it's updated by the `philosophy-orchestrator` in sync with `master_index.json`.
*   **Section 3.4 Workflow Implications:**
    *   For "Analysis Modes" (line 211), clarify that updates to `dynamic_roles` are *proposed* to the `philosophy-orchestrator`.

### 5.2. [`docs/standards/source_material_navigation_guidelines_v1.md`](docs/standards/source_material_navigation_guidelines_v1.md:1)

*   **Section 2. Overview of the Architecture:**
    *   Change item "Unique Identifiers (IDs)" (line 17) to: "Unique Identifiers (`material_id`): Each processed item ... has a unique `material_id` used in its directory name (e.g., `hegel_phenomenology_spirit_intro_processed`). The data field for this in index files is `id`."
*   **Section 3.1. Master Index (`master_index.json`):**
    *   Change field description for `id` (line 31) to: `id`: Unique `material_id` (matches directory name).
    *   Update the description of `dynamic_roles` (line 46) and its usage in Section 5.2 (line 132) to reflect that updates are managed by the `philosophy-orchestrator`.
*   **Section 3.2. Individual Material Index (`[ID]/index.md`):**
    *   In the path example (line 54), use `[material_id]` placeholder: `source_materials/processed/[path_to_material]/[material_id]/index.md`.
    *   Clarify that the `id` field in YAML frontmatter (line 57) stores the `material_id`.

### 5.3. [`docs/specs/clinerules_source_material_v1_updates.md`](docs/specs/clinerules_source_material_v1_updates.md:1)

*   **Throughout the document:**
    *   When referring conceptually to the unique identifier of a processed source material, consistently use the term `material_id`.
    *   When specifying interactions with the actual data field in `master_index.json` or `index.md` files, ensure it refers to the field `id`.
    *   For example, change line 42 from "...find the `source_id`..." to "...find the `material_id` (which corresponds to the `id` field in the index)...".
*   **Section 2. General Changes Applicable to Multiple Modes:**
    *   Update the description of `dynamic_roles` (line 24) to state that modes *propose* updates to the `philosophy-orchestrator`, which then performs the write.
*   **Mode-Specific Sections (3.1 - 3.13):**
    *   Review all references to `source_id`, `MATERIAL_ID`, `LECTURE_ID`, etc., and update to `material_id` for conceptual references, and `id` when referring to the data field.
    *   For any mode that might logically determine or suggest a `dynamic_role`, its `.clinerules` modification should specify that it *proposes* this to the `philosophy-orchestrator` rather than writing directly. (This seems most relevant for analysis modes, but review all).
    *   Specifically for `philosophy-orchestrator.clinerules` (Section 3.8), add a new workflow or enhance an existing one to detail its responsibility for receiving `dynamic_roles` update proposals and performing the synchronized writes to `master_index.json` and the individual `[material_id]/index.md` file.

## 6. Conclusion

Implementing these clarifications will improve terminological consistency across project documentation and provide a clear, robust mechanism for managing `dynamic_roles`. This will reduce ambiguity for developers and enhance the reliability of mode interactions with the V1 Source Material Architecture.