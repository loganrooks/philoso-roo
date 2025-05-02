# Philosophy Mode `.clinerules` Revision Plan V1

**Date:** 2025-05-01
**Version:** 1.0
**Author:** Architect Mode

## 1. Introduction

This document outlines the plan for revising the `.clinerules` files for the Hegel Philosophy RooCode Suite modes, as defined in `architecture_v11.md`. This revision is designated as Corrective Step 2, following the user feedback logged in `memory-bank/feedback/sparc-feedback.md` [2025-05-01 16:57:41].

The primary goals are to:
1.  Establish a **consistent structure** across all philosophy mode `.clinerules`.
2.  Ensure the rules are specifically tailored for **rigorous philosophical work**, moving away from generic templates.
3.  Integrate the capabilities of the **`philosophy-orchestrator`** mode, particularly leveraging `new_task` for sub-task delegation.

**Note on Mode Count:** The initial task request mentioned 10 philosophy modes. However, `architecture_v11.md` (Sections 2.1, 2.2, 2.3, and the example in Section 6) explicitly defines and lists 12 modes. This plan covers all 12 modes identified in the architecture document to ensure comprehensive revision.

## 2. Scope

This revision plan applies to the `.clinerules` files for the following 12 modes:

1.  `philosophy-orchestrator`
2.  `philosophy-text-processing`
3.  `philosophy-pre-lecture`
4.  `philosophy-class-analysis`
5.  `philosophy-secondary-lit`
6.  `philosophy-dialectical-analysis`
7.  `philosophy-questioning`
8.  `philosophy-essay-prep`
9.  `philosophy-evidence-manager`
10. `philosophy-draft-generator`
11. `philosophy-citation-manager`
12. `philosophy-verification-agent`

## 3. Core Objectives & Implementation Strategy

This revision will address the key feedback points as follows:

### 3.1. Consistent Structure

*   **Problem:** Existing rules lack a uniform high-level format (Feedback Point 3).
*   **Solution:** Define and implement a standard template for all philosophy `.clinerules` files.
*   **Proposed Template Sections:**
    *   `mode:` (Slug)
    *   `identity:` (Name, Description - tailored to philosophical role)
    *   `core_principles:` (Philosophical rigor, evidence saturation, determinacy, etc., relevant to the mode)
    *   `primary_responsibilities:` (Detailed description based on `architecture_v11.md`)
    *   `workflow_triggers:` (Conditions under which the mode activates or is called by the orchestrator)
    *   `input_expectations:` (Expected format/content of inputs, e.g., specific KB queries, handoff packages)
    *   `output_specifications:` (Expected format/content of outputs, e.g., structured analysis, draft sections, verification reports)
    *   `orchestrator_integration:` (How the mode interacts with `philosophy-orchestrator`, including specific `new_task` delegations it might request or respond to)
    *   `knowledge_base_interaction:` (How the mode interacts with `philosophy-evidence-manager` to read/write to the KB)
    *   `philosophical_methods:` (Specific prompts, techniques, or checks to ensure philosophical rigor, e.g., argument mapping, concept clarification prompts, bias checks)
    *   `error_handling:` (Mode-specific error conditions and recovery steps, emphasizing philosophical integrity)
    *   `memory_bank_updates:` (Mode-specific triggers and content for MB updates, following standard format)
    *   `custom_instructions:` (Placeholder for future specific instructions)

### 3.2. Philosophical Focus

*   **Problem:** Existing rules are too generic, based on coding templates, and lack specificity for philosophical tasks (Feedback Point 4).
*   **Solution:** Tailor the content of each `.clinerules` file, particularly the `identity`, `core_principles`, `primary_responsibilities`, and `philosophical_methods` sections, to reflect the unique demands of philosophical research and analysis.
*   **Implementation Details:**
    *   **Identity/Description:** Emphasize the philosophical function (e.g., "Analyzes dialectical structures", "Verifies claims against source evidence").
    *   **Core Principles:** Explicitly state principles like "Evidence Saturation", "Conceptual Determinacy", "Argumentative Coherence".
    *   **Responsibilities:** Align strictly with `architecture_v11.md`.
    *   **Philosophical Methods:** This is crucial. Define specific instructions, prompts, or heuristics relevant to the mode's task. Examples:
        *   `philosophy-dialectical-analysis`: Prompts for identifying thesis, antithesis, synthesis; checks for consistency in negation.
        *   `philosophy-pre-lecture`: Instructions to focus on identifying implicit assumptions, defining key terms *before* seeing lecture context.
        *   `philosophy-verification-agent`: Rules for comparing claims against source text nuances, checking logical fallacies within the draft.
        *   `philosophy-draft-generator`: Instructions to maintain a consistent philosophical voice, structure arguments logically, use transition phrases appropriate for philosophical discourse.
    *   **Avoid Generic Rules:** Remove or adapt rules clearly derived from coding contexts (e.g., generic linting rules, code formatting preferences).

### 3.3. Orchestrator Integration

*   **Problem:** Existing rules do not leverage the capabilities of the `philosophy-orchestrator`, particularly `new_task` delegation (Feedback Point 5).
*   **Solution:** Explicitly define how each mode interacts with the orchestrator within its `.clinerules`.
*   **Implementation Details:**
    *   **`orchestrator_integration` Section:** Detail the specific tasks the mode expects to receive from the orchestrator and the tasks it might delegate *back* to the orchestrator (using `new_task`) for other modes to handle.
    *   **Example (`philosophy-essay-prep`):**
        *   Receives: `write_essay` task from Orchestrator.
        *   Delegates via `new_task` to Orchestrator:
            *   `gather_evidence` (Target: `philosophy-evidence-manager`) with specific query parameters.
            *   `generate_draft_section` (Target: `philosophy-draft-generator`) with outline section and evidence package.
            *   `format_citations` (Target: `philosophy-citation-manager`) with draft path.
            *   `verify_draft` (Target: `philosophy-verification-agent`) with draft path and evidence context.
    *   **Input/Output Specs:** Define clear data formats for handoffs managed by the orchestrator.
    *   **Workflow Awareness:** Rules should reflect the mode's place within the larger workflows defined in `architecture_v11.md` (e.g., `analyze_material_cycle`, `write_essay_cycle`).

## 4. Revision Process

1.  **Draft Standard Template:** Create a detailed `.clinerules` template incorporating all sections defined in 3.1.
2.  **Apply Template:** Create new draft `.clinerules` files for all 12 modes using the standard template.
3.  **Tailor Content (Iterative):** For each mode, populate the template sections based on `architecture_v11.md` and the principles outlined in 3.2 and 3.3. This requires careful consideration of each mode's specific philosophical function and interactions.
4.  **Internal Review:** Review the drafted rules for consistency, philosophical rigor, clarity, and correct integration logic.
5.  **User Review:** Present the revised `.clinerules` files (or a representative sample) to the user for feedback.
6.  **Finalization:** Incorporate user feedback and finalize the `.clinerules` files in their respective `.roo/rules-[mode-slug]/` directories.

## 5. Next Steps

1.  **Delegate Template Creation:** Assign the task of creating the detailed `.clinerules` template (as a Markdown file or draft `.clinerules` file) potentially to `spec-pseudocode` or `architect` mode.
2.  **Delegate Rule Revision:** Once the template is approved, delegate the task of applying the template and tailoring content for each of the 12 modes. This could be done sequentially or in parallel, likely assigned to `architect` or `spec-pseudocode` mode, potentially involving `code` mode for final file writing.