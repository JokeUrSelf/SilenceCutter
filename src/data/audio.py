from pydub import AudioSegment

from lib.path import Path
from lib.pub_sub import Subscriber


class AudioData(Subscriber):

    def __init__(self, broker):
        super().__init__("audio_data")
        broker.subscribe("input_path", self)
        self._volume_percentage: float = .0
        self._volume_range = []
        self.pivot_volume: float = .0
        self.max_volume = .0
        self.fps = None

    def get_volume_percentage(self):
        return self._volume_percentage

    def set_volume_percentage(self, percentage):
        self._volume_percentage = percentage

    @property
    def volume_range(self):
        return self._volume_range

    @volume_range.setter
    def volume_range(self, x):
        self._volume_range = x

    def notify(self, mark, path: Path):
        if mark == "input_path":
            audio_segment = AudioSegment.from_file(path.full_path)
            self.max_volume = audio_segment.max
            self.volume_range = [x.max for x in audio_segment]
            self.fps = audio_segment.frame_rate

            # if path.file_format not in ".wav.flac.ogg.mp3.mp4.raw":
            #     # convert
            #     ffmpeg.input(path.full_path).output("tmp.wav").run()
            #     self._audio_segment = AudioSegment.from_file("tmp.wav")
            #
            #     try:
            #         ManagedThread(target=os.remove("tmp.wav"))
            #     except FileNotFoundError:
            #         print("Temporary file does not exist")
            # else:
            #     self._audio_segment = AudioSegment.from_file(path.full_path)
