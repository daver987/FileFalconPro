import os
import shutil


def preview_changes(
    folder_path, mode, selected_category, selected_types, keyword, match_type
):
    # Validation
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
                    elif match_type == "Exact Match" and keyword.lower() == file.lower():
                        print(f"Matched file: {file}")
                else:
                    print(f"Matched file: {file}")

    # Print preview summary
    print("Preview of changes to be made:")
    # ...


def execute_changes(
    folder_path, mode, selected_category, selected_types, keyword, match_type
):
    # Validation logic here (e.g., does folder_path exist?)

    # File scanning logic based on mode, category, and types
    # If in Advanced Mode, also consider keyword and match_type

    print("Executing changes:")

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext in selected_types:
                if mode == "Advanced":
                    if match_type == "Contains" and keyword.lower() in file.lower():
                        print(f"Processing file: {file}")
                        dest = os.path.join(folder_path, selected_category)
                        os.makedirs(dest, exist_ok=True)
                        shutil.move(os.path.join(root, file), os.path.join(dest, file))
                    elif match_type == "Exact Match" and keyword.lower() == file.lower():
                        print(f"Processing file: {file}")
                        dest = os.path.join(folder_path, selected_category)
                        os.makedirs(dest, exist_ok=True)
                        shutil.move(os.path.join(root, file), os.path.join(dest, file))
                else:
                    print(f"Processing file: {file}")
                    dest = os.path.join(folder_path, selected_category)
                    os.makedirs(dest, exist_ok=True)
                    shutil.move(os.path.join(root, file), os.path.join(dest, file))

    print("File organization complete.")
