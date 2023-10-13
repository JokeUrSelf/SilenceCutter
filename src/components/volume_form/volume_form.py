import pygame

from src.UI_elements import histogram, red_line

from lib.observer import Listener
from .volume_meter import VolumeMeter
from ...data import AudioData, InputPathData


class VolumeForm(Listener):

    def __init__(self, window, volume_data: AudioData, input_path_data: InputPathData):
        super().__init__()
        self.window = window
        self.volume_data = volume_data
        self.volume_meter = VolumeMeter(volume_data.set_volume_percentage)

        self.volume_meter.value_change_notifier.add_listeners(
            lambda _: window.fill(pygame.Color('#323436')),
            lambda _: histogram(window, self.volume_data.volume_range, self.volume_data.max_volume),
            lambda _: red_line(window, self.volume_meter.slider.scroll_position)
        )
        input_path_data.on_change.add_listeners(
            lambda _: window.fill(pygame.Color('#323436')),
            lambda _: histogram(window, self.volume_data.volume_range, self.volume_data.max_volume),
            lambda _: red_line(window, self.volume_meter.slider.scroll_position)
        )
        self.volume_meter.value_change_notifier.notify_listeners(.0)

    def update(self, data):
        self.volume_meter.update(data)
