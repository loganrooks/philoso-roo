# Code Mode Specific Memory
<!-- Entries below should be added reverse chronologically (newest first) -->

### [2025-05-02 12:15:30] `philosophy-dialectical-analysis` Mode Rules (V14 Update)
- **Purpose**: Defines the `philosophy-dialectical-analysis` mode, responsible for analyzing concepts through dialectical movement, contradictions, and resolutions. Updated to V14 to use `philosophy-kb-manager` for all KB interactions and support context-aware querying.
- **Files**: `.roo/rules-philosophy-dialectical-analysis/philosophy-dialectical-analysis.clinerules`
- **Status**: Implemented (Updated to V14)
- **Dependencies**: Relies on `philosophy-orchestrator` (for task delegation), `philosophy-kb-manager` (for KB interaction), `philosophy-evidence-manager` (for SPARC context), and the RooCode mode execution framework.
- **API Surface**: N/A (Configuration file defining mode behavior).
- **Tests**: N/A (Configuration file).
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
### [2025-05-02 12:30:42] `philosophy-essay-prep` Mode Rules (V1.1 - V14 Update)
- **Purpose**: Defines the `philosophy-essay-prep` mode, responsible for managing the essay writing process according to V14 architecture. Coordinates outlining, thesis development (via KB), research integration (context-aware KB queries), drafting, citation, revision, and Git version control.
- **Files**: `.roo/rules-philosophy-essay-prep/philosophy-essay-prep.clinerules`
- **Status**: Implemented (Updated to V14)
- **Dependencies**: Relies on `philosophy-orchestrator` (for task delegation), `philosophy-kb-manager` (for KB interaction), `philosophy-draft-generator`, `philosophy-citation-manager`, `philosophy-verification-agent`, `execute_command` (for Git), and the RooCode mode execution framework.
- **API Surface**: N/A (Configuration file defining mode behavior).
- **Tests**: N/A (Configuration file).
### [2025-05-02 12:22:46] `philosophy-questioning` Mode Rules (V1.0 - V14 Spec)
- **Purpose**: Defines the `philosophy-questioning` mode, responsible for refining proto-questions from the KB using context-aware queries via `kb-manager` and storing refined questions tagged as `inquiry`.
- **Files**: `.roo/rules-philosophy-questioning/philosophy-questioning.clinerules`
- **Status**: Implemented
- **Dependencies**: Relies on `philosophy-orchestrator` (for task delegation), `philosophy-kb-manager` (for KB interaction), `philosophy-evidence-manager` (for SPARC context), and the RooCode mode execution framework.
- **API Surface**: N/A (Configuration file defining mode behavior).
- **Tests**: N/A (Configuration file).
### [2025-05-02 05:54:27] `philosophy-pre-lecture` Mode Rules (V14 Update)
- **Purpose**: Defines the `philosophy-pre-lecture` mode, responsible for analyzing readings using processed data via `kb-manager`, identifying concepts/arguments/questions, and storing findings in the KB. Updated to V14 to use `kb-manager` and support context-aware querying.
- **Files**: `.roo/rules-philosophy-pre-lecture/philosophy-pre-lecture.clinerules`
- **Status**: Implemented (Updated to V14)
- **Dependencies**: Relies on `philosophy-orchestrator` (for task delegation), `philosophy-kb-manager` (for KB interaction), and the RooCode mode execution framework.
- **API Surface**: N/A (Configuration file defining mode behavior).
- **Tests**: N/A (Configuration file).
### [2025-05-02 05:47:38] `philosophy-text-processor` Mode Rules (V1.0 - V14 Spec)
- **Purpose**: Defines the `philosophy-text-processor` mode, responsible for pre-processing source texts from `source_materials/raw/`, extracting context from paths, executing `scripts/process_source_text.py`, and handing off processed data (index, citations, context tags) to `philosophy-kb-manager`.
- **Files**: `.roo/rules-philosophy-text-processor/philosophy-text-processor.clinerules`
- **Status**: Implemented
- **Dependencies**: Relies on `philosophy-orchestrator` (for task delegation), `scripts/process_source_text.py` (for core logic), `philosophy-kb-manager` (for data storage), `execute_command` tool, and the RooCode mode execution framework. Assumes V14 source directory structure.
- **API Surface**: N/A (Configuration file defining mode behavior).
- **Tests**: N/A (Configuration file).
### [2025-05-02 05:39:26] `philosophy-kb-manager` Mode Rules (V1.0 - V14 Spec)
- **Purpose**: Defines the `philosophy-kb-manager` mode, the sole interface to the Philosophy Knowledge Base (`philosophy-knowledge-base/`). Manages CRUD, context-aware querying (V14 `context:key:value` tags), linking, integrity, and executes approved modifications.
- **Files**: `.roo/rules-philosophy-kb-manager/philosophy-kb-manager.clinerules`
- **Status**: Implemented
- **Dependencies**: Relies on `philosophy-orchestrator` (for modification approvals), `philosophy-text-processor` (for receiving context tags), all modes requiring KB access, and the RooCode mode execution framework.
- **API Surface**: N/A (Configuration file defining mode behavior and interaction methods like `create_kb_entry`, `query_kb_entries`).
- **Tests**: N/A (Configuration file).
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