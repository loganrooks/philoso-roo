#!/usr/bin/env python3
import os
import sys
import json
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from pathlib import Path

class BatchUpdateError(Exception):
    """Base exception for batch update errors."""
    pass

class ConfigError(BatchUpdateError):
    """Raised when there are issues with the update configuration."""
    pass

class FileOperationError(BatchUpdateError):
    """Raised when file operations fail."""
    pass

def create_backup(filepath: str) -> str:
    """Create a backup of a file with timestamp.
    
    Args:
        filepath: Path to the file to backup
    
    Returns:
        Path to the backup file
    
    Raises:
        FileOperationError: If backup creation fails
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{filepath}.{timestamp}.bak"
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        if os.path.exists(filepath):
            shutil.copy2(filepath, backup_path)
        else:
            # For new files, create empty backup
            Path(backup_path).touch()
            
        return backup_path
    except Exception as e:
        raise FileOperationError(f"Failed to create backup of {filepath}: {str(e)}\n"
                               f"Context: Attempted to create backup at {backup_path}\n"
                               f"Verify file permissions and disk space.")

def restore_from_backup(backup_path: str, target_path: str) -> None:
    """Restore a file from its backup.
    
    Args:
        backup_path: Path to the backup file
        target_path: Path to restore to
        
    Raises:
        FileOperationError: If restoration fails
    """
    try:
        if os.path.exists(backup_path):
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            shutil.copy2(backup_path, target_path)
        else:
            raise FileOperationError(f"Backup file not found: {backup_path}")
    except Exception as e:
        raise FileOperationError(f"Failed to restore {target_path} from {backup_path}: {str(e)}")

def convert_legacy_path(filepath: str) -> str:
    """Convert legacy paths to new format.
    
    Args:
        filepath: Original file path
        
    Returns:
        Converted path
    """
    if filepath.startswith("concepts/"):
        filepath = filepath.replace("concepts/definitions/", "memory-bank/concepts/")
        filepath = filepath.replace("concepts/evolution/", "memory-bank/concept-evolution/")
    elif filepath.startswith("evidence/"):
        filepath = filepath.replace("evidence/readings/", "sources/readings/")
        filepath = filepath.replace("evidence/lectures/", "sources/lectures/")
        filepath = filepath.replace("evidence/secondary/", "sources/secondary/")
    return filepath

def load_file_content(filepath: str) -> str:
    """Load content from a file.
    
    Args:
        filepath: Path to the file
        
    Returns:
        File content as string
        
    Raises:
        FileOperationError: If file cannot be read
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # Try legacy path
        legacy_path = convert_legacy_path(filepath)
        if legacy_path != filepath:
            try:
                with open(legacy_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                pass
        raise FileOperationError(f"File not found: {filepath}\n"
                               f"Also tried legacy path: {legacy_path}\n"
                               f"Verify file path and permissions.")
    except Exception as e:
        raise FileOperationError(f"Error reading {filepath}: {str(e)}")

def replace_section(filepath: str, identifier: str, content: str) -> None:
    """Replace content between section markers.
    
    Args:
        filepath: Target file path
        identifier: Section identifier
        content: New content
        
    Raises:
        FileOperationError: If section replacement fails
    """
    try:
        file_content = load_file_content(filepath)
        
        start_marker = f"<!-- SECTION:{identifier}:start -->"
        end_marker = f"<!-- SECTION:{identifier}:end -->"
        
        start_pos = file_content.find(start_marker)
        if start_pos == -1:
            raise FileOperationError(f"Section start marker not found: {identifier}\n"
                                   f"Expected marker: {start_marker}")
        
        start_pos = start_pos + len(start_marker)
        end_pos = file_content.find(end_marker, start_pos)
        if end_pos == -1:
            raise FileOperationError(f"Section end marker not found: {identifier}\n"
                                   f"Expected marker: {end_marker}")
        
        new_content = (file_content[:start_pos] + "\n" + 
                      content.strip() + "\n" + 
                      file_content[end_pos:])
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
    except FileOperationError:
        raise
    except Exception as e:
        raise FileOperationError(f"Failed to replace section {identifier} in {filepath}: {str(e)}")

def replace_lines(filepath: str, start_line: int, end_line: int, content: str) -> None:
    """Replace specific line range in a file.
    
    Args:
        filepath: Target file path
        start_line: First line to replace (1-based)
        end_line: Last line to replace (1-based)
        content: New content
        
    Raises:
        FileOperationError: If line replacement fails
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if start_line < 1 or start_line > len(lines) + 1:
            raise FileOperationError(f"Invalid start line {start_line} for {filepath}\n"
                                   f"File has {len(lines)} lines")
        if end_line < start_line or end_line > len(lines) + 1:
            raise FileOperationError(f"Invalid end line {end_line} for {filepath}\n"
                                   f"Must be between {start_line} and {len(lines)}")
        
        # Convert to 0-based indexing
        start_idx = start_line - 1
        end_idx = end_line - 1
        
        # Split new content into lines
        new_lines = content.split('\n')
        if not content.endswith('\n'):
            new_lines[-1] += '\n'
        else:
            new_lines.append('')
        
        # Replace lines
        lines[start_idx:end_idx+1] = new_lines
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            
    except FileOperationError:
        raise
    except Exception as e:
        raise FileOperationError(f"Failed to replace lines {start_line}-{end_line} in {filepath}: {str(e)}")

def append_content(filepath: str, content: str) -> None:
    """Append content to a file.
    
    Args:
        filepath: Target file path
        content: Content to append
        
    Raises:
        FileOperationError: If append operation fails
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Ensure content ends with newline
        if not content.endswith('\n'):
            content += '\n'
        
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        raise FileOperationError(f"Failed to append to {filepath}: {str(e)}")

def create_file(filepath: str, content: str) -> None:
    """Create a new file with content.
    
    Args:
        filepath: Target file path
        content: File content
        
    Raises:
        FileOperationError: If file creation fails
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        if os.path.exists(filepath):
            raise FileOperationError(f"File already exists: {filepath}\n"
                                   f"Use a different operation to modify existing files")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except FileOperationError:
        raise
    except Exception as e:
        raise FileOperationError(f"Failed to create {filepath}: {str(e)}")

def process_update(update: Dict[str, Any], backups: Dict[str, str]) -> None:
    """Process a single update operation.
    
    Args:
        update: Update operation configuration
        backups: Mapping of file paths to their backups
        
    Raises:
        BatchUpdateError: If update fails
    """
    try:
        filepath = update.get('file')
        if not filepath:
            raise ConfigError("Missing 'file' field in update")
        
        operation = update.get('operation')
        if not operation:
            raise ConfigError("Missing 'operation' field in update")
        
        # Create backup if we haven't already
        if filepath not in backups:
            backups[filepath] = create_backup(filepath)
        
        # Convert legacy paths
        filepath = convert_legacy_path(filepath)
        
        if operation == 'replace_section':
            identifier = update.get('identifier')
            content = update.get('content')
            if not identifier or not content:
                raise ConfigError("Missing 'identifier' or 'content' for replace_section")
            replace_section(filepath, identifier, content)
            
        elif operation == 'replace_lines':
            start_line = update.get('start_line')
            end_line = update.get('end_line')
            content = update.get('content')
            if not all([start_line, end_line, content]):
                raise ConfigError("Missing required fields for replace_lines")
            replace_lines(filepath, start_line, end_line, content)
            
        elif operation == 'append':
            content = update.get('content')
            if not content:
                raise ConfigError("Missing 'content' for append")
            append_content(filepath, content)
            
        elif operation == 'create_file':
            content = update.get('content', '')
            create_file(filepath, content)
            
        else:
            raise ConfigError(f"Unknown operation: {operation}")
            
    except Exception as e:
        raise BatchUpdateError(f"Failed to process update for {filepath}: {str(e)}")

def process_updates() -> None:
    """Process all pending updates from the updates file."""
    update_file = "memory-bank/pending_updates.json"
    backups: Dict[str, str] = {}
    
    try:
        # Load updates
        try:
            with open(update_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"No pending updates file found at {update_file}")
            return
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON in updates file: {str(e)}")
        
        updates = data.get('updates', [])
        if not updates:
            print("No updates to process")
            return
        
        print(f"Processing {len(updates)} updates...")
        
        # Process each update
        success_count = 0
        failed_count = 0
        
        for i, update in enumerate(updates):
            try:
                print(f"[{i+1}/{len(updates)}] Processing update...")
                process_update(update, backups)
                success_count += 1
            except Exception as e:
                print(f"Error processing update {i+1}: {str(e)}")
                failed_count += 1
                
                # Try to restore from backup
                filepath = update.get('file')
                if filepath and filepath in backups:
                    try:
                        restore_from_backup(backups[filepath], filepath)
                        print(f"Restored {filepath} from backup")
                    except Exception as restore_error:
                        print(f"Failed to restore from backup: {str(restore_error)}")
        
        print(f"\nUpdates completed: {success_count} successful, {failed_count} failed")
        
        # Clear the updates file
        with open(update_file, 'w', encoding='utf-8') as f:
            json.dump({"updates": []}, f)
            
    except Exception as e:
        print(f"Fatal error processing updates: {str(e)}", file=sys.stderr)
        # Try to restore all backups
        for filepath, backup_path in backups.items():
            try:
                restore_from_backup(backup_path, filepath)
                print(f"Restored {filepath} from backup")
            except Exception as restore_error:
                print(f"Failed to restore {filepath}: {str(restore_error)}")
        sys.exit(1)

if __name__ == "__main__":
    process_updates()