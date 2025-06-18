import pygame
import sys
import os
from set import Kaart, Spel

pygame.init()
pygame.font.init()

selected_cards = []
SCREEN_WIDTH, SCREEN_HEIGHT = 960, 728
FPS = 60
FONT = pygame.font.SysFont('Arial', 24)
BIG_FONT = pygame.font.SysFont('Arial', 36)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "kaarten")

WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (200, 50, 50)
ORANGE= (209, 125, 15)
GREEN = (50, 200, 50)
BLACK = (0, 0, 0)
BLUE = (50, 50, 200)

CARD_WIDTH, CARD_HEIGHT = 100, 200
card_images = {}

# UI States
START, RULES, GAME, GREEN_SCREEN, RED_SCREEN, TIME_OVER, GREY_SCREEN, END = range(8)
state = END



# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SET!")
clock = pygame.time.Clock()

# Variabelen
time_easy = 60
time_medium = 30
time_hard=1
round_timer = 30

def get_timer_for_difficulty():
    if difficulty == "Easy":
        return time_easy
    elif difficulty == "Medium":
        return time_medium
    elif difficulty == "Hard":
        return time_hard
    return time_medium

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

def init_game():
    global player_score, computer_score, S, cards_on_table, deck_count, input_text, total_elapsed_time, difficulty
    player_score = 0
    computer_score = 0
    S = Spel(["green", "purple", "red"], ["oval", "diamond", "squiggle"], ["empty", "shaded", "filled"], ["1", "2", "3"])
    cards_on_table = S.maak_start_tafel()
    deck_count = len(S.alle_kaarten)
    input_text = ""
    total_elapsed_time = 0
    difficulty = "Medium"

init_game()

class Button:
    def __init__(self, rect, color, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.color = color

    def draw(self, surface):
        global selected_button
        pygame.draw.rect(surface, self.color, self.rect)
        if self == selected_button:
            pygame.draw.rect(surface, RED, self.rect, 4)
        txt = FONT.render(self.text, True, BLACK)
        surface.blit(txt, (self.rect.x + 10, self.rect.y + 10))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def __eq__(self, other):
        if isinstance(other, Button):
            return self.rect==other.rect and self.color==other.color and self.text==other.text
        return False
buttons = []
selected_button = []
def set_selected_button(button):
    global selected_button
    selected_button = button

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

def update_score(player):
    global player_score, computer_score
    if player=='player':
        player_score+=1
    elif player=="computer":
        computer_score+=1
#all different screens:
def start_screen():
    global buttons
    easy_btn = Button((400, 200, 200, 50), GRAY, f"Easy: {time_easy}s", None)
    medium_btn = Button((400, 270, 200, 50), GRAY, f"Medium: {time_medium}s", None)
    hard_btn = Button((400, 340, 200, 50), GRAY, f"Hard: {time_hard}s", None)
    start_btn = Button((400, 420, 200, 50), BLUE, "Start Game", lambda: (start_game(), set_selected_button(None)))

    easy_btn.callback = lambda: (set_difficulty("Easy"), set_selected_button(easy_btn))
    medium_btn.callback = lambda: (set_difficulty("Medium"), set_selected_button(medium_btn))
    hard_btn.callback = lambda: (set_difficulty("Hard"), set_selected_button(hard_btn))

    buttons = [easy_btn, medium_btn, hard_btn, start_btn]
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

    continue_btn = Button((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50), GRAY, "Continue", lambda: change_state(GAME))
    continue_btn.draw(screen)
    buttons.clear()
    buttons.append(continue_btn)

def game_screen():
    screen.fill((164, 173, 237))
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
            screen.blit(FONT.render("UNKNOWN CARD", True, BLACK), (x + 90, y + 50))
        if i in selected_cards:
            pygame.draw.rect(screen, BLUE, (x, y+2,CARD_HEIGHT , CARD_WIDTH), 8) #changes HEIGHT and WITH in stead of rotating the rectangle

    screen.blit(FONT.render(f"Time: {round(round_timer, 1)}s", True, BLACK), (SCREEN_WIDTH // 2 - 50, 20))
    screen.blit(FONT.render(f"Deck: {len(S.alle_kaarten)} cards", True, BLACK), (SCREEN_WIDTH - 250, 20))
    screen.blit(FONT.render(f"Computer Score: {computer_score}", True, BLACK), (750, SCREEN_HEIGHT - 50))
    screen.blit(FONT.render(f"Player Score: {player_score}", True, BLACK), (50, SCREEN_HEIGHT - 50))

    input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 60, 200, 40)
    pygame.draw.rect(screen, GRAY, input_rect)
    txt_surface = FONT.render(input_text, True, BLACK)
    screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))

def green_screen():
    screen.fill(GREEN)
    msg = BIG_FONT.render("Correct Set!", True, BLACK)
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY, "Continue", continue_from_green)
    continue_btn.draw(screen)
    buttons.clear()
    buttons.append(continue_btn)
    text = FONT.render(f"Time needed: {round(round_timer, 1)}s", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250))
    text = FONT.render(f"Deck: {len(S.alle_kaarten)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 340))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 310))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 280))

def continue_from_green():
    global cards_on_table, round_timer, choosen_indices, selected_cards
    selected_cards=[]
    S.verwijder_set(*choosen_indices, cards_on_table)
    S.voeg_kaarten_toe_op_tafel(cards_on_table)
    round_timer = get_timer_for_difficulty()
    change_state(GAME)

def red_screen():
    screen.fill(RED)
    msg = BIG_FONT.render("Wrong!", True, BLACK)
    global input_text
    input_text=""
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY, "Continue", continue_from_red)
    continue_btn.draw(screen)
    buttons.clear()
    text = FONT.render(f"Time needed: {round(round_timer, 1)}s", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250))
    text = FONT.render(f"Deck: {len(S.alle_kaarten)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 340))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 310))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 280))
    buttons.append(continue_btn)

def continue_from_red():
    global cards_on_table, round_timer, selected_cards, selected_cards
    selected_cards=[]
    if len(S.controleer_sets(cards_on_table))!=0:
        S.verwijder_willekeurige_set(cards_on_table)
        S.voeg_kaarten_toe_op_tafel(cards_on_table)
    else:
        pass
    round_timer = get_timer_for_difficulty()
    change_state(GAME)

def find_set_by_computer():
    x, gevonden_set=S.verwijder_willekeurige_set(cards_on_table)
    return gevonden_set

def time_screen(gevonden_set):
    screen.fill(ORANGE)
    msg = BIG_FONT.render("TIME IS OVER!", True, BLACK)
    for i, card in enumerate(gevonden_set):
        x = SCREEN_WIDTH//2 + (i % 4) * 220 -320
        y = 290
        key = str(card)
        if key in card_images:
            screen.blit(card_images[key], (x, y))
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))
            screen.blit(FONT.render("UNKNOWN CARD", True, BLACK), (x + 90, y + 50))
    global input_text
    input_text=""
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY, "Continue", continue_from_time)
    continue_btn.draw(screen)
    buttons.clear()
    text = FONT.render(f"The computer found this set:", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250))
    text = FONT.render(f"Deck: {len(S.alle_kaarten)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 460))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 430))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 400))
    buttons.append(continue_btn)

def continue_from_time():
    global round_timer, selected_cards, cards_on_table
    S.voeg_kaarten_toe_op_tafel(cards_on_table)
    selected_cards=[]
    round_timer = get_timer_for_difficulty()
    change_state(GAME)

def grey_screen():
    screen.fill(GRAY)
    msg = BIG_FONT.render("No sets possible!", True, BLACK)
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY,  "Continue", continue_from_grey)
    continue_btn.draw(screen)
    buttons.clear()
    buttons.append(continue_btn)

def continue_from_grey():
    global cards_on_table, round_timer, selected_cards
    selected_cards=[]
    S.verwijder_eerste_3_kaarten(cards_on_table)
    round_timer = get_timer_for_difficulty()
    change_state(GAME)

def end_screen():
    screen.fill(WHITE)
    title = BIG_FONT.render("Game Over!", True, BLACK)
    under_title = FONT.render("There are no sets possible anymore", True, BLACK)
    score_text = FONT.render(f"Final Score — Player: {player_score} | Computer: {computer_score}", True, BLACK)
    time_text = FONT.render(f"Total Time: {int(total_elapsed_time)} seconds", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
    screen.blit(under_title, (SCREEN_WIDTH // 2 - under_title.get_width() // 2, 190))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))
    screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, 300))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY, "Back to Menu", lambda: (change_state(START), init_game()))
    continue_btn.draw(screen)
    buttons.clear()
    buttons.append(continue_btn)

# Main loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)
    if state==GAME:
        if len(S.alle_kaarten+cards_on_table)<=20:
            if len(S.controleer_sets(S.alle_kaarten+cards_on_table))==0:
                change_state(END)
    if state == GAME:
        round_timer -= 1 / FPS
        total_elapsed_time += 1 / FPS
        if round_timer <= 0:
            if len(S.controleer_sets(cards_on_table))!=0:
                update_score("computer")
                computer_set=find_set_by_computer()
                change_state(TIME_OVER)
            else:
                change_state(GREY_SCREEN)

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
                        selected_set = [cards_on_table[i] for i in selected_cards]
                        #print(selected_set)
                        #for card in selected_set:
                            #print(card, card.kleur, card.vorm, card.vulling, card.aantal, type(card.aantal))
                        if selected_set[0].check_3_cards_if_set(selected_set[1], selected_set[2]):
                            choosen_indices = indices
                            #print(selected_cards)
                            update_score("player")
                            change_state(GREEN_SCREEN)
                            
                        else:
                            update_score("computer")
                            change_state(RED_SCREEN)
                            
                except:
                    update_score("computer")
                    change_state(RED_SCREEN)
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
    if state == START:
        start_screen()
    elif state == RULES:
        rules_screen()
    elif state == GAME:
        game_screen()
    elif state == GREEN_SCREEN:
        green_screen()
    elif state == RED_SCREEN:
        red_screen()
    elif state == TIME_OVER:
        time_screen(computer_set)
    elif state == GREY_SCREEN:
        grey_screen()
    elif state == END:
        end_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()
