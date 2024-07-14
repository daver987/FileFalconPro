import sys
from typing import Optional

from PyQt6.QtWidgets import (
	QApplication,
	QComboBox,
	QFileDialog,
	QLabel,
	QLineEdit,
	QListWidget,
	QMainWindow,
	QPushButton,
	QRadioButton,
	QVBoxLayout,
	QWidget,
)

from config import Config
from operations.file_extensions import (
	database,
	design,
	image_all,
	image_basic,
	json_documents,
	layout,
	markup,
	pdf_documents,
	spreadsheet,
	text,
	video_all,
	video_basic,
)
from operations.file_operations import FileOperationConfig, execute_changes, preview_changes

config = Config()


def select_folder(folder_type: str) -> None:
	folder_path = QFileDialog.getExistingDirectory()
	if folder_type == "source":
		config.set_source_folder_path(folder_path)
		print(f"Selected source folder: {folder_path}")
	elif folder_type == "destination":
		config.set_dest_folder_path(folder_path)
		print(f"Selected destination folder: {folder_path}")


def update_file_types() -> None:
	selected_category = category_combo.currentText()
	file_type_combo.clear()

	match selected_category:
		case "Video Basic":
			file_type_combo.addItems(video_basic or [])
		case "Video All":
			file_type_combo.addItems(video_all or [])
		case "Image Basic":
			file_type_combo.addItems(image_basic or [])
		case "Image All":
			file_type_combo.addItems(image_all or [])
		case "Text":
			file_type_combo.addItems(text or [])
		case "JSON":
			file_type_combo.addItems(json_documents or [])
		case "Spreadsheet":
			file_type_combo.addItems(spreadsheet or [])
		case "PDF":
			file_type_combo.addItems((pdf_documents or []) + (layout or []) + (database or []))
		case "Design":
			file_type_combo.addItems(design or [])
		case "Markup":
			file_type_combo.addItems(markup or [])


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


def get_folder_path(folder_type: str) -> str:
	folder_path: Optional[str] = (
		config.get_source_folder_path()
		if folder_type == "source"
		else config.get_dest_folder_path()
	)
	if folder_path is None:
		raise ValueError(f"{folder_type.capitalize()} folder path is not set.")
	return folder_path


def main() -> None:
	global category_combo, file_type_combo, keyword_entry, radio_contains, radio_exact, radio_move

	app = QApplication(sys.argv)

	main_window = QMainWindow()
	main_window.setWindowTitle("File Falcon Pro")
	main_window.setGeometry(100, 100, 640, 480)

	central_widget = QWidget()
	main_window.setCentralWidget(central_widget)
	layout = QVBoxLayout(central_widget)

	for folder_type in ["source", "destination"]:
		button = QPushButton(f"Select {folder_type.capitalize()} Folder")
		button.clicked.connect(lambda checked, ft=folder_type: select_folder(ft))
		layout.addWidget(button)

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

	layout.addWidget(QLabel("Advanced Mode:"))

	keyword_entry = QLineEdit()
	keyword_entry.setPlaceholderText("Enter keyword or filename")
	layout.addWidget(keyword_entry)

	radio_contains = QRadioButton("Contains")
	radio_exact = QRadioButton("Exact Match")
	radio_contains.setChecked(True)
	layout.addWidget(radio_contains)
	layout.addWidget(radio_exact)

	radio_move = QRadioButton("Move Files")
	radio_copy = QRadioButton("Copy Files")
	radio_move.setChecked(True)
	layout.addWidget(radio_move)
	layout.addWidget(radio_copy)

	def get_file_operation_config() -> FileOperationConfig:
		return FileOperationConfig(
			folder_path=get_folder_path("source"),
			dest_folder_path=get_folder_path("destination"),
			mode="Advanced" if radio_advanced.isChecked() else "Basic",
			selected_category=category_combo.currentText(),
			selected_types=[item.text() for item in file_type_combo.selectedItems()],
			keyword=keyword_entry.text(),
			match_type="Contains" if radio_contains.isChecked() else "Exact Match",
			operation_type="Move" if radio_move.isChecked() else "Copy",
		)

	for button_text, operation in [("Preview", preview_changes), ("Execute", execute_changes)]:
		button = QPushButton(button_text)
		button.clicked.connect(lambda checked, op=operation: op(get_file_operation_config()))
		layout.addWidget(button)

	main_window.show()
	sys.exit(app.exec())


if __name__ == "__main__":
	main()
