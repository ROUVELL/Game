import os
import ctypes

user32 = ctypes.windll.user32


class Config:
    # window
    WIDTH, HEIGHT = (user32.GetSystemMetrics(78), user32.GetSystemMetrics(79))  # always fullscreen
    HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
    DOUBLE_WIDTH, DOUBLE_HEIGHT = WIDTH * 2, HEIGHT * 2
    CENTER = (HALF_WIDTH, HALF_HEIGHT)
    SCREEN = (WIDTH, HEIGHT)
    # fps
    FPS = 60
    FPS_POS = (0, 0)
    FPS_COLOR = 'orange'
    # camera
    CAMERA_RECT = (WIDTH * .1, HEIGHT * .1, WIDTH * .8, HEIGHT * .8)
    # player
    PLAYER_SIZE = (WIDTH * .0219, HEIGHT * .0704)  # 42, 76
    PLAYER_RECT = (WIDTH * .0198, HEIGHT * .0333)  # 38, 36  # not using
    PLAYER_POS = (HALF_WIDTH - PLAYER_RECT[0] * .5, HALF_HEIGHT - PLAYER_RECT[1] * .5)  # not using
    PLAYER_SPEED = WIDTH / 480  # 4
    # paths
    DIR = os.path.dirname(__file__)
    RESOUCES = f'{DIR}/resources/'
    STATIC = f'{RESOUCES}static/'
    ANIMATION = f'{RESOUCES}animation/'
    PLAYER_ANIM = f'{ANIMATION}player/'
    MAPS = f'{RESOUCES}maps/'
    CURRENT_MAP = f'{MAPS}map1.json'
    # editor
    OBJECTS_LIST_POS = (0, 0)
    OBJECTS_LIST_SIZE = (WIDTH * .075, HEIGHT)
    SLIDE_SENSETIVITY = 50  # For sliding imgs list
    EDITING_TAB_POS = (WIDTH - (WIDTH * .20) - 1, 0)
    EDITING_TAB_SIZE = (WIDTH * .20, HEIGHT)
    INTERNAL_SURFACE_SIZE = (WIDTH * .75, HEIGHT * .75)
    ZOOM_SPEED = .01
    # debug
    DRAW_PLAYER_RECT = False
    DRAW_TEXTURE_RECT = False
    DRAW_CAMERA_RECT = False
    DRAW_SCREEN_CENTER = False
