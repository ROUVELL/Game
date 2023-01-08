import os
import ctypes

user32 = ctypes.windll.user32


class Config:
    # window
    WIDTH, HEIGHT = (user32.GetSystemMetrics(78) // 2, user32.GetSystemMetrics(79) // 2)  # always fullscreen
    HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
    CENTER = (HALF_WIDTH, HALF_HEIGHT)
    SCREEN = (WIDTH, HEIGHT)
    # fps
    FPS = 60
    FPS_POS = (0, 0)
    FPS_COLOR = 'orange'
    # camera
    CAMERA_RECT = (WIDTH * .1, HEIGHT * .1, WIDTH * .8, HEIGHT * .8)
    # player
    PLAYER_SPEED = WIDTH / 480  # 4
    # paths
    DIR = os.path.dirname(__file__)
    RESOUCES = f'{DIR}/resources/'
    FONTS = f'{RESOUCES}fonts/'
    INFO_FONT = f'{FONTS}Mystery Font.ttf'
    STATIC = f'{RESOUCES}static/'
    ANIMATION = f'{RESOUCES}animation/'
    PLAYER_ANIM = f'{ANIMATION}player/'
    MAPS = f'{RESOUCES}maps/'
    CURRENT_MAP = f'{MAPS}map1.json'
    UI = f'{RESOUCES}UI/'
    # editor
    OBJECTS_LIST_POS = (0, 0)
    OBJECTS_LIST_SIZE = (WIDTH * .075, HEIGHT)
    SLIDE_SENSETIVITY = 30  # For sliding imgs list
    AUTOSAVE_ON_EXIT = False  # Чи зберігати світ при виході
    AUTOSAVE = False
    AUTOSAVE_DELEY = 15  # sec
    DRAW_COORDINATE_AXIS = False
    DRAW_TILE_GRID = False
    # debug
    DRAW_PLAYER_RECT = False
    DRAW_TEXTURE_RECT = False
    DRAW_SPRITE_RECT = False
    DRAW_CAMERA_RECT = False
    DRAW_SCREEN_CENTER = False
