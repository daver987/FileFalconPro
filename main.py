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

from modules.file_extensions import (
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
)
from operations.file_operations import preview_changes, execute_changes
import sys
from dotenv import load_dotenv

load_dotenv()

folder_path = "some_folder"
mode = "Standard"
selected_category = "Videos"
selected_types = [".mp4", ".avi"]
keyword = "sample"
match_type = "Contains"


def select_folder():
    global source_folder_path
    source_folder_path = QFileDialog.getExistingDirectory()
    print(f"Selected source folder: {source_folder_path}")


def select_dest_folder():
    global dest_folder_path
    dest_folder_path = QFileDialog.getExistingDirectory()
    print(f"Selected destination folder: {dest_folder_path}")


def update_file_types(presentation=None):
    selected_category = category_combo.currentText()
    file_type_combo.clear()

    if selected_category == "Video Basic":
        file_type_combo.addItems(video_basic)
    elif selected_category == "Video All":
        file_type_combo.addItems(video_all)
    elif selected_category == "Image Basic":
        file_type_combo.addItems(image_basic)
    elif selected_category == "Image All":
        file_type_combo.addItems(image_all)
    elif selected_category == "Text":
        file_type_combo.addItems(text)
    elif selected_category == "Spreadsheet":
        file_type_combo.addItems(spreadsheet)
    elif selected_category == "PDF":
        file_type_combo.addItems(pdf_documents)
    elif selected_category == "Presentation":
        file_type_combo.addItems(presentation)
    elif selected_category == "Layout":
        file_type_combo.addItems(layout)
    elif selected_category == "Database":
        file_type_combo.addItems(database)
    elif selected_category == "Design":
        file_type_combo.addItems(design)
    elif selected_category == "Markup":
        file_type_combo.addItems(markup)


formats = [
    "Video Basic",
    "Video All",
    "Image Basic",
    "Image All",
    "Text",
    "Spreadsheet",
    "PDF",
    "Presentation",
    "Layout",
    "Database",
    "Design",
    "Markup",
]


def get_selected_folder():
    global source_folder_path
    return source_folder_path


def get_dest_folder():
    global dest_folder_path
    return dest_folder_path


def main():
    global category_combo, file_type_combo

    def get_selected_types():
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

    def get_keyword():
        global keyword_entry
        return keyword_entry.text()

    global radio_contains, radio_exact
    radio_contains = QRadioButton("Contains")
    radio_exact = QRadioButton("Exact Match")
    layout.addWidget(radio_contains)
    layout.addWidget(radio_exact)

    def get_match_type():
        global radio_contains, radio_exact
        return "Contains" if radio_contains.isChecked() else "Exact Match"

    radio_contains.setChecked(True)

    def get_selected_category():
        return category_combo.currentText()

    def get_selected_mode():
        return "Standard" if radio_standard.isChecked() else "Advanced"

    preview_button = QPushButton("Preview")
    preview_button.clicked.connect(
        lambda: preview_changes(
            get_selected_folder(),
            get_selected_mode(),
            get_selected_category(),
            get_selected_types(),
            get_keyword(),
            get_match_type(),
        )
    )

    layout.addWidget(preview_button)

    execute_button = QPushButton("Execute")
    execute_button.clicked.connect(
        lambda: execute_changes(
            get_selected_folder(),
            get_dest_folder(),
            get_selected_mode(),
            get_selected_category(),
            get_selected_types(),
            get_keyword(),
            get_match_type(),
            get_operation_type(),
        )
    )
    radio_move = QRadioButton("Move Files")
    radio_move.setChecked(True)
    radio_copy = QRadioButton("Copy Files")
    layout.addWidget(radio_move)
    layout.addWidget(radio_copy)

    def get_operation_type():
        return "Move" if radio_move.isChecked() else "Copy"

    layout.addWidget(execute_button)

    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
