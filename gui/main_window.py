"""
Main window implementation for File Falcon Pro.
This module contains the primary UI components and layout.
"""
import time
from typing import Optional

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QStatusBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from config import Config
from operations.file_extensions import CATEGORIES_MAP
from operations.file_operations import FileOperationConfig, execute_changes, preview_changes


class LogHandler:
    """Handler for displaying log messages in the UI."""
    
    def __init__(self, log_area: QTextEdit):
        """Initialize the log handler.
        
        Args:
            log_area: Text edit widget to display logs
        """
        self.log_area = log_area
    
    def log(self, message: str, level: str = "info") -> None:
        """Log a message to the UI.
        
        Args:
            message: Message to log
            level: Log level (info, success, warning, error)
        """
        timestamp = time.strftime("%H:%M:%S")
        
        # Set color based on level
        if level == "success":
            color = "green"
        elif level == "warning":
            color = "orange"
        elif level == "error":
            color = "red"
        else:  # info
            color = "white"
        
        # Format and append message
        formatted_message = f"<span style='color:gray'>[{timestamp}]</span> <span style='color:{color}'>{message}</span>"
        self.log_area.append(formatted_message)
        
        # Scroll to bottom
        self.log_area.verticalScrollBar().setValue(
            self.log_area.verticalScrollBar().maximum()
        )


class MainWindow(QMainWindow):
    """Main window for the File Falcon Pro application."""
    
    def __init__(self, config: Config):
        """Initialize the main window.
        
        Args:
            config: Application configuration
        """
        super().__init__()
        self.config = config
        
        # Initialize UI components
        self.source_btn = None
        self.dest_btn = None
        self.source_label = None
        self.dest_label = None
        self.category_combo = None
        self.file_type_list = None
        self.mode_basic_radio = None
        self.mode_advanced_radio = None
        self.mode_group = None
        self.keyword_entry = None
        self.contains_radio = None
        self.exact_radio = None
        self.match_type_group = None
        self.move_radio = None
        self.copy_radio = None
        self.operation_group = None
        self.preview_btn = None
        self.execute_btn = None
        self.status_bar = None
        self.log_area = None
        self.log_handler = None
        
        # Set window properties
        self.setWindowTitle("File Falcon Pro")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(640, 480)
        
        # Initialize UI
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize all UI components."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create category selection (moved up before file type selection)
        category_group = QGroupBox("Media Category")
        category_layout = QVBoxLayout()
        category_group.setLayout(category_layout)
        
        self.category_combo = QComboBox()
        self.category_combo.addItems(sorted(CATEGORIES_MAP.keys()))
        self.category_combo.currentTextChanged.connect(self._update_file_types)
        category_layout.addWidget(self.category_combo)
        
        main_layout.addWidget(category_group)
        
        # Create folder selection area
        folder_group = QGroupBox("Folder Selection")
        folder_layout = QGridLayout()
        folder_group.setLayout(folder_layout)
        
        # Source folder button
        self.source_btn = QPushButton("Select Source Folder")
        self.source_btn.clicked.connect(lambda: self._select_folder("source"))
        self.source_label = QLabel("No source folder selected")
        self.source_label.setStyleSheet("color: gray;")
        
        # Destination folder button
        self.dest_btn = QPushButton("Select Destination Folder")
        self.dest_btn.clicked.connect(lambda: self._select_folder("destination"))
        self.dest_label = QLabel("No destination folder selected")
        self.dest_label.setStyleSheet("color: gray;")
        
        # Add to folder layout
        folder_layout.addWidget(QLabel("Source:"), 0, 0)
        folder_layout.addWidget(self.source_btn, 0, 1)
        folder_layout.addWidget(self.source_label, 0, 2)
        folder_layout.addWidget(QLabel("Destination:"), 1, 0)
        folder_layout.addWidget(self.dest_btn, 1, 1)
        folder_layout.addWidget(self.dest_label, 1, 2)
        
        # Add folder group to main layout
        main_layout.addWidget(folder_group)
        
        # Create mode selection
        mode_group = QGroupBox("Mode")
        mode_layout = QHBoxLayout()
        mode_group.setLayout(mode_layout)
        
        self.mode_basic_radio = QRadioButton("Basic Mode")
        self.mode_advanced_radio = QRadioButton("Advanced Mode")
        self.mode_basic_radio.setChecked(True)
        
        self.mode_group = QButtonGroup()
        self.mode_group.addButton(self.mode_basic_radio)
        self.mode_group.addButton(self.mode_advanced_radio)
        self.mode_group.buttonClicked.connect(self._on_mode_change)
        
        mode_layout.addWidget(self.mode_basic_radio)
        mode_layout.addWidget(self.mode_advanced_radio)
        main_layout.addWidget(mode_group)
        
        # Create file type selection
        filetype_group = QGroupBox("File Types")
        filetype_layout = QVBoxLayout()
        filetype_group.setLayout(filetype_layout)
        
        self.file_type_list = QListWidget()
        self.file_type_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        filetype_layout.addWidget(self.file_type_list)
        
        main_layout.addWidget(filetype_group)
        
        # Create advanced options
        advanced_group = QGroupBox("Advanced Options")
        advanced_layout = QVBoxLayout()
        advanced_group.setLayout(advanced_layout)
        
        # Keyword entry
        keyword_layout = QHBoxLayout()
        keyword_layout.addWidget(QLabel("Keyword or Filename:"))
        self.keyword_entry = QLineEdit()
        self.keyword_entry.setPlaceholderText("Enter keyword or filename...")
        keyword_layout.addWidget(self.keyword_entry)
        advanced_layout.addLayout(keyword_layout)
        
        # Match type options
        match_layout = QHBoxLayout()
        self.contains_radio = QRadioButton("Contains")
        self.exact_radio = QRadioButton("Exact Match")
        self.contains_radio.setChecked(True)
        
        self.match_type_group = QButtonGroup()
        self.match_type_group.addButton(self.contains_radio)
        self.match_type_group.addButton(self.exact_radio)
        
        match_layout.addWidget(QLabel("Match Type:"))
        match_layout.addWidget(self.contains_radio)
        match_layout.addWidget(self.exact_radio)
        match_layout.addStretch()
        advanced_layout.addLayout(match_layout)
        
        main_layout.addWidget(advanced_group)
        
        # Show/hide advanced options based on mode
        advanced_group.setVisible(False)
        self.mode_advanced_radio.toggled.connect(lambda checked: advanced_group.setVisible(checked))
        
        # Operation type selection
        operation_group = QGroupBox("Operation Type")
        operation_layout = QHBoxLayout()
        operation_group.setLayout(operation_layout)
        
        self.move_radio = QRadioButton("Move Files")
        self.copy_radio = QRadioButton("Copy Files")
        self.copy_radio.setChecked(True)
        
        self.operation_group = QButtonGroup()
        self.operation_group.addButton(self.move_radio)
        self.operation_group.addButton(self.copy_radio)
        
        operation_layout.addWidget(self.move_radio)
        operation_layout.addWidget(self.copy_radio)
        main_layout.addWidget(operation_group)
        
        # Create log area
        log_group = QGroupBox("Operation Log")
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("background-color: #1e1e1e; color: white;")
        self.log_area.setMinimumHeight(150)
        log_layout.addWidget(self.log_area)
        
        main_layout.addWidget(log_group)
        
        # Create log handler
        self.log_handler = LogHandler(self.log_area)
        self.log_handler.log("File Falcon Pro started. Ready for operations.")
        
        # Create button area
        button_layout = QHBoxLayout()
        
        self.preview_btn = QPushButton("Preview Changes")
        self.preview_btn.setIcon(QIcon.fromTheme("document-preview"))
        self.preview_btn.clicked.connect(self._preview_changes)
        
        self.execute_btn = QPushButton("Execute Changes")
        self.execute_btn.setIcon(QIcon.fromTheme("document-save"))
        self.execute_btn.clicked.connect(self._execute_changes)
        
        button_layout.addStretch()
        button_layout.addWidget(self.preview_btn)
        button_layout.addWidget(self.execute_btn)
        main_layout.addLayout(button_layout)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Initialize file types
        self._update_file_types()
        
        # Update labels if paths are already set
        self._update_folder_labels()
    
    def _select_folder(self, folder_type: str) -> None:
        """Handle selecting a folder.
        
        Args:
            folder_type: Either 'source' or 'destination'
        """
        folder_path = QFileDialog.getExistingDirectory(self, f"Select {folder_type.capitalize()} Folder")
        if not folder_path:
            return
            
        if folder_type == "source":
            self.config.set_source_folder_path(folder_path)
            self.source_label.setText(folder_path)
            self.source_label.setStyleSheet("color: white;")
            self.status_bar.showMessage(f"Source folder set to: {folder_path}", 3000)
            self.log_handler.log(f"Source folder set to: {folder_path}")
        elif folder_type == "destination":
            self.config.set_dest_folder_path(folder_path)
            self.dest_label.setText(folder_path)
            self.dest_label.setStyleSheet("color: white;")
            self.status_bar.showMessage(f"Destination folder set to: {folder_path}", 3000)
            self.log_handler.log(f"Destination folder set to: {folder_path}")
    
    def _update_folder_labels(self) -> None:
        """Update folder labels with current paths."""
        source_path = self.config.get_source_folder_path()
        if source_path:
            self.source_label.setText(str(source_path))
            self.source_label.setStyleSheet("color: white;")
        
        dest_path = self.config.get_dest_folder_path()
        if dest_path:
            self.dest_label.setText(str(dest_path))
            self.dest_label.setStyleSheet("color: white;")
    
    def _update_file_types(self) -> None:
        """Update the file types list based on selected category."""
        selected_category = self.category_combo.currentText()
        self.file_type_list.clear()
        
        if selected_category in CATEGORIES_MAP:
            for ext in sorted(CATEGORIES_MAP[selected_category]):
                self.file_type_list.addItem(ext)
                
        self.log_handler.log(f"Selected category: {selected_category}")
    
    def _on_mode_change(self, button) -> None:
        """Handle mode change between Basic and Advanced.
        
        Args:
            button: The radio button that was clicked
        """
        is_advanced = button == self.mode_advanced_radio
        mode = "Advanced" if is_advanced else "Basic"
        self.config.set_mode(mode)
        self.log_handler.log(f"Switched to {mode} mode")
    
    def _get_file_operation_config(self) -> Optional[FileOperationConfig]:
        """Create a FileOperationConfig based on current UI state.
        
        Returns:
            FileOperationConfig if valid, None otherwise
        """
        source_path = self.config.get_source_folder_path()
        dest_path = self.config.get_dest_folder_path()
        
        # Validate paths
        if not source_path or not dest_path:
            self.log_handler.log("Missing folders: Please select both source and destination folders", "error")
            QMessageBox.warning(
                self, 
                "Missing Folders", 
                "Please select both source and destination folders."
            )
            return None
        
        # Get selected file types
        selected_types = [
            self.file_type_list.item(i).text() 
            for i in range(self.file_type_list.count()) 
            if self.file_type_list.item(i).isSelected()
        ]
        
        if not selected_types:
            self.log_handler.log("No file types selected: Please select at least one file type", "error")
            QMessageBox.warning(
                self, 
                "No File Types Selected", 
                "Please select at least one file type."
            )
            return None
        
        # Create config
        try:
            operation_type = "Move" if self.move_radio.isChecked() else "Copy"
            mode = "Advanced" if self.mode_advanced_radio.isChecked() else "Basic" 
            match_type = "Contains" if self.contains_radio.isChecked() else "Exact Match"
            
            self.log_handler.log(f"Configuration: {operation_type} in {mode} mode with {len(selected_types)} file types")
            if mode == "Advanced":
                self.log_handler.log(f"Advanced options: {match_type} match with keyword '{self.keyword_entry.text()}'")
                
            return FileOperationConfig(
                folder_path=str(source_path),
                dest_folder_path=str(dest_path),
                mode=mode,
                selected_category=self.category_combo.currentText(),
                selected_types=selected_types,
                keyword=self.keyword_entry.text(),
                match_type=match_type,
                operation_type=operation_type,
            )
        except ValueError as e:
            self.log_handler.log(f"Configuration error: {str(e)}", "error")
            QMessageBox.critical(self, "Configuration Error", str(e))
            return None
    
    def _preview_changes(self) -> None:
        """Preview the file changes without executing them."""
        config = self._get_file_operation_config()
        if not config:
            return
            
        self.status_bar.showMessage("Previewing changes...")
        self.log_handler.log("Starting preview operation...", "info")
        
        # Connect the log handler to the operations module
        class UILogAdapter:
            def __init__(self, log_handler):
                self.log_handler = log_handler
                
            def __call__(self, message):
                self.log_handler.log(message)
                
        # Override rich print function to capture output
        import operations.file_operations
        original_print = operations.file_operations.console.print
        
        def ui_print(message, *args, **kwargs):
            original_print(message, *args, **kwargs)
            if hasattr(message, "style") and message.style == "bold red":
                self.log_handler.log(str(message), "error")
            elif hasattr(message, "style") and message.style == "bold green":
                self.log_handler.log(str(message), "success")
            elif hasattr(message, "style") and message.style == "yellow":
                self.log_handler.log(str(message), "warning")
            else:
                self.log_handler.log(str(message), "info")
        
        operations.file_operations.console.print = ui_print
        
        try:
            results = preview_changes(config)
            
            if not results:
                self.log_handler.log("No files found matching your criteria.", "warning")
            else:
                total_files = sum(len(files) for files in results.values())
                self.log_handler.log(f"Preview complete: Found {total_files} matching files", "success")
        finally:
            # Restore original print function
            operations.file_operations.console.print = original_print
            
        self.status_bar.showMessage("Preview complete", 3000)
    
    def _execute_changes(self) -> None:
        """Execute the file changes based on current configuration."""
        config = self._get_file_operation_config()
        if not config:
            return
            
        # Confirm operation, especially for moves
        if config.operation_type == "Move":
            self.log_handler.log("Waiting for move operation confirmation...", "warning")
            result = QMessageBox.question(
                self,
                "Confirm Move Operation",
                "You are about to MOVE files from the source directory. This operation cannot be undone. Continue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if result != QMessageBox.StandardButton.Yes:
                self.log_handler.log("Move operation cancelled by user", "warning")
                return
        
        # Execute changes
        self.status_bar.showMessage(f"Executing {config.operation_type.lower()} operation...")
        self.log_handler.log(f"Starting {config.operation_type} operation...", "info")
        
        # Override rich print function to capture output
        import operations.file_operations
        original_print = operations.file_operations.console.print
        
        def ui_print(message, *args, **kwargs):
            original_print(message, *args, **kwargs)
            if hasattr(message, "style") and message.style == "bold red":
                self.log_handler.log(str(message), "error")
            elif hasattr(message, "style") and message.style == "bold green":
                self.log_handler.log(str(message), "success")
            elif hasattr(message, "style") and message.style == "yellow":
                self.log_handler.log(str(message), "warning")
            else:
                self.log_handler.log(str(message), "info")
        
        operations.file_operations.console.print = ui_print
        
        try:
            success = execute_changes(config)
            
            if success:
                self.log_handler.log("Operation completed successfully", "success")
                self.status_bar.showMessage("Operation completed successfully", 5000)
            else:
                self.log_handler.log("Operation completed with errors", "error")
                self.status_bar.showMessage("Operation completed with errors", 5000)
        finally:
            # Restore original print function
            operations.file_operations.console.print = original_print
