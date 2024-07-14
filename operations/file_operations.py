import os
import shutil
from typing import Literal

from pydantic import BaseModel, Field, field_validator
from rich import print


class FileOperationConfig(BaseModel):
	folder_path: str = Field(..., description="The folder path to organize.")
	dest_folder_path: str = Field(..., description="The destination folder path.")
	mode: Literal["Basic", "Advanced"]
	selected_category: str
	selected_types: list[str]
	keyword: str = ""
	match_type: Literal["Contains", "Exact Match"] = "Contains"
	operation_type: Literal["Move", "Copy"] = "Copy"

	@field_validator("folder_path", "dest_folder_path")
	def validate_paths(cls, v: str) -> str:
		if v and not os.path.exists(v):
			raise ValueError(f"Path does not exist: {v}")
		return v


def preview_changes(config: FileOperationConfig) -> None:
	if not config.selected_types:
		print("No file types selected.")
		return

	print(f"Scanning folder: {config.folder_path}")
	for root, _, files in os.walk(config.folder_path):
		for file in files:
			if _file_matches(file, config):
				print(f"Matched file: {file}")

	print("Preview of changes to be made:")


def execute_changes(config: FileOperationConfig) -> None:
	print("Executing changes:")

	for root, _, files in os.walk(config.folder_path):
		for file in files:
			if _file_matches(file, config):
				print(f"Processing file: {file}")
				_process_file(root, file, config)

	print("File organization complete.")


def _file_matches(file: str, config: FileOperationConfig) -> bool:
	file_ext = os.path.splitext(file)[1]
	if file_ext not in config.selected_types:
		return False

	if config.mode == "Advanced":
		if config.match_type == "Contains" and config.keyword.lower() in file.lower():
			return True
		if config.match_type == "Exact Match" and config.keyword.lower() == file.lower():
			return True
	else:
		return True

	return False


def _process_file(root: str, file: str, config: FileOperationConfig) -> None:
	dest = os.path.join(config.dest_folder_path, config.selected_category)
	os.makedirs(dest, exist_ok=True)
	src_path = os.path.join(root, file)
	dest_path = os.path.join(dest, file)

	if config.operation_type == "Move":
		shutil.move(src_path, dest_path)
	else:
		shutil.copy(src_path, dest_path)
