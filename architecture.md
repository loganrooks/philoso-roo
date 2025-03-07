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

### 1.2 Core Architectural Principles

1. **Chronological Integrity**: All modes enforce strict chronological progression through course material
2. **Evidence Standards**: All modes require explicit textual/source evidence for interpretations, with extensive direct quotations
3. **Conceptual Determinacy**: All analyses define concepts both positively and negatively to achieve precise determination
4. **Disambiguation Requirements**: All potentially ambiguous terms must be explicitly disambiguated from both ordinary language and related philosophical usages
5. **Active Context Management**: All modes maintain persistent state through dated context files to enable seamless resumption
6. **Cycle Completion**: Analysis cycles must be completed for each date before progression
7. **Date Specificity**: All files and analyses are explicitly tied to specific dates
8. **Shared Memory Model**: All modes access and maintain a common memory structure
9. **Verification Protocols**: All modes implement rigorous verification steps
10. **Standardized Handoffs**: All inter-mode transitions follow consistent protocols

### 1.3 System-Wide Memory Model

The system uses a unified memory management approach across all modes:

- **Chronological Index**: Central source of truth for course progression
- **Date-Specific Files**: Named consistently using [DATE] format
- **Concept/Argument Indices**: Shared across all modes for consistent tracking
- **Active Context Files**: Persistent state management for resuming interrupted analyses
- **Handoff Context**: Standardized format for mode transitions
- **Workspace Structure**: Common folder organization across modes
- **Terminology Database**: Shared repository of determinate concept definitions

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

analysis_tools: [templates for file creation]

workflows:
  default: [standard workflow sequence]
  specialized: [optional workflows]

instructions: [operational guidelines]

memory_bank_implementation:
  status_prefix: "[MEMORY BANK: ACTIVE][MODE-PREFIX]"
  context_management: [loading priorities]

handoff_protocols: [mode transition protocols]

cycle_management:
  full_cycle_definition: [mode's place in analysis cycle]
  enforcement: [cycle completion requirements]
  progression_rules: [chronological rules]
  
active_context_management:
  checkpoint_triggers: [list of checkpoint events]
  resumption_protocol: [steps for resuming analysis]
  multi_part_progression: [handling multi-part content]
```

### 2.2 Optional Components

```yaml
error_prevention: [error detection and handling]
real_time_updates: [status reporting structure]
extensibility: [modification protocols]
workflow_extensions: [custom workflow handling]
prerequisite_management: [prerequisite categorization and handling]
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

## Course Schedule and Cycle Status
| Date | Topic | Pre-Lecture | Class Analysis | Integration | Cycle Status |
|------|-------|-------------|---------------|------------|--------------|
[SCHEDULE_ROWS]
```

### 3.2 Analysis Cycle Definition

The standard full analysis cycle is:
1. **Pre-lecture analysis** (required)
2. **Class analysis** (required)
3. **Secondary literature review** (optional)
4. **Dialectical analysis** (optional)
5. **Integration** (optional)

### 3.3 Chronological Enforcement Rules

1. Analysis must proceed in strict chronological order
2. Pre-lecture for date N+1 cannot begin until class analysis for date N is complete
3. When initializing a new workspace, must start with earliest course date
4. All modes must verify chronological integrity before operations
5. Chronological violations must be blocked with clear error messages
6. Active contexts must be date-specific and enforce chronological integrity

## 4. Memory Management System

### 4.1 Standard Workspace Structure

```
analysis_workspace/
├── prelecture/                 # Pre-lecture analyses
├── lectures/                   # Lecture analyses
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
├── analysis_logs/              # Analysis tracking
│   ├── chronological_index.md  # Master schedule
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

### 4.3 Context Loading Priority System

All modes must implement a consistent priority loading system:

```yaml
context_files:
  high_priority:
    - "analysis_logs/chronological_index.md"  # ALWAYS first
    - "analysis_logs/active_contexts/[MODE]/[DATE]_active_context.md"  # ALWAYS second
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
6. Explicit rejection protocol for invalid handoffs

### 5.3 Standard Handoff Protocol Implementation

```yaml
handoff_protocols:
  to_[target_mode]:
    preparation: |
      1. Extract CURRENT_TARGET_DATE from chronological_index.md
      2. Verify [prerequisite] is complete
      3. Ensure active context is properly checkpointed
      4. Create handoff/handoff_context.md with:
         - EXPLICIT statement: "Target date: [CURRENT_TARGET_DATE]"
         - Clear instruction to continue with SAME date
         - Active context file location and status
      5. Update chronological_index.md with transition status
      6. REQUIRE explicit confirmation of target date understanding
    context_transfer:
      files:
        - "analysis_logs/chronological_index.md"
        - "handoff/handoff_context.md"
        - "analysis_logs/active_contexts/[MODE]/[DATE]_active_context.md"
      summary_description: "Clear description of handoff purpose for [DATE]"
  
  from_[source_mode]:
    preparation: |
      1. Load handoff context and EXPLICITLY extract target date
      2. VERIFY this matches expected chronological progression
      3. Verify required files exist
      4. Load active context file if present
      5. Initialize workspace for THIS SPECIFIC date
      6. REJECT handoff if date inconsistency detected
      7. CONFIRM receipt of correct date context
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
        4. [workflow implementation steps]
        5. Create checkpoints at key progress points
        6. Update active context with completion status
        7. Update chronological_index.md with completion status
      completion_behavior: |
        1. Finalize active context with completion status
        2. Report completion status for specific date
        3. Recommend next appropriate workflow
```

### 6.2 Prerequisite Management

```yaml
prerequisite_management:
  categorization:
    necessary:
      description: "Prerequisites required for logical progression"
    
    optional:
      description: "Prerequisites that enhance quality but aren't required"
```

### 6.3 Workflow Completion Behavior

All workflows must implement these completion behaviors:

1. Report specific date in completion message
2. Update chronological index with completion status
3. Finalize active context with completion status
4. Provide clear next step recommendations
5. Verify prerequisites before progression
6. Catch and handle errors appropriately

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
    - "Analysis must use complete paragraphs, not bullet points, for all substantive content"
  
  verification_workflow:
    enabled: true
    coverage_threshold: 90%
    quote_requirement_threshold: 75%
    confidence_assessment_required: true
    negative_definition_required: true
    disambiguation_required: true
    bullet_point_maximum: 3  # Maximum consecutive bullet points allowed
```

### 7.2 Mode-Specific Evidence Standards

- **Pre-lecture mode**: Page/section references for readings with extensive quotations
- **Class-analysis mode**: Timestamp/section references for lectures with transcribed quotes
- **Secondary-lit mode**: Page numbers and proper citations for scholarly sources with direct quotations
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
       - Verify analyses use complete paragraphs, not just bullet points
    2. Calculate evidence coverage and quotation percentages
    3. Flag sections below threshold
    4. Block completion if evidence standards not met
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

### Negative Determination
[WHAT_THE_TERM_IS_NOT]

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
```

## 9. Active Context Management System

### 9.1 Active Context File Structure

Each mode must maintain a date-specific active context file with this structure:

```markdown
# Active Context: [DATE] [ANALYSIS_TYPE]
Last Updated: [TIMESTAMP]
Status: [IN_PROGRESS/PAUSED/COMPLETED]

## Current Position
- Reading: [CURRENT_READING_TITLE]
- Section: [CURRENT_SECTION]
- Progress: [PERCENTAGE_COMPLETE]
- Last Analyzed Point: [SPECIFIC_REFERENCE]

## Readings Queue
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
  
  checkpoint_process: |
    1. Save current analysis state to active context file
    2. Update progress tracking metrics
    3. Generate resumption instructions
    4. Record timestamp and specific position
    5. Update pending determinations list
  
  resumption_protocol: |
    1. Load most recent active context file for target date
    2. Validate chronological integrity
    3. Present clear resumption point with specific reference
    4. Reload relevant context from checkpoint position
    5. Present pending determinations requiring attention
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

**Implementation Requirements**:
```yaml
active_context_implementation:
  active_context_location: "analysis_logs/active_contexts/prelecture/"
  checkpoint_frequency: 
    - after_each_section
    - after_each_determination
    - every_15_minutes
  resumption_protocol:
    required_context:
      - current_position_with_quote
      - pending_determinations
      - concepts_in_progress
```

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

**Key Workflows**:
1. Initialize class analysis or resume from active context
2. Analyze lecture with extensive quotation
3. Extract concepts and arguments with both positive and negative determination
4. Document terminology clarifications and disambiguation from lecture
5. Contrast lecturer's usage with alternative interpretations
6. Update active context with checkpoint after each major section
7. Integrate with course
8. Prepare for next cycle

**Quotation Requirements**:
- Timestamp references for all significant points
- Transcription of key definitions and explanations
- Documentation of lecturer's own disambiguation efforts
- Tracking of terminology consistency/inconsistency across lectures

**Handoff Protocols**:
- FROM pre-lecture
- TO pre-lecture (next date)
- TO secondary-lit (optional)
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

**Key Workflows**:
1. Initialize secondary lit workspace or resume from active context
2. Assess available materials
3. Analyze secondary sources with extensive quotation
4. Map scholarly debates with determinate concept use
5. Create disambiguation notes for key terminology
6. Update active context after each source analysis
7. Integrate scholarly perspectives with primary texts

**Handoff Protocols**:
- FROM pre-lecture
- FROM class-analysis
- FROM essay-prep
- TO text-processing
- TO class-analysis
- TO dialectical-analysis
- TO essay-prep

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

**Key Workflows**:
1. Initialize dialectical workspace or resume from active context
2. Identify contradictions with textual evidence
3. Map dialectical moments with determinacy
4. Analyze transitions with direct quotation
5. Update active context after each dialectical moment
6. Synthesize resolutions with determinate articulation

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

## 11. Implementation Guidelines

The implementation of this architecture requires all modes to:

1. Prioritize determinate understanding over breadth of coverage
2. Enforce strict textual evidence requirements with extensive direct quotation
3. Implement templates that require both positive and negative determination
4. Mandate disambiguation of potentially ambiguous terminology
5. Reject analyses that rely on bullet points or ambiguous language
6. Maintain strict verification protocols for determinacy requirements
7. Build comprehensive terminology indices with both positive and negative definitions
8. Implement active context management for all multi-step processes
9. Create automatic checkpoints to enable seamless recovery from interruptions
10. Maintain chronological integrity across all operations
11. Use complete paragraphs with determinate language for all substantive content

## 12. Extension and Modification System

### 12.1 Adding New Modes

To add a new mode:
1. Create new .clinerules-philosophy-[mode-name] file
2. Implement all required components
3. Define handoff protocols for all relevant mode transitions
4. Ensure compatibility with chronological management
5. Implement evidence standards and verification
6. Define mode-specific workflows
7. Implement active context management
8. Define conceptual determinacy protocols

### 12.2 Modifying Existing Modes

To modify an existing mode:
1. Maintain backward compatibility with other modes
2. Update all affected handoff protocols
3. Ensure chronological management remains consistent
4. Document changes in version history
5. Update related modes if necessary
6. Update active context management if workflow changes

### 12.3 Cross-Mode Updates

For system-wide changes:
1. Update chronological_index.md structure across all modes
2. Modify handoff_protocols in all affected modes
3. Update evidence_standards across all modes
4. Ensure file naming and folder structure compatibility
5. Test all mode transitions
6. Update active context management system