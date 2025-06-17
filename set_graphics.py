import pygame
import sys
import os
from set import Kaart, Spel

pygame.init()
pygame.font.init()

selected_cards = []
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 728
FPS = 60
FONT = pygame.font.SysFont('Arial', 24)
BIG_FONT = pygame.font.SysFont('Arial', 36)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "kaarten")

WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLACK = (0, 0, 0)
BLUE = (50, 50, 200)

CARD_WIDTH, CARD_HEIGHT = 100, 200
card_images = {}

# UI States
START, RULES, GAME, GREEN_SCREEN, RED_SCREEN, GREY_SCREEN, END = range(7)
state = START
difficulty = "Medium"


# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SET!")
clock = pygame.time.Clock()

# Variabelen
player_score = 0
computer_score = 0
S = Spel(["green", "purple", "red"], ["oval", "diamond", "squiggle"], ["empty", "shaded", "filled"], ["1", "2", "3"])
cards_on_table = S.maak_start_tafel()
deck_count = len(S.alle_kaarten)
input_text = ""
round_timer = 30
total_elapsed_time = 0

def get_timer_for_difficulty():
    if difficulty == "Easy":
        return 60
    elif difficulty == "Medium":
        return 30
    elif difficulty == "Hard":
        return 15
    return 30

def load_card_images():
    global card_images
    for cl in ["green", "purple", "red"]:
        for sh in ["oval", "diamond", "squiggle"]:
            for fi in ["empty", "shaded", "filled"]:
                for nu in ["1", "2", "3"]:
                    path = os.path.join(ASSET_PATH, f"{cl}{sh}{fi}{nu}.gif")
                    if os.path.exists(path):
                        img = pygame.image.load(path)
                        img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
                        img = pygame.transform.rotozoom(img, 90, 1)
                        card_images[f"{cl}{sh}{fi}{nu}"] = img
                    else:
                        print(f"Missing: {path}")

load_card_images()

class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        txt = FONT.render(self.text, True, BLACK)
        surface.blit(txt, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

buttons = []

def set_difficulty(level):
    global difficulty
    difficulty = level

def change_state(new_state):
    global state
    state = new_state
    buttons.clear()

def start_game():
    global round_timer
    round_timer = get_timer_for_difficulty()
    change_state(RULES)

def start_screen():
    screen.fill(WHITE)
    title = BIG_FONT.render("Welcome to SET", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
    for button in buttons:
        button.draw(screen)

def rules_screen():
    screen.fill(WHITE)
    rules = [
        "RULES OF SET:",
        "- Identify a set of 3 cards.",
        "- Each card has 4 features.",
        "- A valid set has all the same or all different features.",
        "Input your set in the format: 0 1 2 (card indices)"
    ]
    for i, line in enumerate(rules):
        txt = FONT.render(line, True, BLACK)
        screen.blit(txt, (50, 50 + i * 40))

    continue_btn = Button((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50), "Continue", lambda: change_state(GAME))
    continue_btn.draw(screen)
    buttons.clear()
    buttons.append(continue_btn)

def game_screen():
    screen.fill(WHITE)
    for i, card in enumerate(cards_on_table):
        x = 50 + (i % 4) * 220
        y = 150 + (i // 4) * 150
        key = str(card)
        if key in card_images:
            screen.blit(card_images[key], (x, y))
            index_txt = FONT.render(str(i+1), True, BLACK)
            screen.blit(index_txt, (x + CARD_WIDTH // 2 - 10, y - 25))
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))
            screen.blit(FONT.render("?", True, BLACK), (x + 90, y + 50))
        if i in selected_cards:
            pygame.draw.rect(screen, BLUE, (x, y,CARD_HEIGHT , CARD_WIDTH), 4)

    screen.blit(FONT.render(f"Time: {int(round_timer)}s", True, BLACK), (SCREEN_WIDTH // 2 - 50, 20))
    screen.blit(FONT.render(f"Deck: {len(S.alle_kaarten)} cards", True, BLACK), (SCREEN_WIDTH - 250, 20))
    screen.blit(FONT.render(f"Computer Score: {computer_score}", True, BLACK), (50, SCREEN_HEIGHT - 50))
    screen.blit(FONT.render(f"Player Score: {player_score}", True, BLACK), (550, SCREEN_HEIGHT - 50))

    input_rect = pygame.Rect(300, SCREEN_HEIGHT - 60, 200, 40)
    pygame.draw.rect(screen, GRAY, input_rect)
    txt_surface = FONT.render(input_text, True, BLACK)
    screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))

def green_screen():
    screen.fill(GREEN)
    msg = BIG_FONT.render("Correct Set!", True, BLACK)
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), "Continue", continue_from_green)
    continue_btn.draw(screen)
    buttons.clear()
    buttons.append(continue_btn)

def continue_from_green():
    global player_score, cards_on_table, round_timer, selected_cards
    player_score += 1
    S.verwijder_set(*[item+1 for item in selected_cards], cards_on_table)
    S.voeg_kaarten_toe_op_tafel(cards_on_table)
    selected_cards=[]
    round_timer = get_timer_for_difficulty()
    change_state(GAME)

def red_screen():
    screen.fill(RED)
    msg = BIG_FONT.render("Wrong!", True, BLACK)
    global input_text
    input_text=""
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), "Continue", continue_from_red)
    continue_btn.draw(screen)
    buttons.clear()
    buttons.append(continue_btn)

def continue_from_red():
    global computer_score, cards_on_table, round_timer, selected_cards
    computer_score += 1
    if len(S.controleer_sets(cards_on_table))!=0:
        S.verwijder_willekeurige_set(cards_on_table)
        S.voeg_kaarten_toe_op_tafel(cards_on_table)
    else:
        pass
    selected_cards=[]
    round_timer = get_timer_for_difficulty()
    change_state(GAME)

def grey_screen():
    screen.fill(GRAY)
    msg = BIG_FONT.render("No sets possible!", True, BLACK)
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), "Continue", continue_from_grey)
    continue_btn.draw(screen)
    buttons.clear()
    buttons.append(continue_btn)

def continue_from_grey():
    global cards_on_table, round_timer, selected_cards
    S.verwijder_eerste_3_kaarten(cards_on_table)
    selected_cards=[]
    round_timer = get_timer_for_difficulty()
    change_state(GAME)

def end_screen():
    screen.fill(WHITE)
    title = BIG_FONT.render("Game Over!", True, BLACK)
    score_text = FONT.render(f"Final Score — Player: {player_score} | Computer: {computer_score}", True, BLACK)
    time_text = FONT.render(f"Total Time: {int(total_elapsed_time)} seconds", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))
    screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, 300))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), "Back to Menu", lambda: change_state(START))
    continue_btn.draw(screen)
    buttons.clear()
    buttons.append(continue_btn)

# Main loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)
    if state == GAME:
        round_timer -= 1 / FPS
        total_elapsed_time += 1 / FPS
        if round_timer <= 0:
            if len(S.controleer_sets(cards_on_table))!=0:
                change_state(RED_SCREEN)
                selected_cards=[]
            else:
                change_state(GREY_SCREEN)
                selected_cards=[]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.handle_event(event)
        if event.type == pygame.KEYDOWN and state == GAME:
            indices = list(map(int, input_text.strip().split()))
            selected_cards = [index-1 for index in indices]
            if event.key == pygame.K_RETURN:
                try:
                    if len(indices) == 3 and len(set(indices)) == 3:
                        selected = [cards_on_table[i] for i in selected_cards]
                        print(selected)
                        for card in selected:
                            print(card, card.kleur, card.vorm, card.vulling, card.aantal, type(card.aantal))
                        if selected[0].check_3_cards_if_set(selected[1], selected[2]):
                            selected = indices
                            print(selected_cards)
                            change_state(GREEN_SCREEN)
                        else:
                            change_state(RED_SCREEN)
                except:
                    change_state(RED_SCREEN)
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
    if state == START:
        buttons = [
            Button((400, 200, 200, 50), "Easy", lambda: set_difficulty("Easy")),
            Button((400, 270, 200, 50), "Medium", lambda: set_difficulty("Medium")),
            Button((400, 340, 200, 50), "Hard", lambda: set_difficulty("Hard")),
            Button((400, 420, 200, 50), "Start Game", start_game)
        ]
        start_screen()
    elif state == RULES:
        rules_screen()
    elif state == GAME:
        game_screen()
    elif state == GREEN_SCREEN:
        green_screen()
    elif state == RED_SCREEN:
        red_screen()
    elif state == GREY_SCREEN:
        grey_screen()
    elif state == END:
        end_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()
