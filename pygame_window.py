import sys
import time

import subprocess
import threading

from tkinter import filedialog, Tk
import pygame
import pygame_gui as pygui

import backend
from data import *
from pygame_widgets import Widgets, relative_rect


def init():
    pygame.init()
    pygame.display.set_caption('Silence Cutter')

    icon_image = pygame.image.load("hqicon.png")
    pygame.display.set_icon(icon_image)

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), vsync=1)
    manager = pygui.UIManager(window.get_size(), 'theme.json')

    return window, manager


window, manager = init()


def get_output_file_path():
    pygame.event.set_blocked(None)

    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    file_path: str = filedialog.asksaveasfilename(
        filetypes=[("Media", " ".join(Store.supported_formats))],
        initialfile="untitled",
        parent=root,
    )
    root.destroy()
    pygame.event.set_allowed(None)
    Store.set_output_file_path(file_path)


def get_input_file_path():
    pygame.event.set_blocked(None)
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    file_path: str = filedialog.askopenfilename(filetypes=[("Media", " ".join(Store.supported_formats))], parent=root)
    root.destroy()
    pygame.event.set_allowed(None)
    Store.set_input_file_path(file_path)


def main():
    error_label = Widgets.error_label()
    import_button, import_label = Widgets.import_button(), Widgets.import_label()
    volume_slider, volume_meter = Widgets.volume_slider(), Widgets.volume_meter()

    # volume_slider.sliding_button=500
    #
    export_label = Widgets.export_label()
    #
    render_button = Widgets.render_button()
    render_button.disable()
    #
    format_dropdown = Widgets.format_dropdown()
    format_dropdown.disable()
    #
    progress_chunk_bar: Union[pygui.elements.UIProgressBar, None] = None
    progress_t_bar: Union[pygui.elements.UIProgressBar, None] = None

    rects = []
    volume_range_last = []
    buffered_scroll_position: Union[float, None] = None

    def render_operation():
        nonlocal progress_t_bar, progress_chunk_bar
        backend.render()
        path = Store.get_output_directory_path()

        subprocess.run(f"explorer.exe {path}")
        render_button.enable()
        volume_slider.enable()
        if Store.is_video():
            format_dropdown.enable()
        import_button.enable()
        Store.error_list.clear()

        progress_chunk_bar.kill()
        progress_t_bar.kill()
        progress_chunk_bar = None
        progress_t_bar = None

    thread = threading.Thread(target=render_operation)
    blame_bool: bool = False
    while True:
        time.sleep(1 / FPS)
        for event in pygame.event.get():
            if event.type == pygui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element == volume_meter:
                    if volume_meter.text:
                        symbol: str = volume_meter.text[-1]
                        if symbol not in "123456789.0%":
                            volume_meter.set_text(volume_meter.text[:-1])
            if event.type == pygui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == volume_meter:
                    try:
                        percentage: float = float(volume_meter.text.removesuffix("%"))
                    except ValueError:
                        pass
                    else:
                        if 0 > percentage:
                            percentage = 0
                        elif percentage > 100:
                            percentage = 100
                        cord: float = 200 - percentage * 2
                        volume_slider.sliding_button.set_relative_position((0, cord))
                        volume_slider.scroll_position = cord

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygui.UI_BUTTON_PRESSED:
                if event.ui_element == render_button:
                    get_output_file_path()
                    export_label.set_text(Store.get_output_file_path())
                    progress_chunk_bar = Widgets.progress_chunk_bar()
                    progress_t_bar = Widgets.progress_t_bar()
                    render_button.disable()
                    format_dropdown.disable()
                    import_button.disable()
                    volume_slider.disable()

                    blame_bool = True

                    Store.error_list_add_item("warning: rendering have started")
                    thread.start()

                if event.ui_element == import_button:
                    Store.error_list.clear()
                    get_input_file_path()
                    import_label.set_text(Store.get_input_file_path())
                    if Store.get_input_file_path():
                        render_button.enable()
                        if Store.is_video():
                            format_dropdown.enable()

            manager.process_events(event)

        if error_label.text != Store.get_error_list_last():
            error_label.set_text(Store.get_error_list_last())

        if blame_bool and not thread.is_alive():
            blame_bool = False
            thread.join()
            thread = threading.Thread(target=render_operation)

        if progress_chunk_bar:
            if progress_chunk_bar.current_progress != Store.get_progress()["chunk"]:
                progress_chunk_bar.set_current_progress(Store.get_progress()["chunk"])
            if progress_t_bar != Store.get_progress()["t"]:
                progress_t_bar.set_current_progress(Store.get_progress()["t"])

        window.fill(color=pygame.Color('#323436'))
        if Store.get_error_list_last():
            pygame.draw.rect(window, (59, 52, 54), pygame.Rect(0, 0, 800, 50))

        if volume_range_last != Store.volume_range:
            volume_range_last = Store.volume_range
            rects.clear()
            for i, y in enumerate(Store.volume_range):
                tmp = max(Store.volume_range)
                sample_height: float = 200 * (y / tmp) if tmp else 0

                rects.append(
                    relative_rect(
                        width=2,
                        height=1 + sample_height,
                        margin_left=45 + 4 * i,
                        margin_top=290 + 80 - sample_height
                    )
                )

                pygame.draw.rect(
                    window,
                    (255, 255, 255),
                    rects[-1]
                )
        else:
            for x in rects:
                pygame.draw.rect(window, (255, 255, 255), x)
        if volume_slider.scroll_position != buffered_scroll_position:
            buffered_scroll_position = volume_slider.scroll_position
            slider_percentage: float = 100 - volume_slider.scroll_position / 2
            Store.min_volume = Store.max_possible_volume * slider_percentage / 100
            volume_meter.set_text(f"{slider_percentage}%")
        pygame.draw.rect(window, (255, 0, 0), relative_rect(
            width=745,
            height=2,
            margin_top=170 + volume_slider.scroll_position,
            margin_left=45
        ))
        manager.update(1 / FPS)
        manager.draw_ui(window)
        pygame.display.update()


if __name__ == '__main__':
    main()
