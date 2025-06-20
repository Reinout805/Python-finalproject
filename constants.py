import pygame
import os
pygame.init()
pygame.font.init()


#colors
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (200, 50, 50)
RED2 = (122, 5, 5)
ORANGE= (209, 125, 15)
GREEN = (50, 200, 50)
GREEN2=(15, 122, 53)
BLACK = (0, 0, 0)
BLUE = (50, 50, 200)

#general
SCREEN_WIDTH, SCREEN_HEIGHT = 960, 728
CARD_WIDTH, CARD_HEIGHT = 100, 200
FPS = 60
FONT = pygame.font.SysFont('Arial', 24)
BIG_FONT = pygame.font.SysFont('Arial', 36)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "kaarten")

#time
time_easy = 60
time_medium = 30
time_hard=15
round_timer = 30

#init's
buttons = []
selected_button = []