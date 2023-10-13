from typing import Callable

import pygame_gui as pygui
from lib.observer import Listener
from src.UI_elements import export_button, export_label
from .get_path_output_popup import GetPathOutputPopup


class ExportForm(Listener):

    def __init__(self, supported_formats: list[str], set_export_path: Callable):
        super().__init__()
        self.button = export_button()
        self.label = export_label()
        self.output_getter_popup = GetPathOutputPopup(supported_formats)
        self.output_getter_popup.add_listeners(set_export_path, self.label.set_text)

    def update(self, event):
        if event.type == pygui.UI_BUTTON_PRESSED:
            if event.ui_element == self.button:
                self.output_getter_popup.show()
