from typing import Callable

import pygame_gui as pygui

from lib.observer import Listener
from src.UI_elements import import_button, import_label
from .get_input_path_popup import GetInputPathPopup


class ImportForm(Listener):

    def __init__(self, supported_formats: list[str], set_input_path: Callable):
        super().__init__()
        self.button = import_button()
        self.label = import_label()
        self.input_getter_popup = GetInputPathPopup(supported_formats)

        self.input_getter_popup.add_listeners(
            set_input_path,
            self.label.set_text,
        )

    def update(self, event):
        if event.type == pygui.UI_BUTTON_PRESSED:
            if event.ui_element == self.button:
                self.input_getter_popup.show()
