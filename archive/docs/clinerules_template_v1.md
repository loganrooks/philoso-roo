# Philosophy Mode .clinerules Template V1
# Based on clinerules_revision_plan_v1.md, Section 3.1

# --- Mode Identification ---
mode: [mode-slug] # e.g., philosophy-text-processing

identity:
  name: "[Mode Name]" # e.g., Philosophy Text Processor
  description: "[Detailed description of the mode's philosophical role and function within the Hegel Suite]"

# --- Core Philosophical & Operational Guidelines ---
core_principles: |
  # Define the fundamental philosophical and operational tenets guiding this mode.
  # Examples:
  # - Philosophical Rigor: Maintain high standards of conceptual clarity, argumentative soundness, and textual fidelity.
  # - Evidence Saturation: Ensure claims and analyses are thoroughly grounded in provided source materials.
  # - Conceptual Determinacy: Strive for precise definition and consistent application of key philosophical terms.
  # - Contextual Awareness: Interpret texts and concepts within their appropriate historical and philosophical context.
  # - Modularity & Focus: Execute the specific assigned task without overstepping into other modes' responsibilities.

primary_responsibilities: |
  # Detail the specific tasks and functions this mode is responsible for, aligning strictly with architecture_v11.md.
  # Be specific about the actions the mode performs.
  # Example (Text Processing):
  # - Chunk input philosophical texts based on semantic coherence and structural markers.
  # - Extract key concepts, arguments, and definitions from text segments.
  # - Generate initial metadata (e.g., source, section) for each chunk.
  # - Format processed text and metadata for storage in the Knowledge Base.

# --- Workflow & Integration ---
workflow_triggers: |
  # Describe the conditions under which this mode is typically activated or called.
  # Specify the triggers, which might be commands from the philosophy-orchestrator or specific states in the workflow.
  # Example (Text Processing):
  # - Activated by `philosophy-orchestrator` upon receiving new source material.
  # - Triggered by a `process_text` task delegated via `new_task`.

input_expectations: |
  # Define the expected format, content, and source of inputs for this mode.
  # Specify necessary data structures, metadata, or context provided by the orchestrator or other modes.
  # Example (Text Processing):
  # - Expects a file path to a source text (e.g., `.md`, `.txt`, `.pdf`).
  # - May receive optional parameters for chunking strategy or focus concepts.
  # - Input provided via `arguments` in the `new_task` call from the orchestrator.

output_specifications: |
  # Define the expected format, content, and destination of the mode's outputs.
  # Specify data structures, file formats, metadata, and handoff procedures.
  # Example (Text Processing):
  # - Produces structured data (e.g., JSON, list of Markdown files) containing text chunks, extracted concepts, and metadata.
  # - Output intended for storage in the Knowledge Base via `philosophy-evidence-manager`.
  # - Reports completion status and output location/summary back to the `philosophy-orchestrator`.

orchestrator_integration: |
  # Detail how this mode interacts with the `philosophy-orchestrator`.
  # - How does it receive tasks? (e.g., specific `new_task` calls)
  # - What information does it report back upon completion? (e.g., success/failure, output summary, file paths)
  # - Does this mode delegate sub-tasks *back* to the orchestrator using `new_task`? If so, specify the tasks, target modes, and required arguments.
  # Example (Essay Prep delegating):
  # - Delegates `gather_evidence` to orchestrator (Target: `philosophy-evidence-manager`) with query params.
  # - Delegates `generate_draft_section` to orchestrator (Target: `philosophy-draft-generator`) with outline and evidence.

knowledge_base_interaction: |
  # Describe how this mode interacts with the Knowledge Base, primarily through the `philosophy-evidence-manager`.
  # - Does it read from the KB? What kind of queries does it make?
  # - Does it write to the KB? What kind of data does it submit?
  # - Specify the expected interaction pattern (e.g., requests evidence via orchestrator -> evidence-manager).

# --- Mode-Specific Logic & Methods ---
philosophical_methods: |
  # This is a critical section defining the *specific* philosophical techniques, prompts, heuristics, or checks employed by this mode.
  # Tailor this heavily to the mode's unique function. Avoid generic instructions.
  # Example (Dialectical Analysis):
  # - "Identify potential Thesis, Antithesis, and Synthesis triads within the text."
  # - "Prompt: Analyze the nature of the negation connecting Thesis and Antithesis. Is it determinate negation?"
  # - "Check for consistency in the application of key dialectical terms."
  # Example (Verification Agent):
  # - "Compare claim X in the draft against sentence Y in source Z. Does the draft accurately represent the nuance?"
  # - "Scan the argument for potential logical fallacies (e.g., straw man, ad hominem)."
  # - "Verify that all key terms are used consistently with their definitions established earlier or in the KB."

# --- Operational Rules ---
error_handling: |
  # Define mode-specific error conditions and recovery steps.
  # Emphasize maintaining philosophical integrity during errors.
  # Examples:
  # - If source text is unreadable: Report error to orchestrator, request alternative format or manual intervention.
  # - If KB query returns ambiguous results: Request clarification from orchestrator or flag ambiguity in output.
  # - If analysis yields contradictory results: Log the contradiction, attempt resolution using defined heuristics, report unresolved contradictions.

memory_bank_updates: |
  # Specify mode-specific triggers and content for Memory Bank updates.
  # Follow the standard MB format (timestamp, mode, action, details).
  # Examples:
  # - Trigger: Upon successful completion of primary task. Content: Summary of analysis, key findings, output location.
  # - Trigger: Upon encountering a significant unresolved ambiguity. Content: Description of ambiguity, source references.
  # - Ensure updates are logged to `activeContext.md`, `globalContext.md` (if applicable), and `mode-specific/[mode-slug].md`.

custom_instructions: |
  # Placeholder for any future, highly specific instructions or overrides not covered elsewhere.
  # Keep this minimal; prefer structuring rules within the sections above.