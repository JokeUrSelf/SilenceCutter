from typing import Callable

import pygame_gui as pygui
from lib.observer import Listener, Notifier
from src.UI_elements import volume_slider, volume_textbox


class VolumeMeter(Listener):
    def __init__(self, set_percentage: Callable):
        super().__init__()
        self.textbox = volume_textbox()
        self.slider = volume_slider()
        self.value_change_notifier = Notifier()
        self.value_change_notifier.add_listeners(
            set_percentage,
            self.assign_value_to_textbox,
            self.slider.set_percentage,
        )
        self.value_change_notifier.notify_listeners(.0)

    def get_textbox_value(self):
        try:
            percentage: float = float(self.textbox.text.replace("%", ""))
        except ValueError:
            print("Value in volume meter textbox is not a number")
        else:
            if percentage < 0:
                percentage = 0
            elif percentage > 100:
                percentage = 100

            return percentage

    def assign_value_to_textbox(self, value):
        self.textbox.set_text(f"{value}%")

    def sanitize_textbox_value(self):
        if self.textbox.text:
            symbol: str = self.textbox.text[-1]
            if symbol not in "123456789.0%":
                self.textbox.set_text(self.textbox.text[:-1])

    def update(self, e):
        if e.type == pygui.UI_TEXT_ENTRY_CHANGED:
            if e.ui_element == self.textbox:
                self.sanitize_textbox_value()

        if e.type == pygui.UI_TEXT_ENTRY_FINISHED:
            if e.ui_element == self.textbox:
                value = self.get_textbox_value()
                self.value_change_notifier.notify_listeners(
                    value if value else self.slider.get_percentage()
                )

        if e.type == self.slider.type:
            if e.ui_element == self.slider:
                self.value_change_notifier.notify_listeners(
                    self.slider.get_percentage()
                )
