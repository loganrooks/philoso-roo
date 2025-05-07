# Proposal: Source Material Processed Directory Architecture V1

**Date:** 2025-05-06
**Author:** Architect Mode
**Version:** 1.0
**Status:** Draft

## 1. Introduction

This document proposes a new architecture for the `source_materials/processed/` directory within the Hegel Philosophy RooCode Suite. The current structure (as per `docs/architecture/architecture_v18.md` and its predecessors) and any existing ad-hoc organization are deemed inadequate to meet the evolving research needs of the system, particularly concerning flexible categorization, nuanced identification of primary/secondary literature, robust indexing, and efficient navigation for various philosophical research modes.

This proposal addresses critical user feedback requesting a more sophisticated and usable system for managing processed source materials.

## 2. Goals & Requirements

The primary goals of this architectural redesign are to:

*   **Improve Organization:** Provide a clear and intuitive structure for diverse types of processed materials.
*   **Enhance Accessibility:** Make it easier for all relevant modes to find and utilize processed texts.
*   **Support Nuance:** Accommodate flexible categorization, especially for course-specific vs. general library materials, and the context-dependent nature of "primary" vs. "secondary" literature.
*   **Boost Discoverability:** Implement robust indexing and tagging to allow for efficient searching and filtering.
*   **Manage Context Window:** Ensure that navigation and indexing mechanisms are efficient and do not unduly burden the context window of AI modes.
*   **Maintain Scalability:** Design a structure that can scale with an increasing volume of processed materials.

This design specifically addresses the following user requirements:

*   **Flexible & Nuanced Categorization:**
    *   Support for course-specific materials (e.g., lectures, readings, notes for courses like PHL316).
    *   Support for a general library of research materials not tied to specific courses.
    *   Ability to identify materials as "primary" or "secondary" relative to a specific inquiry or task, rather than a fixed global status.
*   **Optimal Structure:**
    *   A well-reasoned balance between hierarchical folder structures and flatter, tag-driven organization.
*   **Robust Indexing & Tagging:**
    *   A comprehensive strategy for indexing and tagging processed materials.
    *   Tags should include: course code, topic, author, specific work/text, date, type of material, and a mechanism for dynamic primary/secondary status.
*   **Context Window Management:**
    *   Efficient structure and management of index file(s) for navigation without excessive context window consumption.

## 3. Proposed Architecture

The proposed architecture introduces a clear distinction between course-specific materials and a general library, utilizing a hybrid hierarchical and tag-based approach. A master JSON index will provide a global overview, while individual Markdown indexes will detail specific materials.

### 3.1. Directory Structure

```
source_materials/processed/
├── courses/
│   └── [COURSE_CODE]/         # e.g., PHL316, PHL400
│       ├── index.md           # Index for this course's processed materials (lists readings, lectures, notes for the course)
│       ├── lectures/
│       │   └── [LECTURE_ID]/    # Unique ID, e.g., PHL316_lec_2025-01-15_hegel_intro
│       │       ├── index.md      # Metadata, chunk list, tags for this specific lecture
│       │       └── chunks/       # Directory containing processed text chunks
│       │           └── chunk_001.md
│       │           └── chunk_002.md
│       │           └── ...
│       ├── readings/
│       │   └── [READING_ID]/   # Unique ID, e.g., hegel_phenomenology_spirit_intro_processed
│       │       ├── index.md      # Metadata, chunk list, tags for this specific reading
│       │       └── chunks/
│       │           └── chunk_001.md
│       │           └── ...
│       └── notes/              # Personal or shared notes related to the course
│           └── [NOTE_ID]/      # Unique ID, e.g., PHL316_personal_notes_on_being
│               ├── index.md      # Metadata, chunk list, tags for this specific note
│               └── chunks/
│                   └── chunk_001.md
│                   └── ...
├── library/                   # General research materials not tied to a specific course
│   └── [material_id]/         # Globally unique ID, e.g., kant_cpr_b_edition_processed
│       ├── index.md           # Metadata, chunk list, tags for this specific library material
│       └── chunks/
│           └── chunk_001.md
│           └── ...
└── master_index.json          # Master JSON index for all processed materials
```

**Key Structural Elements:**

*   **`courses/[COURSE_CODE]/`**: Top-level directory for materials specific to a course.
    *   `index.md`: An index file within each course directory, listing all processed lectures, readings, and notes for that course, with links to their respective `[ID]/index.md` files.
    *   Subdirectories for `lectures/`, `readings/`, `notes/` provide content-type organization within a course.
    *   `[LECTURE_ID]`, `[READING_ID]`, `[NOTE_ID]`: Unique `material_id`s for each processed item. These should be human-readable yet unique, possibly derived from course, type, and original filename/key attributes (e.g., `PHL316_reading_Hegel_Phen_Intro`).
*   **`library/`**: Top-level directory for general research materials.
    *   `[material_id]`: A globally unique `material_id` for each library item (e.g., `kant_critique_pure_reason_b_1787_processed`).
*   **`[ID]/index.md` (for all material types):** A Markdown file containing:
    *   YAML frontmatter with detailed metadata (see Section 3.2.2).
    *   A list of links to its constituent `chunks/chunk_XXX.md` files, possibly with brief descriptions or keywords for each chunk.
*   **`[ID]/chunks/`**: Directory containing the actual processed text chunks as individual Markdown files.
*   **`master_index.json`**: A single JSON file at the root of `source_materials/processed/` serving as the comprehensive, machine-readable index for all processed materials.

### 3.2. Indexing and Tagging Strategy

#### 3.2.1. `master_index.json`

This file is the central, machine-parsable index for all processed materials.

*   **Format:** A JSON array, where each element is an object representing one processed material.
*   **Fields per entry (example):**
    ```json
    {
      "id": "hegel_phenomenology_spirit_intro_processed", // Unique material_id matching directory name
      "path_to_index": "courses/PHL316/readings/hegel_phenomenology_spirit_intro_processed/index.md",
      "title": "Hegel - Phenomenology of Spirit - Introduction",
      "original_path": "source_materials/raw/courses/PHL316/readings/Hegel_Phenomenology_Spirit_Introduction.md",
      "material_type": "reading", // lecture, reading, note, library_material
      "source_type": "course_material", // course_material, library_primary, library_secondary, personal_note
      "course_code": "PHL316", // If applicable
      "project_name": null, // If applicable
      "authors": ["G.W.F. Hegel"],
      "work_title": "Phenomenology of Spirit", // Title of the larger work
      "section_title": "Introduction", // Specific section processed, if applicable
      "publication_date": "1807", // Or original lecture date
      "processing_date": "2025-05-07T10:00:00Z",
      "chunk_count": 15,
      "summary": "An introduction to Hegel's method and the journey of consciousness.",
      "tags": [
        "hegel",
        "phenomenology",
        "spirit",
        "idealism",
        "epistemology",
        "PHL316_W2" // Course week/module if applicable
      ],
      "dynamic_roles": [ // Examples, managed by analysis modes
        // {"inquiry_id": "inq_001_hegel_self_consciousness", "role": "primary_source"},
        // {"essay_id": "essay_003_hegel_vs_kant", "role": "key_text"}
      ]
    }
    ```
*   **Key `tags`:**
    *   `course:[COURSE_CODE]` (e.g., `course:PHL316`)
    *   `topic:[TOPIC_NAME]` (e.g., `topic:being`, `topic:idealism`)
    *   `author:[AUTHOR_NAME]` (e.g., `author:hegel`, `author:kant`)
    *   `work:[WORK_TITLE_SLUG]` (e.g., `work:phenomenology-of-spirit`)
    *   `material_type:[TYPE]` (e.g., `material_type:lecture`, `material_type:primary_text`, `material_type:secondary_analysis`, `material_type:personal_note`)
    *   `date:[YYYY]` or `date:[YYYY-MM-DD]`
    *   Custom tags as needed (e.g., `kant_critique`, `hegel_early_writings`).
*   **`dynamic_roles`:** This array allows modes to tag a material's role (e.g., primary, secondary, supporting, critique) *relative to a specific task, inquiry, or other KB item*. Each object would contain a context identifier (e.g., `inquiry_id`, `essay_id`, `concept_id_being_discussed`) and the assigned role. Updates to this field are managed by the `philosophy-orchestrator` as per the protocol defined in [`docs/proposals/terminology_clarification_v1_dynamic_roles_source_id.md#42-term-dynamic_roles`](docs/proposals/terminology_clarification_v1_dynamic_roles_source_id.md:53). This addresses the requirement for context-dependent primary/secondary status.
*   **Maintenance:** The `philosophy-text-processor` mode is responsible for adding new entries to this index upon successful processing of a source and for ensuring the `id` is unique.

#### 3.2.2. Individual Material `index.md` Files

Located within each material's directory (e.g., `courses/PHL316/readings/[READING_ID]/index.md`).

*   **Format:** Markdown with YAML frontmatter.
*   **YAML Frontmatter:** Contains a subset of the metadata found in `master_index.json` relevant to that specific item, including:
    *   `id: [material_id] # Unique material_id`
    *   `title`
    *   `authors`
    *   `work_title`
    *   `section_title`
    *   `publication_date`
    *   `material_type`
    *   `source_type`
    *   `course_code` (if applicable)
    *   `tags` (static tags relevant to this item)
    *   `dynamic_roles` (roles specific to this item in various contexts, updated by `philosophy-orchestrator` in sync with `master_index.json`)
    *   `summary`
    *   `chunk_count`
    *   `list_of_chunks`: An array of objects, each describing a chunk:
        ```yaml
        list_of_chunks:
          - file: "chunks/chunk_001.md"
            summary: "Initial discussion of sense-certainty."
            keywords: ["sense-certainty", "immediate"]
          - file: "chunks/chunk_002.md"
            summary: "The 'this', 'here', and 'now'."
            keywords: ["this", "here", "now", "deixis"]
        ```
*   **Markdown Body:** Provides a human-readable table of contents, listing and linking to each chunk file in the `chunks/` subdirectory, possibly with the chunk summary.
    ```markdown
    # Processed Chunks for: Hegel - Phenomenology of Spirit - Introduction

    - [Chunk 1: Initial discussion of sense-certainty.](chunks/chunk_001.md)
    - [Chunk 2: The 'this', 'here', and 'now'.](chunks/chunk_002.md)
    - ...
    ```

### 3.3. Addressing Specific Requirements

*   **Flexible & Nuanced Categorization:**
    *   The `courses/` vs. `library/` top-level split provides clear initial categorization.
    *   The `material_type` tag (e.g., `lecture`, `primary_text`, `secondary_analysis`, `note`) within `master_index.json` and individual `index.md` files allows for fine-grained typing.
    *   The `dynamic_roles` array in both index types allows modes to assign primary/secondary status (or other roles) relative to specific inquiries, tasks, or contexts. For example, a mode analyzing "Hegel's concept of Being in the Science of Logic" might tag the relevant sections of SoL as `{"inquiry_id": "hegel_being_sol", "role": "primary_source"}` and a commentary by Pippin as `{"inquiry_id": "hegel_being_sol", "role": "secondary_source"}`.

*   **Optimal Structure:**
    *   The proposed hybrid structure offers clear, course-based or general library-based hierarchical organization at the top levels, aiding human understanding and initial filtering by modes.
    *   Within each processed material's directory, the structure is flat (`index.md` and `chunks/`), simplifying access once a specific material is identified.
    *   The `master_index.json` provides a powerful, flat, taggable index for global discovery, mitigating the need for excessively deep or complex folder hierarchies for searching.

*   **Robust Indexing & Tagging:**
    *   **`master_index.json`:** Serves as the primary, machine-optimized index. Its JSON format allows for efficient querying and filtering by modes based on any combination of its fields (ID, title, type, course, author, tags, etc.).
    *   **Individual `index.md` files:** Provide human-readable and mode-parsable metadata and chunk listings for specific materials.
    *   **Comprehensive Tagging:** The suggested tag set (`course_code`, `topic`, `author`, `work_title`, `material_type`, `date`, custom tags) combined with `dynamic_roles` offers rich discoverability.
    *   **Tag Generation:** `philosophy-text-processor` will generate initial tags based on source path and potentially light NLP. Analysis modes will be responsible for adding more nuanced topic tags and `dynamic_roles`.

*   **Context Window Management:**
    *   **`master_index.json`:** While it could grow large, modes will typically query it for specific subsets of data (e.g., "all readings for PHL316 tagged 'Hegel'") rather than loading the entire file if it's too big. If `master_index.json` becomes excessively large for direct loading by some modes, a future enhancement could involve an MCP providing a query interface to it, or sharding the index. For now, a single JSON is proposed.
    *   **Staged Access:** Modes first query `master_index.json` to identify relevant materials. Then, they load the much smaller individual `index.md` for those specific materials. Finally, they load only the necessary chunks. This staged approach minimizes the context loaded at any one time.
    *   The individual `index.md` files, being per-material, are inherently limited in size.

### 3.4. Workflow Implications

*   **`philosophy-text-processor`:**
    *   Responsible for creating the directory structure for each new processed item (`courses/[COURSE_CODE]/[TYPE]/[ID]/` or `library/[MATERIAL_ID]/`).
    *   Generates the `[ID]/index.md` file with its YAML frontmatter and chunk list.
    *   Generates the individual `chunks/chunk_XXX.md` files.
    *   **Crucially, adds/updates the entry for the processed material in `source_materials/processed/master_index.json`.**
    *   Updates the course-specific `courses/[COURSE_CODE]/index.md` if applicable.
*   **Analysis Modes (e.g., `philosophy-pre-lecture`, `philosophy-class-analysis`, `philosophy-secondary-lit`):**
    *   Query `master_index.json` to find relevant materials based on course, topic, author, tags, etc.
    *   Read individual `[ID]/index.md` files for metadata and chunk overview.
    *   Read specific `chunks/chunk_XXX.md` files for detailed analysis.
    *   Can *propose* updates to the `dynamic_roles` field to the `philosophy-orchestrator` to reflect the material's role in the current analysis.
*   **Navigation by Modes:**
    *   Modes can perform broad searches on `master_index.json`.
    *   For course-specific tasks, they can directly navigate to `courses/[COURSE_CODE]/index.md` to see all materials for that course.
    *   Once a material is identified, its local `index.md` provides the map to its chunks.

## 4. Rationale for Design Choices

*   **Separation of Concerns:** `courses/` vs. `library/` provides a clear top-level distinction often needed by users and modes.
*   **Unique IDs:** `[LECTURE_ID]`, `[READING_ID]`, `[MATERIAL_ID]` ensure stability and allow for future re-categorization if needed (e.g., moving an item from a course to the general library by updating its path in `master_index.json`).
*   **JSON Master Index:** Chosen for machine-readability and efficient querying over a large Markdown file. It centralizes discovery.
*   **Markdown Individual Indexes:** Provide human-readable summaries and chunk navigation for specific items once discovered. YAML frontmatter is standard and easily parsed.
*   **Hybrid Hierarchy/Tagging:** Offers the benefits of structured browsing (hierarchy) and powerful, flexible searching (tags in `master_index.json`).
*   **Dynamic Roles:** Directly addresses the user's need for context-dependent primary/secondary status without creating complex, duplicative folder structures.
*   **Chunk-Based Processing:** Assumed from existing architecture; this design supports it by organizing chunks under their parent material.

## 5. Future Considerations

*   **`master_index.json` Scalability:** If the number of processed items grows extremely large, querying a single large JSON file might become inefficient. Future solutions could include:
    *   Sharding `master_index.json` (e.g., by first letter of ID, or by year).
    *   Implementing a lightweight database (e.g., SQLite) managed by a dedicated MCP to serve index queries.
*   **Advanced Tag Management:** A dedicated tagging UI or mode could help manage the vocabulary and application of tags.
*   **Semantic Search:** Integrating semantic search capabilities over the `master_index.json` or chunk content.

## 6. Conclusion

This proposed architecture for the `source_materials/processed/` directory aims to provide a flexible, scalable, and discoverable system for managing processed philosophical texts. It balances hierarchical organization with powerful indexing and tagging, addresses the nuanced requirements for categorization and contextual roles, and lays a foundation for efficient use by various research modes.
## 7. Addendum V1.1: Integration of Dated Course Materials (2025-05-07)

This addendum details how dated raw course materials (lectures, readings) and syllabus information are integrated with the V1 Source Material Architecture, specifically concerning their processing into the `source_materials/processed/` directory and the incorporation of date metadata. This aligns with the [`docs/plans/dated_course_material_integration_plan_v1.md`](docs/plans/dated_course_material_integration_plan_v1.md:1).

### 7.1. Dated Raw Material Paths

As per the integration plan, raw dated course materials are stored as follows:

*   **Raw Lectures:** `source_materials/raw/courses/[COURSE_CODE]/lectures/[YYYY-MM-DD_LECTURE_TITLE_SLUG]/[FILENAME.ext]`
*   **Raw Readings:** `source_materials/raw/courses/[COURSE_CODE]/readings/[YYYY-MM-DD_READING_TITLE_SLUG]/[FILENAME.ext]`
*   **Raw Syllabuses:** `source_materials/raw/courses/[COURSE_CODE]/syllabuses/[SYLLABUS_FILENAME.ext]`

The `YYYY-MM-DD` prefix in lecture and reading subdirectories is critical for date extraction.

### 7.2. Mapping to Processed Structure & Metadata Incorporation

The V1 architecture for `source_materials/processed/courses/[COURSE_CODE]/` is extended to explicitly handle these dated materials:

*   **Processed Lectures:**
    *   Stored under: `source_materials/processed/courses/[COURSE_CODE]/lectures/[LECTURE_ID]/`
    *   `LECTURE_ID` is derived to incorporate the date (e.g., `phl316_lec_2025-09-08_hegel_concepts`).
    *   The `index.md` within this directory will have `lecture_date: YYYY-MM-DD` in its YAML frontmatter.
    *   The `master_index.json` entry for this lecture will include `lecture_date: "YYYY-MM-DD"`.

*   **Processed Readings:**
    *   Stored under: `source_materials/processed/courses/[COURSE_CODE]/readings/[READING_ID]/`
    *   `READING_ID` is derived to incorporate the primary assigned date (e.g., `phl316_reading_2025-09-08_hegel_phen_preface`).
    *   The `index.md` within this directory will have `assigned_date: YYYY-MM-DD` (or `week_start_date`) in its YAML frontmatter.
    *   The `master_index.json` entry for this reading will include `assigned_date: "YYYY-MM-DD"`.

*   **Processed Syllabuses:**
    *   Stored under: `source_materials/processed/courses/[COURSE_CODE]/syllabuses/[SYLLABUS_ID]/` (where `SYLLABUS_ID` incorporates term/year).
    *   Contains `index.md` (with metadata like `term_start_date`, `term_end_date`, `year`, `is_active_syllabus`) and `extracted_data.json` (structured syllabus content).
    *   The `master_index.json` entry for the syllabus will include `term_start_date`, `term_end_date`, and `year`.

### 7.3. Script Modifications for Date Handling

*   The `scripts/process_source_text.py` (or a similar script dedicated to dated materials if `process_source_text.py` remains for generic library items) MUST be updated to:
    *   Parse the `YYYY-MM-DD` from the raw material path for lectures and readings.
    *   Incorporate this extracted date into the derived `LECTURE_ID` or `READING_ID`.
    *   Add the `lecture_date` or `assigned_date` to the YAML frontmatter of the material's `index.md` in the `processed` directory.
    *   Add the corresponding date field to the material's entry in `master_index.json`.
*   A new `scripts/process_syllabus.py` (or enhanced `process_source_text.py`) is responsible for processing syllabuses, generating `extracted_data.json`, and updating `master_index.json` and the course-specific `index.md` with syllabus metadata and associations.

### 7.4. Tagging for Temporal Context

*   The syllabus processing script and/or the text processing script (when handling dated course materials) should add week-specific and topic-specific tags (e.g., `PHL316_Week_2`, `PHL316_Topic_SelfConsciousness`, `date_YYYY-MM-DD`) to the `tags` array in `master_index.json` entries and the YAML frontmatter of individual processed material `index.md` files. This facilitates temporal querying and association by analysis modes.

This addendum clarifies the integration of dated materials into the V1 source material architecture, ensuring that temporal context is captured and made available throughout the system.