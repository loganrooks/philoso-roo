# Specification: `.clinerules` Modifications for Source Material Architecture V1

**Date:** 2025-05-06
**Author:** Architect Mode
**Version:** 1.0
**Target Documents:**
*   V1 Source Material Architecture Proposal: [`docs/proposals/source_material_architecture_v1.md`](docs/proposals/source_material_architecture_v1.md:1)
*   V1 Source Material Navigation Guidelines: [`docs/standards/source_material_navigation_guidelines_v1.md`](docs/standards/source_material_navigation_guidelines_v1.md:1)

## 1. Introduction

This document outlines the required modifications to relevant philosophy mode `.clinerules` files to align them with the new V1 architecture for the `source_materials/processed/` directory and its associated navigation guidelines. These changes will ensure modes can correctly locate, interpret, and utilize processed source materials.

## 2. General Changes Applicable to Multiple Modes

Many modes that read from `source_materials/processed/` will need similar updates to their `kb_interaction_protocols` and `mode_specific_workflows`. These generally involve:

*   **Adopting Staged Access:**
    1.  Query `source_materials/processed/master_index.json` for initial discovery and filtering based on task context (course, author, topic, tags).
    2.  From `master_index.json` results, retrieve the `path_to_index` for specific materials.
    3.  Read the material-specific `[ID]/index.md` (e.g., `source_materials/processed/courses/PHL316/readings/hegel_phen_intro_processed/index.md`) to get detailed metadata, chunk lists, and summaries.
    4.  Read specific `chunks/chunk_XXX.md` files as needed.
*   **Course-Specific Navigation:** For course-focused tasks, modes may start by reading the relevant `source_materials/processed/courses/[COURSE_CODE]/index.md`.
*   **Utilizing `dynamic_roles`:** Modes that assign or interpret primary/secondary source status must be updated to read the `dynamic_roles` array. Modes that determine new roles must *propose* these updates to the `philosophy-orchestrator`, which is responsible for writing to the `dynamic_roles` array in `master_index.json` and individual material `index.md` files, associating roles with specific `context_id`s (e.g., `inquiry_id`, `essay_id`).
*   **Updating Path References:** All hardcoded or inferred paths to older `processed_texts` or `indices` structures within `philosophy-knowledge-base/` (if any were used for source material access) must be updated to point to the new `source_materials/processed/` structure.

## 3. Mode-Specific `.clinerules` Modifications

The following sections detail required changes for each identified `.clinerules` file.

### 3.1. `philosophy-citation-manager.clinerules`

*   **File:** [`rules-philosophy-citation-manager/philosophy-citation-manager.clinerules`](.roo/rules-philosophy-citation-manager/philosophy-citation-manager.clinerules:1)
*   **Reason for Change:** Currently references `source_materials/processed/` for contextual verification of citations (e.g., checking extraction markers).
*   **Modifications:**
    *   **`kb_interaction_protocols.read_access`:**
        *   Update path patterns for `source_materials/processed/` to reflect the new V1 structure (e.g., `source_materials/processed/courses/[COURSE_CODE]/[TYPE]/[MATERIAL_ID]/chunks/*.md`, `source_materials/processed/library/[MATERIAL_ID]/chunks/*.md`).
        *   Add read access for `source_materials/processed/master_index.json` and `source_materials/processed/**/index.md`.
    *   **`kb_interaction_protocols.querying` (and corresponding workflow steps):**
        *   Modify step 7 (lines 197-201) and the `mode_specific_workflows.citation_formatting_and_bibliography_generation` (steps 9a-9e, lines 247-267) to reflect the V1 navigation pattern:
            *   If needing to verify an `extraction_marker` from a KB Reference:
                1.  Use `source_ref_keys` from the Reference to find the `material_id` (this might involve looking up the Reference entry itself if it contains the `material_id` (as field `id`), or the `material_id` might be part of the `source_ref_key` format).
                2.  Consult `source_materials/processed/master_index.json` to get the `path_to_index` for the `material_id` (querying by the `id` field).
                3.  Read the material-specific `[material_id]/index.md` to understand its chunk structure.
                4.  Use `extraction_markers` to locate and read the specific chunk file within `source_materials/processed/[path_from_master_index_to_material_dir]/chunks/`.
*   **Considerations:** Ensure the mode can correctly parse `extraction_markers` that now point into the new V1 structure.

### 3.2. `philosophy-class-analysis.clinerules`

*   **File:** [`rules-philosophy-class-analysis/philosophy-class-analysis.clinerules`](.roo/rules-philosophy-class-analysis/philosophy-class-analysis.clinerules:1)
*   **Reason for Change:** Analyzes lecture transcripts/notes which will be stored in `source_materials/processed/`.
*   **Modifications:**
    *   **`input_schema.properties.lecture_material_kb_ids`:** Clarify that these IDs now refer to `material_id`s (which correspond to the `id` field in `master_index.json`) in `source_materials/processed/`. The description should guide the Orchestrator to provide these.
    *   **`kb_interaction_protocols.read_access`:**
        *   Update path patterns for `source_materials/processed/` to V1 structure.
        *   Add read access for `source_materials/processed/master_index.json` and relevant `index.md` files (course-specific and material-specific).
    *   **`mode_specific_workflows.lecture_analysis_and_integration`:**
        *   Update Step 2 (line 315): "Retrieve and Read Lecture Materials":
            *   For each `material_id` (which corresponds to the `id` field in `master_index.json` from the V1 architecture):
                1.  Consult `master_index.json` (querying by `id`) to get the `path_to_index`.
                2.  Read the material-specific `[material_id]/index.md` (e.g., `source_materials/processed/courses/[COURSE_CODE]/lectures/[LECTURE_ID]/index.md`).
                3.  Use the chunk list in this `index.md` to read relevant lecture chunks.
        *   Ensure rigor field population (`source_ref_keys`, `extraction_markers`) in new KB entries correctly points to the V1 chunk paths.

### 3.3. `philosophy-dialectical-analysis.clinerules`

*   **File:** [`rules-philosophy-dialectical-analysis/philosophy-dialectical-analysis.clinerules`](.roo/rules-philosophy-dialectical-analysis/philosophy-dialectical-analysis.clinerules:1)
*   **Reason for Change:** May need to trace evidence in KB entries back to `source_materials/processed/`.
*   **Modifications:**
    *   **`kb_interaction_protocols.read_access`:**
        *   Update path patterns for `source_materials/processed/` to V1 structure.
        *   Add read access for `source_materials/processed/master_index.json` and relevant `index.md` files.
    *   **`mode_specific_workflows.source_evidence_traceability_workflow` (lines 328-352):**
        *   Update steps to align with V1 navigation:
            1.  (Step 2) Read KB Reference entry to get `material_id` (likely stored as field `id`).
            2.  (New Step) Consult `master_index.json` using `material_id` (querying by `id` field) to get `path_to_index`.
            3.  (Step 3) Navigate `source_materials/processed/[path_to_material_dir]/` using its `index.md` files to locate the chunk indicated by `extraction_markers`.
            4.  (Step 4) Read the target chunk.
*   **Considerations:** Ensure `extraction_markers` used by this mode are compatible with the V1 chunk paths.

### 3.4. `philosophy-draft-generator.clinerules`

*   **File:** [`rules-philosophy-draft-generator/philosophy-draft-generator.clinerules`](.roo/rules-philosophy-draft-generator/philosophy-draft-generator.clinerules:1)
*   **Reason for Change:** Accesses processed source materials for evidence context.
*   **Modifications:**
    *   **`kb_interaction_protocols.read_access`:**
        *   Update path patterns for `source_materials/processed/` to V1 structure.
        *   Add read access for `source_materials/processed/master_index.json` and relevant `index.md` files.
    *   **`kb_interaction_protocols.querying_and_navigation` (lines 301-306):**
        *   Update logic for consulting `source_materials/processed/`:
            1.  Use `source_ref_keys` from KB entries to identify the `material_id` (which will be the value of the `id` field in the index).
            2.  Consult `master_index.json` (querying by `id`) to get `path_to_index` for the `material_id`.
            3.  Read the material-specific `[material_id]/index.md`.
            4.  Navigate hierarchical `index.md` files within `source_materials/processed/[path_to_material_dir]/` to locate specific chunks via `extraction_markers`.
    *   **`mode_specific_workflows.draft_generation_workflow` (Step 4, lines 176-186):**
        *   Update sub-steps 1-3 to reflect the V1 navigation pattern described above for `kb_interaction_protocols.querying_and_navigation`.

### 3.5. `philosophy-essay-prep.clinerules`

*   **File:** [`rules-philosophy-essay-prep/philosophy-essay-prep.clinerules`](.roo/rules-philosophy-essay-prep/philosophy-essay-prep.clinerules:1)
*   **Reason for Change:** Explores `source_materials/processed/` for relevant source chunks.
*   **Modifications:**
    *   **`kb_interaction_protocols.read_access`:**
        *   Update path patterns for `source_materials/processed/` to V1 structure.
        *   Add read access for `source_materials/processed/master_index.json` and relevant `index.md` files.
    *   **`mode_specific_workflows.thesis_and_outline_generation` (Step 4, lines 338-348):**
        *   Update sub-steps to reflect V1 navigation:
            1.  (Sub-step 1) Identify relevant `material_id`(s) (e.g., from `kb_context.source_ref_keys` which link to Reference entries containing `material_id`s (as field `id`), or by searching `master_index.json` with keywords, querying the `id` field or other metadata).
            2.  (Sub-step 2) For each `material_id`, read its main `index.md` (e.g., `source_materials/processed/courses/[COURSE_CODE]/readings/[READING_ID]/index.md` or `source_materials/processed/library/[MATERIAL_ID]/index.md`) via `path_to_index` from `master_index.json` (obtained by querying the `id` field).
            3.  (Sub-step 3) Navigate hierarchical `index.md` files within the material's directory to locate relevant sections/chunks.
            4.  (Sub-step 4) Read content of identified chunks.
*   **Considerations:** Ensure `evidence_standards.linking_mechanism` (lines 307-312) correctly reflects how `extraction_markers` will point into the V1 structure.

### 3.6. `philosophy-evidence-manager.clinerules`

*   **File:** [`rules-philosophy-evidence-manager/philosophy-evidence-manager.clinerules`](.roo/rules-philosophy-evidence-manager/philosophy-evidence-manager.clinerules:1)
*   **Reason for Change:** Retrieves evidence using `extraction_markers` which point to `source_materials/processed/`.
*   **Modifications:**
    *   **`kb_interaction_protocols.read_access`:**
        *   Update path patterns for `source_materials/processed/` (if any are implicitly covered by `philosophy-knowledge-base/processed_texts/` which should be changed). Add explicit V1 paths.
        *   Add read access for `source_materials/processed/master_index.json` and relevant `index.md` files.
    *   **`mode_specific_workflows.evidence_retrieval` (and its sub-workflows like `source_navigation_procedure` if this mode were to have one, or if its logic for resolving markers implies navigation):**
        *   If this mode resolves `extraction_markers` to file paths, its logic must be updated to:
            1.  Parse `material_id` (conceptual) from the marker or associated `source_ref_key`.
            2.  Use `master_index.json` (querying the `id` field with the conceptual `material_id`) to find the base path for that `material_id`.
            3.  Navigate the material-specific `index.md` files and chunk structure within `source_materials/processed/[path_to_material_dir]/` to locate the precise chunk.
        *   The existing `source_navigation_procedure` (lines 322-357 in `philosophy-verification-agent.clinerules`, which seems to be a more detailed example than what's in `philosophy-evidence-manager.clinerules` itself) provides a good basis but needs adaptation to V1 (e.g., starting with `master_index.json` if only a `material_id` is known, then using the material's `index.md`).

### 3.7. `philosophy-meta-reflector.clinerules`

*   **File:** [`rules-philosophy-meta-reflector/philosophy-meta-reflector.clinerules`](.roo/rules-philosophy-meta-reflector/philosophy-meta-reflector.clinerules:1)
*   **Reason for Change:** May access `source_materials/processed/` to verify evidence linking or analyze text processing outputs.
*   **Modifications:**
    *   **`kb_interaction_protocols.read_access.patterns` (line 330-332):**
        *   Ensure the path `source_materials/processed/` correctly allows access to the new V1 structure including `master_index.json` and all `index.md` files.
    *   **`meta_reflection_protocols.evaluation_frameworks` (relevant sub-sections):**
        *   If any analysis involves checking how `source_materials/processed/` is used or linked from the KB, update procedures to reflect V1 navigation (query `master_index.json`, then material `index.md`, then chunks). For example, when checking `link_integrity` (line 397).

### 3.8. `philosophy-orchestrator.clinerules`

*   **File:** [`rules-philosophy-orchestrator/philosophy-orchestrator.clinerules`](.roo/rules-philosophy-orchestrator/philosophy-orchestrator.clinerules:1)
*   **Reason for Change:** Needs to correctly delegate tasks involving `source_materials/processed/`.
*   **Modifications:**
    *   **`input_schema.context.properties.source_material_paths` (lines 206-209):** Clarify that these paths should now refer to `material_id`s (which are values for the `id` field in `master_index.json`) or paths that align with the V1 architecture (e.g., paths to specific `index.md` files or `master_index.json` if a broad search is implied).
    *   **`mode_specific_workflows`:**
        *   **`process_source_text` (lines 376-390):**
            *   Ensure the delegation message to `philosophy-text-processor` (Step 2, line 382) correctly instructs it to use the V1 architecture for output, including generating `master_index.json`, course `index.md` files, and material-specific `index.md` files. The script itself is now responsible for this, but the orchestrator's understanding of the output paths and index files needs to align.
        *   **`analyze_material_cycle` (lines 391-413):**
            *   When delegating to analysis modes (e.g., `philosophy-pre-lecture`, Step 2, line 396), ensure `source_material_paths` or `knowledge_base_references` passed in the context correctly refer to V1 `material_id`s (i.e., values for the `id` field) or paths to V1 `index.md` files.
            *   Instruct analysis modes to use V1 navigation patterns.
        *   **`write_essay_cycle` (lines 415-454):**
            *   Similar to `analyze_material_cycle`, ensure context passed to modes like `philosophy-essay-prep` (Step 2, line 421) and `philosophy-draft-generator` (Step 4, line 428) correctly references V1 source materials.
    *   **General Delegation:** For any task involving access to processed source materials, the orchestrator must ensure the delegated mode is aware of and uses the V1 navigation guidelines (master index, then material index, then chunks).
    *   **New Workflow for `dynamic_roles` Updates:** Add a new workflow or enhance an existing one (e.g., within `analyze_material_cycle` or as a standalone utility workflow) to detail its responsibility for:
        *   Receiving `dynamic_roles` update proposals from other modes (specifying the target `material_id` and the role object: `{'context_id': '...', 'role': '...'}`).
        *   Validating these proposals (optional, based on future requirements).
        *   Performing the synchronized, atomic (or near-atomic) updates to both `master_index.json` (locating the entry by its `id` field) and the relevant individual `[material_id]/index.md` file.
        *   Handling potential errors during the update process (e.g., file not found, write errors).
        *   Logging the successful or failed update.

### 3.9. `philosophy-pre-lecture.clinerules`

*   **File:** [`rules-philosophy-pre-lecture/philosophy-pre-lecture.clinerules`](.roo/rules-philosophy-pre-lecture/philosophy-pre-lecture.clinerules:1)
*   **Reason for Change:** Analyzes readings from `source_materials/processed/`.
*   **Modifications:**
    *   **`input_schema.properties.source_material_ids` (lines 153-157):** Confirm these are `material_id`s (values for the `id` field in `master_index.json`) from the V1 architecture.
    *   **`kb_interaction_protocols.read_access` (line 229):**
        *   Update path patterns for `source_materials/processed/` to V1 structure.
        *   Add read access for `source_materials/processed/master_index.json`.
    *   **`mode_specific_workflows.pre_lecture_analysis_workflow` (Step 2, lines 281-284):**
        *   For each `material_id` (which is a value for the `id` field):
            1.  Consult `master_index.json` (querying by `id`) to get `path_to_index`.
            2.  Read the material-specific `[material_id]/index.md`.
            3.  Use its chunk list/summaries to read relevant chunks.
    *   **`evidence_standards.linking_mechanism` (lines 261-264):** Ensure `extraction_markers` correctly reference paths within the V1 `source_materials/processed/[material_id]/...` structure.

### 3.10. `philosophy-questioning.clinerules`

*   **File:** [`rules-philosophy-questioning/philosophy-questioning.clinerules`](.roo/rules-philosophy-questioning/philosophy-questioning.clinerules:1)
*   **Reason for Change:** May consult `source_materials/processed/` for deeper context.
*   **Modifications:**
    *   **`input_schema.properties.source_material_paths` (lines 184-188):** Clarify these paths should align with V1 (e.g., paths to `index.md` files or specific chunks if already known).
    *   **`kb_interaction_protocols.read_access` (line 245):**
        *   Update path patterns for `source_materials/processed/` to V1 structure.
        *   Add read access for `source_materials/processed/master_index.json`.
    *   **`mode_specific_workflows.question_refinement_workflow` (Step 4, lines 301-304):**
        *   Update to use V1 navigation: If `source_material_paths` are provided or if deeper context is needed:
            1.  Identify relevant `material_id`(s) (from input or by searching `master_index.json`, querying the `id` field or other metadata).
            2.  For each `material_id`, consult `master_index.json` (querying by `id`) for `path_to_index`.
            3.  Read the material-specific `[material_id]/index.md`.
            4.  Navigate its structure (sub-indices, chunk list) to find relevant textual context.
    *   **`evidence_standards.linking_mechanism` (lines 275-279):** Ensure any implicit reliance on `extraction_markers` (if questions are linked to concepts/arguments that have them) correctly understands the V1 path structure.

### 3.11. `philosophy-secondary-lit.clinerules`

*   **File:** [`rules-philosophy-secondary-lit/philosophy-secondary-lit.clinerules`](.roo/rules-philosophy-secondary-lit/philosophy-secondary-lit.clinerules:1)
*   **Reason for Change:** Analyzes secondary literature which may be stored in `source_materials/processed/`.
*   **Modifications:**
    *   **`kb_interaction_protocols.read_access` (lines 250-257, 281):**
        *   Update path patterns for `source_materials/processed/` to V1 structure.
        *   Add read access for `source_materials/processed/master_index.json`.
    *   **`kb_interaction_protocols.querying.strategy` (lines 277-281):**
        *   Update to reflect V1 navigation when consulting `source_materials/processed/master_index.json` and material-specific `index.md` files.
    *   **`mode_specific_workflows.secondary_literature_analysis_workflow`:**
        *   Update Step 2 (lines 335-338): If retrieving from KB, use V1 navigation (query `master_index.json` for `material_id`s (i.e. `id` field values) matching `secondary_lit_context`, then read material-specific `index.md` and chunks).
        *   Update Step 3 (lines 340-343): If new external content is processed by `philosophy-text-processor`, ensure this mode understands that the output will be in V1 format.
    *   **`evidence_standards.linking_mechanism` (lines 300-307):** Ensure `extraction_markers` for secondary literature correctly point into the V1 structure if the secondary lit itself is processed and chunked into `source_materials/processed/`.

### 3.12. `philosophy-text-processor.clinerules`

*   **File:** [`rules-philosophy-text-processor/philosophy-text-processor.clinerules`](.roo/rules-philosophy-text-processor/philosophy-text-processor.clinerules:1)
*   **Reason for Change:** This mode is responsible for creating the V1 structure in `source_materials/processed/`.
*   **Modifications (Significant):**
    *   **`identity.description` and `identity.details` (lines 7-17):** Update to accurately reflect V1 architecture:
        *   Script creates hierarchical `index.md` files *within each processed source's directory* (e.g., `source_materials/processed/[material_id]/index.md`, `source_materials/processed/[material_id]/level_0/index.md`).
        *   Script generates/updates `source_materials/processed/master_index.json`.
        *   Script generates/updates course-specific `source_materials/processed/courses/[COURSE_CODE]/index.md`.
        *   Mode parses script output and writes to KB.
        *   Mode *does not* update the root `source_materials/processed/index.md` (this is now `master_index.json`, handled by the script).
    *   **`script_execution.script_responsibilities` (lines 200-207):**
        *   Update to match V1 architecture proposal:
            *   Script creates `courses/[COURSE_CODE]/[TYPE]/[MATERIAL_ID]/` or `library/[MATERIAL_ID]/` structure.
            *   Script generates `master_index.json` entries.
            *   Script generates material-specific `[ID]/index.md` (YAML frontmatter + chunk list).
            *   Script generates course-specific `courses/[COURSE_CODE]/index.md`.
            *   Script outputs structured JSON with paths relative to the new structure.
    *   **`script_execution.mode_responsibilities` (lines 208-216):**
        *   Remove responsibility for updating `source_materials/processed/index.md` (line 214). The script now handles `master_index.json` and course `index.md` files. The mode's role is to orchestrate the script and ingest its structured output into the KB.
    *   **`mode_specific_workflows.text_processing_and_kb_ingestion` (lines 225-270):**
        *   Update Step 4 (lines 243-246): Script generates `master_index.json`, course `index.md`, and material `index.md` files.
        *   Update Step 7 (lines 257-261): Remove this step. The script handles creation/update of `master_index.json` and course `index.md`.
    *   **`mode_specific_workflows.processed_source_navigation_guidance` (lines 271-298):**
        *   **CRITICAL:** This entire section needs to be rewritten to align with [`docs/standards/source_material_navigation_guidelines_v1.md`](docs/standards/source_material_navigation_guidelines_v1.md:1).
        *   Emphasize starting with `master_index.json`.
        *   Describe the role and content of course-specific `index.md` files.
        *   Describe the role and content of material-specific `[ID]/index.md` files (YAML frontmatter, chunk list).
        *   Explain how `extraction_markers` in KB entries link to specific chunks within the V1 structure.
        *   Explain how to use `dynamic_roles`.

### 3.13. `philosophy-verification-agent.clinerules`

*   **File:** [`rules-philosophy-verification-agent/philosophy-verification-agent.clinerules`](.roo/rules-philosophy-verification-agent/philosophy-verification-agent.clinerules:1)
*   **Reason for Change:** Verifies content against processed source materials.
*   **Modifications:**
    *   **`input_schema.properties.source_extraction_markers` (lines 154-158):** Ensure description clarifies these markers point into the V1 `source_materials/processed/` structure.
    *   **`kb_interaction_protocols.read_access` (line 228):**
        *   Update path patterns for `source_materials/processed/` to V1 structure.
        *   Add read access for `source_materials/processed/master_index.json`.
    *   **`evidence_standards.linking_mechanism` (lines 248-250):**
        *   Update example of `extraction_markers` to reflect V1 paths (e.g., `[material_id_value]/courses/[COURSE_CODE]/[TYPE]/[MATERIAL_ID_value]/chunks/chunk_XXX.md#para_Y`, where `material_id_value` is the actual ID string).
    *   **`mode_specific_workflows.verification_procedures`:**
        *   Update Step 4 (lines 274-277): "Consistency Check against Processed Source":
            *   For each marker, use V1 navigation (parse conceptual `material_id`, consult `master_index.json` querying by `id` field, then material `index.md`, then chunks) to locate and read the source chunk.
        *   Update Step 6 (lines 285-288): "Evidence Link Check for Processed Source":
            *   Verify markers point to relevant sections using V1 navigation.
    *   **`mode_specific_workflows.source_navigation_procedure` (lines 322-357):**
        *   This procedure needs to be updated to fully align with [`docs/standards/source_material_navigation_guidelines_v1.md`](docs/standards/source_material_navigation_guidelines_v1.md:1).
        *   Start with `master_index.json` if only conceptual `material_id` is known from `extraction_marker` (query by `id` field).
        *   Correctly parse `extraction_marker` to get conceptual `material_id` and relative path within that source's processed directory.
        *   Use material-specific `index.md` files for navigation within a source.

## 4. Potentially Obsolete / Needs Major Review

### 4.1. `philosophy-kb-manager.clinerules`

*   **File:** [`rules-philosophy-kb-manager/philosophy-kb-manager.clinerules`](.roo/rules-philosophy-kb-manager/philosophy-kb-manager.clinerules:1)
*   **Reason:** Based on V14 architecture where it was the sole KB interface. V18.3.6 and V1 Source Material Architecture emphasize direct KB access for most modes.
*   **Recommendation:** Review if this mode still has a valid role. If its CRUD/querying functions are now distributed, its `.clinerules` may be largely obsolete or require a complete redefinition of responsibilities (e.g., highly specialized, complex KB operations not suitable for other modes). It does not directly interact with `source_materials/processed/` in a way that needs V1 navigation updates, but its premise is outdated.

## 5. Conclusion

The changes outlined above are essential for aligning the philosophy modes with the new V1 source material architecture. Implementing these modifications will enable modes to effectively leverage the improved organization, indexing, and navigation capabilities of the processed source materials.