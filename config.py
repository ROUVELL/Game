# window
WIDTH, HEIGHT = (1600, 900)

# fps
FPS = 60

# paths
RESOUCES_PATH = 'resources/'
TILES_PATH = f'{RESOUCES_PATH}tiles/'

# tiles
TILES = {
    # Необов'язкові параметри!
    # 'size': (int, int) -> змінити розміри
    # 'scale': int | float -> змаштабувати
    'S': {
        'name': 'stone-floor.png',
        'scale': 2,
        'is_alpha': False
    },
    'G-C': {
        'name': 'grass-center.png',
        'scale': 2,
        'is_alpha': False
    },
    'G-TL': {
        'name': 'grass-topleft.png',
        'scale': 2,
        'is_alpha': True
    },
    'G-T': {
        'name': 'grass-top.png',
        'scale': 2,
        'is_alpha': True
    },
    'G-TR': {
        'name': 'grass-topright.png',
        'scale': 2,
        'is_alpha': True
    },
    'G-R': {
        'name': 'grass-right.png',
        'scale': 2,
        'is_alpha': True
    },
    'G-BR': {
        'name': 'grass-bottomright.png',
        'scale': 2,
        'is_alpha': True
    },
    'G-B': {
        'name': 'grass-bottom.png',
        'scale': 2,
        'is_alpha': True
    },
    'G-BL': {
        'name': 'grass-bottomleft.png',
        'scale': 2,
        'is_alpha': True
    },
    'G-L': {
        'name': 'grass-left.png',
        'scale': 2,
        'is_alpha': True
    }
}