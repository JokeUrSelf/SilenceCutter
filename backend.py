import modified_libs.editor as mpe
from data import *
from pydub import AudioSegment
from proglog import ProgressBarLogger


class MyBarLogger(ProgressBarLogger):
    def bars_callback(self, bar, attr, value, old_value=None):
        # Every time the logger progress is updated, this function is called
        percentage: int = int(value / self.bars[bar]['total'] * 100)
        Store.set_progress(bar, percentage)


def get_ranges_of_time(min_volume: float) -> list[list[float]]:
    sound: AudioSegment = Store.get_pydub_segment()
    optimal_range = 100

    arr: list[list[float]] = []
    subarr: list[float] = []
    for millisecond in range(len(sound) - 1):
        sample = sound[millisecond].max
        if sample >= min_volume:
            if subarr and subarr[1] == millisecond:
                subarr[1] = millisecond + 1
            else:
                subarr = [millisecond, millisecond + 1]
        elif subarr:
            if subarr[1] - subarr[0] >= optimal_range:
                arr.append(subarr)
            subarr = []
    if subarr:
        arr.append(subarr)
    return arr


def render() -> None:
    path: str = Store.get_input_file_path()
    save_path: str = Store.get_output_file_path() + Store.format
    min_volume: float = Store.min_volume

    sub_arrays = get_ranges_of_time(min_volume)

    if not all(sub_arrays):
        Store.error_list_add_item("Error: Couldn't calculate ranges of time")
        return

    if Store.is_video():
        general_clip: mpe.VideoFileClip = mpe.VideoFileClip(path)
        clips: list = [general_clip.subclip(x[0] / 1000.0, x[1] / 1000.0) for x in sub_arrays]
        video = mpe.concatenate_videoclips(clips)
        video.write_videofile(save_path, logger=MyBarLogger())
    else:
        general_clip: mpe.AudioFileClip = mpe.AudioFileClip(path)
        clips: list = [general_clip.subclip(x[0] / 1000.0, x[1] / 1000.0) for x in sub_arrays]
        audio = mpe.concatenate_audioclips(clips)
        audio.write_audiofile(save_path, logger=MyBarLogger())