
class Config:
    # window
    WIDTH, HEIGHT = (1600, 900)
    HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
    CENTER = (HALF_WIDTH, HALF_HEIGHT)
    SCREEN = (WIDTH, HEIGHT)
    # fps
    FPS = 60
    # player
    PLAYER_SIZE = (42, 72)
    PLAYER_SPEED = 4
    # paths
    RESOUCES = 'resources/'
    STATIC = f'{RESOUCES}static/'
    ANIMATION = f'{RESOUCES}animation/'
    PLAYER_ANIM = f'{ANIMATION}player/'
    MAPS = f'{RESOUCES}maps/'
    CURRENT_MAP = f'{MAPS}map1.json'
