"""
Various unchanging values used throughout the game
"""

# general

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 720

DISPLAY_SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

# player constants
PLAYER_SPEED = 2
PLAYER_GRAVITY = 1
PLAYER_FRICTION = 0.7
PLAYER_JUMP_HEIGHT = 10

# terrain engine constants

# 0 - solid
# 1 - obstacle
TILE_TYPES = {
    0: 0,
    1: 1
}
