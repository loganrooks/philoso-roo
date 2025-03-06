# Document 1: Philosophy Analysis System Architecture

## 1. System Overview

### 1.1 Purpose and Design Philosophy

The Philosophy Analysis System is an integrated suite of specialized modes designed to support comprehensive philosophical analysis throughout a course's chronological progression. The system enables:

- Chronologically-aware analysis that respects the developmental sequence of course material
- Evidence-based interpretation with rigorous textual/lecture references
- Seamless transitions between different types of analytical work
- Comprehensive documentation of philosophical concepts, arguments, and their evolution

### 1.2 Core Architectural Principles

1. **Chronological Integrity**: All modes enforce strict chronological progression through course material
2. **Evidence Standards**: All modes require explicit textual/source evidence for interpretations
3. **Cycle Completion**: Analysis cycles must be completed for each date before progression
4. **Date Specificity**: All files and analyses are explicitly tied to specific dates
5. **Shared Memory Model**: All modes access and maintain a common memory structure
6. **Verification Protocols**: All modes implement rigorous verification steps
7. **Standardized Handoffs**: All inter-mode transitions follow consistent protocols

### 1.3 System-Wide Memory Model

The system uses a unified memory management approach across all modes:

- **Chronological Index**: Central source of truth for course progression
- **Date-Specific Files**: Named consistently using [DATE] format
- **Concept/Argument Indices**: Shared across all modes for consistent tracking
- **Handoff Context**: Standardized format for mode transitions
- **Workspace Structure**: Common folder organization across modes

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
  initialization_checks: [list of startup verification steps]

memory_management:
  workspace: [folder structure]
  context_files: [priority loading structure]
  indexing: [file format definitions]

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
```

### 2.2 Optional Components

```yaml
error_prevention: [error detection and handling]
real_time_updates: [status reporting structure]
extensibility: [modification protocols]
workflow_extensions: [custom workflow handling]
prerequisite_management: [prerequisite categorization and handling]
evidence_standards: [mode-specific evidence requirements]
verification_protocol: [content verification steps]
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

## 4. Memory Management System

### 4.1 Standard Workspace Structure

```
analysis_workspace/
├── prelecture/                 # Pre-lecture analyses
├── lectures/                   # Lecture analyses
├── concepts/                   # Concept tracking
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
├── handoff/                    # Mode transition documents
```

### 4.2 File Naming Conventions

- **Date-specific files**: Always use `[DATE]_[type].md` format (e.g., `Jan07_analysis.md`)
- **Concept files**: Use `[CONCEPT_NAME].md` format
- **Argument files**: Use `[ARGUMENT_NAME].md` format
- **Version tracking**: Use `v[VERSION]` for versioned files (e.g., `thesis_v2.md`)
- **Handoff files**: Use `[FROM_MODE]_to_[TO_MODE]_context.md`

### 4.3 Context Loading Priority System

All modes must implement a consistent priority loading system:

```yaml
context_files:
  high_priority:
    - "analysis_logs/chronological_index.md"  # ALWAYS first
    - "[MODE-SPECIFIC]/[DATE]_[TYPE].md"      # Current date files
  medium_priority:
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

## Completion Status
[COMPLETION_STATUS]

## Required Context
[REQUIRED_CONTEXT]

## Required Follow-up
[REQUIRED_FOLLOWUP]
```

### 5.2 Handoff Verification Requirements

All handoffs must include these verification steps:

1. Explicit date reference in both sending and receiving modes
2. Date consistency check between handoff and chronological index
3. Required file existence verification
4. Completion status verification
5. Explicit rejection protocol for invalid handoffs

### 5.3 Standard Handoff Protocol Implementation

```yaml
handoff_protocols:
  to_[target_mode]:
    preparation: |
      1. Extract CURRENT_TARGET_DATE from chronological_index.md
      2. Verify [prerequisite] is complete
      3. Create handoff/handoff_context.md with:
         - EXPLICIT statement: "Target date: [CURRENT_TARGET_DATE]"
         - Clear instruction to continue with SAME date
      4. Update chronological_index.md with transition status
      5. REQUIRE explicit confirmation of target date understanding
    context_transfer:
      files:
        - "analysis_logs/chronological_index.md"
        - "[mode-specific]/[DATE]_[type].md"
        - "handoff/handoff_context.md"
      summary_description: "Clear description of handoff purpose for [DATE]"
  
  from_[source_mode]:
    preparation: |
      1. Load handoff context and EXPLICITLY extract target date
      2. VERIFY this matches expected chronological progression
      3. Verify required files exist
      4. Initialize workspace for THIS SPECIFIC date
      5. REJECT handoff if date inconsistency detected
      6. CONFIRM receipt of correct date context
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
        2. [implementation steps]
        3. Update chronological_index.md with completion status
      completion_behavior: |
        1. Report completion status for specific date
        2. Recommend next appropriate workflow
```

### 6.2 Prerequisite Management

```yaml
prerequisite_management:
  categorization:
    necessary:
      description: "Prerequisites required for logical progression"
      handling: |
        1. Auto-execute without user confirmation
        2. Block further progress until complete
        3. Report automatic execution with rationale
      examples:
        - "Previous date's class analysis"
        - "Pre-lecture analysis for current date"
    
    optional:
      description: "Prerequisites that enhance quality but aren't required"
      handling: |
        1. Present clear benefits of completion
        2. Request explicit user decision
        3. Document decision in logs
      examples:
        - "Secondary literature review"
        - "Deeper hermeneutic reading"
```

### 6.3 Workflow Completion Behavior

All workflows must implement these completion behaviors:

1. Report specific date in completion message
2. Update chronological index with completion status
3. Provide clear next step recommendations
4. Verify prerequisites before progression
5. Catch and handle errors appropriately

## 7. Evidence Standards System

### 7.1 Cross-Mode Evidence Requirements

All modes must implement these minimum evidence standards:

```yaml
evidence_standards:
  requirements:
    - "All interpretations must reference specific text/lecture sections"
    - "Major concepts require direct quotes with proper citation"
    - "Interpretations must include confidence assessment"
    - "Complex passages require documentation of alternative readings"
  
  verification_workflow:
    enabled: true
    coverage_threshold: 90%
    quote_requirement_threshold: 75%
    confidence_assessment_required: true
```

### 7.2 Mode-Specific Evidence Standards

- **Pre-lecture mode**: Page/section references for readings
- **Class-analysis mode**: Timestamp/section references for lectures
- **Secondary-lit mode**: Page numbers and proper citations for scholarly sources
- **Dialectical-analysis mode**: Explicit textual evidence for dialectical moments
- **Essay-prep mode**: Proper source attribution for all claims

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
    2. Calculate evidence coverage percentages
    3. Flag sections below threshold
    4. Block completion if evidence standards not met
```

## 8. Mode-Specific Responsibilities

### 8.1 Pre-Lecture Mode

**Primary Role**: Analyze course readings before lectures
**Key Responsibilities**:
- Identify key passages, concepts, and arguments in readings
- Generate questions for upcoming lecture
- Develop hypotheses about concepts and arguments
- Prepare for lecture comprehension

**Key Workflows**:
1. Initialize chronological tracking
2. Analyze lecture materials
3. Evidence verification check
4. Prepare for class analysis

**Handoff Protocols**:
- TO class-analysis (primary)
- TO secondary-lit (optional)

### 8.2 Class-Analysis Mode

**Primary Role**: Analyze lecture content and relate to readings
**Key Responsibilities**:
- Analyze lecture concepts and arguments
- Compare with pre-lecture expectations
- Extract and track concept development
- Integrate with course themes
- Identify research needs

**Key Workflows**:
1. Initialize class analysis
2. Analyze lecture
3. Extract concepts and arguments
4. Integrate with course
5. Prepare for next cycle

**Handoff Protocols**:
- FROM pre-lecture
- TO pre-lecture (next date)
- TO secondary-lit (optional)
- TO dialectical-analysis (optional)
- TO essay-prep (optional)

### 8.3 Secondary-Literature Mode

**Primary Role**: Research scholarly perspectives on course topics
**Key Responsibilities**:
- Analyze scholarly interpretations of primary texts
- Map scholarly debates and competing perspectives
- Provide historical context for concepts
- Build bibliographies
- Relate scholarly insights to course materials

**Key Workflows**:
1. Initialize secondary lit workspace
2. Assess available materials
3. Analyze secondary sources
4. Map scholarly debates
5. Integrate scholarly perspectives

**Handoff Protocols**:
- FROM pre-lecture
- FROM class-analysis
- FROM essay-prep
- TO text-processing
- TO class-analysis
- TO dialectical-analysis
- TO essay-prep

### 8.4 Dialectical-Analysis Mode

**Primary Role**: Analyze philosophical concepts through dialectical movement
**Key Responsibilities**:
- Identify dialectical contradictions in concepts
- Map dialectical moments in concept development
- Analyze transitions between dialectical moments
- Synthesize dialectical resolutions
- Create visualizations of dialectical movement

**Key Workflows**:
1. Initialize dialectical workspace
2. Identify contradictions
3. Map dialectical moments
4. Analyze transitions
5. Synthesize resolutions

**Handoff Protocols**:
- FROM class-analysis
- FROM secondary-lit
- FROM essay-prep
- TO class-analysis
- TO secondary-lit
- TO essay-prep

### 8.5 Essay-Prep Mode

**Primary Role**: Develop philosophical essays from conception to draft
**Key Responsibilities**:
- Analyze essay prompts
- Develop and refine thesis statements
- Map arguments supporting theses
- Create outlines and drafts
- Integrate course materials chronologically
- Compile and manage bibliographies

**Key Workflows**:
1. Initialize essay project
2. Analyze essay prompt
3. Develop thesis
4. Map arguments
5. Create outline
6. Create draft

**Handoff Protocols**:
- FROM class-analysis
- FROM secondary-lit
- FROM dialectical-analysis
- TO secondary-lit
- TO dialectical-analysis
- TO class-analysis

### 8.6 Text-Processing Mode

**Primary Role**: Process and chunk texts into manageable units
**Key Responsibilities**:
- Analyze text structure to determine chunking strategy
- Divide texts into semantically meaningful chunks
- Create hierarchical indices for text navigation
- Generate semantic indices by concept and argument
- Facilitate selective context loading

**Key Workflows**:
1. Analyze text structure
2. Process text into chunks
3. Generate semantic indices
4. Create cross-references

**Handoff Protocols**:
- FROM secondary-lit
- FROM pre-lecture
- TO secondary-lit
- TO pre-lecture
- TO class-analysis

## 9. Extension and Modification System

### 9.1 Adding New Modes

To add a new mode:
1. Create new .clinerules-philosophy-[mode-name] file
2. Implement all required components
3. Define handoff protocols for all relevant mode transitions
4. Ensure compatibility with chronological management
5. Implement evidence standards and verification
6. Define mode-specific workflows

### 9.2 Modifying Existing Modes

To modify an existing mode:
1. Maintain backward compatibility with other modes
2. Update all affected handoff protocols
3. Ensure chronological management remains consistent
4. Document changes in version history
5. Update related modes if necessary

### 9.3 Cross-Mode Updates

For system-wide changes:
1. Update chronological_index.md structure across all modes
2. Modify handoff_protocols in all affected modes
3. Update evidence_standards across all modes
4. Ensure file naming and folder structure compatibility
5. Test all mode transitions