# Philoso-Roo: A Hegel Philosophy RooCode Suite

## Description

Philoso-Roo is a SPARC-based (Specification, Pseudocode, Architecture, Refinement, Completion) suite of tools and modes designed to assist in the study and analysis of Hegelian philosophy. It leverages a structured Knowledge Base (KB), source material processing, and a series of specialized AI-driven modes to facilitate deep engagement with complex philosophical texts and concepts. The system aims to provide a robust framework for philosophical research, analysis, essay writing, and knowledge management.

## Key Features & System Overview

The Philoso-Roo system is built upon the RooCode framework, utilizing a collection of specialized modes to perform various tasks:

*   **Philosophy Modes:** A suite of modes tailored for philosophical work, including:
    *   [`philosophy-orchestrator`](.roomodes:272): Coordinates complex philosophical tasks.
    *   [`philosophy-text-processor`](.roomodes:280): Processes source texts using [`scripts/process_source_text.py`](scripts/process_source_text.py:1).
    *   Analysis Modes (e.g., [`philosophy-pre-lecture`](.roomodes:288), [`philosophy-class-analysis`](.roomodes:296), [`philosophy-secondary-lit`](.roomodes:304), [`philosophy-dialectical-analysis`](.roomodes:312)): Analyze texts and KB content.
    *   Inquiry & Essay Modes (e.g., [`philosophy-questioning`](.roomodes:320), [`philosophy-essay-prep`](.roomodes:328), [`philosophy-draft-generator`](.roomodes:336), [`philosophy-citation-manager`](.roomodes:344)): Support research and writing.
    *   Verification & Reflection Modes (e.g., [`philosophy-verification-agent`](.roomodes:352), [`philosophy-meta-reflector`](.roomodes:360)): Ensure rigor and system improvement.
    *   Utility Modes (e.g., [`philosophy-kb-doctor`](.roomodes:368), [`philosophy-evidence-manager`](.roomodes:376)): Maintain KB health and retrieve evidence.
*   **Knowledge Base (`philosophy-knowledge-base/`):** A structured repository for philosophical domain knowledge, including concepts, arguments, quotations, references, and their relationships. Modes interact directly with the KB using file tools.
*   **Source Material Processing (`source_materials/`, `scripts/process_source_text.py`):** Raw source materials are stored in `source_materials/raw/` and processed by [`scripts/process_source_text.py`](scripts/process_source_text.py:1) into a structured format in `source_materials/processed/`. This includes chunking texts and generating navigational indices (`master_index.json` and per-material `index.md` files).
*   **Memory Bank (`memory-bank/`, `phil-memory-bank/`):**
    *   `memory-bank/`: Contains operational context for the general SPARC system.
    *   `phil-memory-bank/`: Contains operational context specific to the Philoso-Roo system's operations, ensuring separation from the philosophical domain knowledge.

## Directory Structure Overview

*   **`.roo/`**: Contains `.clinerules` files defining the behavior and custom instructions for each mode, and the [`.roomodes`](.roomodes:1) file listing all available modes.
*   **`docs/`**: Project documentation, including:
    *   `architecture/`: System architecture documents (latest is [`architecture_v18.md`](docs/architecture/architecture_v18.md:1)).
    *   `proposals/`: Design proposals for new features or changes.
    *   `reviews/`: Review reports, like the [`holistic_review_v1.md`](docs/reviews/holistic_review_v1.md:1).
    *   `specs/`: Requirement specifications.
    *   `standards/`: Project standards, like the [`clinerules_standard_v2.md`](docs/standards/clinerules_standard_v2.md:1).
*   **`scripts/`**: Contains Python scripts used by the system, notably [`process_source_text.py`](scripts/process_source_text.py:1) for source material processing.
*   **`philosophy-knowledge-base/`**: The central repository for structured philosophical knowledge.
*   **`source_materials/`**:
    *   `raw/`: Location for original, unprocessed source texts.
    *   `processed/`: Output location for processed source texts, including chunked files and navigational indices.
*   **`memory-bank/`**: General operational context for the Philoso-Roo system.
*   **`phil-memory-bank/`**: Operational context specific to the Philoso-Roo system.
*   **`tests/`**: Contains test files, e.g., [`test_dynamic_roles_protocol.py`](tests/test_dynamic_roles_protocol.py:1).
*   **`analysis_workspace/`**: Workspace for ongoing analysis tasks.
*   **`essay_prep/`**: Directory for essay preparation, including outlines and drafts.

## Setup Instructions

1.  **Python Environment:** The project uses Python for its scripting components. It is recommended to use a virtual environment.
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```
2.  **Install Dependencies:** Install the required Python packages using pip:
    ```bash
    pip install -r scripts/requirements.txt
    ```
    Key dependencies include:
    *   `markdown-it-py`
    *   `tiktoken`
    *   `mdit_plain`

## Basic Usage

Interaction with the Philoso-Roo system is primarily mediated through the the system's orchestrator and its specialized modes.

1.  **Source Text Processing:**
    *   Place raw source texts (Markdown, PDF, DOCX) into the appropriate subdirectory within `source_materials/raw/`.
    *   The [`philosophy-text-processor`](.roomodes:280) mode, when invoked (typically by the [`philosophy-orchestrator`](.roomodes:272)), will run the [`scripts/process_source_text.py`](scripts/process_source_text.py:1) script.
    *   This script processes the text, chunks it, generates navigational indices, and outputs structured JSON. The mode then populates the `philosophy-knowledge-base/` and `source_materials/processed/`.
2.  **Analysis Cycles:**
    *   The [`philosophy-orchestrator`](.roomodes:272) delegates tasks to various analysis modes (e.g., [`philosophy-pre-lecture`](.roomodes:288), [`philosophy-class-analysis`](.roomodes:296), [`philosophy-dialectical-analysis`](.roomodes:312)).
    *   These modes read from the `philosophy-knowledge-base/` and `source_materials/processed/`, perform their analyses, and write their findings back to the KB, adhering to rigor standards.
3.  **Essay Writing:**
    *   The [`philosophy-essay-prep`](.roomodes:328) mode manages the essay writing workflow, developing theses and outlines.
    *   [`philosophy-draft-generator`](.roomodes:336) creates draft sections based on KB content.
    *   [`philosophy-citation-manager`](.roomodes:344) handles citations.
    *   [`philosophy-verification-agent`](.roomodes:352) verifies content against the KB.

## Key Documents

*   **System Architecture:** [`docs/architecture/architecture_v18.md`](docs/architecture/architecture_v18.md:1)
*   **Source Material Architecture Proposal:** [`docs/proposals/source_material_architecture_v1.md`](docs/proposals/source_material_architecture_v1.md:1)
*   **`.clinerules` Standard:** [`docs/standards/clinerules_standard_v2.md`](docs/standards/clinerules_standard_v2.md:1) (describes V2.5)
*   **Holistic Review (identifying this README task):** [`docs/reviews/holistic_review_v1.md`](docs/reviews/holistic_review_v1.md:1)

## How to Contribute / Current Status

*(To be developed. This section can include guidelines for contributing to the project, reporting issues, or an overview of the current development status and future roadmap.)*

This project is under active development. Please refer to the Memory Bank (`memory-bank/activeContext.md` and `phil-memory-bank/activeContext.md`) for the latest operational context and ongoing tasks.