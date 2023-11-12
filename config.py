class Config:
    def __init__(self):
        self._folder_path = "some_folder"
        self._mode = "Standard"
        self._selected_category = "Videos"
        self._selected_types = [".mp4", ".avi"]
        self._keyword = "sample"
        self._match_type = "Contains"
        self._source_folder_path = None
        self._dest_folder_path = None

    @property
    def folder_path(self):
        return self._folder_path

    @folder_path.setter
    def folder_path(self, value):
        # Add validation or preprocessing if necessary
        self._folder_path = value

    # Repeat the pattern of property and setter for each configuration attribute
    # ...

    # The rest of the methods remain unchanged

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
