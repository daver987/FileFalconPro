"""
File operation utilities for File Falcon Pro.
This module handles file system operations such as moving and copying files.
"""
import logging
import os
import shutil
from typing import Dict, List, Literal

from pydantic import BaseModel, Field, field_validator
from rich.console import Console

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("file_operations")

# Setup rich console for prettier output
console = Console()


class FileOperationConfig(BaseModel):
    """Configuration model for file operations."""
    
    folder_path: str = Field(..., description="The folder path to organize.")
    dest_folder_path: str = Field(..., description="The destination folder path.")
    mode: Literal["Basic", "Advanced"]
    selected_category: str
    selected_types: List[str]
    keyword: str = ""
    match_type: Literal["Contains", "Exact Match"] = "Contains"
    operation_type: Literal["Move", "Copy"] = "Copy"

    @field_validator("folder_path", "dest_folder_path")
    @classmethod
    def validate_paths(cls, v: str) -> str:
        """Validate that paths exist."""
        if v and not os.path.exists(v):
            raise ValueError(f"Path does not exist: {v}")
        return v


def preview_changes(config: FileOperationConfig) -> Dict[str, List[str]]:
    """
    Preview file changes without executing them.
    
    Args:
        config: File operation configuration
        
    Returns:
        Dictionary of matched files and their destinations
    """
    if not config.selected_types:
        console.print("[bold red]No file types selected.[/bold red]")
        return {}

    console.print(f"[bold blue]Scanning folder:[/bold blue] {config.folder_path}")
    
    matched_files = {}
    try:
        for root, _, files in os.walk(config.folder_path):
            for file in files:
                if _file_matches(file, config):
                    src_path = os.path.join(root, file)
                    dest_dir = os.path.join(config.dest_folder_path, config.selected_category)
                    dest_path = os.path.join(dest_dir, file)
                    
                    relative_src = os.path.relpath(src_path, config.folder_path)
                    if config.selected_category not in matched_files:
                        matched_files[config.selected_category] = []
                    matched_files[config.selected_category].append(relative_src)
                    
                    console.print(f"  [green]• {relative_src}[/green] -> [yellow]{dest_path}[/yellow]")
        
        if not matched_files:
            console.print("[yellow]No files matched your criteria.[/yellow]")
        else:
            console.print(f"\n[bold green]Found {sum(len(files) for files in matched_files.values())} files to {config.operation_type.lower()}.[/bold green]")
            
    except Exception as e:
        logger.error(f"Error previewing changes: {str(e)}")
        console.print(f"[bold red]Error previewing changes:[/bold red] {str(e)}")
    
    return matched_files


def execute_changes(config: FileOperationConfig) -> bool:
    """
    Execute file operations (move or copy).
    
    Args:
        config: File operation configuration
        
    Returns:
        True if successful, False otherwise
    """
    console.print(f"[bold blue]Executing {config.operation_type} operation...[/bold blue]")
    
    success_count = 0
    error_count = 0
    
    try:
        # Create destination category folder if it doesn't exist
        dest_dir = os.path.join(config.dest_folder_path, config.selected_category)
        os.makedirs(dest_dir, exist_ok=True)
        
        for root, _, files in os.walk(config.folder_path):
            for file in files:
                if _file_matches(file, config):
                    relative_path = os.path.relpath(os.path.join(root, file), config.folder_path)
                    console.print(f"  Processing: [green]{relative_path}[/green]")
                    
                    try:
                        src_path = os.path.join(root, file)
                        dest_path = os.path.join(dest_dir, file)
                        
                        # Check for existing file with same name
                        if os.path.exists(dest_path):
                            base, ext = os.path.splitext(file)
                            counter = 1
                            while os.path.exists(dest_path):
                                new_name = f"{base}_{counter}{ext}"
                                dest_path = os.path.join(dest_dir, new_name)
                                counter += 1
                            console.print(f"    [yellow]File already exists, renamed to: {os.path.basename(dest_path)}[/yellow]")
                        
                        _process_file(src_path, dest_path, config.operation_type)
                        success_count += 1
                    
                    except Exception as e:
                        error_count += 1
                        logger.error(f"Error processing {file}: {str(e)}")
                        console.print(f"    [bold red]Error:[/bold red] {str(e)}")
        
        if success_count > 0:
            console.print(f"\n[bold green]Successfully processed {success_count} files.[/bold green]")
        if error_count > 0:
            console.print(f"[bold red]Encountered errors with {error_count} files.[/bold red]")
        
        console.print("[bold blue]File organization complete.[/bold blue]")
        return success_count > 0 and error_count == 0
    
    except Exception as e:
        logger.error(f"Error executing changes: {str(e)}")
        console.print(f"[bold red]Error executing changes:[/bold red] {str(e)}")
        return False


def _file_matches(file: str, config: FileOperationConfig) -> bool:
    """
    Check if a file matches the criteria specified in the config.
    
    Args:
        file: Filename to check
        config: File operation configuration
        
    Returns:
        True if the file matches, False otherwise
    """
    # Check file extension match
    file_ext = os.path.splitext(file)[1].lower()
    if file_ext not in [ext.lower() for ext in config.selected_types]:
        return False

    # If in Basic mode, we only check extension
    if config.mode != "Advanced":
        return True

    # Advanced mode: check keyword match
    if not config.keyword:  # If no keyword specified, match all files with the extension
        return True
        
    # Check Contains or Exact Match
    if config.match_type == "Contains":
        return config.keyword.lower() in file.lower()
    else:  # Exact Match
        filename = os.path.splitext(file)[0].lower()
        return filename == config.keyword.lower()


def _process_file(src_path: str, dest_path: str, operation_type: str) -> None:
    """
    Process a single file (move or copy).
    
    Args:
        src_path: Source file path
        dest_path: Destination file path
        operation_type: 'Move' or 'Copy'
    """
    try:
        if operation_type == "Move":
            shutil.move(src_path, dest_path)
        else:  # Copy
            shutil.copy2(src_path, dest_path)  # copy2 preserves metadata
    except Exception as e:
        logger.error(f"Error processing file {src_path} to {dest_path}: {str(e)}")
        raise  # Reraise to be caught by the calling function
