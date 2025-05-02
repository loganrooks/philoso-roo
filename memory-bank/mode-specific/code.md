# Code Mode Specific Memory
<!-- Entries below should be added reverse chronologically (newest first) -->

### [2025-05-01 16:33:16] .roomodes Configuration File
- **Purpose**: Defines the available RooCode modes and their corresponding rule file paths for the Hegel Philosophy Suite.
- **Files**: `.roo/.roomodes`
- **Status**: Implemented
- **Dependencies**: Relies on the existence of the `.clinerules` files specified within it.
- **API Surface**: N/A (Configuration file)
- **Tests**: N/A (Configuration file)

## Intervention Log
<!-- Append intervention details using the format below -->

## Components Implemented
### [2025-05-01 21:10:59] `philosophy-draft-generator` Mode Rules (V1.1 Update)
- **Purpose**: Defines the `philosophy-draft-generator` mode, responsible for generating philosophical prose based on outlines and V12 evidence packages, using citation placeholders. Updated to explicitly handle V12 evidence structure.
- **Files**: `.roo/rules-philosophy-draft-generator/philosophy-draft-generator.clinerules`
- **Status**: Implemented (Updated to V1.1)
- **Dependencies**: Relies on `philosophy-essay-prep` (for input), `philosophy-evidence-manager` (indirectly via V12 evidence package), `philosophy-orchestrator` (for task delegation/signaling), and the RooCode mode execution framework.
- **API Surface**: N/A (Configuration file)
- **Tests**: N/A (Configuration file)
### [2025-05-01 20:09:58] `.roo/.roomodes` Configuration File (Philosophy Suite)
- **Purpose**: Defines the 12 custom philosophy modes for the Hegel Philosophy Suite, mapping slugs to `.clinerules` paths. Created as per Phase 3, Step 1 of `philosophy_mode_improvement_plan_v2.md`.
- **Files**: `.roo/.roomodes`
- **Status**: Implemented (Corrected format after intervention [See Feedback: 2025-05-01 20:09:01])
- **Dependencies**: Relies on the existence of the `.clinerules` files specified within it.
- **API Surface**: N/A (Configuration file)
- **Tests**: N/A (Configuration file)
### [2025-05-01 19:58:13] `philosophy-draft-generator` Mode Rules
- **Purpose**: Defines the `philosophy-draft-generator` mode, responsible for generating philosophical prose based on outlines and evidence, using citation placeholders.
- **Files**: `.roo/rules-philosophy-draft-generator/philosophy-draft-generator.clinerules`
- **Status**: Implemented
- **Dependencies**: Relies on `philosophy-essay-prep` (for input), `philosophy-evidence-manager` (indirectly via evidence package), `philosophy-orchestrator` (for task delegation/signaling), and the RooCode mode execution framework.
- **API Surface**: N/A (Configuration file)
- **Tests**: N/A (Configuration file)
### [2025-05-01 19:50:11] `philosophy-text-processor` Mode Rules
- **Purpose**: Defines the `philosophy-text-processor` mode, its identity, and the trigger (`process_source_material`) which executes the `scripts/process_source_text.py` script via `execute_command`.
- **Files**: `.roo/rules-philosophy-text-processor/philosophy-text-processor.clinerules`
- **Status**: Implemented
- **Dependencies**: Relies on `scripts/process_source_text.py` and the RooCode mode execution framework.
- **API Surface**: N/A (Configuration file)
- **Tests**: N/A (Configuration file)
### [2025-05-01 19:45:52] Text Processing Script (`process_source_text.py`)
- **Purpose**: Parses Markdown, splits by headers, chunks text by token limit, extracts citations, generates index files. Core logic for `philosophy-text-processor` mode.
- **Files**: `scripts/process_source_text.py`, `scripts/requirements.txt`, `scripts/README.md`
- **Status**: Implemented
- **Dependencies**: Python 3, `markdown-it-py`, `tiktoken`, `mdit_plain` (external); Relies on source files in `source_materials/raw/` or specified input path.
- **API Surface**: Command-line interface defined in `parse_arguments()`.
- **Tests**: None implemented yet.
<!-- Track components implemented and their status -->
<!-- Newest entries go above this line -->

## Technical Debt
<!-- Track identified technical debt items -->

## Dependencies
<!-- Track key external dependencies -->
### [2025-05-01 19:45:52] Python Dependencies for Text Processing
- **Purpose**: Required libraries for Markdown parsing, token counting, and plain text conversion in `process_source_text.py`.
- **Scope**: `scripts/process_source_text.py`
- **Dependencies**:
    - `markdown-it-py`: Robust Markdown parsing. Chosen for its extensibility and adherence to CommonMark spec.
    - `tiktoken`: Accurate token counting using OpenAI's tokenizers. Essential for managing chunk sizes for LLM context windows.
    - `mdit_plain`: Plugin for `markdown-it-py` to easily extract plain text, useful for summaries or simpler processing.
- **Alternatives Considered**: Standard `re` for splitting (less robust for complex Markdown), basic `split()` for token counting (inaccurate).
- **Decision Rationale**: Selected libraries provide reliable and standard methods for handling Markdown and tokenization, crucial for consistent processing.