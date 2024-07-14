from typing import Optional
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QFileDialog,
    QRadioButton,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QLabel,
    QLineEdit,
    QListWidget,
)
from operations.file_extensions import (
    video_basic,
    video_all,
    image_basic,
    image_all,
    spreadsheet,
    layout,
    database,
    design,
    markup,
    pdf_documents,
    text,
    json_documents,
)
from operations.file_operations import (
    preview_changes,
    execute_changes,
    FileOperationConfig,
)
import sys
from config import Config

config = Config()


def select_folder() -> None:
    folder_path = QFileDialog.getExistingDirectory()
    config.set_source_folder_path(folder_path)
    print(f"Selected source folder: {config.get_source_folder_path()}")


def select_dest_folder() -> None:
    folder_path = QFileDialog.getExistingDirectory()
    config.set_dest_folder_path(folder_path)
    print(f"Selected destination folder: {config.get_dest_folder_path()}")


def update_file_types(presentation=None) -> None:
    selected_category = category_combo.currentText()
    file_type_combo.clear()

    if selected_category == "Video Basic" and video_basic is not None:
        file_type_combo.addItems(video_basic)
    elif selected_category == "Video All" and video_all is not None:
        file_type_combo.addItems(video_all)
    elif selected_category == "Image Basic" and image_basic is not None:
        file_type_combo.addItems(image_basic)
    elif selected_category == "Image All" and image_all is not None:
        file_type_combo.addItems(image_all)
    elif selected_category == "Text" and text is not None:
        file_type_combo.addItems(text)
    elif selected_category == "JSON" and json_documents is not None:
        file_type_combo.addItems(json_documents)
    elif selected_category == "Spreadsheet" and spreadsheet is not None:
        file_type_combo.addItems(spreadsheet)
    elif selected_category == "PDF":
        if pdf_documents is not None:
            file_type_combo.addItems(pdf_documents)
        if presentation is not None:
            file_type_combo.addItems(presentation)
        if layout is not None:
            file_type_combo.addItems(layout)
        if database is not None:
            file_type_combo.addItems(database)
    elif selected_category == "Design" and design is not None:
        file_type_combo.addItems(design)
    elif selected_category == "Markup" and markup is not None:
        file_type_combo.addItems(markup)


formats = [
    "Video Basic",
    "Video All",
    "Image Basic",
    "Image All",
    "Text",
    "JSON",
    "Spreadsheet",
    "PDF",
    "Presentation",
    "Layout",
    "Database",
    "Design",
    "Markup",
]


def get_selected_folder() -> str:
    folder_path: Optional[str] = config.get_source_folder_path()
    if folder_path is None:
        raise ValueError("Source folder path is not set.")
    return folder_path


def get_dest_folder() -> str:
    folder_path: Optional[str] = config.get_dest_folder_path()
    if folder_path is None:
        raise ValueError("Destination folder path is not set.")
    return folder_path


def main() -> None:
    global category_combo, file_type_combo

    def get_selected_types() -> list[str]:
        selected_items = file_type_combo.selectedItems()
        return [item.text() for item in selected_items]

    app = QApplication(sys.argv)

    main_window = QMainWindow()
    main_window.setWindowTitle("File Falcon Pro")
    main_window.setGeometry(100, 100, 640, 480)

    layout = QVBoxLayout()
    central_widget = QWidget()
    main_window.setCentralWidget(central_widget)
    central_widget.setLayout(layout)

    select_folder_button = QPushButton("Select Source Folder")
    select_folder_button.clicked.connect(select_folder)
    layout.addWidget(select_folder_button)

    select_dest_folder_button = QPushButton("Select Destination Folder")
    select_dest_folder_button.clicked.connect(select_dest_folder)
    layout.addWidget(select_dest_folder_button)

    radio_standard = QRadioButton("Standard Mode")
    radio_standard.setChecked(True)
    radio_advanced = QRadioButton("Advanced Mode")
    layout.addWidget(radio_standard)
    layout.addWidget(radio_advanced)

    category_combo = QComboBox()
    category_combo.addItems(formats)
    layout.addWidget(category_combo)

    file_type_combo = QListWidget()
    file_type_combo.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
    layout.addWidget(file_type_combo)

    category_combo.currentIndexChanged.connect(update_file_types)
    update_file_types()

    advanced_label = QLabel("Advanced Mode:")
    layout.addWidget(advanced_label)

    global keyword_entry
    keyword_entry = QLineEdit()
    keyword_entry.setPlaceholderText("Enter keyword or filename")
    layout.addWidget(keyword_entry)

    def get_keyword() -> str:
        global keyword_entry
        return keyword_entry.text()

    global radio_contains, radio_exact
    radio_contains = QRadioButton("Contains")
    radio_exact = QRadioButton("Exact Match")
    layout.addWidget(radio_contains)
    layout.addWidget(radio_exact)

    def get_match_type() -> str:
        global radio_contains, radio_exact
        return "Contains" if radio_contains.isChecked() else "Exact Match"

    radio_contains.setChecked(True)

    def get_selected_category() -> str:
        return category_combo.currentText()

    def get_selected_mode() -> str:
        return "Standard" if radio_standard.isChecked() else "Advanced"

    def get_operation_type() -> str:
        return "Move" if radio_move.isChecked() else "Copy"

    preview_button = QPushButton("Preview")
    preview_button.clicked.connect(
        lambda: preview_changes(
            FileOperationConfig(
                folder_path=get_selected_folder(),
                dest_folder_path=get_dest_folder(),
                mode="Advanced" if radio_advanced.isChecked() else "Basic",
                selected_category=get_selected_category(),
                selected_types=get_selected_types(),
                keyword=get_keyword(),
                match_type="Contains" if radio_contains.isChecked() else "Exact Match",
                operation_type="Move" if radio_move.isChecked() else "Copy",
            )
        )
    )
    layout.addWidget(preview_button)

    execute_button = QPushButton("Execute")
    execute_button.clicked.connect(
        lambda: execute_changes(
            FileOperationConfig(
                folder_path=get_selected_folder(),
                dest_folder_path=get_dest_folder(),
                mode="Advanced" if radio_advanced.isChecked() else "Basic",
                selected_category=get_selected_category(),
                selected_types=get_selected_types(),
                keyword=get_keyword(),
                match_type="Contains" if radio_contains.isChecked() else "Exact Match",
                operation_type="Move" if radio_move.isChecked() else "Copy",
            )
        )
    )
    layout.addWidget(execute_button)

    radio_move = QRadioButton("Move Files")
    radio_move.setChecked(True)
    radio_copy = QRadioButton("Copy Files")
    layout.addWidget(radio_move)
    layout.addWidget(radio_copy)

    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
