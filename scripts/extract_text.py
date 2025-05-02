#!/usr/bin/env python3
import re
import os
import argparse
from pathlib import Path
from typing import Optional, Union, List, Tuple

def extract_by_position(filepath: str, line_start: int, word_start: int, line_end: int, word_end: int) -> str:
    """Extract text using line and word positions.
    
    Args:
        filepath: Path to the source file
        line_start: Starting line number (1-based)
        word_start: Starting word position (1-based, 0 for line start)
        line_end: Ending line number (1-based)
        word_end: Ending word position (-1 for line end)
    
    Returns:
        Extracted text content
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Validate line numbers
        if line_start < 1 or line_start > len(lines) + 1:
            return f"[ERROR: Invalid start line {line_start}]"
        if line_end < line_start or line_end > len(lines) + 1:
            return f"[ERROR: Invalid end line {line_end}]"
        
        # Handle special position values
        word_start = 0 if word_start == 0 else word_start
        
        result = []
        for i in range(line_start-1, line_end):
            if i >= len(lines):
                return f"[ERROR: Line {i+1} out of range]"
                
            line = lines[i]
            words = line.split()
            
            if i == line_start-1:
                if word_start > 1:
                    words = words[word_start-1:]
            if i == line_end-1 and word_end != -1:
                words = words[:word_end]
            result.append(' '.join(words))
        
        extracted_text = ' '.join(result)
        if line_start == line_end:
            return f"\"{extracted_text}\" [from: {filepath}, line {line_start}]"
        else:
            return f"\"{extracted_text}\" [from: {filepath}, lines {line_start}-{line_end}]"
    except FileNotFoundError:
        # Try legacy path if file not found
        if filepath.startswith("sources/"):
            legacy_path = filepath.replace("sources/readings/", "evidence/readings/")
            legacy_path = legacy_path.replace("sources/lectures/", "evidence/lectures/")
            legacy_path = legacy_path.replace("sources/secondary/", "evidence/secondary/")
            return extract_by_position(legacy_path, line_start, word_start, line_end, word_end)
        elif filepath.startswith("memory-bank/"):
            legacy_path = filepath.replace("memory-bank/concepts/", "concepts/definitions/")
            legacy_path = legacy_path.replace("memory-bank/concept-evolution/", "concepts/evolution/")
            return extract_by_position(legacy_path, line_start, word_start, line_end, word_end)
        return f"[ERROR: File '{filepath}' not found]"
    except Exception as e:
        return f"[EXTRACTION ERROR: {str(e)}]"

def extract_by_boundary(filepath: str, start_text: str, end_text: str) -> str:
    """Extract text using boundary markers.
    
    Args:
        filepath: Path to the source file
        start_text: Text marking the start of extraction
        end_text: Text marking the end of extraction
    
    Returns:
        Extracted text content including boundary markers
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        start_pos = content.find(start_text)
        if start_pos == -1:
            return f"[ERROR: Start text not found]"
        
        search_start = start_pos + len(start_text)
        end_pos = content.find(end_text, search_start)
        if end_pos == -1:
            return f"[ERROR: End text not found]"
        
        # Find line numbers for citation
        start_line = content[:start_pos].count('\n') + 1
        end_line = content[:end_pos + len(end_text)].count('\n') + 1
        
        # Return extracted text with quotation marks and citation
        extracted_text = start_text + content[search_start:end_pos] + end_text
        if start_line == end_line:
            return f"\"{extracted_text}\" [from: {filepath}, line {start_line}]"
        else:
            return f"\"{extracted_text}\" [from: {filepath}, lines {start_line}-{end_line}]"
    
    except FileNotFoundError:
        # Try legacy path if file not found
        if filepath.startswith("sources/"):
            legacy_path = filepath.replace("sources/readings/", "evidence/readings/")
            legacy_path = legacy_path.replace("sources/lectures/", "evidence/lectures/")
            legacy_path = legacy_path.replace("sources/secondary/", "evidence/secondary/")
            return extract_by_boundary(legacy_path, start_text, end_text)
        elif filepath.startswith("memory-bank/"):
            legacy_path = filepath.replace("memory-bank/concepts/", "concepts/definitions/")
            legacy_path = legacy_path.replace("memory-bank/concept-evolution/", "concepts/evolution/")
            return extract_by_boundary(legacy_path, start_text, end_text)
        return f"[ERROR: File '{filepath}' not found]"
    except Exception as e:
        return f"[EXTRACTION ERROR: {str(e)}]"

def process_extraction_markers(content: str) -> str:
    """Process extraction markers in content.
    
    Args:
        content: Text content containing extraction markers
    
    Returns:
        Content with extraction markers replaced with extracted text
    """
    # Position-based extraction pattern
    pos_pattern = r'\[\[EXTRACT:([^:]+):(\d+):(-?\d+)w:(\d+):(-?\d+)w\]\]'
    
    # Boundary-based extraction pattern
    bound_pattern = r'\[\[EXTRACT:([^:]+):"([^"]+)"..."([^"]+)"\]\]'
    
    def pos_replace(match):
        filepath = match.group(1)
        line_start = int(match.group(2))
        word_start = int(match.group(3))
        line_end = int(match.group(4))
        word_end = int(match.group(5))
        
        extracted = extract_by_position(filepath, line_start, word_start, line_end, word_end)
        return extracted
    
    def bound_replace(match):
        filepath = match.group(1)
        start_text = match.group(2)
        end_text = match.group(3)
        
        extracted = extract_by_boundary(filepath, start_text, end_text)
        return extracted
    
    # Process position-based markers first
    content = re.sub(pos_pattern, pos_replace, content)
    
    # Then process boundary-based markers
    content = re.sub(bound_pattern, bound_replace, content)
    
    return content

def process_file(filepath: str, preview: bool = False, keep_markers: bool = True) -> None:
    """Process extraction markers in a file.
    
    Args:
        filepath: Path to the file to process
        preview: If True, only print changes without modifying file
        keep_markers: If True, keep original markers as comments
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        processed = process_extraction_markers(content)
        
        if preview:
            print(f"\nProcessed content for {filepath}:")
            print("-" * 40)
            print(processed)
            print("-" * 40)
            return
        
        # Create backup
        backup_path = f"{filepath}.bak"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Write processed content
        with open(filepath, 'w', encoding='utf-8') as f:
            if keep_markers:
                # Convert original markers to comments
                commented = re.sub(r'\[\[EXTRACT:[^\]]+\]\]',
                                 lambda m: f"<!-- {m.group(0)} -->",
                                 content)
                f.write(processed + "\n\n<!-- Original markers:\n" + commented + "\n-->")
            else:
                f.write(processed)
        
        print(f"Successfully processed {filepath}")
        print(f"Backup saved to {backup_path}")
        
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")

def process_directory(dirpath: str, preview: bool = False, keep_markers: bool = True) -> None:
    """Recursively process all files in a directory.
    
    Args:
        dirpath: Path to the directory
        preview: If True, only print changes without modifying files
        keep_markers: If True, keep original markers as comments
    """
    for root, _, files in os.walk(dirpath):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.isfile(filepath):
                process_file(filepath, preview, keep_markers)

def main():
    parser = argparse.ArgumentParser(description='Process text extraction markers')
    parser.add_argument('--path', default='.',
                      help='File or directory to process')
    parser.add_argument('--preview', action='store_true',
                      help='Preview only, no file modifications')
    parser.add_argument('--keep-markers', action='store_true', default=True,
                      help='Keep markers as comments')
    
    args = parser.parse_args()
    
    path = args.path
    if os.path.isfile(path):
        process_file(path, args.preview, args.keep_markers)
    elif os.path.isdir(path):
        process_directory(path, args.preview, args.keep_markers)
    else:
        print(f"Error: Path '{path}' not found")

if __name__ == "__main__":
    main()