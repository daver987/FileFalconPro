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
        self._folder_path = value

    def set_source_folder_path(self, path):
        self._source_folder_path = path

    def get_source_folder_path(self):
        return self._source_folder_path

    def set_dest_folder_path(self, path):
        self._dest_folder_path = path

    def get_dest_folder_path(self):
        return self._dest_folder_path

    def update_file_types(self, presentation=None):
        pass
