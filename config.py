import os


class Config:
    # window
    WIDTH, HEIGHT = (1600, 900)
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
    PLAYER_SIZE = (42, 72)
    PLAYER_RECT = (38, 36)
    PLAYER_POS = (HALF_WIDTH - PLAYER_RECT[0] * .5, HALF_HEIGHT - PLAYER_RECT[1] * .5)
    PLAYER_SPEED = 4  # 4
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
    OBJECTS_LIST_SIZE = (WIDTH * .05, HEIGHT)
    EDITING_TAB_POS = (WIDTH - WIDTH * .20, 0)
    EDITING_TAB_SIZE = (WIDTH * .20, HEIGHT)
    # debug
    DRAW_PLAYER_RECT = True
    DRAW_TEXTURE_RECT = True
    DRAW_CAMERA_RECT = False
    DRAW_SCREEN_CENTER = True
