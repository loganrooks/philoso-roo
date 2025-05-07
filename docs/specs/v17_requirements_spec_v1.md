# Hegel Philosophy RooCode Suite - V17 Requirements Specification

**Version:** 1.1 (Revised for Detail)
**Date:** 2025-05-02
**Status:** Draft
**Based on:** `docs/architecture/architecture_v16.md` (V17 Design)
**Benchmark:** `docs/specs/v14_requirements_spec_v1.md` (Detail Level)

## 1. Introduction

This document details the functional and non-functional requirements for the V17 architecture of the Hegel Philosophy RooCode Suite. It translates the architectural concepts defined in `docs/architecture/architecture_v16.md` into specific requirements for implementation, aiming for a level of detail comparable to or exceeding the V14 specification. This revision addresses feedback regarding the initial V17 specification's lack of detail [See SPARC MB Intervention Log: 2025-05-02 14:57:43].

## 2. Core Principles Requirements

*   **REQ-V17-CP-01:** The system MUST maintain strict separation between SPARC operational context (`memory-bank/`) and philosophy domain knowledge/operations (`philosophy-knowledge-base/`). No KB-specific operational data (indices, logs, status) should reside in `memory-bank/`.
*   **REQ-V17-CP-02:** The `philosophy-knowledge-base/` directory MUST contain all philosophy domain knowledge (e.g., concepts, arguments) AND the operational data specific to managing that knowledge (indices, logs, status, reports, rules) within a dedicated `_operational/` subdirectory.
*   **REQ-V17-CP-03:** All interactions with the `philosophy-knowledge-base/` (read or write, domain or operational data) MUST be mediated exclusively through the `philosophy-kb-manager` mode. Direct file system access to this directory by other modes is strictly forbidden.
*   **REQ-V17-CP-04:** The `philosophy-kb-manager` mode MUST encapsulate all logic for managing the KB's structure, validation (schema, reference, potentially semantic), indexing, logging, status tracking, reporting, and formatting based on rules defined within `philosophy-knowledge-base/_operational/formatting_templates_rules/`.

## 3. Directory Structure Requirements

*   **REQ-V17-DIR-01:** The `memory-bank/` directory structure MUST remain as defined for SPARC operational context (containing `activeContext.md`, `globalContext.md`, `mode-specific/`, `feedback/`).
*   **REQ-V17-DIR-02:** The `philosophy-knowledge-base/` directory MUST exist at the root level.
*   **REQ-V17-DIR-03:** The `philosophy-knowledge-base/` directory MUST contain subdirectories for domain knowledge types. The initial set includes, but is not limited to: `concepts/`, `arguments/`, `quotations/`, `references/`, `questions/`, `theses/`, `relationships/`, `methods/`, `meta-reflections/`, `processed_texts/`, `analyses/`, `citations/`. The exact structure is managed by `philosophy-kb-manager` based on its configuration.
*   **REQ-V17-DIR-04:** The `philosophy-knowledge-base/` directory MUST contain an `_operational/` subdirectory for KB-internal management data.
*   **REQ-V17-DIR-05:** The `_operational/` subdirectory MUST contain the following subdirectories: `indices/`, `logs/`, `status/`, `reports/`, `formatting_templates_rules/`.

## 4. Mode Interaction Requirements

*   **REQ-V17-MI-01:** All modes MUST interact with `memory-bank/` via the designated system evidence/context manager mode (e.g., `philosophy-evidence-manager`) for retrieving or updating operational context.
*   **REQ-V17-MI-02:** Modes requiring access to or modification of `philosophy-knowledge-base/` data (domain or operational) MUST formulate requests and send them to `philosophy-kb-manager` via its defined API (see Section 5.2).
*   **REQ-V17-MI-03:** `philosophy-kb-manager` MUST handle all file system operations (read, write, list, delete) within the `philosophy-knowledge-base/` directory hierarchy.
*   **REQ-V17-MI-04:** `philosophy-kb-manager` MUST return requested data, confirmation of action (with relevant IDs), or a structured error status to the requesting mode.
*   **REQ-V17-MI-05:** Data Flow Example (Analysis Storage):
    1.  `philosophy-class-analysis` generates analysis content.
    2.  `philosophy-class-analysis` calls `kb-manager` API: `store_entry({ type: 'analysis', content: '...', metadata: { title: '...', tags: [...], source_ref_keys: [...] } })`.
    3.  `kb-manager` validates, formats, writes to `philosophy-knowledge-base/analyses/`, updates indices/logs.
    4.  `kb-manager` returns: `{ status: 'success', entry_id: 'analysis_123' }` or `{ status: 'error', message: 'Validation failed: Missing required field title.' }`.

## 5. `philosophy-kb-manager` Mode Requirements

### 5.1 General Requirements

*   **REQ-V17-KBM-01:** `philosophy-kb-manager` MUST act as the sole gateway to `philosophy-knowledge-base/`.
*   **REQ-V17-KBM-02:** `philosophy-kb-manager` MUST maintain the structure, integrity, and consistency of the `philosophy-knowledge-base/` according to configured rules.
*   **REQ-V17-KBM-03:** `philosophy-kb-manager` MUST log its own mode execution details (requests received, actions taken, responses sent) to `memory-bank/mode-specific/philosophy-kb-manager.md`.
*   **REQ-V17-KBM-04:** `philosophy-kb-manager` MUST NOT directly access `memory-bank/` for KB operational data (e.g., reading KB status from MB). It MAY query the system context manager (`philosophy-evidence-manager`) for its own operational needs (e.g., system-level context) if necessary.
*   **REQ-V17-KBM-05:** `philosophy-kb-manager` MUST load its configuration (schemas, validation rules, templates) from `philosophy-knowledge-base/_operational/formatting_templates_rules/` upon initialization.

### 5.2 API / Interface (Detailed)

*   **REQ-V17-KBM-API-01:** `philosophy-kb-manager` MUST expose a defined set of operations via tool calls (or equivalent mechanism, e.g., MCP tool). The interface SHOULD be documented, potentially using OpenAPI specifications.
*   **REQ-V17-KBM-API-02:** CRUD Operations:
    *   `create_entry(entry_data: dict)`: Creates a new entry. `entry_data` includes `type`, `content`, and metadata (e.g., `title`, `tags`, `related_ids`). Returns `{ status: 'success'|'error', entry_id: str|None, message: str|None }`. Assigns unique `id` and `timestamp`.
    *   `read_entry(entry_id: str)`: Retrieves a single entry by ID. Returns `{ status: 'success'|'error', entry_data: dict|None, message: str|None }`.
    *   `update_entry(entry_id: str, update_data: dict)`: Updates specified fields of an existing entry. Returns `{ status: 'success'|'error', message: str|None }`. Updates `timestamp`.
    *   `delete_entry(entry_id: str)`: Deletes an entry (consider soft delete/archival). Returns `{ status: 'success'|'error', message: str|None }`.
*   **REQ-V17-KBM-API-03:** Query Operations:
    *   `query_entries(query_params: dict)`: Performs complex queries. `query_params` can include `type`, `tags` (exact match, contains any/all), `context_tags` (structured filter `{'type': 'course', 'id': 'PHL316'}`), `related_to_id`, `keyword_search` (in content/metadata), `limit`, `offset`. Returns `{ status: 'success'|'error', results: list[dict]|None, total_matches: int|None, message: str|None }`. Results typically include entry summaries (ID, title, type, tags).
    *   `get_related_entries(entry_id: str, relationship_types: list[str]|None = None, context_filter: dict|None = None)`: Finds entries explicitly linked via `related_ids` or potentially inferred relationships. Returns `{ status: 'success'|'error', related_entries: list[dict]|None, message: str|None }`. Related entries dict includes `id` and `relationship_type`.
*   **REQ-V17-KBM-API-04:** Maintenance Operations:
    *   `trigger_maintenance(task_name: str)`: Initiates background tasks like `rebuild_index`, `run_validation_check`, `generate_report`. Returns `{ status: 'success'|'pending'|'error', task_id: str|None, message: str|None }`.
    *   `get_maintenance_status(task_id: str)`: Checks the status of a background task. Returns `{ status: 'success'|'error', task_status: 'pending'|'running'|'completed'|'failed', result_path: str|None, message: str|None }`.
*   **REQ-V17-KBM-API-05:** Operational Data Retrieval:
    *   `get_kb_status()`: Retrieves overall KB status from `_operational/status/`. Returns `{ status: 'success'|'error', kb_status: dict|None, message: str|None }`.
    *   `get_report(report_name: str)`: Retrieves a specific report content from `_operational/reports/`. Returns `{ status: 'success'|'error', report_content: str|None, message: str|None }`.
    *   `get_schema(entry_type: str)`: Retrieves the schema definition for a given entry type from `_operational/formatting_templates_rules/`. Returns `{ status: 'success'|'error', schema_definition: dict|None, message: str|None }`.
*   **REQ-V17-KBM-API-06:** Data Structures: Request/response structures MUST be clearly defined (e.g., using JSON schema or Python type hints in documentation). Data types for fields (string, integer, list, boolean, ISO timestamp) MUST be specified.

    *Detailed Request/Response Examples:*
    ```json
    // Example: create_entry request (Argument)
    {
      "operation": "create_entry",
      "entry_data": {
        "type": "Argument",
        "title": "Argument from Design",
        "premises": ["Premise 1...", "Premise 2..."],
        "conclusion": "Conclusion...",
        "tags": ["teleological", "philosophy_of_religion", "context:type:course", "context:id:PHL101"],
        "related_ids": ["concept_design", "concept_creator"],
        "source_ref_keys": ["ref_paley_1802"]
      }
    }

    // Example: create_entry response (success)
    { "status": "success", "entry_id": "arg_f4b3a2c1" }

    // Example: query_entries request (Find concepts in PHL316 related to 'logic')
    {
      "operation": "query_entries",
      "query_params": {
        "type": "Concept",
        "tags": ["logic"],
        "context_tags": {"type": "course", "id": "PHL316"},
        "limit": 10
      }
    }

    // Example: query_entries response
    {
      "status": "success",
      "results": [
        {"id": "concept_abc", "title": "Dialectical Logic", "type": "Concept", "tags": ["hegel", "logic", "context:type:course", "context:id:PHL316"]},
        {"id": "concept_def", "title": "Formal Logic", "type": "Concept", "tags": ["logic", "context:type:course", "context:id:PHL316"]}
      ],
      "total_matches": 2,
      "message": null
    }

    // Example: trigger_maintenance request
    { "operation": "trigger_maintenance", "task_name": "run_validation_check" }

    // Example: trigger_maintenance response (pending)
    { "status": "pending", "task_id": "val_task_9876", "message": "Validation task queued." }

    // Example: get_kb_status request
    { "operation": "get_kb_status" }

    // Example: get_kb_status response
    {
      "status": "success",
      "kb_status": {
        "last_validation_run": "2025-05-02T14:00:00Z",
        "validation_status": "PASS",
        "last_index_build": "2025-05-02T14:05:00Z",
        "index_status": "UP_TO_DATE",
        "entry_count": 150
      },
      "message": null
    }
    ```

### 5.3 Internal Logic & Validation (Detailed)

*   **REQ-V17-KBM-LOGIC-01:** `philosophy-kb-manager` MUST possess internal logic modules corresponding to each exposed API operation (CRUD, Query, Maintenance, Status).
*   **REQ-V17-KBM-LOGIC-02:** Configuration Loading: On startup, `kb-manager` MUST load schemas, validation rules, and formatting templates from files within `philosophy-knowledge-base/_operational/formatting_templates_rules/`. Errors during loading MUST be logged and reported.
*   **REQ-V17-KBM-LOGIC-03:** Validation Logic: MUST be applied during `create_entry` and `update_entry`, and can be triggered via `trigger_maintenance`.
    *   Schema Validation: Check submitted `entry_data` against the loaded schema for the specified `type`. Checks include presence of required fields, correct data types (string, list, etc.), and allowed values for specific fields if defined. Reject entries with invalid schemas, providing specific error messages.
    *   Reference Validation: For fields like `related_ids` or `source_ref_keys`, check if the listed IDs correspond to existing entries in the KB. Configurable behavior on failure (IGNORE, WARN, FAIL) defined in `validation_rules.yaml`. Log warnings or reject entries based on configuration.
    *   Link Integrity: (Optional/Future) Parse Markdown content for internal links (`[text](entry_id)`) and verify `entry_id` exists.
    *   Semantic Validation: (Optional/Future) Apply basic semantic rules defined in `validation_rules.yaml` (e.g., an 'Argument' entry must have non-empty `premises` and `conclusion` fields).
    *   Context Tag Validation: Ensure `context:key:value` tags follow the expected format.
*   **REQ-V17-KBM-LOGIC-04:** Indexing Logic: MUST maintain indices in `_operational/indices/` to support efficient querying.
    *   Strategy: Initial implementation MAY use a simple keyword index (e.g., JSON mapping keywords to entry IDs). Future versions MAY incorporate full-text search (e.g., using Whoosh, Lunr.py) or a graph database representation (e.g., NetworkX, Neo4j embedded) for relationships. The chosen strategy MUST be documented.
    *   Triggers: Indexing MUST be updated incrementally on `create_entry`, `update_entry`, `delete_entry`. Full rebuilds triggered via `trigger_maintenance('rebuild_index')`.
    *   Content Indexed: Index should cover relevant YAML fields (title, tags) and potentially the Markdown content.
*   **REQ-V17-KBM-LOGIC-05:** Logging Logic: MUST record significant events to files in `_operational/logs/`.
    *   Log Content: Each log entry SHOULD include: ISO Timestamp, Log Level (INFO, WARN, ERROR), Operation Name (e.g., `create_entry`, `validate_references`), Entry ID (if applicable), Status (Success, Failure), Message/Details.
    *   Log Format: Structured format preferred (e.g., JSON per line) for easier parsing.
    *   Log Rotation: Implement basic rotation (e.g., daily files, keep N most recent files) to prevent excessive disk usage. Configurable in `kb-manager` settings.
*   **REQ-V17-KBM-LOGIC-06:** Status Management Logic: MUST update files in `_operational/status/` to reflect the KB's current state.
    *   Files: `kb_status.yaml` (overall status), potentially task-specific status files (e.g., `indexing_status.json`).
        definition: {{ definition }}
        tags: {{ tags | default([]) | to_yaml }}
        related_ids: {{ related_ids | default([]) | to_yaml }}
        source_ref: {{ source_ref | default("") }}
        ---

        # {{ title }}

        {{ definition }}
        ```

## 6. Performance Considerations (Addressing Arch Question 9.4)

*   **REQ-V17-PERF-01:** The `philosophy-kb-manager` MUST be designed to handle the expected load of requests from other modes without becoming a significant bottleneck.
*   **REQ-V17-PERF-02:** Indexing strategies implemented by `kb-manager` MUST be efficient enough to support timely querying.
*   **REQ-V17-PERF-03:** Long-running `kb-manager` operations (e.g., full re-indexing, extensive validation) SHOULD be executable asynchronously or report progress, allowing requesting modes to proceed or query status later.
*   **REQ-V17-PERF-04:** Caching mechanisms MAY be considered within `kb-manager` for frequently accessed data or query results, if performance analysis indicates a need.
*   **REQ-V17-PERF-05:** Performance metrics (e.g., request latency, operation duration) for `kb-manager` operations SHOULD be logged (potentially within `_operational/logs/` or Operational Memory) to facilitate monitoring and optimization.

## 7. Non-Functional Requirements

*   **REQ-V17-NFR-01:** Error Handling: `philosophy-kb-manager` MUST provide clear error messages to requesting modes upon failure (e.g., validation errors, file access issues).
*   **REQ-V17-NFR-02:** Configurability: Key aspects of `kb-manager` behavior (e.g., validation strictness, logging level) SHOULD be configurable, potentially via files in `_operational/formatting_templates_rules/`.
*   **REQ-V17-NFR-03:** Testability: The internal logic of `kb-manager` SHOULD be designed for unit testing.

## 8. Future Work / Considerations

*   Detailed design of specific indexing strategy.
*   Implementation of asynchronous operation handling.
*   Definition of specific semantic validation rules.
*   Integration with version control for the KB itself (beyond essay drafts).
            source_ref: string
        argument:
          # ... schema definition ...
        ```
    *   *Example (`validation_rules.yaml`):*
        ```yaml
        reference_checking:
          on_create: WARN # Options: IGNORE, WARN, FAIL
          on_update: WARN
        tag_format: "^[a-z0-9_]+(:[a-z0-9_.-]+){0,2}$" # Simple example regex
        ```
    *   *Example (`concept_template.md`):*
        ```markdown
        ---
        title: {{ title }}
        definition: {{ definition }}
        tags: {{ tags | default([]) | to_yaml }}
        related_ids: {{ related_ids | default([]) | to_yaml }}
        source_ref: {{ source_ref | default("") }}
        ---

        # {{ title }}

        {{ definition }}
        ```

## 6. Performance Considerations (Addressing Arch Question 9.4)

*   **REQ-V17-PERF-01:** The `philosophy-kb-manager` MUST be designed to handle the expected load of requests from other modes without becoming a significant bottleneck.
*   **REQ-V17-PERF-02:** Indexing strategies implemented by `kb-manager` MUST be efficient enough to support timely querying.
*   **REQ-V17-PERF-03:** Long-running `kb-manager` operations (e.g., full re-indexing, extensive validation) SHOULD be executable asynchronously or report progress, allowing requesting modes to proceed or query status later.
*   **REQ-V17-PERF-04:** Caching mechanisms MAY be considered within `kb-manager` for frequently accessed data or query results, if performance analysis indicates a need.
*   **REQ-V17-PERF-05:** Performance metrics (e.g., request latency, operation duration) for `kb-manager` operations SHOULD be logged (potentially within `_operational/logs/` or Operational Memory) to facilitate monitoring and optimization.

## 7. Non-Functional Requirements

*   **REQ-V17-NFR-01:** Error Handling: `philosophy-kb-manager` MUST provide clear error messages to requesting modes upon failure (e.g., validation errors, file access issues).
*   **REQ-V17-NFR-02:** Configurability: Key aspects of `kb-manager` behavior (e.g., validation strictness, logging level) SHOULD be configurable, potentially via files in `_operational/formatting_templates_rules/`.
*   **REQ-V17-NFR-03:** Testability: The internal logic of `kb-manager` SHOULD be designed for unit testing.

## 8. Future Work / Considerations

*   Detailed design of specific indexing strategy.
*   Implementation of asynchronous operation handling.
*   Definition of specific semantic validation rules.
*   Integration with version control for the KB itself (beyond essay drafts).