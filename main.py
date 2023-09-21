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
)
from modules.file_operations import preview_changes, execute_changes
import sys
from dotenv import load_dotenv

load_dotenv()

video_extensions = [".mp4", ".avi", ".mkv"]
image_extensions = [".jpg", ".png", ".gif"]
document_extensions = [".txt", ".pdf", ".docx"]

global folder_path
folder_path = "some_folder"  # This will come from the folder selection dialog
mode = "Standard"  # This will come from the radio buttons
selected_category = "Videos"  # This will come from the category combo box
selected_types = [".mp4", ".avi"]  # This will come from the types combo box
keyword = "sample"  # This will come from the keyword text box
match_type = "Contains"  # This will come from the match type radio buttons


def select_folder():
    global folder_path
    folder_path = QFileDialog.getExistingDirectory()
    print(f"Selected folder: {folder_path}")


def update_file_types():
    selected_category = category_combo.currentText()
    file_type_combo.clear()

    if selected_category == "Videos":
        file_type_combo.addItems(video_extensions)
    elif selected_category == "Images":
        file_type_combo.addItems(image_extensions)
    elif selected_category == "Documents":
        file_type_combo.addItems(document_extensions)


def main():
    global category_combo, file_type_combo

    def get_selected_types():
        global file_type_combo
        return file_type_combo.currentText()

    app = QApplication(sys.argv)

    main_window = QMainWindow()
    main_window.setWindowTitle("File Falcon Pro")
    main_window.setGeometry(100, 100, 320, 240)

    layout = QVBoxLayout()
    central_widget = QWidget()
    main_window.setCentralWidget(central_widget)
    central_widget.setLayout(layout)

    select_folder_button = QPushButton("Select Folder")
    select_folder_button.clicked.connect(select_folder)
    layout.addWidget(select_folder_button)

    radio_standard = QRadioButton("Standard Mode")
    radio_advanced = QRadioButton("Advanced Mode")
    layout.addWidget(radio_standard)
    layout.addWidget(radio_advanced)
    radio_standard.setChecked(True)

    # Category selection combo box
    category_combo = QComboBox()
    category_combo.addItems(["Videos", "Images", "Documents"])
    layout.addWidget(category_combo)

    # File type selection combo box
    file_type_combo = QComboBox()
    layout.addWidget(file_type_combo)

    # Update file types when category changes
    category_combo.currentIndexChanged.connect(update_file_types)
    update_file_types()  # Initialize with default category's file types

    # Advanced Mode Interface
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

    radio_contains.setChecked(True)  # Default to "Contains"

    def get_selected_category():
        return category_combo.currentText()

    def get_selected_mode():
        return "Standard" if radio_standard.isChecked() else "Advanced"

    preview_button = QPushButton("Preview")
    preview_button.clicked.connect(
        lambda: preview_changes(
            get_selected_folder(),  # This function needs to be implemented
            get_selected_mode(),
            get_selected_category(),
            get_selected_types(),  # This function needs to be implemented
            get_keyword(),  # This function needs to be implemented
            get_match_type(),  # This function needs to be implemented
        )
    )

    layout.addWidget(preview_button)

    execute_button = QPushButton("Execute")
    execute_button.clicked.connect(
        lambda: execute_changes(
            folder_path, mode, selected_category, selected_types, keyword, match_type
        )
    )
    layout.addWidget(execute_button)

    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
def get_selected_folder():
    global folder_path
    return folder_path
