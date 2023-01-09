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

    icon_image = pygame.image.load("favicon.ico")
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
        filetypes=[("Media", ".mp4 .mp3")],
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
    file_path: str = filedialog.askopenfilename(filetypes=[("Media", ".mp4 .mp3")], parent=root)
    root.destroy()
    pygame.event.set_allowed(None)
    Store.set_input_file_path(file_path)


def main():
    error_label = Widgets.error_label()
    import_button, import_label = Widgets.import_button(), Widgets.import_label()
    volume_slider, volume_meter = Widgets.volume_slider(), Widgets.volume_meter()
    #
    export_button, export_label = Widgets.export_button(), Widgets.export_label()
    export_button.disable()
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

    def render_operation():
        nonlocal progress_t_bar, progress_chunk_bar
        backend.render()
        path = Store.get_output_directory_path()

        subprocess.run(f"explorer.exe {path}")
        render_button.enable()
        if Store.is_mp4():
            format_dropdown.enable()
        import_button.enable()
        export_button.enable()
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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygui.UI_BUTTON_PRESSED:
                if event.ui_element == render_button:
                    progress_chunk_bar = Widgets.progress_chunk_bar()
                    progress_t_bar = Widgets.progress_t_bar()
                    render_button.disable()
                    format_dropdown.disable()
                    import_button.disable()
                    export_button.disable()

                    blame_bool = True

                    Store.error_list_add_item("warning: rendering have started")
                    thread.start()

                if event.ui_element == import_button:
                    Store.error_list.clear()
                    get_input_file_path()
                    import_label.set_text(Store.get_input_file_path())
                    if Store.get_input_file_path():
                        export_button.enable()
                        if Store.is_mp4():
                            format_dropdown.enable()

                if event.ui_element == export_button:
                    get_output_file_path()
                    export_label.set_text(Store.get_output_file_path())
                    if Store.get_output_directory_path():
                        render_button.enable()

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
        pygame.draw.rect(window, (59, 52, 54), pygame.Rect(0, 0, 800, 50))

        if Store.volume_range is not volume_range_last:
            volume_range_last = Store.volume_range
            rects.clear()
            for i, y in enumerate(Store.volume_range):
                tmp = max(Store.volume_range)
                sample_height: float = 200 * (y / tmp) if tmp else 0

                rects.append(
                    relative_rect(
                        width=10,
                        height=1 + sample_height,
                        margin_left=45 + 15 * i,
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

        slider_percentage = 100 - volume_slider.scroll_position / 2
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
