# Enhanced Philosophy Analysis System Architecture

## 1. System Overview

### 1.1 Purpose and Design Philosophy

The Philosophy Analysis System is an integrated suite of specialized modes designed to support comprehensive philosophical analysis throughout a course's chronological progression. The system enables:

- Chronologically-aware analysis that respects the developmental sequence of course material
- Evidence-based interpretation with rigorous textual/lecture references and extensive direct quotations
- Seamless transitions between different types of analytical work
- Comprehensive documentation of philosophical concepts, arguments, and their evolution
- Determinate articulation of philosophical concepts through both positive and negative definition
- Disambiguation of terminology through explicit contrast with potential misinterpretations
- Persistent context management to handle interruptions and multi-step analyses
- Flexible adaptation to missing materials through alternative analysis paths
- Cost-effective content generation through reference instead of duplication

### 1.2 Core Architectural Principles

1. **Chronological Integrity**: All modes enforce strict chronological progression through course material
2. **Evidence Standards**: All modes require explicit textual/source evidence for interpretations, with extensive direct quotations
3. **Conceptual Determinacy**: All analyses define concepts both positively and negatively to achieve precise determination
4. **Disambiguation Requirements**: All potentially ambiguous terms must be explicitly disambiguated from both ordinary language and related philosophical usages
5. **Active Context Management**: All modes maintain persistent state through dated context files to enable seamless resumption
6. **Cycle Completion**: Analysis cycles must be completed for each date before progression, with appropriate alternatives when materials are missing
7. **Date Specificity**: All files and analyses are explicitly tied to specific dates
8. **Shared Memory Model**: All modes access and maintain a common memory structure
9. **Verification Protocols**: All modes implement rigorous verification steps
10. **Standardized Handoffs**: All inter-mode transitions follow consistent protocols
11. **Presentation Flexibility**: Content may be formatted with paragraphs or focused bullet points that maintain determinacy and depth
12. **Content Efficiency**: Generate content once, reference many times to minimize token usage

### 1.3 System-Wide Memory Model

The system uses a unified memory management approach across all modes:

- **Chronological Index**: Central source of truth for course progression
- **Date-Specific Files**: Named consistently using [DATE] format
- **Concept/Argument Indices**: Shared across all modes for consistent tracking
- **Active Context Files**: Persistent state management for resuming interrupted analyses
- **Handoff Context**: Standardized format for mode transitions
- **Workspace Structure**: Common folder organization across modes
- **Terminology Database**: Shared repository of determinate concept definitions
- **Materials Availability Tracker**: Records status of lecture transcripts, notes, and alternative sources
- **Reference System**: Pointers to existing content to minimize duplication

## 2. Standard Mode Structure

### 2.1 Required Components

Every mode configuration file (.clinerules) must include these sections:

```yaml
mode: philosophy-[mode-name]
description: "Concise description of mode purpose"
version: "x.y.z"

capabilities:
  allowed_tools:
    - read_file
    - append_to_file     # For adding new content without rewrites
    - insert_content     # For targeted insertions
    - search_and_replace # For targeted modifications
    - apply_diff         # For small changes to existing files
    - ask_followup_question
    - switch_mode

content_management:
  reference_system:
    enabled: true
    reference_format: "{{REF:filepath:section}}"  # Reference existing content
  
  section_markers:
    enabled: true
    format: "<!-- SECTION:unique_id:start -->...<!-- SECTION:unique_id:end -->"

mode_switching:
  enabled: true
  preserve_context: true
  recommended_transitions: [list of appropriate mode transitions]

workspace_inspection:
  enabled: true
  initialization_checks: [list of startup verification checks]

memory_management:
  workspace: [folder structure]
  context_files: [priority loading structure]
  indexing: [file format definitions]
  active_context: [active context management configuration]

conceptual_determinacy:
  negative_definition: required
  disambiguation_protocol: required
  ordinary_language_contrast: required

evidence_standards:
  quotation_requirements: [minimum thresholds]
  verification_protocol: [verification steps]
  presentation_flexibility: [bullet point usage guidelines]

file_operations:
  update_strategies:
    - name: "full_rewrite"      # Only for new files
    - name: "append_content"    # For adding to existing files
    - name: "update_section"    # For modifying specific sections
    - name: "incremental_update" # For minor changes

workflows:
  default: [standard workflow sequence]
  specialized: [optional workflows]
  alternative: [workflows for missing materials]

instructions: [operational guidelines]

memory_bank_implementation:
  status_prefix: "[MEMORY BANK: ACTIVE][MODE-PREFIX]"
  context_management: [loading priorities]

handoff_protocols: [mode transition protocols]
special_handoffs: [substitution handoffs]

cycle_management:
  full_cycle_definition: [mode's place in analysis cycle]
  enforcement: [cycle completion requirements]
  progression_rules: [chronological rules]
  completion_alternatives: [valid substitutions]
  
active_context_management:
  checkpoint_triggers: [list of checkpoint events]
  resumption_protocol: [steps for resuming analysis]
  multi_part_progression: [handling multi-part content]
  specialized_contexts: [substitution contexts]
```

## 3. Chronological Management System

### 3.1 Chronological Index Structure

The central source of truth for all modes is `analysis_logs/chronological_index.md`, which must contain:

```markdown
# Chronological Analysis Index

Last updated: [TIMESTAMP]

## Current Target
**Date:** [CURRENT_TARGET_DATE]
**Topic:** [CURRENT_TARGET_TOPIC]
**Current Phase:** [CURRENT_PHASE]

## Materials Availability
**Lecture Transcript:** [AVAILABLE/MISSING]
**Lecture Notes:** [AVAILABLE/PARTIAL/MISSING]
**Secondary Sources:** [AVAILABLE/NEEDED/PENDING]

## Course Schedule and Cycle Status
| Date | Topic | Pre-Lecture | Class Analysis | Integration | Cycle Status | Materials Status |
|------|-------|-------------|---------------|------------|--------------|------------------|
[SCHEDULE_ROWS]
```

### 3.2 Analysis Cycle Definition

The standard full analysis cycle is:
1. **Pre-lecture analysis** (required)
2. **Class analysis** (required, or substitutable with secondary literature analysis when lecture unavailable)
3. **Secondary literature review** (optional, but required as substitute when lecture unavailable)
4. **Dialectical analysis** (optional)
5. **Integration** (optional)

### 3.3 Chronological Enforcement Rules

1. Analysis must proceed in strict chronological order
2. Pre-lecture for date N+1 cannot begin until class analysis for date N is complete (or appropriate substitute cycle is complete)
3. When initializing a new workspace, must start with earliest course date
4. All modes must verify chronological integrity before operations
5. Chronological violations must be blocked with clear error messages
6. Active contexts must be date-specific and enforce chronological integrity

### 3.4 Alternative Cycle Paths

#### 3.4.1 Missing Lecture Transcript Path
When a lecture transcript is unavailable, the system supports an alternative cycle path:
1. Pre-lecture analysis → complete as normal
2. Class analysis → detect missing transcript → check for lecture notes
3. If notes available → use notes as partial transcript, noting limitations
4. If notes insufficient/unavailable → transition to secondary literature mode
5. Secondary literature analysis → acts as class analysis substitute
6. Mark cycle as complete with notation of substitution
7. Allow progression to next date's pre-lecture analysis

This alternative path preserves chronological integrity while accommodating practical limitations.

## 4. Memory Management System

### 4.1 Standard Workspace Structure

```
analysis_workspace/
├── prelecture/                 # Pre-lecture analyses
├── lectures/                   # Lecture analyses
│   ├── transcripts/            # Lecture transcripts
│   ├── notes/                  # Lecture notes
├── concepts/                   # Concept tracking
│   ├── definitions/            # Determinate concept definitions
│   ├── terminology_index.md    # Master terminology index
├── arguments/                  # Argument tracking
├── integrated/                 # Integration analyses
│   ├── dialectical/            # Dialectical analyses
├── essay_prep/                 # Essay preparation materials
├── secondary_literature/       # Secondary literature analyses
│   ├── sources/
│   ├── bibliographies/
│   ├── perspectives/
│   ├── debates/
│   ├── substitutions/          # Secondary lit as lecture substitutes
├── shared/                     # Shared content for references
│   ├── evidence/               # Quotation repository
│   ├── determinations/         # Key concept determinations
│   ├── arguments/              # Reusable argument structures
├── analysis_logs/              # Analysis tracking
│   ├── chronological_index.md  # Master schedule
│   ├── materials_status.md     # Materials availability tracking
│   ├── active_contexts/        # Active context management
│   │   ├── prelecture/
│   │   ├── lectures/
│   │   ├── secondary_literature/
│   │   ├── dialectical/
│   │   └── essay_prep/
├── handoff/                    # Mode transition documents
├── indices/                    # Cross-references and pointers
    ├── source_references.md    # Original file locations
```

### 4.2 File Naming Conventions

- **Date-specific files**: Always use `[DATE]_[type].md` format (e.g., `Jan07_analysis.md`)
- **Concept files**: Use `[CONCEPT_NAME].md` format
- **Argument files**: Use `[ARGUMENT_NAME].md` format
- **Active context files**: Use `[DATE]_active_context.md` format
- **Version tracking**: Use `v[VERSION]` for versioned files (e.g., `thesis_v2.md`)
- **Handoff files**: Use `[FROM_MODE]_to_[TO_MODE]_context.md`
- **Substitution files**: Use `[DATE]_[type]_substitute.md` format
- **Index files**: Must include source file references in `source: [FILEPATH]` format

### 4.3 Context Loading Priority System

All modes must implement a consistent priority loading system:

```yaml
context_files:
  high_priority:
    - "analysis_logs/chronological_index.md"  # ALWAYS first
    - "analysis_logs/materials_status.md"     # Materials availability tracking
    - "analysis_logs/active_contexts/[MODE]/[DATE]_active_context.md"  # ALWAYS next
    - "[MODE-SPECIFIC]/[DATE]_[TYPE].md"      # Current date files
  medium_priority:
    - "concepts/terminology_index.md"         # Master terminology index
    - "concepts/index.md"                     # Shared concept tracking
    - "arguments/index.md"                    # Shared argument tracking
    - "integrated/course_overview.md"         # Course integration
  low_priority:
    - "handoff/handoff_context.md"            # Transition context
    - "[MODE-SPECIFIC]/archive/[OLD_DATE]_analysis.md"  # Previous analyses
```

## 5. Cost Optimization System

### 5.1 File Operation Strategies

```yaml
file_operations:
  check_before_write: true  # Always check existence before writing
  
  update_strategies:
    - name: "full_rewrite"
      tool: write_to_file
      usage: "Only for new files or complete reconstructions"
      implementation: |
        1. Check if file exists
        2. If not exists, create with complete content
        3. If exists, prefer other strategies
    
    - name: "append_content"
      tool: append_to_file
      usage: "For adding new analysis sections to existing files"
      implementation: |
        1. Calculate insertion point
        2. Append only new content
        3. Include section markers for future updates
    
    - name: "update_section"
      tool: search_and_replace
      usage: "For modifying specific sections within files"
      implementation: |
        1. Locate section by unique identifier marker
        2. Replace only that section's content
        3. Leave rest of file untouched
    
    - name: "incremental_update"
      tool: apply_diff
      usage: "For minor updates to existing content"
      implementation: |
        1. Generate minimal diff of changes
        2. Apply only necessary modifications
```

### 5.2 Content Reference System

```yaml
reference_system:
  implementation: |
    1. Store canonical content once in appropriate location
    2. In all other locations, use reference pointers
    3. For concept definitions: store in concepts/definitions/
    4. For textual evidence: store in shared/evidence/
    5. For arguments: store in shared/arguments/
  
  reference_patterns:
    - concept_reference: "{{REF:concepts/definitions/[CONCEPT_NAME].md}}"
    - evidence_reference: "{{REF:shared/evidence/[EVIDENCE_ID].md}}"
    - argument_reference: "{{REF:shared/arguments/[ARGUMENT_NAME].md}}"
  
  reference_display: |
    # Referenced content from [SOURCE_PATH]
    ## [CONTENT_TITLE]
    
    [BRIEF_SUMMARY]
    
    See full details at: [SOURCE_PATH]
    
    Key points:
    - [POINT_1]
    - [POINT_2]
```

### 5.3 Index File Guidelines

```yaml
index_file_structure:
  template: |
    # Index: [INDEX_NAME]
    Generated: [TIMESTAMP]
    
    ## Indexed Files
    [LIST_OF_FILES_WITH_PATHS]
    
    ## Content Index
    
    ### [ENTRY_1]
    - **Source File:** [FILEPATH]
    - **Location:** [SECTION/PAGE/TIMESTAMP]
    - **Summary:** [BRIEF_SUMMARY]
    - **References:** [CROSS_REFERENCES]
    
    ### [ENTRY_2]
    ...
  
  update_strategy: incremental  # Only update changed entries
```

### 5.4 Content Fingerprinting

```yaml
content_fingerprinting:
  implementation: |
    1. Generate hash/fingerprint for all content chunks
    2. Before regenerating content:
       - Calculate expected fingerprint of result
       - Skip generation if identical content exists
       - Use reference instead of duplication
    3. For concept determinations:
       - Track fingerprints of all determinations
       - Only update when definition truly changes
  
  tracking_file: "analysis_logs/content_fingerprints.json"
  
  fingerprint_format: |
    {
      "path": "[FILEPATH]",
      "section": "[SECTION_ID]",
      "hash": "[CONTENT_HASH]",
      "last_updated": "[TIMESTAMP]"
    }
```

### 5.5 Section Marking System

```yaml
section_marking:
  implementation: |
    1. Divide all content files into discrete sections with unique identifiers
    2. Format: <!-- SECTION:[UNIQUE_ID]:start --> ... <!-- SECTION:[UNIQUE_ID]:end -->
    3. Use search_and_replace tool to update specific sections
    4. Track section update status in active context
  
  required_sections:
    - concept_determination
    - evidence_collection
    - argument_analysis
    - interpretation
    - integration
```

### 5.6 File Operation Workflow

```yaml
file_operation_workflow:
  standard_sequence: |
    1. check_file_exists
    2. if_exists:
       - load_existing_content
       - identify_changed_sections
       - if changes_are_minor:
         - apply targeted updates (search_and_replace or apply_diff)
       - if changes_are_additions:
         - use append_to_file
       - if changes_are_sectional:
         - use search_and_replace for specific sections
    3. if_not_exists:
       - create_file_with_template
       - include_section_markers
```

### 5.7 Optimization Guidelines

1. **Store once, reference many**: Create canonical definitions and evidence in dedicated locations
2. **Update, don't rewrite**: Modify only changed sections rather than regenerating entire files
3. **Append, don't overwrite**: Add new content to existing files rather than recreating them
4. **Section-based changes**: Target specific sections using unique identifiers
5. **Incremental index updates**: Update only changed entries in index files
6. **Reference source files**: Always include original source location in index entries
7. **Chunk intelligently**: Divide large files into manageable, independently updatable sections

## 6. Handoff Protocol System

### 6.1 Standard Handoff Format

All handoffs between modes must follow this format:

```markdown
# Handoff Context: [FROM_MODE] to [TO_MODE]

## Handoff Information
- **Date:** [DATE]
- **Topic:** [TOPIC]
- **From Mode:** [FROM_MODE]
- **To Mode:** [TO_MODE]
- **Generated:** [TIMESTAMP]

## IMPORTANT: TARGET DATE VERIFICATION
This handoff is for analysis of **[DATE]** material.
The receiving mode MUST continue analysis for this SAME DATE.

## Materials Availability
- **Lecture Transcript:** [AVAILABLE/MISSING]
- **Lecture Notes:** [AVAILABLE/PARTIAL/MISSING]
- **Note Quality Assessment:** [DESCRIPTION]
- **Secondary Sources:** [AVAILABLE/NEEDED/PENDING]

## Target Date Status
[TARGET_DATE_STATUS]

## Active Context Status
[ACTIVE_CONTEXT_STATUS]
- Active context file: [FILEPATH]
- Last checkpoint: [TIMESTAMP]
- Resumption point: [POSITION]

## Completion Status
[COMPLETION_STATUS]

## Required Context
[REQUIRED_CONTEXT]

## Key Concepts Requiring Determination
[KEY_CONCEPTS_LIST]
- [CONCEPT_1]: Current determination status, pending disambiguation needs
- [CONCEPT_2]: Current determination status, pending disambiguation needs

## Required Follow-up
[REQUIRED_FOLLOWUP]
```

### 6.2 Special Case Handoffs

#### 6.2.1 Missing Lecture Substitution Handoff

When a lecture transcript is missing, class analysis must initiate a special handoff to secondary literature mode:

```yaml
special_handoffs:
  missing_lecture_substitution:
    from_class_analysis:
      preparation: |
        1. Extract CURRENT_TARGET_DATE from chronological_index.md
        2. Check for lecture notes availability
        3. If notes available but insufficient:
           - Document note limitations in handoff
        4. Document missing lecture transcript in chronological index
        5. Generate secondary source recommendations based on pre-lecture content
        6. Create handoff/handoff_context.md with:
           - EXPLICIT statement: "Target date: [CURRENT_TARGET_DATE]"
           - EXPLICIT statement: "SUBSTITUTION MODE: Secondary Literature as Class Analysis Substitute"
           - List of recommended sources with justification
           - Key concepts requiring determination from secondary sources
           - Pre-lecture expectations needing validation
           - Available lecture notes with quality assessment
        7. Update chronological_index.md with "Substitution Required" status
```

## 7. Evidence Standards System

### 7.1 Cross-Mode Evidence Requirements

All modes must implement these minimum evidence standards:

```yaml
evidence_standards:
  requirements:
    - "All interpretations must reference specific text/lecture sections with direct quotations"
    - "Major concepts require multiple direct quotes with proper citation"
    - "All interpretations must include confidence assessment"
    - "Complex passages require documentation of alternative readings"
    - "Key philosophical terms must be defined through both positive and negative determination"
    - "Potentially ambiguous terminology must be explicitly disambiguated from ordinary usage"
    - "Interpretations must contrast the author's meaning with potential misinterpretations"
    - "Analysis can use bullet points, but only to remove filler words while maintaining the same level of depth, detail, and determinacy"
  
  verification_workflow:
    enabled: true
    coverage_threshold: 90%
    quote_requirement_threshold: 75%
    confidence_assessment_required: true
    negative_definition_required: true
    disambiguation_required: true
    bullet_point_quality: "Must maintain determinacy" # Quality standard for bullet points
```

### 7.2 Evidence Repository System

To minimize duplication, implement an evidence repository:

```yaml
evidence_repository:
  implementation: |
    1. Store all significant quotations once in shared/evidence/
    2. Assign unique ID to each quotation
    3. Track metadata including:
       - Source document and page/timestamp
       - Context information
       - Concepts referenced
       - Arguments supported
    4. In analysis files, reference evidence by ID
    5. Display minimal context with reference pointer when used
  
  evidence_entry_format: |
    # Evidence ID: [EVIDENCE_ID]
    
    ## Source
    - Document: [SOURCE_DOCUMENT]
    - Location: [PAGE/TIMESTAMP]
    - Date: [SOURCE_DATE]
    
    ## Content
    > [FULL_QUOTATION_TEXT]
    
    ## Context
    [SURROUNDING_CONTEXT]
    
    ## References
    - Concept: [RELATED_CONCEPT]
    - Argument: [RELATED_ARGUMENT]
    
    ## Usage Locations
    - [FILE_1]: [SECTION]
    - [FILE_2]: [SECTION]
```

### 7.3 Bullet Point Usage Guidelines

When using bullet points in philosophical analyses:

1. **Preserve determinacy**: Bullet points should only remove filler words, never substantive content that contributes to determinacy
2. **Maintain depth**: The analysis should maintain the same level of analytical depth regardless of formatting
3. **Ensure detail**: Key details must be preserved even when using bullet point format
4. **Appropriate contexts**: Bullet points are most appropriate for:
   - Listing key features of concepts
   - Enumerating distinct arguments
   - Presenting alternative interpretations
   - Organizing evidence
5. **Inappropriate contexts**: Avoid bullet points for:
   - Complex dialectical movements requiring narrative flow
   - Nuanced interpretations requiring contextual embedding
   - Detailed explication of conceptual relations

The primary goal is to maintain determinacy while improving clarity, not to reduce analytical depth.

## 8. Determinacy Enforcement System

### 8.1 Concept Determination Protocol

All modes must implement this determination process for key philosophical terms:

```yaml
determination_protocol:
  implementation: |
    1. Identify key philosophical terms requiring determination
    2. For each term:
       a. Collect direct textual evidence (quotes) defining or using the term
       b. Provide explicit positive determination (what it IS)
       c. Provide explicit negative determination (what it is NOT)
       d. Contrast with ordinary language usage
       e. Distinguish from related philosophical concepts
       f. Document potential misinterpretations
       g. Update terminology index with determination
```

### 8.2 Concept Repository System

```yaml
concept_repository:
  implementation: |
    1. Store all concept determinations in concepts/definitions/
    2. Each concept gets a unique file with comprehensive determination
    3. Include full evidence, positive and negative definitions
    4. In analysis files, reference concepts by pointer
    5. Track concept evolution through versioned determinations
    6. Maintain usage index for each concept
  
  concept_entry_format: |
    # Concept: [CONCEPT_NAME]
    Version: [VERSION]
    Last Updated: [TIMESTAMP]
    
    ## Textual Evidence
    {{REF:shared/evidence/[EVIDENCE_ID_1].md}}
    {{REF:shared/evidence/[EVIDENCE_ID_2].md}}
    
    ## Positive Determination
    [EXPLICIT_DEFINITION]
    
    ## Negative Determination
    [WHAT_THE_CONCEPT_IS_NOT]
    
    ## Relation to Ordinary Language
    [CONTRAST_WITH_COMMON_USAGE]
    
    ## Related Concepts
    - [RELATED_CONCEPT_1]: [RELATIONSHIP]
    - [RELATED_CONCEPT_2]: [RELATIONSHIP]
    
    ## Potential Misinterpretations
    - [MISINTERPRETATION_1]: [REFUTATION]
    - [MISINTERPRETATION_2]: [REFUTATION]
    
    ## Usage Locations
    - [FILE_1]: [SECTION]
    - [FILE_2]: [SECTION]
    
    ## Version History
    - v1: [DATE] - Initial determination
    - v2: [DATE] - [CHANGE_DESCRIPTION]
```

## 9. Active Context Management System

### 9.1 Active Context File Structure

Each mode must maintain a date-specific active context file with this structure:

```markdown
# Active Context: [DATE] [ANALYSIS_TYPE]
Last Updated: [TIMESTAMP]
Status: [IN_PROGRESS/PAUSED/COMPLETED]

## Materials Status
- Lecture Transcript: [AVAILABLE/MISSING]
- Lecture Notes: [AVAILABLE/PARTIAL/MISSING]
- Note Quality Assessment: [DESCRIPTION]
- Secondary Sources: [AVAILABLE/NEEDED/PENDING]

## Current Position
- Reading/Lecture Section: [CURRENT_SECTION]
- Progress: [PERCENTAGE_COMPLETE]
- Last Analyzed Point: [SPECIFIC_REFERENCE]

## Readings/Sources Queue
1. [READING_1] - Status: [COMPLETE/IN_PROGRESS/PENDING]
2. [READING_2] - Status: [COMPLETE/IN_PROGRESS/PENDING]
3. [READING_3] - Status: [COMPLETE/IN_PROGRESS/PENDING]

## Content Change Tracking
- [FILE_1]: [SECTIONS_MODIFIED], [LAST_MODIFIED_TIMESTAMP]
- [FILE_2]: [SECTIONS_MODIFIED], [LAST_MODIFIED_TIMESTAMP]

## Concepts Under Analysis
[LIST_OF_ACTIVE_CONCEPTS_WITH_CURRENT_DEFINITION_STATUS]

## Pending Determinations
[LIST_OF_TERMS_REQUIRING_DETERMINATION]

## Analysis Notes
[RUNNING_NOTES_ON_CURRENT_READING]

## Checkpoints
- Checkpoint 1: [SECTION] - [TIMESTAMP]
- Checkpoint 2: [SECTION] - [TIMESTAMP]
```

### 9.2 Change Tracking System

```yaml
change_tracking:
  implementation: |
    1. For all content files, track:
       - Last modified timestamp
       - Modified sections
       - Content fingerprints
    2. Before generating content:
       - Check if content already exists
       - Check if content has changed
       - Only update modified sections
    3. Update active context with change records
  
  tracking_format: |
    ## File: [FILEPATH]
    - Last Modified: [TIMESTAMP]
    - Modified Sections: [SECTION_IDS]
    - New Content: [YES/NO]
    - Content Hash: [HASH]
```

## 10. Mode-Specific Responsibilities

### 10.1 Pre-Lecture Mode

**Primary Role**: Analyze course readings before lectures

**Key Responsibilities**:
- Identify key passages, concepts, and arguments in readings with extensive direct quotation
- Generate questions for upcoming lecture that target potential ambiguities
- Develop hypotheses about concepts and arguments with explicit positive and negative determinations
- Document potentially ambiguous philosophical terminology
- Maintain active context through multiple reading assignments
- Track reading-specific progress with detailed position references
- Implement checkpoints at section boundaries and concept determinations

**Cost Optimization Strategies**:
- Store quoted evidence once in shared repository, reference by ID
- Store concept determinations in canonical location, reference elsewhere
- Use section markers for targeted updates to analysis files
- Implement incremental updates to active contexts
- Track content fingerprints to avoid redundant concept determinations
- Use append operations for analysis logs rather than rewrites

### 10.2 Class-Analysis Mode

**Primary Role**: Analyze lecture content and relate to readings

**Key Responsibilities**:
- Analyze lecture concepts and arguments with extensive direct quotation
- Compare with pre-lecture expectations, noting clarifications of ambiguities
- Extract and track concept development with explicit determination
- Document shifts in terminology usage from readings to lecture
- Integrate with course themes
- Create checkpoints at major conceptual transitions in lecture
- Check for available personal notes from lectures and incorporate them as appropriate
- Create substitution workflows when both transcript and notes are insufficient

**Missing Materials Workflow**:
1. Check for lecture transcript availability
2. If missing, check for personal lecture notes
3. Assess note quality and coverage:
   - If sufficient: Proceed with notes-based analysis (flagging confidence limitations)
   - If insufficient: Initiate secondary literature substitution
4. Update materials_status.md with current status

**Cost Optimization Strategies**:
- Reference pre-lecture concepts rather than duplicating
- Store lecture quotes in evidence repository, reference by ID
- Use section markers for targeted updates to analysis files
- Track content changes to minimize rewriting unchanged sections
- Implement partial updates for concept evolutions
- When using notes, leverage existing pre-lecture material with references

### 10.3 Secondary-Literature Mode

**Primary Role**: Research scholarly perspectives on course topics

**Key Responsibilities**:
- Analyze scholarly interpretations of primary texts with extensive quotation
- Map scholarly debates and competing perspectives
- Provide historical context for concepts with determinate definitions
- Function as lecture analysis substitute when required
- Compare scholarly interpretations with lecture notes when appropriate
- Integrate available personal notes when functioning as a substitute
- Cover expected lecture content when functioning as a substitute

**Substitution Mode Workflow**:
1. Receive special handoff from class-analysis with substitute status
2. Load pre-lecture expectations and any available notes
3. Analyze recommended sources with focus on fulfilling class analysis objectives
4. Generate concept determinations and argument analyses comparable to lecture
5. Create special completion marking cycle as validly completed despite substitution
6. Mark all determinations with source attribution

**Cost Optimization Strategies**:
- Share evidence repository with other modes, reference quotes by ID
- Reference pre-lecture concepts rather than duplicating
- When substituting for class analysis, explicitly reference pre-lecture expectations
- Use sectional updates rather than full rewrites
- Create canonical source analysis files, reference in multiple contexts
- Implement scholarly perspective index with references to source files
- Track content fingerprints to avoid redundant source analyses

### 10.4 Text-Processing Mode

**Primary Role**: Process and chunk texts into manageable units

**Key Responsibilities**:
- Analyze text structure to determine chunking strategy
- Divide texts into semantically meaningful chunks
- Create hierarchical indices for text navigation
- Generate semantic indices by concept and argument
- Process and organize lecture notes when transcripts are unavailable

**Cost Optimization Strategies**:
- Include source file references in all indices
- Implement pointer system for content references
- Create canonical text chunks, reference elsewhere by ID
- Use append operations for incremental index building
- Track content fingerprints to avoid reprocessing unchanged text
- Track dependencies between chunks and derived analyses
- Maintain change log to enable targeted updates

**Index File Structure**:
```markdown
# Index: [INDEX_NAME]
Generated: [TIMESTAMP]

## Source Files
- [FILEPATH_1]
- [FILEPATH_2]

## Content Chunks
### [CHUNK_ID_1]
- **Source File:** [FILEPATH]
- **Location:** [START_POSITION]-[END_POSITION]
- **Key Concepts:** [CONCEPT_LIST]
- **Summary:** [BRIEF_SUMMARY]

### [CHUNK_ID_2]
...
```

### 10.5 Dialectical-Analysis Mode

**Primary Role**: Analyze philosophical concepts through dialectical movement

**Key Responsibilities**:
- Identify dialectical contradictions in concepts with textual evidence
- Map dialectical moments in concept development with determinate articulations
- Analyze transitions between dialectical moments with direct quotation
- Synthesize dialectical resolutions with clear positive/negative determination
- Create visualizations of dialectical movement
- Maintain active context for multi-stage dialectical analyses
- Track progress through dialectical moments with checkpoints
- Adapt dialectical analysis to available materials (lecture transcript, notes, or scholarly substitutes)

**Cost Optimization Strategies**:
- Reference existing concept determinations rather than duplicating
- Store dialectical movement patterns in reusable templates
- Reference existing evidence for each dialectical moment
- Use section markers for targeted updates to dialectical analyses
- Create canonical dialectical patterns, reference in specific applications
- Use append operations for incremental dialectical development
- Implement partial updates for evolving dialectical structures
- Reference source materials by pointer rather than re-quoting

**Dialectical Analysis Structure**:
```markdown
# Dialectical Analysis: [CONCEPT]
Date: [DATE]
Source: [ANALYSIS_SOURCE]

## Dialectical Structure
- **Thesis:** [THESIS_STATEMENT]
  - Evidence: {{REF:shared/evidence/[EVIDENCE_ID_1].md}}
- **Antithesis:** [ANTITHESIS_STATEMENT]
  - Evidence: {{REF:shared/evidence/[EVIDENCE_ID_2].md}}
- **Synthesis:** [SYNTHESIS_STATEMENT]
  - Evidence: {{REF:shared/evidence/[EVIDENCE_ID_3].md}}

## Moments of Transition
### Thesis to Antithesis
[TRANSITION_ANALYSIS]
- Evidence: {{REF:shared/evidence/[EVIDENCE_ID_4].md}}

### Antithesis to Synthesis
[TRANSITION_ANALYSIS]
- Evidence: {{REF:shared/evidence/[EVIDENCE_ID_5].md}}

## Concept Evolution
[REFERENCE_TO_CONCEPT_HISTORY]
```

### 10.6 Essay-Prep Mode

**Primary Role**: Develop philosophical essays from conception to draft

**Key Responsibilities**:
- Analyze essay prompts
- Develop and refine thesis statements with determinate concepts
- Map arguments supporting theses with direct textual evidence
- Create outlines and drafts with extensive quotation
- Integrate course materials chronologically
- Compile and manage bibliographies
- Maintain active context for multi-stage essay development
- Create checkpoints at major essay development milestones
- Adapt to material availability constraints

**Cost Optimization Strategies**:
- Reference existing concept determinations rather than regenerating
- Use pointers to evidence repository for quotations
- Reference existing arguments with unique identifiers
- Implement versioned thesis statements with change tracking
- Store structural templates separately from content
- Apply incremental updates to essay components
- Use section markers for targeted revisions
- Maintain outline structure separate from content details
- Reference source analyses rather than re-analyzing
- Track content changes to avoid redundant generations

**Essay Structure Organization**:
```markdown
# Essay Plan: [TOPIC]
Version: [VERSION]
Last Updated: [TIMESTAMP]

## Thesis Statement
Version [VERSION]: [THESIS_STATEMENT]

## Argument Map
<!-- SECTION:argument_structure:start -->
1. [MAIN_POINT_1]
   - Supporting evidence: {{REF:shared/evidence/[EVIDENCE_ID_1].md}}
   - Concept reference: {{REF:concepts/definitions/[CONCEPT_1].md}}

2. [MAIN_POINT_2]
   - Supporting evidence: {{REF:shared/evidence/[EVIDENCE_ID_2].md}}
   - Concept reference: {{REF:concepts/definitions/[CONCEPT_2].md}}
<!-- SECTION:argument_structure:end -->

## Outline
<!-- SECTION:outline:start -->
### Introduction
- [INTRO_POINT_1]
- [INTRO_POINT_2]
- Thesis: [THESIS_STATEMENT]

### Section 1: [SECTION_TITLE]
- [POINT_1]
- [POINT_2]
  - Evidence: {{REF:shared/evidence/[EVIDENCE_ID_3].md}}
<!-- SECTION:outline:end -->

## Evidence Repository
[LIST_OF_EVIDENCE_REFERENCES]

## Version History
- v1: [DATE] - Initial concept
- v2: [DATE] - [CHANGE_DESCRIPTION]
```

## 11. Materials Availability System

### 11.1 Materials Status Tracking

The system must track material availability across all dates and analysis cycles:

```markdown
# Materials Availability Status
Last Updated: [TIMESTAMP]

## Current Analysis Cycle
**Date:** [CURRENT_TARGET_DATE]
**Topic:** [CURRENT_TOPIC]

## Materials Status Table
| Date | Topic | Lecture Transcript | Lecture Notes | Notes Quality | Secondary Sources |
|------|-------|-------------------|--------------|--------------|-------------------|
[MATERIALS_ROWS]

## Missing Materials Documentation
### [DATE]
- **Missing:** [WHAT_IS_MISSING]
- **Impact:** [IMPACT_DESCRIPTION]
- **Alternatives:** [ALTERNATIVE_APPROACH]
- **Status:** [RESOLVED/PENDING]
- **Resolution:** [RESOLUTION_DESCRIPTION]
```

### 11.2 Lecture Notes Assessment

When lecture transcripts are unavailable but notes exist, the system assesses note quality:

```yaml
note_assessment:
  evaluation_criteria:
    - completeness: "Coverage of expected lecture content"
    - concept_specificity: "Clarity of concept definitions"
    - argument_capture: "Completeness of argument structures"
    - quote_preservation: "Presence of direct quotes"
    - organization: "Structural clarity and organization"
  
  assessment_process: |
    1. Evaluate notes against each criterion on 1-5 scale
    2. Calculate overall usability score
    3. Determine appropriate usage level:
       - High (4-5): Can use as primary source with minor confidence limitations
       - Medium (3-3.9): Use with significant confidence limitations
       - Low (1-2.9): Use only to supplement secondary literature
    4. Identify specific gaps requiring secondary sources
    5. Document assessment in materials_status.md
  
  confidence_marking: |
    1. For high-quality notes: "Note-based interpretation (moderate confidence)"
    2. For medium-quality notes: "Note-based interpretation (low confidence)"
    3. For low-quality notes: "Note-based interpretation (minimal confidence, requires verification)"
```

### 11.3 Source Recommendation System

When lecture materials are unavailable, the system generates targeted secondary source recommendations:

```yaml
source_recommendation:
  triggers:
    - missing_lecture_transcript
    - explicit_research_request
    - knowledge_gap_detection
  
  implementation: |
    1. Extract key concepts and arguments from pre-lecture analysis
    2. Identify course themes relevant to current date
    3. Generate search parameters based on:
       - Author names from primary texts
       - Key philosophical terms identified in pre-lecture
       - Historical context of primary texts
       - Course-specific methodological approaches
    4. Prioritize sources based on:
       - Relevance to specific concepts needing determination
       - Coverage of expected lecture topics
       - Scholarly reputation and authority
       - Accessibility and availability
    5. Generate structured recommendations with relevance justification
  
  recommendation_format: |
    ## Recommended Secondary Sources
    
    ### Primary Recommendations (High Priority)
    1. [AUTHOR], [TITLE], [PUBLICATION]
       - Relevance: [SPECIFIC_RELEVANCE_TO_CURRENT_TOPICS]
       - Key concepts covered: [CONCEPT_LIST]
       - Specific chapter/section recommendations: [SECTIONS]
    
    ### Secondary Recommendations
    [ADDITIONAL_SOURCES_WITH_RELEVANCE]
    
    ### Search Parameters
    If sources unavailable, recommended search terms:
    - [TERM_1], [TERM_2], [TERM_3]
    - Combinations: "[TERM_1] AND [TERM_2]"
```

## 12. Content Efficiency System

### 12.1 Content Reference Implementation Guidelines

```yaml
content_reference_implementation:
  standard_approach: |
    1. Store canonical content once in appropriate location
    2. Create rich content IDs that reflect content meaning
    3. Include metadata with each content piece:
       - Creation date
       - Source document/lecture
       - Related concepts
       - Update history
    4. Use standardized reference format to point to canonical content
    5. When displaying referenced content, include:
       - Clear indication of reference source
       - Summary of referenced content
       - Link to full content
       - Key points from referenced content
    6. Update referenced content in place rather than recreating
```

### 12.2 Content Caching Strategy

```yaml
content_caching:
  implementation: |
    1. For all generated content:
       - Apply deterministic fingerprinting
       - Store fingerprint in tracking system
    2. Before generating content:
       - Check if equivalent content already exists
       - If exists, use reference instead of regenerating
    3. For frequent operations:
       - Create templated components
       - Implement partial calculation system
       - Cache intermediate results
    4. For section-based files:
       - Apply fingerprinting to each section
       - Only regenerate changed sections
```

### 12.3 Token Optimization Guidelines

1. **References over duplication**: Always reference existing content rather than duplicating
2. **Append over rewrite**: Add to existing files rather than rewriting them
3. **Section updates over file updates**: Modify only changed sections rather than entire files
4. **Partial rendering**: When displaying referenced content, show summary with link to full content
5. **Content fingerprinting**: Track content signatures to avoid regenerating identical content
6. **Templated structures**: Create reusable templates for common components
7. **Checkpoint efficiency**: Create sparse checkpoints that reference existing content
8. **Index pointers**: Use index files with pointers rather than content duplication
9. **Change tracking**: Only process what has changed since last analysis
10. **Shared evidence repository**: Store quotes once, reference many times

## 13. Implementation Guidelines

The implementation of this architecture requires all modes to:

1. Prioritize determinate understanding over breadth of coverage
2. Enforce strict textual evidence requirements with extensive direct quotation
3. Implement templates that require both positive and negative determination
4. Mandate disambiguation of potentially ambiguous terminology
5. Allow bullet points that maintain determinacy by only removing filler words
6. Maintain strict verification protocols for determinacy requirements
7. Build comprehensive terminology indices with both positive and negative definitions
8. Implement active context management for all multi-step processes
9. Create automatic checkpoints to enable seamless recovery from interruptions
10. Maintain chronological integrity across all operations
11. Check for personal notes when lecture transcripts are unavailable
12. Always perform content existence checks before generating new content
13. Apply section markers to all complex files
14. Use content fingerprinting to avoid redundant generation
15. Reference source files in all index entries

## 14. Extension and Modification System

### 14.1 Adding New Modes

To add a new mode:
1. Create new .clinerules-philosophy-[mode-name] file
2. Implement all required components
3. Define handoff protocols for all relevant mode transitions
4. Ensure compatibility with chronological management
5. Implement evidence standards and verification
6. Define mode-specific workflows
7. Implement active context management
8. Define conceptual determinacy protocols
9. Implement content efficiency strategies

### 14.2 Modifying Existing Modes

To modify an existing mode:
1. Maintain backward compatibility with other modes
2. Update all affected handoff protocols
3. Ensure chronological management remains consistent
4. Document changes in version history
5. Update related modes if necessary
6. Update active context management if workflow changes

### 14.3 Cross-Mode Updates

For system-wide changes:
1. Update chronological_index.md structure across all modes
2. Modify handoff_protocols in all affected modes
3. Update evidence_standards across all modes
4. Ensure file naming and folder structure compatibility
5. Test all mode transitions
6. Update active context management system
