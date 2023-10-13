import sys
import time

import pygame

from lib.observer import Notifier
import src.components as cm
from src.backend import render
from src.init_window import window, pygui_manager, FPS
import data


def fake_input(import_form):
    import_form.input_getter_popup.notify_listeners("D:\\Experiments\\audio_file.mp3")


def fake_output(export_form):
    export_form.output_getter_popup.notify_listeners("D:\\Experiments\\result.mp3")


def main():
    window.fill(color=pygame.Color('#323436'))
    event_manager = Notifier()

    import_form = cm.ImportForm(
        supported_formats=data.options.supported_formats,
        set_input_path=data.input_path.set_full_path
    )
    volume_form = cm.VolumeForm(
        window=window,
        volume_data=data.audio,
        input_path_data=data.input_path
    )
    export_form = cm.ExportForm(
        supported_formats=data.options.supported_formats,
        set_export_path=data.output_path.set_full_path
    )

    render_button = cm.RenderForm(
        output_path_data=data.output_path,
        start_render=render
    )

    event_manager.add_listeners(volume_form, import_form, export_form, render_button)

    fake_input(import_form)
    fake_output(export_form)
    while True:
        time.sleep(1 / FPS)
        pygui_manager.update(1 / FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            event_manager.notify_listeners(event)
            pygui_manager.process_events(event)

        pygui_manager.draw_ui(window)
        pygame.display.update()


if __name__ == '__main__':
    main()
