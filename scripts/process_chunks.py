#!/usr/bin/env python3
import os
import sys
import json
import argparse
import re
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class ChunkMetadata:
    """Metadata for a text chunk."""
    id: str
    title: str
    start_line: int
    end_line: int
    key_concepts: List[str]
    summary: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

class ChunkingError(Exception):
    """Base exception for text chunking errors."""
    pass

class ConfigurationError(ChunkingError):
    """Raised for specification file issues."""
    pass

class ProcessingError(ChunkingError):
    """Raised for chunk processing issues."""
    pass

def load_specification(spec_path: str) -> Dict:
    """Load and validate chunking specification.
    
    Args:
        spec_path: Path to specification JSON file
    
    Returns:
        Validated specification dictionary
    
    Raises:
        ConfigurationError: If specification is invalid
    """
    try:
        with open(spec_path, 'r', encoding='utf-8') as f:
            spec = json.load(f)
        
        # Validate required fields
        if 'source_file' not in spec:
            raise ConfigurationError("Missing 'source_file' in specification")
        if 'chunks' not in spec or not isinstance(spec['chunks'], list):
            raise ConfigurationError("Missing or invalid 'chunks' array in specification")
        
        # Validate each chunk
        for i, chunk in enumerate(spec['chunks']):
            if not all(k in chunk for k in ['id', 'title', 'start_line', 'end_line']):
                raise ConfigurationError(f"Chunk {i} missing required fields")
            
            # Ensure line numbers are integers
            try:
                chunk['start_line'] = int(chunk['start_line'])
                chunk['end_line'] = int(chunk['end_line'])
            except ValueError:
                raise ConfigurationError(f"Invalid line numbers in chunk {i}")
            
            # Ensure key_concepts is a list
            if 'key_concepts' in chunk and not isinstance(chunk['key_concepts'], list):
                raise ConfigurationError(f"'key_concepts' must be a list in chunk {i}")
            
            # Set defaults for optional fields
            chunk.setdefault('key_concepts', [])
            chunk.setdefault('summary', '')
        
        return spec
    
    except json.JSONDecodeError as e:
        raise ConfigurationError(f"Invalid JSON in specification file: {str(e)}")
    except Exception as e:
        raise ConfigurationError(f"Error loading specification: {str(e)}")

def create_chunk_file(chunk_dir: str, chunk_data: ChunkMetadata, content: str) -> None:
    """Create a file for a single chunk.
    
    Args:
        chunk_dir: Directory for chunk files
        chunk_data: Chunk metadata
        content: Chunk content
    
    Raises:
        ProcessingError: If chunk file creation fails
    """
    try:
        # Create chunk directory
        os.makedirs(chunk_dir, exist_ok=True)
        
        # Create chunk file
        chunk_path = os.path.join(chunk_dir, f"{chunk_data.id}.md")
        
        with open(chunk_path, 'w', encoding='utf-8') as f:
            # Write metadata header
            f.write("---\n")
            json.dump(chunk_data.to_dict(), f, indent=2)
            f.write("\n---\n\n")
            
            # Write content
            f.write(content)
    
    except Exception as e:
        raise ProcessingError(f"Failed to create chunk file {chunk_data.id}: {str(e)}")

def create_index_file(chunk_dir: str, chunks: List[ChunkMetadata], source_file: str) -> None:
    """Create an index file linking all chunks.
    
    Args:
        chunk_dir: Directory containing chunks
        chunks: List of chunk metadata
        source_file: Original source file path
    
    Raises:
        ProcessingError: If index creation fails
    """
    try:
        index_path = os.path.join(chunk_dir, "index.md")
        
        with open(index_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"# Text Chunks Index\n\n")
            f.write(f"Source file: {source_file}\n\n")
            
            # Write table of contents
            f.write("## Table of Contents\n\n")
            for chunk in chunks:
                f.write(f"- [{chunk.title}](#{chunk.id})\n")
            f.write("\n")
            
            # Write detailed entries
            f.write("## Chunks\n\n")
            for chunk in chunks:
                f.write(f"### {chunk.title} {{#{chunk.id}}}\n\n")
                f.write(f"ID: {chunk.id}  \n")
                f.write(f"Lines: {chunk.start_line}-{chunk.end_line}  \n")
                if chunk.key_concepts:
                    f.write(f"Key Concepts: {', '.join(chunk.key_concepts)}  \n")
                if chunk.summary:
                    f.write(f"\n{chunk.summary}\n")
                f.write(f"\n[View chunk]({chunk.id}.md)\n\n")
    
    except Exception as e:
        raise ProcessingError(f"Failed to create index file: {str(e)}")

def process_source_file(source_path: str, chunks: List[Dict]) -> List[ChunkMetadata]:
    """Process source file into chunks.
    
    Args:
        source_path: Path to source file
        chunks: Chunk specifications
    
    Returns:
        List of created chunk metadata
    
    Raises:
        ProcessingError: If source processing fails
    """
    try:
        # Read source file
        with open(source_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        chunk_metadata = []
        
        # Process each chunk
        for chunk_spec in chunks:
            # Create chunk metadata
            metadata = ChunkMetadata(
                id=chunk_spec['id'],
                title=chunk_spec['title'],
                start_line=chunk_spec['start_line'],
                end_line=chunk_spec['end_line'],
                key_concepts=chunk_spec['key_concepts'],
                summary=chunk_spec['summary']
            )
            
            # Validate line numbers
            if metadata.start_line < 1 or metadata.end_line > len(lines):
                raise ProcessingError(
                    f"Invalid line numbers for chunk {metadata.id}: "
                    f"start={metadata.start_line}, end={metadata.end_line}, "
                    f"file has {len(lines)} lines"
                )
            
            # Extract chunk content
            content_lines = lines[metadata.start_line-1:metadata.end_line]
            content = ''.join(content_lines)
            
            # Create chunk directory based on source file name
            source_name = os.path.splitext(os.path.basename(source_path))[0]
            chunk_dir = os.path.join('chunks', source_name)
            
            # Create chunk file
            create_chunk_file(chunk_dir, metadata, content)
            
            chunk_metadata.append(metadata)
        
        # Create index file
        create_index_file(chunk_dir, chunk_metadata, source_path)
        
        return chunk_metadata
    
    except Exception as e:
        raise ProcessingError(f"Error processing source file: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description='Process text files into semantic chunks'
    )
    parser.add_argument('spec_file',
                      help='Path to JSON specification file')
    
    args = parser.parse_args()
    
    try:
        # Load and validate specification
        spec = load_specification(args.spec_file)
        
        # Process source file
        chunk_metadata = process_source_file(spec['source_file'], spec['chunks'])
        
        print(f"Successfully created {len(chunk_metadata)} chunks")
        
        # Print chunk info
        for chunk in chunk_metadata:
            print(f"\nChunk: {chunk.id}")
            print(f"Title: {chunk.title}")
            print(f"Lines: {chunk.start_line}-{chunk.end_line}")
            if chunk.key_concepts:
                print(f"Key concepts: {', '.join(chunk.key_concepts)}")
    
    except ChunkingError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()