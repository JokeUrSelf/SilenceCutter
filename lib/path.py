from os.path import exists

class Path:
    def __init__(self):
        super().__init__()
        self._file_path = ["", "", ""]

    @property
    def full_path(self):
        return "".join(self._file_path)

    def set_full_path(self, path: str):
        extract_file_format = path[path.rfind("."):].replace("/", "")
        extract_file_name = path[:path.rfind(".")][path.rfind("/") + 1:]
        extract_file_directory = path[:path.rfind("/") + 1]

        self._file_path = [
            extract_file_directory,
            extract_file_name,
            extract_file_format
        ]

    @full_path.setter
    def full_path(self, path: str):
        self.set_full_path(path)

    @property
    def directory_path(self): return self._file_path[0]

    @directory_path.setter
    def directory_path(self, path: str):
        if exists(path): return
        self._file_path[0] = path

    @property
    def file_name(self): return self._file_path[1]

    @file_name.setter
    def file_name(self, s: str): self._file_path[1] = s

    @property
    def file_format(self): return self._file_path[2]

    @file_format.setter
    def file_format(self, s: str): self._file_path[2] = s
