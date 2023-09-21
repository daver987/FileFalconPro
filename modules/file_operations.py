import os
import shutil


def preview_changes(
    folder_path, mode, selected_category, selected_types, keyword, match_type
):
    if not folder_path or not os.path.exists(folder_path):
        print("Invalid or missing folder path.")
        return
    if not selected_types:
        print("No file types selected.")
        return

    print(f"Scanning folder: {folder_path}")
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext in selected_types:
                if mode == "Advanced":
                    if match_type == "Contains" and keyword.lower() in file.lower():
                        print(f"Matched file: {file}")
                    elif (
                        match_type == "Exact Match" and keyword.lower() == file.lower()
                    ):
                        print(f"Matched file: {file}")
                else:
                    print(f"Matched file: {file}")

    print("Preview of changes to be made:")


def execute_changes(
    folder_path, dest_folder_path, mode, selected_category, selected_types, keyword, match_type, operation_type
):
    print("Executing changes:")

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext in selected_types:
                if mode == "Advanced":
                    if match_type == "Contains" and keyword.lower() in file.lower():
                        print(f"Processing file: {file}")
                        dest = os.path.join(dest_folder_path, selected_category)
                        os.makedirs(dest, exist_ok=True)
                        if operation_type == "Move":
                            shutil.move(os.path.join(root, file), os.path.join(dest, file))
                        else:
                            shutil.copy(os.path.join(root, file), os.path.join(dest, file))
                    elif (
                        match_type == "Exact Match" and keyword.lower() == file.lower()
                    ):
                        print(f"Processing file: {file}")
                        dest = os.path.join(dest_folder_path, selected_category)
                        os.makedirs(dest, exist_ok=True)
                        if operation_type == "Move":
                            shutil.move(os.path.join(root, file), os.path.join(dest, file))
                        else:
                            shutil.copy(os.path.join(root, file), os.path.join(dest, file))
                else:
                    print(f"Processing file: {file}")
                    dest = os.path.join(dest_folder_path, selected_category)
                    os.makedirs(dest, exist_ok=True)
                    if operation_type == "Move":
                        shutil.move(os.path.join(root, file), os.path.join(dest, file))
                    else:
                        shutil.copy(os.path.join(root, file), os.path.join(dest, file))

    print("File organization complete.")
