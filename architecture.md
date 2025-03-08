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

## 2. Standard Mode Structure

### 2.1 Required Components

Every mode configuration file (.clinerules) must include these sections:

```yaml
mode: philosophy-[mode-name]
description: "Concise description of mode purpose"
version: "x.y.z"

capabilities:
  allowed_tools: [list of approved tools]

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

analysis_tools: [templates for file creation]

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

### 2.2 Optional Components

```yaml
error_prevention: [error detection and handling]
real_time_updates: [status reporting structure]
extensibility: [modification protocols]
workflow_extensions: [custom workflow handling]
prerequisite_management: [prerequisite categorization and handling]
materials_availability: [protocols for handling missing materials]
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
```

### 4.2 File Naming Conventions

- **Date-specific files**: Always use `[DATE]_[type].md` format (e.g., `Jan07_analysis.md`)
- **Concept files**: Use `[CONCEPT_NAME].md` format
- **Argument files**: Use `[ARGUMENT_NAME].md` format
- **Active context files**: Use `[DATE]_active_context.md` format
- **Version tracking**: Use `v[VERSION]` for versioned files (e.g., `thesis_v2.md`)
- **Handoff files**: Use `[FROM_MODE]_to_[TO_MODE]_context.md`
- **Substitution files**: Use `[DATE]_[type]_substitute.md` format

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

### 4.4 Materials Availability Tracking

The system tracks the availability of lecture materials in `analysis_logs/materials_status.md`:

```markdown
# Materials Availability Status

## Current Status
**Date:** [CURRENT_TARGET_DATE]
**Lecture Transcript:** [AVAILABLE/MISSING]
**Lecture Notes:** [AVAILABLE/PARTIAL/MISSING]
**Note Quality Assessment:** [DESCRIPTION]
**Secondary Sources:** [AVAILABLE/NEEDED/PENDING]

## Materials Availability by Date
| Date | Transcript | Notes | Notes Quality | Secondary Sources | Action Required |
|------|------------|-------|--------------|-------------------|----------------|
[STATUS_ROWS]
```

## 5. Handoff Protocol System

### 5.1 Standard Handoff Format

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

### 5.2 Handoff Verification Requirements

All handoffs must include these verification steps:

1. Explicit date reference in both sending and receiving modes
2. Date consistency check between handoff and chronological index
3. Required file existence verification
4. Completion status verification
5. Active context status verification
6. Materials availability verification
7. Explicit rejection protocol for invalid handoffs

### 5.3 Standard Handoff Protocol Implementation

```yaml
handoff_protocols:
  to_[target_mode]:
    preparation: |
      1. Extract CURRENT_TARGET_DATE from chronological_index.md
      2. Verify [prerequisite] is complete
      3. Ensure active context is properly checkpointed
      4. Check materials availability status
      5. Create handoff/handoff_context.md with:
         - EXPLICIT statement: "Target date: [CURRENT_TARGET_DATE]"
         - Clear instruction to continue with SAME date
         - Active context file location and status
         - Materials availability status
      6. Update chronological_index.md with transition status
      7. REQUIRE explicit confirmation of target date understanding
    context_transfer:
      files:
        - "analysis_logs/chronological_index.md"
        - "analysis_logs/materials_status.md"
        - "handoff/handoff_context.md"
        - "analysis_logs/active_contexts/[MODE]/[DATE]_active_context.md"
      summary_description: "Clear description of handoff purpose for [DATE]"
  
  from_[source_mode]:
    preparation: |
      1. Load handoff context and EXPLICITLY extract target date
      2. VERIFY this matches expected chronological progression
      3. Verify required files exist
      4. Check materials availability status
      5. Load active context file if present
      6. Initialize workspace for THIS SPECIFIC date
      7. REJECT handoff if date inconsistency detected
      8. CONFIRM receipt of correct date context
```

### 5.4 Special Case Handoffs

#### 5.4.1 Missing Lecture Substitution Handoff

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
      context_transfer:
        files:
          - "analysis_logs/chronological_index.md"
          - "analysis_logs/materials_status.md"
          - "handoff/handoff_context.md"
          - "prelecture/[DATE]_analysis.md"
          - "lectures/notes/[DATE]_notes.md" # If available
          - "concepts/terminology_index.md"
          - "analysis_logs/active_contexts/class_analysis/[DATE]_active_context.md"
        summary_description: "Class analysis for [DATE] requires secondary literature substitution due to missing lecture materials"
    
    to_secondary_lit:
      preparation: |
        1. Load handoff context and EXPLICITLY extract target date
        2. VERIFY handoff contains "SUBSTITUTION MODE" marker
        3. Load pre-lecture analysis and expectations
        4. Load lecture notes if available
        5. Initialize secondary literature workspace with SUBSTITUTION flag
        6. Load recommended sources if provided
        7. Mark active context as "SUBSTITUTION_MODE: TRUE"
      completion_behavior: |
        1. On completion, mark cycle as "Complete (Substitution)" in chronological_index.md
        2. Allow progression to next date's pre-lecture analysis
        3. Generate special notation in concept indices about determination source
```

## 6. Workflow Management System

### 6.1 Standard Workflow Structure

```yaml
workflows:
  default:
    - name: [workflow_name]
      description: "Clear description of workflow purpose"
      prerequisites:
        - type: "workflow_completed"
          workflow: "[prerequisite_workflow]"
          required: true
      implementation: |
        1. Extract CURRENT_TARGET_DATE from chronological_index.md
        2. Check for existing active context for target date
        3. If exists: Resume from active context
           If not: Initialize new active context
        4. Check materials availability status
        5. [workflow implementation steps]
        6. Create checkpoints at key progress points
        7. Update active context with completion status
        8. Update chronological_index.md with completion status
        9. Update materials_status.md if needed
      completion_behavior: |
        1. Finalize active context with completion status
        2. Report completion status for specific date
        3. Recommend next appropriate workflow
```

### 6.2 Alternative Workflows for Missing Materials

```yaml
workflows:
  alternative:
    - name: handle_missing_lecture_transcript
      description: "Process for handling missing lecture transcript"
      trigger: "lecture_transcript_missing"
      implementation: |
        1. Extract CURRENT_TARGET_DATE from chronological_index.md
        2. Update materials_status.md with MISSING status
        3. Check for lecture notes availability
        4. If notes available:
           - Assess quality and completeness of notes
           - If notes are sufficient:
             - Proceed with limited class analysis
             - Flag all conclusions as note-based with lower confidence
           - If notes are insufficient:
             - Recommend secondary literature substitution
        5. If notes unavailable:
           - Initialize secondary literature substitution process
           - Generate source recommendations based on pre-lecture
           - Create substitution handoff to secondary-lit mode
```

### 6.3 Prerequisite Management

```yaml
prerequisite_management:
  categorization:
    necessary:
      description: "Prerequisites required for logical progression"
    
    optional:
      description: "Prerequisites that enhance quality but aren't required"
```

### 6.4 Cycle Completion Exceptions

The system recognizes the following valid exceptions to standard cycle completion:

#### 6.4.1 Secondary Literature Substitution for Missing Lecture

When a lecture transcript is unavailable:
1. The chronological index will mark the cycle as "Complete (Substitution)"
2. The system will accept this as valid cycle completion
3. Progression to the next date's pre-lecture analysis is permitted
4. Concept determinations from substitution are marked with source type

This exception preserves chronological progression while accommodating practical limitations of material availability.

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

### 7.2 Mode-Specific Evidence Standards

- **Pre-lecture mode**: Page/section references for readings with extensive quotations
- **Class-analysis mode**: Timestamp/section references for lectures with transcribed quotes
- **Class-analysis with notes only**: Note references with clear indication of lower confidence
- **Secondary-lit mode**: Page numbers and proper citations for scholarly sources with direct quotations
- **Secondary-lit as substitute**: Higher quotation threshold and explicit mapping to pre-lecture expectations
- **Dialectical-analysis mode**: Explicit textual evidence for dialectical moments, including quotations showing transitions
- **Essay-prep mode**: Proper source attribution with direct quotation for all claims

### 7.3 Evidence Verification Protocol

All modes must implement this verification process:

```yaml
verification_protocol:
  implementation: |
    1. For all analysis files:
       - Verify references are complete and specific
       - Check for required quotations for major points
       - Validate interpretive confidence assessments
       - Ensure alternative readings for complex passages
       - Verify each key concept includes negative determination
       - Check disambiguation of potentially ambiguous terms
       - Validate contrast between author's usage and ordinary language
       - Verify bullet points maintain determinacy and only remove filler words
       - Check that bullet points preserve required depth and detail
    2. Calculate evidence coverage and quotation percentages
    3. Flag sections below threshold
    4. Block completion if evidence standards not met
```

### 7.4 Bullet Point Usage Guidelines

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

### 7.5 Evidence Standards for Alternative Materials

When primary materials (lecture transcripts) are unavailable:

```yaml
alternative_materials_evidence:
  lecture_notes:
    confidence_marker: "Note-based interpretation (lower confidence)"
    requirements:
      - Clear indication of note limitations
      - Explicit marking of interpretive leaps
      - Higher reliance on pre-lecture material for stability
      - Lower confidence assessments for determinations
    verification:
      - Flag all determinations as note-based
      - Require explicit confidence qualifiers
      - Higher threshold for pre-lecture integration
  
  secondary_literature_substitute:
    confidence_marker: "Secondary source substitution for lecture"
    requirements:
      - Multiple scholarly sources for each determination
      - Explicit mapping to pre-lecture expectations
      - Clear source attribution for all determinations
      - Comparative analysis of scholarly perspectives
    verification:
      - Track source coverage of expected lecture topics
      - Flag determinations as scholarly-based
      - Higher quotation threshold (85%)
      - Require explicit comparison to pre-lecture hypotheses
```

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

### 8.2 Ambiguity Detection Protocol

```yaml
ambiguity_detection:
  protocol: |
    1. Maintain running list of potentially ambiguous philosophical terms
    2. For each text analysis, scan for these terms
    3. Flag each instance requiring disambiguation
    4. Apply mandatory disambiguation process to each flagged term
    5. Update master terminology index with new determinations
  
  common_ambiguous_terms:
    - structure
    - necessity
    - universal
    - ideal
    - material
    - concept
    - being
    - essence
    - relation
    - dialectic
    - determination
    - absolute
    - abstraction
    - concrete
    - negation
    - sublation
```

### 8.3 Determination Template

All analyses must use this template for key philosophical terms:

```markdown
## Term: [PHILOSOPHICAL_TERM]

### Direct Textual Evidence
> "[DIRECT_QUOTE_1]" ([SOURCE], [PAGE/TIMESTAMP])

> "[DIRECT_QUOTE_2]" ([SOURCE], [PAGE/TIMESTAMP])

### Positive Determination
[EXPLICIT_DEFINITION]
Note: Can use bullet points to remove filler while maintaining determinacy

### Negative Determination
[WHAT_THE_TERM_IS_NOT]
Note: Can use bullet points to remove filler while maintaining determinacy

### Distinction from Ordinary Usage
[HOW_TERM_DIFFERS_FROM_COMMON_USAGE]

### Potential Misinterpretations
1. [MISINTERPRETATION_1]
   - Why this is incorrect: [EXPLANATION]
   - Textual evidence against: "[QUOTE]"

2. [MISINTERPRETATION_2]
   - Why this is incorrect: [EXPLANATION]
   - Textual evidence against: "[QUOTE]"

### Related Terms Requiring Distinction
- [RELATED_TERM_1]: [HOW_IT_DIFFERS]
- [RELATED_TERM_2]: [HOW_IT_DIFFERS]

### Source Type
[PRIMARY_LECTURE/NOTE_BASED/SECONDARY_SUBSTITUTE]
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

### 9.2 Checkpoint System

```yaml
checkpoint_system:
  automatic_triggers:
    - after_section_completion
    - after_concept_determination
    - after_reading_completion
    - time_based: 15_minutes
    - before_mode_switching
    - after_materials_status_change
  
  checkpoint_process: |
    1. Save current analysis state to active context file
    2. Update progress tracking metrics
    3. Generate resumption instructions
    4. Record timestamp and specific position
    5. Update pending determinations list
    6. Update materials availability status
  
  resumption_protocol: |
    1. Load most recent active context file for target date
    2. Validate chronological integrity
    3. Present clear resumption point with specific reference
    4. Reload relevant context from checkpoint position
    5. Present pending determinations requiring attention
    6. Update materials status if needed
```

### 9.3 Multi-Reading Management

```yaml
multi_reading_management:
  reading_queue_management: |
    1. Initialize ordered list of readings for target date
    2. Track status of each reading (Complete/In-Progress/Pending)
    3. Enforce sequential progression through readings
    4. Update active context file after each reading completion
    5. Maintain cross-reading concept references
  
  reading_transition_process: |
    1. Complete final checkpoint for current reading
    2. Generate reading summary with key determinations
    3. Identify concepts requiring further development
    4. Update reading status in queue
    5. Initialize context for next reading
```

### 9.4 Specialized Active Context Types

#### 9.4.1 Substitution Mode Context

When secondary literature substitutes for class analysis, the active context includes:

```markdown
# Active Context: [DATE] [SECONDARY_LIT_AS_CLASS_SUBSTITUTE]
Last Updated: [TIMESTAMP]
Status: [IN_PROGRESS/PAUSED/COMPLETED]
Substitution Mode: TRUE

## Missing Materials
- Type: Lecture Transcript
- Date: [DATE]
- Topic: [TOPIC]
- Lecture Notes: [AVAILABLE/PARTIAL/MISSING]
- Note Quality Assessment: [DESCRIPTION]

## Substitution Sources
1. [SOURCE_1] - Status: [COMPLETE/IN_PROGRESS/PENDING]
   - Relevance: [EXPLANATION]
   - Coverage: [TOPICS_COVERED]
2. [SOURCE_2] - Status: [COMPLETE/IN_PROGRESS/PENDING]
   - Relevance: [EXPLANATION]
   - Coverage: [TOPICS_COVERED]

## Required Coverage from Pre-Lecture
[LIST_OF_CONCEPTS_AND_ARGUMENTS_NEEDING_COVERAGE]

## Available Lecture Notes
[SUMMARY_OF_AVAILABLE_NOTES_IF_ANY]

## Progress Tracking
- Concepts Determined: [X]/[TOTAL]
- Arguments Analyzed: [X]/[TOTAL]
- Pre-lecture Expectations Addressed: [X]/[TOTAL]

## Checkpoints
[STANDARD_CHECKPOINT_CONTENT]
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

**Key Workflows**:
1. Initialize chronological tracking
2. Initialize or resume active context for target date
3. Process readings sequentially with progress tracking
4. Analyze lecture materials with extensive quotation
5. Extract and define key terminology with negative determination
6. Document potentially ambiguous terms with determinate explanations
7. Implement automatic checkpointing during analysis
8. Update active context after each significant determination
9. Evidence verification check including quotation threshold verification
10. Prepare for class analysis

**Determination Protocol**:
- For each key concept, document:
  1. Direct quotations establishing the concept
  2. Explicit statement of what the concept IS NOT
  3. Contrast with ordinary language usage
  4. Potential misinterpretations to avoid
  5. Related concepts that should be distinguished

**Handoff Protocols**:
- TO class-analysis (primary)
- TO secondary-lit (optional)

### 10.2 Class-Analysis Mode

**Primary Role**: Analyze lecture content and relate to readings

**Key Responsibilities**:
- Analyze lecture concepts and arguments with extensive direct quotation
- Compare with pre-lecture expectations, noting clarifications of ambiguities
- Extract and track concept development with explicit determination
- Document shifts in terminology usage from readings to lecture
- Integrate with course themes
- Maintain active context for lecture analysis with position tracking
- Create checkpoints at major conceptual transitions in lecture
- Identify research needs
- Detect missing lecture materials and initiate appropriate alternative workflows
- Generate targeted recommendations for secondary sources based on pre-lecture content when needed
- Handle lecture notes when transcripts are unavailable, clearly marking confidence limitations
- Check for available personal notes from lectures and incorporate them as appropriate
- Create substitution workflows when both transcript and notes are insufficient

**Key Workflows**:
1. Initialize class analysis or resume from active context
2. Check lecture transcript availability
3. If transcript available:
   - Analyze lecture with extensive quotation
   - Extract concepts and arguments with both positive and negative determination
   - Document terminology clarifications and disambiguation from lecture
   - Contrast lecturer's usage with alternative interpretations
4. If transcript unavailable but notes available:
   - Analyze notes with clear confidence limitations
   - Extract concepts with appropriate confidence markers
   - Flag areas where notes are insufficient
5. If both transcript and notes insufficient:
   - Initiate secondary literature substitution
   - Generate source recommendations
   - Create specialized handoff
6. Update active context with checkpoint after each major section
7. Integrate with course
8. Prepare for next cycle

**Missing Materials Workflow**:
1. Check for lecture transcript availability
2. If missing, check for personal lecture notes
3. Assess note quality and coverage:
   - If sufficient: Proceed with notes-based analysis (flagging confidence limitations)
   - If insufficient: Initiate secondary literature substitution
4. Update materials_status.md with current status
5. Generate appropriate recommendations for alternate sources
6. Create specialized handoff with clear substitution instructions

**Quotation Requirements**:
- Timestamp references for all significant points
- Transcription of key definitions and explanations
- Documentation of lecturer's own disambiguation efforts
- Tracking of terminology consistency/inconsistency across lectures
- Clear marking of note-based interpretations when using personal notes

**Handoff Protocols**:
- FROM pre-lecture
- TO pre-lecture (next date)
- TO secondary-lit (optional or required for substitution)
- TO secondary-lit (substitution when lecture materials missing)
- TO dialectical-analysis (optional)
- TO essay-prep (optional)

### 10.3 Secondary-Literature Mode

**Primary Role**: Research scholarly perspectives on course topics

**Key Responsibilities**:
- Analyze scholarly interpretations of primary texts with extensive quotation
- Map scholarly debates and competing perspectives
- Provide historical context for concepts with determinate definitions
- Build bibliographies
- Relate scholarly insights to course materials
- Maintain active context for multi-part research projects
- Track progress through secondary literature with checkpoints
- Function as lecture analysis substitute when required
- Compare scholarly interpretations with lecture notes when appropriate
- Integrate available personal notes when functioning as a substitute
- Cover expected lecture content when functioning as a substitute

**Key Workflows**:
1. Initialize secondary lit workspace or resume from active context
2. Check if operating in standard or substitution mode
3. If standard mode:
   - Assess available materials
   - Analyze secondary sources with extensive quotation
   - Map scholarly debates with determinate concept use
4. If substitution mode:
   - Load pre-lecture expectations
   - Load available lecture notes if any
   - Target scholarly sources to fulfill class analysis objectives
   - Ensure coverage of expected lecture content
   - Create explicit substitution analysis
5. Create disambiguation notes for key terminology
6. Update active context after each source analysis
7. Integrate scholarly perspectives with primary texts

**Substitution Mode Workflow**:
1. Receive special handoff from class-analysis with substitute status
2. Load pre-lecture expectations and any available notes
3. Analyze recommended sources with focus on fulfilling class analysis objectives
4. Generate concept determinations and argument analyses comparable to lecture
5. Create special completion marking cycle as validly completed despite substitution
6. Mark all determinations with source attribution

**Handoff Protocols**:
- FROM pre-lecture
- FROM class-analysis
- FROM class-analysis (substitution mode)
- FROM essay-prep
- TO text-processing
- TO class-analysis
- TO dialectical-analysis
- TO essay-prep
- TO pre-lecture (next date, when functioning as class-analysis substitute)

### 10.4 Dialectical-Analysis Mode

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

**Key Workflows**:
1. Initialize dialectical workspace or resume from active context
2. Check materials availability status
3. Identify contradictions with textual evidence
4. Map dialectical moments with determinacy
5. Analyze transitions with direct quotation
6. Update active context after each dialectical moment
7. Synthesize resolutions with determinate articulation

**Handoff Protocols**:
- FROM class-analysis
- FROM secondary-lit
- FROM essay-prep
- TO class-analysis
- TO secondary-lit
- TO essay-prep

### 10.5 Essay-Prep Mode

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

**Key Workflows**:
1. Initialize essay project or resume from active context
2. Analyze essay prompt
3. Develop thesis with determinate concepts
4. Map arguments with textual evidence
5. Create outline with quotations
6. Update active context after each major component
7. Create draft with extensive quotation

**Handoff Protocols**:
- FROM class-analysis
- FROM secondary-lit
- FROM dialectical-analysis
- TO secondary-lit
- TO dialectical-analysis
- TO class-analysis

### 10.6 Text-Processing Mode

**Primary Role**: Process and chunk texts into manageable units

**Key Responsibilities**:
- Analyze text structure to determine chunking strategy
- Divide texts into semantically meaningful chunks
- Create hierarchical indices for text navigation
- Generate semantic indices by concept and argument
- Facilitate selective context loading
- Maintain active context for multi-part text processing
- Create checkpoints after each significant text section
- Process and organize lecture notes when transcripts are unavailable

**Key Workflows**:
1. Analyze text structure or resume from active context
2. Process text into chunks
3. Generate semantic indices
4. Create cross-references
5. Update active context after each chunk processing
6. Generate navigation markers

**Handoff Protocols**:
- FROM secondary-lit
- FROM pre-lecture
- TO secondary-lit
- TO pre-lecture
- TO class-analysis

## 11. Source Recommendation System

### 11.1 Automated Source Recommendations

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

## 12. Implementation Guidelines

The implementation of this architecture requires all modes to:

1. Prioritize determinate understanding over breadth of coverage
2. Enforce strict textual evidence requirements with extensive direct quotation
3. Implement templates that require both positive and negative determination
4. Mandate disambiguation of potentially ambiguous terminology
5. Allow bullet points that maintain determinacy by only removing filler words, but reject ambiguous language
6. Maintain strict verification protocols for determinacy requirements
7. Build comprehensive terminology indices with both positive and negative definitions
8. Implement active context management for all multi-step processes
9. Create automatic checkpoints to enable seamless recovery from interruptions
10. Maintain chronological integrity across all operations
11. Implement materials availability tracking and appropriate alternative workflows
12. Check for personal notes when lecture transcripts are unavailable
13. Use complete paragraphs or determinate bullet points that maintain depth, detail, and determinacy

## 13. Extension and Modification System

### 13.1 Adding New Modes

To add a new mode:
1. Create new .clinerules-philosophy-[mode-name] file
2. Implement all required components
3. Define handoff protocols for all relevant mode transitions
4. Ensure compatibility with chronological management
5. Implement evidence standards and verification
6. Define mode-specific workflows including alternatives for missing materials
7. Implement active context management
8. Define conceptual determinacy protocols

### 13.2 Modifying Existing Modes

To modify an existing mode:
1. Maintain backward compatibility with other modes
2. Update all affected handoff protocols
3. Ensure chronological management remains consistent
4. Document changes in version history
5. Update related modes if necessary
6. Update active context management if workflow changes

### 13.3 Cross-Mode Updates

For system-wide changes:
1. Update chronological_index.md structure across all modes
2. Modify handoff_protocols in all affected modes
3. Update evidence_standards across all modes
4. Ensure file naming and folder structure compatibility
5. Test all mode transitions
6. Update active context management system
7. Verify materials availability handling across all modes