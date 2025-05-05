# Code Mode Specific Memory (phil-memory-bank)
<!-- Entries below should be added reverse chronologically (newest first) -->

## Intervention Log
<!-- Append intervention details using the format below -->

## Components Implemented

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