import pygame_gui as pygui
import pygame
from lib.modified.ui_vertical_slider import UIVerticalScrollBar


def progress_chunk_bar() -> pygui.elements.UIProgressBar:
    rr = relative_rect(
        width=630,
        height=30,
        top=500,
        left=160,
    )
    return pygui.elements.UIProgressBar(
        relative_rect=rr,
    )


def progress_t_bar() -> pygui.elements.UIProgressBar:
    rr = relative_rect(
        width=773,
        height=30,
        top=545,
        left=18,
    )
    return pygui.elements.UIProgressBar(
        relative_rect=rr
    )


def error_label() -> pygui.elements.UILabel:
    return pygui.elements.UILabel(
        text="",
        relative_rect=pygame.Rect(15, 0, 700, 50)
    )


def import_button() -> pygui.elements.UIButton:
    return pygui.elements.UIButton(
        relative_rect=pygame.Rect(15, 65, 135, 30),
        text="import file"
    )


def export_button() -> pygui.elements.UIButton:
    return pygui.elements.UIButton(
        relative_rect=pygame.Rect(15, 450, 135, 30),
        text="export to"
    )


def import_label() -> pygui.elements.UILabel:
    rr = relative_rect(
        width=500,
        height=30,
        top=65,
        left=160
    )
    return pygui.elements.UILabel(
        relative_rect=rr,
        text="..."
    )


def export_label() -> pygui.elements.UILabel:
    rr = relative_rect(
        width=500,
        height=30,
        top=450,
        left=160
    )
    return pygui.elements.UILabel(
        relative_rect=rr,
        text="..."
    )


def volume_slider() -> UIVerticalScrollBar:
    rr = relative_rect(
        width=30,
        height=211 + 18,
        left=15,
        top=165 - 10
    )
    slider = UIVerticalScrollBar(
        relative_rect=rr,
        visible_percentage=0.1,
    )
    slider.top_button.kill()
    slider.bottom_button.kill()

    return slider


def render_button() -> pygui.elements.UIButton:
    return pygui.elements.UIButton(
        relative_rect=pygame.Rect(15, 500, 80, 30),
        text='render',
    )


def volume_textbox() -> pygui.elements.UITextEntryLine:
    return pygui.elements.UITextEntryLine(relative_rect=pygame.Rect(15, 390, 60, 30))


def histogram(
        window,
        arr,
        maximum,

        g_width=745,
        g_height=200,
        stick_width=1,
        space_width=1
):
    total_space = stick_width + space_width
    amount_of_sticks = g_width // total_space
    step = len(arr) // amount_of_sticks

    # draw lines
    for i in range(amount_of_sticks):
        height = arr[step * i] / maximum * g_height if arr else 0
        pygame.draw.rect(
            window,
            (255, 255, 255),
            relative_rect(
                width=stick_width,
                height=height + 1,
                left=50 + total_space * i,
                top=170 + g_height - height
            )
        )


def red_line(window, position):
    pygame.draw.rect(
        window,
        (255, 0, 0),
        relative_rect(
            width=748, height=2,
            top=170 + position,
            left=45
        )
    )


def relative_rect(width, height, top, left) -> pygame.Rect:
    return pygame.Rect(left, top, width, height)
