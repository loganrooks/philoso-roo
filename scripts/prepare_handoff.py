#!/usr/bin/env python3
import os
import sys
import argparse
import json
import shutil
from typing import Dict, List, Optional
from datetime import datetime

class HandoffPreparationError(Exception):
    """Base exception for handoff preparation errors."""
    pass

class SourceFileError(HandoffPreparationError):
    """Raised when there are issues with source files."""
    pass

class ExtractionError(HandoffPreparationError):
    """Raised when extraction fails."""
    pass

class ValidationError(HandoffPreparationError):
    """Raised when validation fails."""
    pass

def create_backup(filepath: str) -> str:
    """Create a backup of the file with timestamp.
    
    Args:
        filepath: Path to the file to backup
    
    Returns:
        Path to the backup file
    
    Raises:
        SourceFileError: If backup creation fails
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{filepath}.{timestamp}.bak"
        shutil.copy2(filepath, backup_path)
        return backup_path
    except Exception as e:
        raise SourceFileError(f"Failed to create backup of {filepath}: {str(e)}\n"
                            f"Context: Attempted to create backup at {backup_path}\n"
                            f"File permissions and disk space should be verified.")

def load_file_content(filepath: str) -> str:
    """Load content from a file with detailed error handling.
    
    Args:
        filepath: Path to the file to load
    
    Returns:
        File content as string
    
    Raises:
        SourceFileError: If file cannot be read
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise SourceFileError(f"File not found: {filepath}\n"
                            f"Context: The file does not exist or is not accessible.\n"
                            f"Verify the file path and permissions.")
    except UnicodeDecodeError:
        raise SourceFileError(f"Unicode decode error for {filepath}\n"
                            f"Context: The file is not valid UTF-8.\n"
                            f"Check file encoding and convert if necessary.")
    except Exception as e:
        raise SourceFileError(f"Error reading {filepath}: {str(e)}\n"
                            f"Context: Unexpected error while reading file.\n"
                            f"Check file system status and permissions.")

def expand_extraction_marker(match: str, content_cache: Dict[str, str]) -> str:
    """Expand an extraction marker into its full content.
    
    Args:
        match: The extraction marker to expand
        content_cache: Cache of file contents to avoid repeated file reads
    
    Returns:
        Expanded content with source attribution
    
    Raises:
        ExtractionError: If extraction fails
    """
    try:
        # Position-based pattern: [[EXTRACT:filepath:line_start:char_start:line_end:char_end]]
        if ':' in match:
            parts = match.strip('[]').split(':')
            if len(parts) != 6 or parts[0] != 'EXTRACT':
                raise ExtractionError(f"Invalid extraction marker format: {match}\n"
                                    f"Expected format: [[EXTRACT:filepath:line_start:char_start:line_end:char_end]]")
            
            filepath = parts[1]
            try:
                line_start = int(parts[2])
                char_start = int(parts[3])
                line_end = int(parts[4])
                char_end = int(parts[5])
            except ValueError:
                raise ExtractionError(f"Invalid line/character numbers in marker: {match}\n"
                                    f"All position values must be integers.")
            
            # Get or load file content
            if filepath not in content_cache:
                content_cache[filepath] = load_file_content(filepath)
            
            content = content_cache[filepath]
            lines = content.splitlines()
            
            # Validate line numbers
            if line_start < 1 or line_end > len(lines):
                raise ExtractionError(f"Line numbers out of range in marker: {match}\n"
                                    f"File has {len(lines)} lines, but marker specifies lines {line_start}-{line_end}")
            
            # Extract content
            extracted_lines = lines[line_start-1:line_end]
            
            # Apply character positions
            if char_start > 0:
                extracted_lines[0] = extracted_lines[0][char_start-1:]
            if char_end != -1:
                extracted_lines[-1] = extracted_lines[-1][:char_end]
            
            extracted = '\n'.join(extracted_lines)
            
        # Boundary-based pattern: [[EXTRACT:filepath:"start_text"..."end_text"]]
        else:
            raise ExtractionError(f"Unsupported extraction marker format: {match}\n"
                                f"Only position-based extraction is currently supported.")
        
        # Return extracted content with source attribution
        return (f"{extracted}\n\n"
                f"*[Source: {filepath}, lines {line_start}-{line_end}]*\n")
    
    except HandoffPreparationError:
        raise
    except Exception as e:
        raise ExtractionError(f"Failed to expand extraction marker: {match}\n"
                            f"Error: {str(e)}\n"
                            f"Context: Unexpected error during marker expansion.")

def process_handoff_document(filepath: str, keep_markers: bool = True) -> None:
    """Process a handoff document, expanding all extraction markers.
    
    Args:
        filepath: Path to the document to process
        keep_markers: Whether to keep original markers as comments
    
    Raises:
        HandoffPreparationError: If processing fails
    """
    try:
        print(f"Processing handoff document: {filepath}")
        
        # Create backup first
        backup_path = create_backup(filepath)
        print(f"Created backup at: {backup_path}")
        
        # Load content
        content = load_file_content(filepath)
        
        # Initialize content cache
        content_cache: Dict[str, str] = {}
        
        # Find all extraction markers
        import re
        marker_pattern = r'\[\[EXTRACT:[^\]]+\]\]'
        markers = re.finditer(marker_pattern, content)
        
        # Expand markers
        expanded_content = content
        for match in markers:
            marker = match.group(0)
            try:
                expanded = expand_extraction_marker(marker, content_cache)
                if keep_markers:
                    expanded = f"{expanded}\n<!-- Original marker: {marker} -->\n"
                expanded_content = expanded_content.replace(marker, expanded)
            except HandoffPreparationError as e:
                print(f"Warning: Failed to expand marker {marker}: {str(e)}")
                # Keep original marker on failure
                continue
        
        # Write expanded content
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(expanded_content)
            print(f"Successfully processed {filepath}")
        except Exception as e:
            raise SourceFileError(f"Failed to write expanded content to {filepath}: {str(e)}\n"
                                f"Context: Error occurred while saving processed content.\n"
                                f"Original file has been preserved at {backup_path}")
        
    except HandoffPreparationError as e:
        print(f"Error processing handoff document: {str(e)}")
        # Try to restore from backup if we have one
        if 'backup_path' in locals():
            try:
                shutil.copy2(backup_path, filepath)
                print(f"Restored original file from backup: {backup_path}")
            except Exception as restore_error:
                print(f"Failed to restore from backup: {str(restore_error)}")
        raise
    except Exception as e:
        raise HandoffPreparationError(f"Unexpected error processing {filepath}: {str(e)}\n"
                                    f"Context: Error occurred during handoff preparation.\n"
                                    f"Check system status and file permissions.")

def main():
    parser = argparse.ArgumentParser(
        description='Prepare handoff documents by expanding extraction markers'
    )
    parser.add_argument('filepath', help='Path to the handoff document')
    parser.add_argument('--keep-markers', action='store_true', default=True,
                       help='Keep original markers as comments (default: True)')
    
    args = parser.parse_args()
    
    try:
        process_handoff_document(args.filepath, args.keep_markers)
    except HandoffPreparationError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()