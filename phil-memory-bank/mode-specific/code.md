### [2025-05-05 19:02:34] `philosophy-meta-reflector` Mode Rules (V2.0 - V2.2 Standard Compliant)
- **Purpose**: Defines the `philosophy-meta-reflector` mode, responsible for evaluating rigor, analyzing logs/KB for patterns, assessing quality, and proposing improvements. Aligned with `clinerules_standard_v2.2.md` (explicit rules, no inheritance section/headers, correct `phil-memory-bank/` paths) and V18.3.5 architecture (direct KB/MB access, meta-analysis logic).
- **Files**: `.roo/rules-philosophy-meta-reflector/philosophy-meta-reflector.clinerules`
- **Status**: Implemented (Updated to V2.0 - Pending Verification)
- **Dependencies**: Relies on `philosophy-orchestrator` (for task delegation/routing), file system tools (for KB, docs, rules, and `phil-memory-bank/` access), `docs/standards/clinerules_standard_v2.md`, `docs/architecture/architecture_v18.md`, and the RooCode mode execution framework. Assumes V18.3.5 KB and `phil-memory-bank` structures.
- **API Surface**: N/A (Configuration file defining mode behavior). Input schema defines interaction contract.
- **Tests**: N/A (Configuration file).
- **Cross-ref:** [Global Progress: 2025-05-05 19:02:14], [Global System Pattern: 2025-05-05 19:02:14]
# Code Mode Specific Memory (phil-memory-bank)
<!-- Entries below should be added reverse chronologically (newest first) -->

## Intervention Log
<!-- Append intervention details using the format below -->

## Components Implemented
### [2025-05-05 19:09:26] `philosophy-kb-doctor` Mode Rules (V2.0 - V2.2 Standard Compliant - Pending Verification)
- **Purpose**: Defines the `philosophy-kb-doctor` mode, responsible for monitoring KB health by reading operational logs/status/reports. Aligned with `clinerules_standard_v2.2.md` (explicit rules, no inheritance section/headers, correct `phil-memory-bank/` paths) and V18.3.5 architecture (monitoring role, direct KB operational read access, no script execution).
- **Files**: `.roo/rules-philosophy-kb-doctor/philosophy-kb-doctor.clinerules`
- **Status**: Implemented (Updated to V2.0 - Pending Verification)
- **Dependencies**: Relies on `philosophy-orchestrator` (for task delegation), file system tools (for KB operational dir and `phil-memory-bank/` access), `docs/standards/clinerules_standard_v2.md`, `docs/architecture/architecture_v18.md`, and the RooCode mode execution framework. Assumes V18.3.5 KB and `phil-memory-bank` structures.
- **API Surface**: N/A (Configuration file defining mode behavior). Input schema defines interaction contract.
- **Tests**: N/A (Configuration file).
- **Cross-ref:** [Global Progress: 2025-05-05 19:09:10]
### [2025-05-05 18:50:35] `philosophy-verification-agent` Mode Rules (V2.2 - Pending Verification)
- **Purpose**: Defines the `philosophy-verification-agent` mode, responsible for verifying content against KB entries, source chunks, and rigor standards (V18.3.5). Aligned with `clinerules_standard_v2.2.md` (explicit rules, no inheritance section/headers).
- **Files**: `.roo/rules-philosophy-verification-agent/philosophy-verification-agent.clinerules`
- **Status**: Implemented (Updated to V2.2 - Pending Verification)
- **Dependencies**: Relies on `philosophy-orchestrator` (for task delegation), file system tools (for KB, processed sources, and `phil-memory-bank/` access), `docs/standards/clinerules_standard_v2.md`, `docs/architecture/architecture_v18.md`, and the RooCode mode execution framework. Assumes V18.3.5 KB and `phil-memory-bank` structures.
- **API Surface**: N/A (Configuration file defining mode behavior). Input schema defines interaction contract.
- **Tests**: N/A (Configuration file).
- **Cross-ref:** [Global Progress: 2025-05-05 18:50:19]

### [2025-05-05 18:28:30] `philosophy-citation-manager` Mode Rules (V2.2 - V2.2 Standard Compliant)
- **Purpose**: Defines the `philosophy-citation-manager` mode, responsible for formatting citations and bibliographies based on KB reference entries. Aligned with `clinerules_standard_v2.2.md` (explicit rules, no inheritance section/headers) and V18.3.5 architecture (direct KB read, `phil-memory-bank/` access, evidence standards).
- **Files**: `.roo/rules-philosophy-citation-manager/philosophy-citation-manager.clinerules`
- **Status**: Implemented (Updated to V2.2)
- **Dependencies**: Relies on `philosophy-orchestrator` (for task delegation), file system tools (for KB and `phil-memory-bank/` access), `docs/standards/clinerules_standard_v2.md`, `docs/architecture/architecture_v18.md`, and the RooCode mode execution framework. Assumes V18.3.5 KB and `phil-memory-bank` structures.
- **API Surface**: N/A (Configuration file defining mode behavior). Input schema defines interaction contract.
### [2025-05-05 22:13:50] `philosophy-evidence-manager` Mode Rules (V2.0 - V2.2 Standard Compliant)
- **Purpose**: Defines the `philosophy-evidence-manager` mode, responsible for retrieving evidence and associated rigor context (source links, extraction markers) directly from the Knowledge Base (`philosophy-knowledge-base/`). Aligned with `clinerules_standard_v2.2.md` and V18.3.5 architecture.
- **Files**: `.roo/rules-philosophy-evidence-manager/philosophy-evidence-manager.clinerules`
- **Status**: Implemented (Updated to V2.0 - V2.2 Standard Compliant)
- **Dependencies**: Relies on `philosophy-orchestrator` (for task delegation), file system tools (for KB and `phil-memory-bank/` access), `docs/standards/clinerules_standard_v2.md`, `docs/architecture/architecture_v18.md`, and the RooCode mode execution framework. Assumes V18.3.5 KB and `phil-memory-bank` structures.
- **API Surface**: N/A (Configuration file defining mode behavior). Input schema defines interaction contract.
- **Tests**: N/A (Configuration file).
- **Cross-ref:** [Global Progress: 2025-05-05 22:13:24], [Global System Pattern: 2025-05-05 22:13:24]
- **Tests**: N/A (Configuration file).
- **Cross-ref:** [Global Progress: 2025-05-05 18:28:30], [Global System Pattern: 2025-05-05 18:28:30]
### [2025-05-05 18:03:48] `philosophy-draft-generator` Mode Rules (V2.2 - V2.2 Standard Compliant)
- **Purpose**: Defines the `philosophy-draft-generator` mode, responsible for generating draft prose based on KB outlines and context, incorporating evidence links. Aligned with `clinerules_standard_v2.2.md` (explicit rules, no inheritance section/headers) and V18.3.5 architecture (direct KB read, `phil-memory-bank/` access).
- **Files**: `.roo/rules-philosophy-draft-generator/philosophy-draft-generator.clinerules`
- **Status**: Implemented (Updated to V2.2)
- **Dependencies**: Relies on `philosophy-orchestrator` (for task delegation), file system tools (for KB and `phil-memory-bank/` access), `docs/standards/clinerules_standard_v2.md`, `docs/architecture/architecture_v18.md`, and the RooCode mode execution framework. Assumes V18.3.5 KB and `phil-memory-bank` structures.
- **API Surface**: N/A (Configuration file defining mode behavior). Input schema defines interaction contract.
- **Tests**: N/A (Configuration file).
- **Cross-ref:** [Global Progress: 2025-05-05 18:03:48], [Global System Pattern: 2025-05-05 18:03:48]

## Technical Debt
<!-- Track identified technical debt items -->

## Dependencies
<!-- Track key external dependencies -->