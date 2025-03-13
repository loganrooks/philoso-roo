# [MEMORY BANK: INACTIVE]

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
- Cost-effective content generation through extraction-based token optimization strategies

### 1.2 Core Architectural Principles

1. **Determinacy**: All concept definitions must be both positively and negatively determined with explicit disambiguation
2. **Evidence**: All interpretations must be grounded in direct quotations from primary or secondary sources
3. **Chronological Integrity**: The system must maintain strict chronological progression in course analysis
4. **Context Persistence**: Active context must be maintained across sessions and modes
5. **Adaptability**: The system must adapt to missing materials while maintaining analytical rigor
6. **Verification**: All analyses must undergo systematic verification for evidence standards and conceptual determinacy
7. **Token Efficiency**: The system must minimize token usage while maintaining analytical depth through extraction-based content management
8. **Workflow Management**: All analytical work must follow defined workflows with clear prerequisites and completion criteria
9. **Interoperability**: All modes must communicate through standardized handoff protocols
10. **Content Reusability**: Generated content should be stored efficiently and accessed through extraction mechanisms

## 2. System Architecture

### 2.1 Mode Structure

The system is composed of specialized modes, each with specific responsibilities:

1. **Philosophy-Pre-Lecture**: Analyzes assigned readings before lectures
2. **Philosophy-Class-Analysis**: Analyzes lecture content and integrates with readings
3. **Philosophy-Secondary-Lit**: Analyzes scholarly sources and integrates with course materials
4. **Philosophy-Dialectical-Analysis**: Analyzes dialectical movement of concepts
5. **Philosophy-Essay-Prep**: Develops philosophical essays from conception to draft
6. **Philosophy-Text-Processing**: Processes and chunks texts into manageable units

### 2.2 Shared Components

All modes share these architectural components:

1. **Chronological Management**: Controls progression through course material
2. **Evidence Standards**: Enforces quotation and reference requirements using extraction-based markers
3. **Concept Tracking**: Monitors conceptual development throughout course progression
4. **Verification Workflows**: Ensures analytical quality through systematic checks
5. **Memory Bank Integration**: Maintains persistent state across sessions
6. **Token Optimization Framework**: Implements token-saving strategies across all modes
7. **Materials Availability System**: Tracks and adapts to available source materials
8. **Real-Time Updates**: Maintains synchronization of analysis artifacts

## 3. Token Optimization Framework

### 3.1 Extraction-Based Content Management

The system uses a two-phase document approach that optimizes for both token efficiency during generation and context efficiency during handoffs:

#### 3.1.1 Generation Phase (Token-Optimized)

During content generation, the system minimizes token usage by replacing direct quotations with extraction markers:

```yaml
extraction_markers:
  position_based: "[[EXTRACT:filepath:line_start:char_start:line_end:char_end]]"
  boundary_based: "[[EXTRACT:filepath:\"start_text\"...\"end_text\"]]"
  special_values:
    start_char: "0 represents beginning of line"
    end_char: "-1 represents end of line"
```

Example usage:
```
Heidegger defines Being as: [[EXTRACT:being_and_time.txt:45:0:45:-1]]
```

This approach reduces token usage by ~90% for quoted material while maintaining precise references to source content.

#### 3.1.2 Handoff Phase (Context-Optimized)

Before handoffs between analytical sessions, extracted content is expanded inline:

```yaml
handoff_preparation:
  process: "Run preparation script on documents before handoff"
  result: "All markers expanded inline with full content and source attribution"
  benefit: "AI receives documents with complete context without loading multiple files"
```

This ensures the AI has direct access to all relevant textual evidence without needing to load multiple source files or manage external references.

### 3.2 Extraction Scripts

The system includes scripts to handle extraction marker processing:

#### 3.2.1 Basic Extraction Script (extract_text.py)

```yaml
script_purpose: "Process files containing extraction markers"
usage: "python extract_text.py [--path FILE_OR_DIR] [--preview] [--keep-markers]"
features:
  - "Position-based extraction (line and character positions)"
  - "Boundary-based extraction (text delimiters)"
  - "Special values: 0 for line start, -1 for line end"
  - "Preview mode to see replacements without modifying files"
  - "Optional retention of markers as comments"
```

Script Implementation (extract_text.py):
```python
import re
import os
import argparse

def extract_by_position(filepath, line_start, char_start, line_end, char_end):
    """Extract text using line and character positions"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        result = []
        for i in range(line_start-1, line_end):
            if i >= len(lines):
                return f"[ERROR: Line {i+1} out of range]"
                
            line = lines[i]
            if i == line_start-1:
                # Handle special case for start of line
                if char_start == 0:
                    pass  # Use the whole line from the beginning
                else:
                    line = line[char_start-1:]
            if i == line_end-1:
                # Handle special case for end of line
                if char_end == -1:
                    pass  # Use the whole line to the end
                else:
                    line = line[:char_end]
            result.append(line)
        
        return ''.join(result)
    except Exception as e:
        return f"[EXTRACTION ERROR: {str(e)}]"

# Rest of the script implementation...
```

#### 3.2.2 Handoff Preparation Script (prepare_handoff.py)

```yaml
script_purpose: "Prepare handoff documents by expanding all extraction markers"
usage: "python prepare_handoff.py <handoff_file>"
features:
  - "Expands all extraction markers with full content"
  - "Preserves source attribution for each expansion"
  - "Creates backup of original marker-based file"
  - "Optimizes for AI context efficiency"
```

### 3.3 Text Chunking Framework

For large texts (books, lengthy lectures), the system uses semantic chunking:

```yaml
chunking_workflow:
  1. "AI analyzes text structure and identifies semantic boundaries"
  2. "AI generates chunking specification with metadata"
  3. "Chunking script creates individual files for each chunk"
  4. "Comprehensive index file links all chunks with metadata"
```

Chunk specification format:
```json
{
  "source_file": "path/to/source.txt",
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

## 4. Chronological Management

### 4.1 Structure

The chronological management component maintains the temporal position in course material:

```yaml
chronological_units:
  - level: "Course"
    attributes: ["course_id", "term", "instructor"]
  - level: "Module"
    attributes: ["module_id", "title", "start_date", "end_date"]
  - level: "Session"
    attributes: ["session_id", "date", "topic"]
  - level: "Material"
    attributes: ["material_id", "type", "title", "due_date"]
```

### 4.2 Operations

```yaml
chronological_operations:
  - "validate_chronological_position": "Ensures analysis respects course chronology"
  - "get_available_materials": "Retrieves materials available at current position"
  - "advance_position": "Moves chronological position forward"
  - "material_status": "Tracks completion status of materials"
```

### 4.3 Chronological Enforcement

```yaml
chronological_enforcement:
  access_rules:
    - "Content from future lectures/readings must not be referenced"
    - "Content from past lectures/readings must respect chronological order"
    - "References to past materials must indicate chronological distance"
  
  materialization:
    - "All references to course materials must include timestamp/page and relative position"
    - "Concepts are tagged with their introduction point in the course"
```

## 5. Evidence Standards System

### 5.1 Requirements

```yaml
evidence_requirements:
  - "All interpretations must be supported by direct quotations (using extraction markers)"
  - "All concept determinations require multiple supporting quotations"
  - "All text references must include specific page/section numbers"
  - "All lecture references must include timestamp or section markers"
```

### 5.2 Quotation Implementation

Standard format with token optimization:
```markdown
Heidegger argues: [[EXTRACT:being_and_time.txt:45:0:45:-1]] (Being and Time, p. 26)
```

After extraction processing:
```markdown
Heidegger argues: "Being is that which determines entities as entities, that on the basis of which entities are already understood." (Being and Time, p. 26)

*[Source: being_and_time.txt, lines 45-45]*
```

### 5.3 Verification Process

```yaml
evidence_verification:
  steps:
    - "Identify all interpretative claims"
    - "Check each claim for supporting quotations"
    - "Verify quotation markers resolve to relevant content"
    - "Ensure sufficient context for accurate interpretation"
  implementation: "Automatic verification workflow at the end of all analyses"
```

### 5.4 Documentation Requirements

```yaml
documentation_requirements:
  primary_sources:
    - "Title, author, and edition"
    - "Page number or section identifier"
    - "Extraction marker to specific text"
  
  lecture_sources:
    - "Lecture title and date"
    - "Timestamp or section reference"
    - "Extraction marker to transcript section"
  
  secondary_sources:
    - "Complete citation information"
    - "Page number or section identifier" 
    - "Extraction marker to specific text"
```

## 6. Concept Management System

### 6.1 Dynamic Concept Tracking

The system tracks philosophical concepts while respecting their contextual evolution:

```yaml
concept_tracking:
  concept_structure:
    - "concept_id": "Unique identifier"
    - "name": "Primary term for concept"
    - "aliases": "Alternative terms"
    - "chronological_instances": "Tracked occurrences through course"
    - "related_concepts": "Conceptual relationships"
  
  instance_structure:
    - "source": "Text or lecture reference"
    - "temporal_position": "Position in course chronology"
    - "determination":
        "positive": "What the concept is (extraction marker)"
        "negative": "What the concept is not (extraction marker)"
    - "context": "Specific context of this instance"
    - "evolution": "Changes from previous instances"
```

### 6.2 Concept Unity

The system tracks both the diversity of concept articulations and their underlying unity:

```yaml
concept_unity:
  tracking:
    - "Formal unity": "Logical/structural commonalities"
    - "Historical unity": "Developmental trajectory"
    - "Dialectical unity": "Through contradictions and transformations"
```

### 6.3 Concept Template

```markdown
# Concept: [CONCEPT_NAME]

## Chronological Instances

### Instance 1: [TEMPORAL_POSITION]
- **Source**: [SOURCE_REFERENCE]
- **Positive Determination**: [[EXTRACT:filepath:line_start:char_start:line_end:char_end]]
- **Negative Determination**: [[EXTRACT:filepath:line_start:char_start:line_end:char_end]]
- **Context**: [SPECIFIC_CONTEXT]

### Instance 2: [TEMPORAL_POSITION]
- **Source**: [SOURCE_REFERENCE]
- **Positive Determination**: [[EXTRACT:filepath:line_start:char_start:line_end:char_end]]
- **Negative Determination**: [[EXTRACT:filepath:line_start:char_start:line_end:char_end]]
- **Context**: [SPECIFIC_CONTEXT]
- **Evolution**: [CHANGES_FROM_PREVIOUS]

## Related Concepts
- **[RELATED_CONCEPT_1]**: [RELATIONSHIP_TYPE]
- **[RELATED_CONCEPT_2]**: [RELATIONSHIP_TYPE]

## Underlying Unity
[EXPLANATION_OF_SELF_SAMENESS]
```

## 7. Memory Bank System

### 7.1 Structure

```yaml
memory_bank:
  core_files:
    - "activeContext.md": "Current analytical context"
    - "productContext.md": "Project overview"
    - "progress.md": "Progress tracking"
    - "decisionLog.md": "Decision history"
  analysis_files:
    pattern: "{date}_{material}_{type}.md"
```

### 7.2 Handoff Protocol

```yaml
handoff_protocol:
  preparation:
    1. "Complete current analytical step"
    2. "Update memory bank files"
    3. "Run extraction expansion on handoff documents"
    4. "Prepare activeContext.md with current state"
  reception:
    1. "Load expanded handoff documents"
    2. "Establish current chronological position"
    3. "Validate analytical prerequisites"
```

### 7.3 Active Context Management

```yaml
active_context:
  required_components:
    - "Current chronological position"
    - "Current analysis status"
    - "Prior context dependencies"
    - "Available materials"
  
  checkpoint_system:
    - "Regular state snapshots during analysis"
    - "Completion markers for analytical stages"
    - "Resumption points for interrupted analyses"
  
  specialized_contexts:
    - "lecture_analysis_context": "For class analysis mode"
    - "reading_analysis_context": "For pre-lecture mode" 
    - "essay_development_context": "For essay preparation mode"
```

## 8. Workflow Management System

### 8.1 Analysis Workflow

```yaml
analysis_workflow:
  steps:
    1. "Material Processing": "Reading/organizing source materials"
    2. "Initial Analysis": "Core concept/argument identification (with extraction markers)"
    3. "Detailed Analysis": "In-depth examination of key components"
    4. "Integration": "Connecting with previous materials"
    5. "Verification": "Checking evidence standards and concept determinacy"
    6. "Documentation": "Updating memory bank"
```

### 8.2 Essay Preparation Workflow

```yaml
essay_prep_workflow:
  steps:
    1. "Prompt Analysis": "Breaking down requirements"
    2. "Material Identification": "Finding relevant sources"
    3. "Thesis Development": "Formulating core argument"
    4. "Evidence Collection": "Gathering supporting quotations (as extraction markers)"
    5. "Outline Creation": "Structuring argument flow"
    6. "Section Drafting": "Writing individual sections"
    7. "Integration": "Combining sections into coherent whole"
    8. "Revision": "Refining argument and evidence"
```

### 8.3 Alternative Workflows

```yaml
alternative_workflows:
  missing_lecture:
    1. "Identify missing material"
    2. "Determine impact on analytical continuity"
    3. "Identify alternative sources for key concepts"
    4. "Develop parallel analysis path"
    5. "Document assumptions and limitations"
  
  missing_reading:
    1. "Identify missing material"
    2. "Locate secondary sources or summaries"
    3. "Extract key concepts from available references"
    4. "Document limitations of analysis"
    5. "Develop contingent interpretations"
```

## 9. Verification System

### 9.1 Verification Types

```yaml
verification_types:
  - "evidence_verification": "Checks quotation standards"
  - "concept_verification": "Validates concept determinations"
  - "chronological_verification": "Ensures chronological integrity"
  - "workflow_verification": "Confirms workflow completion"
  - "extraction_verification": "Validates extraction markers"
```

### 9.2 Implementation

```yaml
verification_implementation:
  frequency: "After each analytical stage"
  documentation: "Issues logged in verification_report section"
  remediation: "Required before proceeding to next stage"
  
  extraction_verification:
    - "Check all extraction markers are properly formatted"
    - "Verify source files exist and are accessible"
    - "Test marker resolution to ensure content is extractable"
    - "Validate line and character positions are within bounds"
```

### 9.3 Verification Report Template

```markdown
# Verification Report: [ANALYSIS_NAME]

## Evidence Verification
- **Total claims**: [NUMBER]
- **Claims with adequate support**: [NUMBER]
- **Claims requiring additional evidence**: [LIST_OF_CLAIMS]

## Concept Verification
- **Concepts analyzed**: [NUMBER]
- **Concepts with complete determinations**: [NUMBER]
- **Concepts requiring additional determination**: [LIST_OF_CONCEPTS]

## Chronological Verification
- **Chronological violations**: [NUMBER_OR_NONE]
- **Corrective actions**: [LIST_OR_NONE]

## Extraction Verification
- **Total extraction markers**: [NUMBER]
- **Valid markers**: [NUMBER]
- **Invalid markers**: [LIST_WITH_ISSUES]

## Overall Status
[PASS_OR_REMEDIATION_NEEDED]
```

## 10. Materials Availability System

### 10.1 Material Types

```yaml
material_types:
  - "assigned_readings":
      attributes: ["title", "author", "pages", "due_date", "format"]
  - "lecture_notes":
      attributes: ["date", "topic", "completeness", "format"]
  - "secondary_sources":
      attributes: ["title", "author", "relevance", "availability"]
```

### 10.2 Availability Status

```yaml
availability_status:
  - "available": "Material is present and accessible"
  - "partial": "Material is partially available (incomplete)"
  - "unavailable": "Material is completely missing"
  - "pending": "Material will be available in the future"
```

### 10.3 Adaptation Strategies

```yaml
adaptation_strategies:
  available:
    - "Standard analytical workflow"
    - "Complete extraction-based evidence"
  
  partial:
    - "Extract concepts from available portions"
    - "Document limitations in analysis"
    - "Use secondary sources to fill gaps"
  
  unavailable:
    - "Identify alternative sources"
    - "Use lecture context if reading is missing"
    - "Use reading context if lecture is missing"
    - "Document specific limitations"
```

### 10.4 Source Recommendation System

```yaml
source_recommendation:
  criteria:
    - "Relevance to current topic"
    - "Chronological appropriateness"
    - "Conceptual coverage"
    - "Analytical depth"
  
  implementation:
    - "When primary sources are unavailable, suggest alternatives"
    - "Prioritize sources that have extraction markers already defined"
    - "Recommend sections with highest concept density"
```

## 11. Real-Time Updates System

### 11.1 Update Categories

```yaml
update_categories:
  - "analytical_progress": "Status of ongoing analyses"
  - "material_status": "Changes in material availability"
  - "concept_development": "Evolution of concept understanding" 
  - "workflow_status": "Completion of workflow steps"
```

### 11.2 Status Reporting

```yaml
status_reporting:
  frequency: "At completion of each analytical stage"
  components:
    - "Current position in workflow"
    - "Completed analyses and verifications"
    - "Pending analyses and prerequisites"
    - "Blocked paths and reasons"
```

### 11.3 Progress Tracking

```yaml
progress_tracking:
  metrics:
    - "Concepts fully determined": "[X/Y]"
    - "Analytical coverage": "[X%]"
    - "Verification status": "[PASS/FAIL]"
    - "Extraction marker validity": "[X/Y]"
```

## 12. Mode-Specific Components

### 12.1 Philosophy-Pre-Lecture

```yaml
pre_lecture_mode:
  purpose: "Analyze assigned readings before lecture"
  
  key_functions:
    - "identify_key_concepts": "Extract central terms with extraction markers"
    - "reconstruct_arguments": "Map argumentative structure"
    - "prepare_questions": "Generate engagement points for lecture"
  
  workflow:
    1. "Read assigned material"
    2. "Identify key concepts and arguments"
    3. "Generate extraction markers for important passages"
    4. "Develop concept determinations"
    5. "Map argument structures"
    6. "Prepare engagement questions"
    7. "Verify and document"
  
  token_optimization:
    - "Use extraction markers for all quotations"
    - "Focus on conceptual mapping rather than extensive quotation"
    - "Generate markers for future reference in class analysis"
  
  output_template:
    format: "{date}_{reading}_pre-lecture.md"
    sections:
      - "Key Concepts": "List of concepts with determinations"
      - "Argument Structure": "Reconstruction of main arguments"
      - "Questions": "Points for lecture engagement"
      - "Evidence": "Extraction markers to key passages"
```

### 12.2 Philosophy-Class-Analysis

```yaml
class_analysis_mode:
  purpose: "Analyze lecture content and integrate with readings"
  
  key_functions:
    - "lecture_summary": "Structured overview of lecture"
    - "reading_integration": "Connect lecture to readings"
    - "concept_evolution": "Track development of concepts"
  
  workflow:
    1. "Process lecture materials"
    2. "Identify key concepts and arguments presented"
    3. "Generate extraction markers for important lecture segments"
    4. "Compare with pre-lecture reading analysis"
    5. "Document concept evolution"
    6. "Integrate reading and lecture perspectives"
    7. "Verify and document"
  
  token_optimization:
    - "Use extraction markers for lecture content"
    - "Cross-reference pre-lecture analyses"
    - "Focus on evolution and integration rather than repetition"
  
  output_template:
    format: "{date}_{lecture}_class-analysis.md"
    sections:
      - "Lecture Summary": "Overview of main points"
      - "Key Concepts": "Concepts with updated determinations"
      - "Integration": "Connections between reading and lecture"
      - "Evolution": "How concepts have developed or changed"
      - "Evidence": "Extraction markers to key lecture segments"
```

### 12.3 Philosophy-Secondary-Lit

```yaml
secondary_lit_mode:
  purpose: "Analyze scholarly sources and integrate with course materials"
  
  key_functions:
    - "source_analysis": "Examine secondary literature"
    - "position_mapping": "Place in scholarly discourse"
    - "primary_text_connection": "Link to primary materials"
  
  workflow:
    1. "Process secondary source"
    2. "Identify scholarly position and approach"
    3. "Generate extraction markers for key interpretations"
    4. "Map to relevant primary sources"
    5. "Evaluate interpretative framework"
    6. "Integrate with course concepts"
    7. "Verify and document"
  
  token_optimization:
    - "Use extraction markers for all quotations"
    - "Create indexed chunks for larger scholarly works"
    - "Cross-reference to existing concept determinations"
  
  output_template:
    format: "{date}_{source}_secondary-analysis.md"
    sections:
      - "Source Overview": "Brief description and context"
      - "Key Interpretations": "Major scholarly positions"
      - "Primary Text Connections": "Links to course materials"
      - "Evaluation": "Assessment of interpretative approach"
      - "Evidence": "Extraction markers to key passages"
```

### 12.4 Philosophy-Dialectical-Analysis

```yaml
dialectical_analysis_mode:
  purpose: "Analyze dialectical movement of concepts"
  
  key_functions:
    - "contradiction_identification": "Find conceptual tensions"
    - "movement_tracking": "Map concept transformations"
    - "synthesis_analysis": "Examine resolutions"
  
  workflow:
    1. "Identify concept for dialectical analysis"
    2. "Map chronological instances of the concept"
    3. "Identify contradictions or tensions"
    4. "Generate extraction markers for key moments"
    5. "Trace dialectical movement"
    6. "Articulate synthetic resolutions"
    7. "Verify and document"
  
  token_optimization:
    - "Use extraction markers for evidencing tensions and resolutions"
    - "Reference prior analyses of concepts"
    - "Focus on transformational points rather than full exposition"
  
  output_template:
    format: "{date}_{concept}_dialectical-analysis.md"
    sections:
      - "Concept Timeline": "Chronological development"
      - "Tensions": "Identified contradictions"
      - "Movement": "Dialectical progression"
      - "Resolution": "Synthesis or outcome"
      - "Evidence": "Extraction markers to key dialectical moments"
```

### 12.5 Philosophy-Essay-Prep

```yaml
essay_prep_mode:
  purpose: "Develop philosophical essays from conception to draft"
  
  key_functions:
    - "prompt_analysis": "Break down requirements"
    - "evidence_gathering": "Collect supporting quotations"
    - "argument_structure": "Develop logical framework"
  
  workflow:
    1. "Analyze essay prompt"
    2. "Identify relevant concepts and materials"
    3. "Develop thesis statement"
    4. "Map argument structure"
    5. "Gather evidence using extraction markers"
    6. "Outline essay sections"
    7. "Draft sections"
    8. "Integrate sections"
    9. "Revise and refine"
  
  token_optimization:
    - "Use extraction markers for all evidence gathering"
    - "Reference existing concept determinations"
    - "Expand markers only for final draft review"
  
  output_template:
    format: "{date}_{topic}_essay-prep.md"
    sections:
      - "Prompt Analysis": "Breakdown of requirements"
      - "Thesis": "Central argument statement"
      - "Outline": "Structured argument flow"
      - "Evidence": "Extraction markers organized by section"
      - "Drafts": "Section-by-section development"
```

### 12.6 Philosophy-Text-Processing

```yaml
text_processing_mode:
  purpose: "Process and chunk texts into manageable units"
  
  key_functions:
    - "semantic_chunking": "Divide texts by conceptual boundaries"
    - "index_generation": "Create navigable index"
    - "metadata_enrichment": "Add concept tags and summaries"
  
  workflow:
    1. "Analyze text structure"
    2. "Identify semantic boundaries"
    3. "Create chunking specification"
    4. "Generate chunk files"
    5. "Create comprehensive index"
  
  implementation:
    chunking_specification:
      format: "JSON configuration"
      elements:
        - "source_file": "Original text path"
        - "chunks": "Array of chunk definitions"
        - "chunk_definition":
            - "id": "Unique identifier"
            - "title": "Descriptive title"
            - "start_line": "Beginning line number"
            - "end_line": "Ending line number"
            - "key_concepts": "Array of concepts"
            - "summary": "Brief description"
    
    processing_script: "process_chunks.py"
    
    index_format:
      - "Table of chunks with metadata"
      - "Concept cross-reference"
      - "Navigation structure"
```

## 13. Extension and Modification System

### 13.1 Adding New Modes

```yaml
mode_addition:
  requirements:
    - "Clear purpose definition"
    - "Distinct function from existing modes"
    - "Defined inputs and outputs"
    - "Standardized components"
  
  implementation:
    1. "Define core purpose and functionality"
    2. "Specify workflow steps"
    3. "Design token optimization strategy"
    4. "Create output templates"
    5. "Define handoff protocols"
    6. "Document in architecture"
```

### 13.2 Modifying Existing Modes

```yaml
mode_modification:
  requirements:
    - "Backward compatibility with existing analyses"
    - "Preservation of core architectural principles"
    - "Documentation of changes"
  
  implementation:
    1. "Identify modification requirements"
    2. "Assess impact on existing analyses"
    3. "Design change implementation"
    4. "Update documentation"
    5. "Test with existing workflows"
```

## 14. Implementation Guidelines

### 14.1 Token Optimization Implementation

```yaml
token_optimization_implementation:
  during_analysis:
    - "Use extraction markers for all quotations"
    - "Include source attribution with all markers"
    - "Maintain precise position information"
  
  before_handoff:
    - "Run prepare_handoff.py on relevant documents"
    - "Ensure all markers are expanded for AI context"
    - "Preserve source attributions in expanded form"
    
  script_usage:
    - "extract_text.py": "For viewing extracted content in context"
    - "prepare_handoff.py": "For handoff document preparation"
    - "process_chunks.py": "For processing text chunking specifications"
```

### 14.2 Extraction Format Selection

```yaml
extraction_format_selection:
  position_based:
    best_for: "Stable source documents"
    advantages: "Precise, compact"
    format: "[[EXTRACT:filepath:line_start:char_start:line_end:char_end]]"
    special_values:
      - "char_start=0: Beginning of line"
      - "char_end=-1: End of line"
  
  boundary_based:
    best_for: "Documents that may change slightly"
    advantages: "More resilient to minor changes"
    format: "[[EXTRACT:filepath:\"start_text\"...\"end_text\"]]"
```

### 14.3 Verification Standards

All verification workflows remain fully functional with extraction-based content:

```yaml
extraction_verification:
  evidence_standard: "All extraction markers must resolve to relevant content"
  resolution_checking: "Extraction markers are verified for validity"
  context_maintenance: "Sufficient context is preserved in extraction boundaries"
```

## 14.4 Cost Efficiency Metrics

```yaml
cost_efficiency_metrics:
  direct_quotation: "~90% token reduction by using extraction markers"
  handoff_optimization: "~80% context efficiency through pre-expanded handoffs"
  output_reduction: "~70% overall token reduction for analytical documents"
```

### 14.5 Handoff Preparation Guidelines

```yaml
handoff_preparation:
  required_steps:
    1. "Identify all documents needed for handoff"
    2. "Process extraction markers in active context files"
    3. "Ensure expanded content maintains source attribution"
    4. "Backup original marker-based files"
  
  command_example: "python prepare_handoff.py activeContext.md"
  
  context_optimization:
    - "Include only necessary content for analytical context"
    - "Prioritize current chronological position materials"
    - "Include full concept determinations for active concepts"
```

## 15. Integration Guidelines

### 15.1 Cross-Mode Integration

```yaml
cross_mode_integration:
  handoff_requirements:
    - "Chronological position must be explicitly transferred"
    - "Extraction-processed documents for active context"
    - "Material availability status"
    - "Current concept determinations"
  
  workflow_continuity:
    - "Clear indication of completed steps"
    - "Identification of next steps"
    - "Explicit transfer of verification status"
```

### 15.2 Memory Bank Synchronization

```yaml
memory_bank_synchronization:
  update_frequency:
    - "After each analytical stage"
    - "Before any mode transition"
    - "After extraction processing of significant content"
  
  update_protocol:
    1. "Process any extraction markers in core files"
    2. "Update progress tracking information"
    3. "Document any token optimization changes"
    4. "Ensure concept determinations are current"
```

## 16. System Maintenance

### 16.1 File Management

```yaml
file_management:
  recommended_structure:
    - "memory-bank/": "Core context files"
    - "analyses/": "Analytical output files"
    - "sources/": "Course materials and references"
    - "chunks/": "Processed text chunks"
  
  naming_conventions:
    - "analysis files": "{date}_{material}_{type}.md"
    - "concept files": "concept_{name}.md"
    - "chunk files": "{source}_{chunk_id}.md"
```

### 16.2 Script Maintenance

```yaml
script_maintenance:
  update_scenarios:
    - "Adding new extraction format options"
    - "Enhancing handoff preparation capabilities"
    - "Improving text chunking algorithms"
    - "Adding new verification checks"
  
  compatibility_requirements:
    - "Maintain backward compatibility with existing markers"
    - "Preserve source attribution conventions"
    - "Support special position values (0, -1)"
```

## 17. Conclusion

The Enhanced Philosophy Analysis System Architecture provides a comprehensive framework for rigorous philosophical analysis while optimizing token usage through extraction-based content management. By implementing the two-phase document approach, the system achieves significant cost savings without sacrificing analytical depth or evidence standards.

Key architectural innovations include:
1. The extraction marker system for referencing source material
2. The handoff preparation process for context optimization
3. The semantic chunking framework for large text management
4. The verification system for extraction marker validation

This architecture supports the full range of philosophical analysis activities while ensuring cost-efficient operation, chronological integrity, and evidential rigor.