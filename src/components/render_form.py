from typing import Callable

import pygame_gui as pygui
from src.UI_elements import render_button, progress_t_bar, progress_chunk_bar

from lib.observer import Listener
from src.data import OutputPath


class RenderForm(Listener):
    def __init__(self, output_path_data: OutputPath, start_render: Callable):
        super().__init__()
        self.button = render_button()
        self.progress_chunk_bar: pygui.elements.UIProgressBar = progress_chunk_bar()
        self.progress_t_bar: pygui.elements.UIProgressBar = progress_t_bar()

        self.button.disable()
        self.progress_chunk_bar.hide()
        self.progress_t_bar.hide()

        output_path_data.on_change(lambda _: self.button.enable())
        self.start_render = start_render

    def update(self, event):
        if event.type == pygui.UI_BUTTON_PRESSED:
            if event.ui_element == self.button:
                self.start_render()
