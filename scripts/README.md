# Philosophy Analysis System Scripts

This directory contains the core scripts for the Philosophy Analysis System as defined in architectureV6.md.

## Scripts Overview

### extract_text.py
Processes extraction markers that optimize token usage by replacing direct quotations with position or boundary references.

```bash
python extract_text.py --path FILE_OR_DIR [--preview] [--keep-markers]

Arguments:
  --path          File or directory to process
  --preview       Preview changes without modifying files
  --keep-markers  Keep original markers as comments (default: True)
```

Example usage:
```bash
# Process a single file
python extract_text.py --path analysis/current.md

# Process directory with preview
python extract_text.py --path analysis/ --preview
```

### prepare_handoff.py
Prepares documents for AI handoff by expanding extraction markers into full content.

```bash
python prepare_handoff.py <handoff_file>

Arguments:
  handoff_file    Path to the handoff document to process
```

Example usage:
```bash
python prepare_handoff.py analysis_workspace/handoff/class_to_prelecture_handoff.md
```

### process_updates.py
Processes batch updates from pending_updates.json, supporting atomic operations across multiple files.

```bash
python process_updates.py

The script reads from memory-bank/pending_updates.json
```

Example pending_updates.json:
```json
{
  "updates": [
    {
      "file": "memory-bank/activeContext.md",
      "operation": "replace_section",
      "identifier": "current_analysis",
      "content": "Updated content here..."
    },
    {
      "file": "memory-bank/progress.md",
      "operation": "append",
      "content": "- Completed analysis of section 15\n"
    }
  ]
}
```

### process_chunks.py
Processes large texts into semantic chunks with metadata and indexing.

```bash
python process_chunks.py <spec_file>

Arguments:
  spec_file    Path to JSON specification file
```

Example specification file:
```json
{
  "source_file": "Readings/Hegel_ScienceOfLogic.pdf",
  "chunks": [
    {
      "id": "chapter1-section2",
      "title": "Being and Time",
      "start_line": 120,
      "end_line": 152,
      "key_concepts": ["Being", "Dasein", "Temporality"],
      "summary": "Introduces the fundamental question of Being"
    }
  ]
}
```

## Error Handling

All scripts include detailed error handling to help diagnose issues:

- **FileNotFoundError**: Includes attempted file paths and suggestions
- **ValidationError**: Details on what validation failed and why
- **ProcessingError**: Specific information about where processing failed
- **ConfigurationError**: Details about configuration problems

Each error includes:
- Error type and message
- Context of what was being attempted
- Relevant file paths or line numbers
- Suggestions for resolution

## Best Practices

1. Always use --preview first when processing extraction markers
2. Keep backups before running batch updates
3. Validate chunk specifications before processing large texts
4. Review expanded handoff documents for context completeness
5. Monitor memory-bank/pending_updates.json for queued changes

## Dependencies

- Python 3.8 or higher
- Standard library only (no external dependencies)