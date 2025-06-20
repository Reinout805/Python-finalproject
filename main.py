import pygame
import random
import sys
import os
from classes import Kaart, Spel, Button
from constants import *
from screens import *
from help_functions import *


pygame.init()
pygame.font.init()


# UI States
START, RULES, GAME, GREEN_SCREEN, RED_NO_SET_SCREEN, RED_SCREEN, TIME_OVER, GREY_SCREEN, NO_SET_CORRECT, NO_SET_INCORRECT, END = range(11)
state = START
state_functions = {
    START: lambda: start_screen(),
    RULES: lambda: rules_screen(),
    GAME: lambda: game_screen(),
    GREEN_SCREEN: lambda: green_screen(),
    NO_SET_CORRECT: lambda: no_set_correct_screen(),
    NO_SET_INCORRECT: lambda: no_set_incorrect_screen(computer_set),
    RED_SCREEN: lambda: red_screen(computer_set),
    RED_NO_SET_SCREEN: lambda: red_no_set_screen(),
    TIME_OVER: lambda: time_screen(computer_set),
    GREY_SCREEN: lambda: grey_screen(),
    END: lambda: end_screen()
}


# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SET!")
clock = pygame.time.Clock()



def print_warning(text):
    global warning
    warning=text
def pauze_change(text=""):
    global wait_pauze, Pauze
    if text=="click":
        if wait_pauze<=0:
            if Pauze==False:
                Pauze=True
            else:
                Pauze=False
            wait_pauze=1/30
    else:
        if Pauze==False:
            Pauze=True
        else:
            Pauze=False

def cheat(text=""):
    global cheat_cards, not_in_set_cards, cheat_amount, round_timer, wait_cheat
    if Pauze==False:
        if text=="click":
            if wait_cheat<=0:
                cheat_amount+=1
                x=random.choice(not_in_set_cards)
                cheat_cards.append(x)
                not_in_set_cards.remove(x)
                if round_timer>=5:
                    round_timer-=5
                else:
                    round_timer=0
                wait_cheat=1/30
        else: 
            cheat_amount+=1
            x=random.choice(not_in_set_cards)
            cheat_cards.append(x)
            not_in_set_cards.remove(x)
            if round_timer>=5:
                round_timer-=5
            else:
                round_timer=0

#main functions
def init_game():
    global selected_cards, Pauze, wait_cheat, wait_pauze, card_images, warning, cheat_cards, cheat_amount, not_in_set_cards, player_score, computer_score, S, input_text, total_elapsed_time, difficulty, fastest_set
    Pauze=False
    wait_cheat=0
    wait_pauze=0
    player_score = 0
    computer_score = 0
    cheat_amount=0
    total_elapsed_time = 0
    fastest_set=-1
    warning=""
    input_text = ""
    difficulty = "Medium"
    cheat_cards=[]
    not_in_set_cards=[]
    selected_cards = []
    card_images = {}
    S = Spel(["green", "purple", "red"], ["oval", "diamond", "squiggle"], ["empty", "shaded", "filled"], ["1", "2", "3"])
    S.maak_start_tafel()
    load_card_images()

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

def get_timer_for_difficulty():
    if difficulty == "Easy":
        return time_easy
    elif difficulty == "Medium":
        return time_medium
    elif difficulty == "Hard":
        return time_hard
    return time_medium









def set_selected_button(button):
    global selected_button
    selected_button = button

def set_difficulty(level):
    global difficulty
    difficulty = level

def change_state(new_state):
    global state, not_in_set_cards, cheat_cards, cheat_amount
    state = new_state
    if state==GAME:
        cheat_cards = []
        cheat_amount=0
        not_in_set_cards=S.all_cards_not_in_sets()
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
    start_btn = Button((400, 420, 200, 50), BLUE, "Continue", lambda: (start_game(), set_selected_button(None)))

    easy_btn.callback = lambda: (set_difficulty("Easy"), set_selected_button(easy_btn))
    medium_btn.callback = lambda: (set_difficulty("Medium"), set_selected_button(medium_btn))
    hard_btn.callback = lambda: (set_difficulty("Hard"), set_selected_button(hard_btn))

    buttons = [easy_btn, medium_btn, hard_btn, start_btn]
    screen.fill(WHITE)
    title = BIG_FONT.render("Welcome to SET", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
    under_title = FONT.render("Choose your difficulty:", True, BLACK)
    screen.blit(under_title, (SCREEN_WIDTH // 2 - under_title.get_width() // 2, 140))
    for button in buttons:
        button.draw(screen)

def rules_screen():
    screen.fill(WHITE)
    rules = [
        "RULES OF SET:",
        "- Identify a set of 3 cards",
        "- Each card has 4 features",
        "- A valid set has all the same or all different features",
        "INPUT:",
        "- Input your set in the format: 0 1 2 (card indices)",
        "- Select 'No set possible' or press 'n' when you think that no sets are possible",
        "- Select 'Begin/End break' or press 'p' to start/end the break",
        "- Select 'Hide a card' or press 'h' to hide a card which is not in any possible set:",
        "               - you lose 5 seconds!",
        "               - maximum of 6 hide's per round",
        "POINTS:",
        "- You CORRECTLY identified a set: you get 1 point",
        "- You INCORRETLY identified a set: computer gets 1 point",
        "- You CORRECTLY identified that no sets are possible: you get 5 points",
        "- You INCORRECTLY identified that no sets are possible: computer gets 1 point",
        "- You run out of time while sets are possible: computer gets 1 point",
        "- You run out of time while no sets are possible: - ",


    ]
    for i, line in enumerate(rules):
        txt = FONT.render(line, True, BLACK)
        screen.blit(txt, (5, 5 + i * 35))

    continue_btn = Button((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 80, 200, 50), GRAY, "Start game", lambda: change_state(GAME))
    continue_btn.draw(screen)
    buttons.clear()
    buttons.append(continue_btn)

def no_set_input():
    if not Pauze:
        if len(S.controleer_sets())==0:
            for _ in range(5):
                update_score("player")
            change_state(NO_SET_CORRECT)
        else:
            update_score("computer")
            global computer_set
            computer_set=find_set_by_computer()
            change_state(NO_SET_INCORRECT)
        

def game_screen():
    global buttons,warning, no_set_button, pauze_button
    screen.fill((164, 173, 237))
    for i, card in enumerate(S.cards_on_table):
        x = 50 + (i % 4) * 220
        y = 150 + (i // 4) * 150
        key = str(card)
        if key in card_images:
            if i in cheat_cards:
                pygame.draw.rect(screen, BLACK, (x, y+2, CARD_HEIGHT, CARD_WIDTH))
                screen.blit(FONT.render("NOT IN SET", True, WHITE), (x +45, y + 35))
            else:
                screen.blit(card_images[key], (x, y))
                index_txt = FONT.render(str(i+1), True, BLACK)
                screen.blit(index_txt, (x + CARD_WIDTH // 2 - 40, y - 25))
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_HEIGHT, CARD_WIDTH))
            screen.blit(FONT.render("?", True, BLACK), (x + 90, y + 50))
        if i in selected_cards:
            pygame.draw.rect(screen, BLUE, (x, y+2,CARD_HEIGHT , CARD_WIDTH), 8) #changes HEIGHT and WITH in stead of rotating the rectangle
        if Pauze:
            pygame.draw.rect(screen, GRAY, (x, y+2, CARD_HEIGHT, CARD_WIDTH))
            screen.blit(FONT.render("?", True, BLACK), (x + 90, y + 50))
    screen.blit(FONT.render(f"Time: {round(round_timer, 1)}s", True, BLACK), (SCREEN_WIDTH // 2 - 50, 20))
    screen.blit(FONT.render(f"Deck: {len(S.alle_kaarten)} cards", True, BLACK), (SCREEN_WIDTH - 250, 20))
    screen.blit(FONT.render(f"Computer Score: {computer_score}", True, BLACK), (750, SCREEN_HEIGHT - 50))
    screen.blit(FONT.render(f"Player Score: {player_score}", True, BLACK), (50, SCREEN_HEIGHT - 50))
    if fastest_set>0:
        screen.blit(FONT.render(f"Fastest set: {round(fastest_set,1)}", True, BLACK), (50, SCREEN_HEIGHT - 90))
    else:
        screen.blit(FONT.render(f"Fastest set: -", True, BLACK), (50, SCREEN_HEIGHT - 90))
    no_set_button = Button((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 110, 200, 40), GRAY, "No set possible", lambda: (no_set_input()))
    buttons.append(no_set_button)
    no_set_button.draw(screen)
    if Pauze==True:
        text="End break"
    else: 
        text="Begin break"
    pauze_button = Button((SCREEN_WIDTH // 2 - 60, 50, 130, 40), GRAY, text, lambda: (pauze_change("click")))
    buttons.append(pauze_button)
    pauze_button.draw(screen)
    exit_game_button = Button((20, 20, 130, 40), GRAY, "Exit game", lambda: (change_state(END)))
    buttons.append(exit_game_button)
    exit_game_button.draw(screen)
    if len(not_in_set_cards)>0 and cheat_amount<6:
        cheat_button = Button((SCREEN_WIDTH - 250, 60, 200, 40), GRAY, f"Hide a card: {min((6-cheat_amount),len(not_in_set_cards))} left", lambda: (cheat("click")))
        buttons.append(cheat_button)
        cheat_button.draw(screen)
    else: 
        cheat_surface = FONT.render("No hide's left!", True, RED)
        screen.blit(cheat_surface, (SCREEN_WIDTH - 250, 60))
    input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 60, 200, 40)
    pygame.draw.rect(screen, WHITE, input_rect)
    txt_surface = FONT.render(input_text, True, BLACK)
    warning_surface=FONT.render(warning, True, RED)
    if warning!="":
        screen.blit(warning_surface, (input_rect.x + 5, input_rect.y + 5))
    screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))

def green_screen():
    global fastest_set
    screen.fill(GREEN)
    msg = BIG_FONT.render("Correct Set!", True, BLACK)
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 140))
    for i, card in enumerate(selected_set):
        x = SCREEN_WIDTH//2 + (i % 4) * 220 -320
        y = 230
        key = str(card)
        if key in card_images:
            screen.blit(card_images[key], (x, y))
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))
            screen.blit(FONT.render("UNKNOWN CARD", True, BLACK), (x + 90, y + 50))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY, "Continue", continue_from_green)
    continue_btn.draw(screen)
    exit_game_button = Button((20, 20, 130, 40), GRAY, "Exit game", lambda: (change_state(END)))
    buttons.append(exit_game_button)
    exit_game_button.draw(screen)
    buttons.append(continue_btn)
    new_time=get_timer_for_difficulty()-round_timer
    if fastest_set==-1:
        fastest_set=new_time
    if fastest_set>new_time:
        fastest_set=new_time
    text = FONT.render(f"Time used: {round(new_time, 1)}s", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 340))
    text = FONT.render(f"Your correct set:", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 190))
    if fastest_set>0:
        text = FONT.render(f"Fastest set: {round(fastest_set, 1)}s", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    else:
        text = FONT.render(f"Fastest set: -", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    text = FONT.render(f"Deck: {len(S.alle_kaarten)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 460))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 430))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 400))


def continue_from_green():
    global round_timer, choosen_indices, selected_cards
    selected_cards=[]
    S.verwijder_set(*choosen_indices)
    S.voeg_kaarten_toe_op_tafel()
    round_timer = get_timer_for_difficulty()
    change_state(GAME)

def red_screen(gevonden_set):
    global selected_set, input_text
    input_text=""
    screen.fill(RED)
    msg = BIG_FONT.render("Wrong set!", True, BLACK)
    for i, card in enumerate(selected_set):
        x = SCREEN_WIDTH//2 + (i % 4) * 220 -320
        y = 100
        key = str(card)
        if key in card_images:
            screen.blit(card_images[key], (x, y))
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))
            screen.blit(FONT.render("UNKNOWN CARD", True, BLACK), (x + 90, y + 50))
    for i, card in enumerate(gevonden_set):
        x = SCREEN_WIDTH//2 + (i % 4) * 220 -320
        y = 260
        key = str(card)
        if key in card_images:
            screen.blit(card_images[key], (x, y))
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))
            screen.blit(FONT.render("UNKNOWN CARD", True, BLACK), (x + 90, y + 50))
    text = FONT.render(f"The computer found this set:", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 220))
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 10))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY, "Continue", continue_from_red)
    continue_btn.draw(screen)
    exit_game_button = Button((20, 20, 130, 40), GRAY, "Exit game", lambda: (change_state(END)))
    buttons.append(exit_game_button)
    exit_game_button.draw(screen)
    text = FONT.render(f"Your incorrect set:", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 60))
    if fastest_set>0:
        text = FONT.render(f"Fastest set: {round(fastest_set, 1)}s", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    else:
        text = FONT.render(f"Fastest set: -", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    text = FONT.render(f"Time used: {round(get_timer_for_difficulty()-round_timer, 1)}s", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 560))
    text = FONT.render(f"Deck: {len(S.alle_kaarten)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 460))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 430))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 400))
    buttons.append(continue_btn)

def continue_from_red():
    global round_timer, selected_cards, selected_cards
    selected_cards=[]
    S.voeg_kaarten_toe_op_tafel()
    round_timer = get_timer_for_difficulty()
    change_state(GAME)

def red_no_set_screen():
    global selected_set, input_text
    input_text=""
    screen.fill(RED)
    msg = BIG_FONT.render("Wrong set!", True, BLACK)
    for i, card in enumerate(selected_set):
        x = SCREEN_WIDTH//2 + (i % 4) * 220 -320
        y = 200
        key = str(card)
        if key in card_images:
            screen.blit(card_images[key], (x, y))
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))
            screen.blit(FONT.render("UNKNOWN CARD", True, BLACK), (x + 90, y + 50))
    text = BIG_FONT.render(f"There was no set possible", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 320))
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 110))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY, "Continue", continue_from_red_no_set)
    continue_btn.draw(screen)
    exit_game_button = Button((20, 20, 130, 40), GRAY, "Exit game", lambda: (change_state(END)))
    buttons.append(exit_game_button)
    exit_game_button.draw(screen)
    text = FONT.render(f"Your incorrect set:", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 160))
    if fastest_set>0:
        text = FONT.render(f"Fastest set: {round(fastest_set, 1)}s", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    else:
        text = FONT.render(f"Fastest set: -", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    text = FONT.render(f"Time used: {round(get_timer_for_difficulty()-round_timer, 1)}s", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 560))
    text = FONT.render(f"Deck: {len(S.alle_kaarten)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 460))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 430))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 400))
    buttons.append(continue_btn)

def continue_from_red_no_set():
    global round_timer, selected_cards, selected_cards
    selected_cards=[]
    S.verwijder_eerste_3_kaarten()
    round_timer = get_timer_for_difficulty()
    change_state(GAME)

def find_set_by_computer():
    gevonden_set=S.verwijder_willekeurige_set()
    return gevonden_set

def time_screen(gevonden_set):
    screen.fill(ORANGE)
    msg = BIG_FONT.render("TIME IS OVER!", True, BLACK)
    for i, card in enumerate(gevonden_set):
        x = SCREEN_WIDTH//2 + (i % 4) * 220 -320
        y = 260
        key = str(card)
        if key in card_images:
            screen.blit(card_images[key], (x, y))
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))
            screen.blit(FONT.render("UNKNOWN CARD", True, BLACK), (x + 90, y + 50))
    global input_text
    input_text=""
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 170))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY, "Continue", continue_from_time)
    continue_btn.draw(screen)
    exit_game_button = Button((20, 20, 130, 40), GRAY, "Exit game", lambda: (change_state(END)))
    buttons.append(exit_game_button)
    exit_game_button.draw(screen)
    text = FONT.render(f"The computer found this set:", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 220))
    if fastest_set>0:
        text = FONT.render(f"Fastest set: {round(fastest_set, 1)}s", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    else:
        text = FONT.render(f"Fastest set: -", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    text = FONT.render(f"Deck: {len(S.alle_kaarten)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 460))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 430))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 400))
    buttons.append(continue_btn)

def continue_from_time():
    global round_timer, selected_cards
    S.voeg_kaarten_toe_op_tafel()
    selected_cards=[]
    round_timer = get_timer_for_difficulty()
    change_state(GAME)

def grey_screen():
    screen.fill(GRAY)
    msg = BIG_FONT.render("Time over: No sets possible!", True, BLACK)
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 400, 200, 50), BLUE,  "Continue", continue_from_grey)
    if fastest_set>0:
        text = FONT.render(f"Fastest set: {round(fastest_set, 1)}s", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 280))
    else:
        text = FONT.render(f"Fastest set: -", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 280))
    text = FONT.render(f"Cards 1, 2 and 3 will be replaced. ", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250))
    text = FONT.render(f"Deck: {len(S.alle_kaarten)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 340))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 310))
    continue_btn.draw(screen)
    exit_game_button = Button((20, 20, 130, 40), GRAY, "Exit game", lambda: (change_state(END)))
    buttons.append(exit_game_button)
    exit_game_button.draw(screen)
    buttons.append(continue_btn)

def continue_from_grey():
    global round_timer, selected_cards
    selected_cards=[]
    S.verwijder_eerste_3_kaarten()
    round_timer = get_timer_for_difficulty()
    change_state(GAME)

def no_set_correct_screen():
    screen.fill(GREEN2)
    msg = BIG_FONT.render("You are correct, no sets possible!", True, BLACK)
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 160))
    msg2 = FONT.render("You get 5 points!", True, BLACK)
    screen.blit(msg2, (SCREEN_WIDTH // 2 - msg2.get_width() // 2, 200))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY,  "Continue", continue_from_no_set_correct)
    if fastest_set>0:
        text = FONT.render(f"Fastest set: {round(fastest_set, 1)}s", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 280))
    else:
        text = FONT.render(f"Fastest set: -", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 280))
    text = FONT.render(f"Cards 1, 2 and 3 will be replaced. ", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250))
    text = FONT.render(f"Deck: {len(S.alle_kaarten)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 340))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 310))
    continue_btn.draw(screen)
    exit_game_button = Button((20, 20, 130, 40), GRAY, "Exit game", lambda: (change_state(END)))
    buttons.append(exit_game_button)
    exit_game_button.draw(screen)
    buttons.append(continue_btn)

def continue_from_no_set_correct():
    global round_timer, selected_cards
    selected_cards=[]
    S.verwijder_eerste_3_kaarten()
    round_timer = get_timer_for_difficulty()
    change_state(GAME)

def no_set_incorrect_screen(gevonden_set):
    screen.fill(RED2)
    msg = BIG_FONT.render("You are wrong, there is a set possible!", True, BLACK)
    for i, card in enumerate(gevonden_set):
        x = SCREEN_WIDTH//2 + (i % 4) * 220 -320
        y = 260
        key = str(card)
        if key in card_images:
            screen.blit(card_images[key], (x, y))
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))
            screen.blit(FONT.render("UNKNOWN CARD", True, BLACK), (x + 90, y + 50))
    global input_text
    input_text=""
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 170))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY, "Continue", continue_from_time)
    continue_btn.draw(screen)
    exit_game_button = Button((20, 20, 130, 40), GRAY, "Exit game", lambda: (change_state(END)))
    buttons.append(exit_game_button)
    exit_game_button.draw(screen)
    text = FONT.render(f"The computer found this set:", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 220))
    if fastest_set>0:
        text = FONT.render(f"Fastest set: {round(fastest_set, 1)}s", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    else:
        text = FONT.render(f"Fastest set: -", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    text = FONT.render(f"Deck: {len(S.alle_kaarten)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 460))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 430))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 400))
    buttons.append(continue_btn)

def continue_from_no_set_incorrect():
    global round_timer, selected_cards
    selected_cards=[]
    S.voeg_kaarten_toe_op_tafel()
    round_timer = get_timer_for_difficulty()
    change_state(GAME)

def end_screen():
    screen.fill(WHITE)
    if len(S.alle_kaarten+S.cards_on_table)<=20:
        if len(S.controleer_sets(S.alle_kaarten+S.cards_on_table))==0:
            title = BIG_FONT.render("Game ended: no sets possible anymore!", True, BLACK)
    else:
        title = BIG_FONT.render("Game ended!", True, BLACK)
    if player_score>computer_score:
        winner="You won!"
    elif player_score<computer_score:
        winner="The computer won!"
    else:
        winner="Draw!"
    under_title = BIG_FONT.render(winner, True, BLACK)
    score_text = FONT.render(f"Final Score — Player: {player_score} | Computer: {computer_score}", True, BLACK)
    time_text = FONT.render(f"Total Time: {int(total_elapsed_time)//60} minutes and {int(total_elapsed_time)-60*(int(total_elapsed_time)//60)} seconds", True, BLACK)
    if fastest_set>0:
        fasttime_text = FONT.render(f"Fastest set in {round(fastest_set,1)} seconds", True, BLACK)
    else:
        fasttime_text = FONT.render(f"Fastest set: -", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
    screen.blit(under_title, (SCREEN_WIDTH // 2 - under_title.get_width() // 2, 210))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))
    screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, 360))
    screen.blit(fasttime_text, (SCREEN_WIDTH // 2 - fasttime_text.get_width() // 2, 280))
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY, "Back to Menu", lambda: (change_state(START), init_game()))
    continue_btn.draw(screen)
    buttons.clear()
    buttons.append(continue_btn)

# Main loop
init_game()
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)
    if state==GAME:
        if len(S.alle_kaarten+S.cards_on_table)<=20:
            if len(S.controleer_sets(S.alle_kaarten+S.cards_on_table))==0:
                change_state(END)
    if state == GAME:
        if wait_pauze>0:
            wait_pauze-= 1/FPS
        if Pauze == False:
            round_timer -= 1 / FPS
            total_elapsed_time += 1 / FPS
            if wait_cheat>0:
                wait_cheat-=1 / FPS
        if round_timer <= 0:
            if len(S.controleer_sets())!=0:
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
            warning=""
            if event.key == pygame.K_p:
                pauze_change()
            if not Pauze:
                if event.key == pygame.K_n:
                    no_set_button.callback()
                elif event.key == pygame.K_h:
                    if len(not_in_set_cards)>0 and cheat_amount<6:
                        cheat()
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key != pygame.K_BACKSPACE and event.key != pygame.K_RETURN and event.key != pygame.K_p :
                    input_text += event.unicode
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_BACKSPACE:
                    try:
                        indices = list(map(int, input_text.strip().split()))
                        selected_cards = [index-1 for index in indices]
                        if max(selected_cards)>12 or min(selected_cards)<0:
                            print_warning("Index not in range!")
                            selected_cards=[]
                            input_text=''
                    except:
                        print_warning("No integer!")
                        selected_cards=[]
                        input_text=""

                if event.key == pygame.K_RETURN:
                    try:
                        if len(indices) == 3 and len(set(indices)) == 3:
                            selected_set = [S.cards_on_table[i] for i in selected_cards]
                            if selected_set[0].check_3_cards_if_set(selected_set[1], selected_set[2]):
                                choosen_indices = indices
                                update_score("player")
                                change_state(GREEN_SCREEN)
                                
                            else:
                                update_score("computer")
                                if len(S.controleer_sets(S.cards_on_table))==0:
                                    change_state(RED_NO_SET_SCREEN)
                                else:
                                    computer_set=find_set_by_computer()
                                    change_state(RED_SCREEN)
                        else:
                            if len(indices) < 3:
                                print_warning("Not enough cards!")
                                selected_cards=[]
                            elif len(indices) >3:
                                print_warning("Too many cards!")
                                selected_cards=[]
                            else:
                                print_warning("Same cards selected!")
                                selected_cards=[]
                    except:
                        pass
                    input_text = ""
    if state in state_functions:
        state_functions[state]()

    pygame.display.flip()

pygame.quit()
sys.exit()
