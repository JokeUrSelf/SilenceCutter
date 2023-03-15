from pydub import AudioSegment
from os.path import exists

from typing import Union

FPS: int = 240
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
TITLE = "Silence Cutter"


# Stores all global variables
class Store:
    error_list = []
    volume_range = [0 for _ in range(0, 186)]
    min_volume: float = .0
    max_possible_volume: float = .0
    format: str = ".mp3"
    output_file_name: str = "untitled"
    supported_formats = [".mp3", ".mp4", ".webm"]

    _input_file_path: Union[str, None] = None
    _output_directory_path: Union[str, None] = None
    _pydub_audio_segment: AudioSegment

    _progress = {"chunk": 0, "t": 0}

    @staticmethod
    def get_progress() -> dict[str, int]:
        return Store._progress

    @staticmethod
    def set_progress(bar, percentage):
        Store._progress[bar] = percentage

    @staticmethod
    def get_pydub_segment() -> AudioSegment:
        return Store._pydub_audio_segment

    @staticmethod
    def set_pydub_segment(value: AudioSegment) -> None:

        val = [x.max for x in value]

        Store.volume_range = val[::len(val) // (len(Store.volume_range) - 1)]
        Store._pydub_audio_segment = value

    @staticmethod
    def get_output_directory_path() -> str:
        return Store._output_directory_path if Store._output_directory_path is not None else ""

    @staticmethod
    def set_output_file_path(value: str) -> None:
        if value in {None, ""}: return

        value = value.replace("/", "\\")
        idx = value.rfind("\\")
        path = value[:idx + 1]

        err_mess = "Error: The save file path is invalid"
        if exists(path):
            Store.error_list_remove_item(err_mess)
        else:
            Store.error_list_add_item(err_mess)
            return

        Store.output_file_name = value[idx + 1:]
        Store._output_directory_path = path

    @staticmethod
    def get_input_file_path() -> str:
        return Store._input_file_path if Store._input_file_path is not None else ""

    @staticmethod
    def error_list_remove_item(value: str):
        if value in Store.error_list:
            Store.error_list.remove(value)

    @staticmethod
    def error_list_add_item(value: str):
        if value in Store.error_list:
            Store.error_list.remove(value)
        Store.error_list.append(value)

    @staticmethod
    def set_input_file_path(value: str) -> None:
        if value in {None, ""}: return
        value.replace("/", "\\")

        err_mess = "Error: The import file path is invalid"

        if Store.path_check(value):
            Store.error_list_remove_item(err_mess)
        else:
            Store.error_list_add_item(err_mess)
            return

        hint: str = "hint: adjust a slider to lower values to eliminate segments with low volume levels."

        if hint not in Store.error_list:
            Store.error_list_add_item(hint)

        try:
            audio_seg: AudioSegment = AudioSegment.from_file(value)
        except:
            Store.error_list_add_item("Error: Couldn't load the file, try checking file format")
            return

        if len(audio_seg) < 50:
            Store.error_list_add_item("Error: the file is either too short or corrupted")
            return
        else:
            Store.set_pydub_segment(audio_seg)
        Store.max_possible_volume = Store.get_pydub_segment().max
        Store.format = value[-4:]
        Store._input_file_path = value

    @staticmethod
    def is_video() -> bool:
        return Store.format in {".mp4", ".webm"}

    @staticmethod
    def path_check(path: str) -> bool:

        return exists(path) and path[path.rfind("."):] in Store.supported_formats

    @staticmethod
    def get_error_list_last() -> str:
        if Store.error_list:
            return Store.error_list[-1]
        return ""

    @staticmethod
    def get_output_file_path():
        return Store.get_output_directory_path() + Store.output_file_name
