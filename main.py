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
from modules.file_operations import preview_changes, execute_changes
import sys
from dotenv import load_dotenv

load_dotenv()

video_extensions = [".mp4", ".avi", ".mkv"]
image_extensions = [".jpg", ".png", ".gif"]
document_extensions = [".txt", ".pdf", ".docx"]

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


def update_file_types():
    selected_category = category_combo.currentText()
    file_type_combo.clear()

    if selected_category == "Videos":
        file_type_combo.addItems(video_extensions)
    elif selected_category == "Images":
        file_type_combo.addItems(image_extensions)
    elif selected_category == "Documents":
        file_type_combo.addItems(document_extensions)


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
    main_window.setGeometry(100, 100, 320, 240)

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
    radio_advanced = QRadioButton("Advanced Mode")
    layout.addWidget(radio_standard)
    layout.addWidget(radio_advanced)
    radio_standard.setChecked(True)

    category_combo = QComboBox()
    category_combo.addItems(["Videos", "Images", "Documents"])
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
        )
    )
    layout.addWidget(execute_button)

    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
