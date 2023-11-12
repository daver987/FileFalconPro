class Config:
    def __init__(self):
        # Initialize default configuration settings
        self.folder_path = "some_folder"
        self.mode = "Standard"
        self.selected_category = "Videos"
        self.selected_types = [".mp4", ".avi"]
        self.keyword = "sample"
        self.match_type = "Contains"
        self.source_folder_path = None
        self.dest_folder_path = None

    def select_folder(self):
        # This method will be used to select the source folder
        pass

    def select_dest_folder(self):
        # This method will be used to select the destination folder
        pass

    def get_selected_folder(self):
        return self.source_folder_path

    def get_dest_folder(self):
        return self.dest_folder_path

    def update_file_types(self, presentation=None):
        # This method will be used to update the file types based on the selected category
        pass

    # Additional methods and properties can be added here as needed
