"""
Configuration management for File Falcon Pro.
Handles persistent storage of user preferences and application settings.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class Config:
    """Configuration class for the File Falcon Pro application."""
    
    # Default folder paths
    _source_folder_path: Optional[Path] = None
    _dest_folder_path: Optional[Path] = None
    
    # Default mode options
    _mode: str = "Basic"
    
    # Default file selection
    _selected_category: str = "Video Basic"
    _selected_types: List[str] = field(default_factory=lambda: [".mp4", ".avi"])
    
    # Default advanced options
    _keyword: str = ""
    _match_type: str = "Contains"
    _operation_type: str = "Copy"
    
    def set_source_folder_path(self, path: str) -> None:
        """Set the source folder path.
        
        Args:
            path: Path to the source folder
        """
        if not path:
            return
        self._source_folder_path = Path(path).resolve()
    
    def get_source_folder_path(self) -> Optional[Path]:
        """Get the source folder path.
        
        Returns:
            Path to the source folder or None if not set
        """
        return self._source_folder_path
    
    def set_dest_folder_path(self, path: str) -> None:
        """Set the destination folder path.
        
        Args:
            path: Path to the destination folder
        """
        if not path:
            return
        self._dest_folder_path = Path(path).resolve()
    
    def get_dest_folder_path(self) -> Optional[Path]:
        """Get the destination folder path.
        
        Returns:
            Path to the destination folder or None if not set
        """
        return self._dest_folder_path
    
    def set_mode(self, mode: str) -> None:
        """Set the operation mode.
        
        Args:
            mode: 'Basic' or 'Advanced'
        """
        self._mode = mode
    
    def get_mode(self) -> str:
        """Get the current operation mode.
        
        Returns:
            The current mode ('Basic' or 'Advanced')
        """
        return self._mode
    
    def set_selected_category(self, category: str) -> None:
        """Set the selected file category.
        
        Args:
            category: The selected category (e.g., 'Video Basic')
        """
        self._selected_category = category
    
    def get_selected_category(self) -> str:
        """Get the selected file category.
        
        Returns:
            The selected category
        """
        return self._selected_category
    
    def set_selected_types(self, types: List[str]) -> None:
        """Set the selected file types.
        
        Args:
            types: List of file extensions to operate on
        """
        self._selected_types = types
    
    def get_selected_types(self) -> List[str]:
        """Get the selected file types.
        
        Returns:
            List of file extensions
        """
        return self._selected_types
    
    def set_keyword(self, keyword: str) -> None:
        """Set the keyword for file matching.
        
        Args:
            keyword: Keyword to match in filenames
        """
        self._keyword = keyword
    
    def get_keyword(self) -> str:
        """Get the keyword for file matching.
        
        Returns:
            Current keyword
        """
        return self._keyword
    
    def set_match_type(self, match_type: str) -> None:
        """Set the match type for file matching.
        
        Args:
            match_type: 'Contains' or 'Exact Match'
        """
        self._match_type = match_type
    
    def get_match_type(self) -> str:
        """Get the match type for file matching.
        
        Returns:
            Current match type
        """
        return self._match_type
    
    def set_operation_type(self, operation_type: str) -> None:
        """Set the operation type.
        
        Args:
            operation_type: 'Copy' or 'Move'
        """
        self._operation_type = operation_type
    
    def get_operation_type(self) -> str:
        """Get the operation type.
        
        Returns:
            Current operation type
        """
        return self._operation_type
