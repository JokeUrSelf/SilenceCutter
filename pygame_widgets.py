import pygame_gui as pygui
import pygame
from modified_libs.ui_vertical_slider import UIVerticalScrollBar


class Widgets:

    @staticmethod
    def progress_chunk_bar() -> pygui.elements.UIProgressBar:
        rr = relative_rect(
            width=630,
            height=30,
            margin_top=500,
            margin_left=160,
        )
        return pygui.elements.UIProgressBar(
            relative_rect=rr,

        )

    @staticmethod
    def progress_t_bar() -> pygui.elements.UIProgressBar:
        rr = relative_rect(
            width=773,
            height=30,
            margin_top=545,
            margin_left=18,
        )
        return pygui.elements.UIProgressBar(
            relative_rect=rr
        )

    @staticmethod
    def error_label() -> pygui.elements.UILabel:
        return pygui.elements.UILabel(
            text="",
            relative_rect=pygame.Rect(15, 0, 700, 50)
        )

    @staticmethod
    def import_button() -> pygui.elements.UIButton:
        return pygui.elements.UIButton(
            relative_rect=pygame.Rect(15, 65, 135, 30),
            text="import file..."
        )

    @staticmethod
    def import_label() -> pygui.elements.UILabel:
        rr = relative_rect(
            width=500,
            height=30,
            margin_top=65,
            margin_left=160
        )
        return pygui.elements.UILabel(
            relative_rect=rr,
            text=""
        )

    @staticmethod
    def volume_slider() -> UIVerticalScrollBar:
        rr = relative_rect(
            width=30,
            height=211 + 18,
            margin_left=15,
            margin_top=165 - 10
        )
        slider = UIVerticalScrollBar(
            relative_rect=rr,
            visible_percentage=0.1,
        )
        slider.top_button.kill()
        slider.bottom_button.kill()

        return slider



    @staticmethod
    def export_label() -> pygui.elements.UILabel:
        rr = relative_rect(
            width=500,
            height=30,
            margin_top=450,
            margin_left=130
        )
        return pygui.elements.UILabel(
            relative_rect=rr,
            text=""
        )

    @staticmethod
    def render_button() -> pygui.elements.UIButton:
        return pygui.elements.UIButton(
            relative_rect=pygame.Rect(15, 500, 80, 30),
            text='render',
        )

    @staticmethod
    def format_dropdown() -> pygui.elements.UIDropDownMenu:
        return pygui.elements.UIDropDownMenu(
            options_list=[".mp4", ".mp3"],
            relative_rect=pygame.Rect(95, 500, 60, 30),
            starting_option=".mp3"
        )

    @staticmethod
    def volume_meter() -> pygui.elements.UILabel:
        rr = relative_rect(
            width=50,
            height=20,
            margin_top=400,
            margin_left=15
        )
        return pygui.elements.UILabel(
            relative_rect=rr,
            text="100.0%",
        )


def relative_rect(width, height, margin_top, margin_left) -> pygame.Rect:
    return pygame.Rect(margin_left, margin_top, width, height)
