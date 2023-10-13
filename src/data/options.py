class OptionsData:
    def __init__(self, broker):
        self._current_format: str = ".mp3"
        self.supported_formats = [".mp3", ".mp4"]

    @property
    def current_format(self):
        return self._current_format

    @current_format.setter
    def current_format(self, f):
        self._current_format = f

    def is_video(self) -> bool:
        return self._current_format in {".mp4"}
