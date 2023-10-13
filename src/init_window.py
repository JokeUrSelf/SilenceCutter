import pygame
import pygame_gui as pygui

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
TITLE = "Silence Cutter"
FPS = 240


# initializes the window
def init():
    pygame.init()
    pygame.display.set_caption(TITLE)

    try:
        icon_image = pygame.image.load("../assets/hqicon.png")
        pygame.display.set_icon(icon_image)
    except FileNotFoundError:
        print("couldn't load image")

    _window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), vsync=1)
    _manager = pygui.UIManager(_window.get_size(), 'theme.json')

    return _window, _manager


window, pygui_manager = init()
