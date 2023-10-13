from abc import abstractmethod
import pygame
from tkinter import Tk

from lib.observer import Notifier


class TkPopup(Notifier):
    def __init__(self, supported_formats):
        super().__init__()
        self.supported_formats = supported_formats

    @staticmethod
    def create_tk_popup_field():
        pygame.event.set_blocked(None)
        root = Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        return root

    @staticmethod
    def destroy_tk_popup_field(root):
        root.destroy()
        pygame.event.set_allowed(None)

    @abstractmethod
    def show(self):
        root = self.create_tk_popup_field()
        self.destroy_tk_popup_field(root)
