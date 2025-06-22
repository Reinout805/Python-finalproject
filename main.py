import pygame
import random
import sys
import os
from classes import Kaart, Spel, Button
from constants import *

'''
In this file 'main', the game is played. You can found:
    - Setup: initialize the screen, time and caption
    - UI States: the different states that our game could have and the dictionary 'statefunctions' with
        the related screens to display at every state 
    - Main functions: the function 'init_game' which initializes a SET game and the variables of a single game
        and the function 'load_cards_images' which initializes all the images of the cards of the game in a dictionary
    - Extra function: other seperated functions we used in the code, for example about setting the difficulty,
        change the states (of pauze), update the score and print a warning etc
    - All screens: all the different screens to display related to every state
    - Continue functions: the function with the code of what to do when changing from a screen to another screen
    - Main loop: the loop of running the game
We explain certain details about these categories below at the place itself.
'''

pygame.init()
pygame.font.init()

# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SET!")
clock = pygame.time.Clock()


'''
UI STATES

In UI we give the different states of the game. A short summary:
    - START: begin screen, to welcome user and choose difficulty
    - RULES: display all the rules of the game
    - GAME: the screen where you play the game, with all the cards, scores, time and extra features
    - END: when the game is finished, display results
    Feedback states:
    - GREEN_SCREEN: when your inputted set is correct
    - RED_NO_SET_SCREEN: when your inputted set is incorrect and there is no set possible at all
    - RED_SCREEN: when your inputted set is incorrect and there is a correct set possible
    - TIME_OVER: when the time is over, but there are sets possible
    - GREY_SCREEN: when the timer is over, but there were no sets possible
    - NO_SET_CORRECT: when you input that there are no sets possible and you are TRUE with this
    - NO_SET_INCORRECT: when you input that there are no sets possible and you are FALSE with this
state_functions displays the screen to display when at a certain state in the game
'''

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


'''
MAIN FUNCTIONS

In main functions, we have the two functions who initialize the game:
    - init_game: initialize all the starting variables, initialize an object 'SPEL', make starting table and load all images
    - load_card_images: load all the possible cards in the game and pick from folder 'kaarten' their images to make a dictionary with the card names and images
'''

def init_game():
    global selected_cards, automative_end, Pauze, wait_cheat, wait_pauze, card_images, warning, cheat_cards, cheat_amount, not_in_set_cards, buttons, selected_button, player_score, computer_score, S, input_text, total_elapsed_time, difficulty, fastest_set
    Pauze=False
    automative_end = False
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
    buttons = []
    selected_button = []
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


'''
EXTRA FUNCTIONS

The extra functions we have are:
    - print_warning: initialize the warning to print when inputting something wrong, clear selected cards and 
        input_text such that the player is able to input something else
    - pauze_change: change the status Pauze from True to False or from False to True.
    - cheat: if allowed, choose the indix of a random card which is not in a set of the current table and 
        add this index to the cheat_cards list. The cards in this cheat_cards list will be displayed black on the game screen
    - get_timer_for_difficulty: return the time per round choosen at the beginning of the game
    - set_selected_button: change the selected_button to the button you selected as input
    - set_difficulty: set the difficulty at the level the player wants
    - change_state: change the state of the game to the new state and also clear all the buttons in the buttons list
        such that they won't be shown own the screen anymore
    - update_score: update the score depended on whether player or computer has been inputted 
    - update_score_no_set: update score in case that the player inputted "no sets possible" (other score system than update_score)
    - find_set_by_computer: the computer will give 1 random set from the table and return this as a list of 3 cards, while deleting the set from the table
    - set_fasted_time: update the fastest time if neccesary
For further explanaitions, see the notitions in the functions itself.
'''

def print_warning(text):
    global warning, selected_cards, input_text
    warning=text #the text that will be printed when the user inputted something wrong
    selected_cards=[] #the cards the player selected at the gamescreen and will be highlighted
    input_text="" #the input the player has typed in so far

def pauze_change(text=""):
    global wait_pauze, Pauze
    if text=="click": #this will be true if this function is called by a click on a button
        if wait_pauze<=0: #there should be 1/30 seconds between two clicks on the pauze button. Only when the wait_time is over, so <=0, there state of Pauze could be changed
            if Pauze==False:
                Pauze=True
            else:
                Pauze=False
            wait_pauze=1/30 #start the wait_time again
    else: #when the function is called via pressing 'b' on keyboard
        if Pauze==False:
            Pauze=True
        else:
            Pauze=False

def cheat(text=""):
    global cheat_cards, not_in_set_cards, cheat_amount, round_timer, wait_cheat
    if Pauze==False: #only possible when game is not pauzed
        if text=="click": #same logic as pauze_change, but now with wait_cheat as time between two clicks on the button
    #maximum amount of hints is 6, so cheat_amount counts how many cards are already hided. 
    #there should only be a hide when there are elements in the "not_in_set_cards" list. this list displays all the cards which are not in any set of the current table and are not hided yet     
            if cheat_amount<6 and len(not_in_set_cards)>0: 
                if wait_cheat<=0:
                    cheat_amount+=1
                    x=random.choice(not_in_set_cards)
                    cheat_cards.append(x) #cheat_cards is the list of indices of cards which should be hided on the screen
                    not_in_set_cards.remove(x)
                    if round_timer>=5: #the hide costs 5 seconds of time
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

def get_timer_for_difficulty():
    if difficulty == "Easy":
        return time_easy
    elif difficulty == "Medium":
        return time_medium
    elif difficulty == "Hard":
        return time_hard
    return time_medium #if no difficulty set, the time is medium

def set_selected_button(button):
    global selected_button
    selected_button = button #the selected_button will be highlighted on the screen

def set_difficulty(level):
    global difficulty
    difficulty = level

def change_state(new_state):
    global state, not_in_set_cards, cheat_cards, cheat_amount, input_text, warning, all_possible_sets, selected_cards, round_timer
    state = new_state
    if state==GAME: #in this case, these variables should be refreshed
        selected_cards=[]
        cheat_cards = []
        cheat_amount=0
        input_text=''
        warning=''
        not_in_set_cards=S.all_cards_not_in_sets() #calculate all the cards on the table who are not in any possible set. We store these cards in the list "not_in_set_cards"
        all_possible_sets=S.controleer_sets() #give the list with all possible sets of current table
        round_timer = get_timer_for_difficulty() #initialize the timer again
    buttons.clear() 

def update_score(player):
    global player_score, computer_score
    if player=='player':
        player_score+=1
    elif player=="computer":
        computer_score+=1

def update_score_no_set():
    if not Pauze: #if pressing the "no set possible" button, only do someting when the game is not pauzed
        if len(all_possible_sets)==0: # the player is true
            for _ in range(5):
                update_score("player")
            change_state(NO_SET_CORRECT)
        else: # the player is false, there are sets possible
            update_score("computer")
            global computer_set
            computer_set=find_set_by_computer() #the computer should find a set hemself and store it as computer_set. This list will be used to display the set of the computer on the screen
            change_state(NO_SET_INCORRECT)

def find_set_by_computer():
    gevonden_set=S.verwijder_willekeurige_set() 
    return gevonden_set

def set_fastest_time():
    global fastest_set, current_time_used, round_timer
    current_time_used=get_timer_for_difficulty()-round_timer
    if fastest_set==-1:
        fastest_set = current_time_used
    elif fastest_set>current_time_used:
        fastest_set=current_time_used


'''
ALL SCREENS

For the meaning when which screen should be displayed, see UI states and the state_function dictionary earlier.
For further explanaitions, see the notitions in the functions itself.
'''

def start_screen():
    global buttons

    #screen:
    screen.fill(WHITE)

    #buttons:
    easy_btn = Button((400, 200, 200, 50), GRAY, f"Easy: {time_easy}s", None)
    medium_btn = Button((400, 270, 200, 50), GRAY, f"Medium: {time_medium}s", None)
    hard_btn = Button((400, 340, 200, 50), GRAY, f"Hard: {time_hard}s", None)
    start_btn = Button((400, 420, 200, 50), BLUE, "Continue", lambda: (continue_from_start(), set_selected_button(None))) #when going to RULES, the previously selected button should be unselected

    easy_btn.callback = lambda: (set_difficulty("Easy"), set_selected_button(easy_btn))
    medium_btn.callback = lambda: (set_difficulty("Medium"), set_selected_button(medium_btn))
    hard_btn.callback = lambda: (set_difficulty("Hard"), set_selected_button(hard_btn))

    buttons = [easy_btn, medium_btn, hard_btn, start_btn]
    for button in buttons:
        button.draw(screen)

    #texts:
    title = BIG_FONT.render("Welcome to SET", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
    under_title = FONT.render("Choose your difficulty:", True, BLACK)
    screen.blit(under_title, (SCREEN_WIDTH // 2 - under_title.get_width() // 2, 140))

def rules_screen():
    global buttons

    #screen:
    screen.fill(WHITE)

    #buttons:
    buttons.clear() #we do not want to add the same button multiple times in the list
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 80, 200, 50), GRAY, "Start game", lambda: change_state(GAME))
    
    buttons = [continue_btn]
    for button in buttons:
        button.draw(screen)

    #texts:
    rules = [
        "RULES OF SET:",
        "- Identify a set of 3 cards",
        "- Each card has 4 features",
        "- A valid set has all the same or all different features",
        "INPUT:",
        "- Input your set in the format: 0 1 2 (card indices), press enter to evaluate",
        "- Select 'No set possible' or press 'n' when you think that no sets are possible",
        "- Select 'Begin/End break' or press 'b' to start/end the break",
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
   
def game_screen():
    global buttons, warning, no_set_button, pauze_button

    #screen:
    screen.fill(BLUE2)

    #buttons:
    buttons.clear()
    if Pauze==True: # determine whether the pauze should be ended or started when pressing the pauze button
        text="End break"
    else: 
        text="Begin break"
    pauze_button = Button((SCREEN_WIDTH // 2 - 60, 50, 130, 40), GRAY, text, lambda: (pauze_change("click")))
    exit_game_button = Button((20, 20, 130, 40), GRAY, "Exit game", lambda: (change_state(END)))
    no_set_button = Button((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 110, 200, 40), GRAY, "No set possible", lambda: (update_score_no_set()))    
    if len(not_in_set_cards)>0 and cheat_amount<6: #only display the cheat_button if hide's are allowd
        cheat_button = Button((SCREEN_WIDTH - 250, 60, 200, 40), GRAY, f"Hide a card: {min((6-cheat_amount),len(not_in_set_cards))} left", lambda: (cheat("click")))
        buttons = [pauze_button,exit_game_button, no_set_button, cheat_button]
    else:
        buttons = [pauze_button,exit_game_button, no_set_button]

    for button in buttons:
        button.draw(screen)

    #texts:
    screen.blit(FONT.render(f"Time: {round(round_timer, 1)}s", True, BLACK), (SCREEN_WIDTH // 2 - 50, 20))
    screen.blit(FONT.render(f"Deck: {len(S.cards_on_deck)} cards", True, BLACK), (SCREEN_WIDTH - 250, 20))
    screen.blit(FONT.render(f"Computer Score: {computer_score}", True, BLACK), (750, SCREEN_HEIGHT - 50))
    screen.blit(FONT.render(f"Player Score: {player_score}", True, BLACK), (50, SCREEN_HEIGHT - 50))
    if fastest_set>0: #only when we actually had a set by the player. When there hasn't been a set found by the player, fastest_set=-1 (see init_game)
        screen.blit(FONT.render(f"Fastest set: {round(fastest_set,1)}", True, BLACK), (50, SCREEN_HEIGHT - 90))
    else:
        screen.blit(FONT.render(f"Fastest set: -", True, BLACK), (50, SCREEN_HEIGHT - 90))
    if len(not_in_set_cards)<=0 or cheat_amount>=6: #when the hide card button is not displayd, we should display this message
        screen.blit(FONT.render("No hide's left!", True, RED), (SCREEN_WIDTH - 250, 60))
            #drawing a rectangle for the inputs 
    input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 60, 200, 40)
    pygame.draw.rect(screen, WHITE, input_rect)
            #in this rectangle, display the warning if possible and the inputted text
    if warning!="":
        screen.blit(FONT.render(warning, True, RED), (input_rect.x + 5, input_rect.y + 5))
    screen.blit(FONT.render(input_text, True, BLACK), (input_rect.x + 5, input_rect.y + 5))

    #cards:
    for i, card in enumerate(S.cards_on_table):
        x = 50 + (i % 4) * 220
        y = 150 + (i // 4) * 150
        key = str(card)
        if key in card_images: #only if we could find the cards in the dictionary of cards
            if i in cheat_cards: #the card should be hided, so it is displayed black with the text "NOT IN SET"
                pygame.draw.rect(screen, BLACK, (x, y+2, CARD_HEIGHT, CARD_WIDTH))
                screen.blit(FONT.render("NOT IN SET", True, WHITE), (x +45, y + 35))
            else:
                screen.blit(card_images[key], (x, y))
                index_txt = FONT.render(str(i+1), True, BLACK)
                screen.blit(index_txt, (x + CARD_WIDTH // 2 - 40, y - 25))
        else: #display a gray card when the card is not available in the dictionary
            pygame.draw.rect(screen, GRAY, (x, y, CARD_HEIGHT, CARD_WIDTH))
            screen.blit(FONT.render("?", True, BLACK), (x + 90, y + 50))
        if i in selected_cards: #higlight the card if it is selected in the input
            pygame.draw.rect(screen, BLUE, (x, y+2,CARD_HEIGHT , CARD_WIDTH), 8) #changed HEIGHT and WITH in stead of rotating the rectangle
        if Pauze: #all the cards should be gray and with a questionmark
            pygame.draw.rect(screen, GRAY, (x, y+2, CARD_HEIGHT, CARD_WIDTH))
            screen.blit(FONT.render("?", True, BLACK), (x + 90, y + 50))
    
def green_screen():
    global fastest_set, buttons

    #screen:
    screen.fill(GREEN)

    #button:
    buttons.clear()
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY, "Continue", continue_from_green)
    exit_game_button = Button((20, 20, 130, 40), GRAY, "Exit game", lambda: (change_state(END)))

    buttons = [continue_btn, exit_game_button]
    for button in buttons:
        button.draw(screen)

    #text:
    msg = BIG_FONT.render("Correct Set!", True, BLACK)
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 140))
    text = FONT.render(f"Time used: {round(current_time_used, 1)}s", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 340))
    text = FONT.render(f"Your correct set:", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 190))
    if fastest_set>0:
        text = FONT.render(f"Fastest set: {round(fastest_set, 1)}s", True, BLACK)
    else:
        text = FONT.render(f"Fastest set: -", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    text = FONT.render(f"Deck: {len(S.cards_on_deck)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 460))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 430))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 400))

    #cards:
    for i, card in enumerate(selected_set): #display cards of the set from the user, whitch are the cards who are selected via the input
        x = SCREEN_WIDTH//2 + (i % 4) * 220 -320
        y = 230
        key = str(card)
        if key in card_images:
            screen.blit(card_images[key], (x, y))
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))
            screen.blit(FONT.render("UNKNOWN CARD", True, BLACK), (x + 90, y + 50))

def red_screen(gevonden_set):
    global selected_set, input_text, buttons

    #screen:
    screen.fill(WHITE)

    #button:
    buttons.clear()
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY, "Continue", continue_from_red)
    exit_game_button = Button((20, 20, 130, 40), GRAY, "Exit game", lambda: (change_state(END)))

    buttons=[continue_btn, exit_game_button]
    for button in buttons:
        button.draw(screen)

    #text:
    msg = BIG_FONT.render("Wrong set!", True, BLACK)
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 10))
    text = FONT.render(f"The computer found this set:", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 220))
    text = FONT.render(f"Your incorrect set:", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 60))
    if fastest_set>0:
        text = FONT.render(f"Fastest set: {round(fastest_set, 1)}s", True, BLACK)
    else:
        text = FONT.render(f"Fastest set: -", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    text = FONT.render(f"Time used: {round(get_timer_for_difficulty()-round_timer, 1)}s", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 560))
    text = FONT.render(f"Deck: {len(S.cards_on_deck)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 460))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 430))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 400))

    #cards:
    for i, card in enumerate(selected_set): #display the wrong set the user inputted 
        x = SCREEN_WIDTH//2 + (i % 4) * 220 -320
        y = 100
        key = str(card)
        if key in card_images:
            screen.blit(card_images[key], (x, y))
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))
            screen.blit(FONT.render("UNKNOWN CARD", True, BLACK), (x + 90, y + 50))
    for i, card in enumerate(gevonden_set): #display the correct set the computer found
        x = SCREEN_WIDTH//2 + (i % 4) * 220 -320
        y = 260
        key = str(card)
        if key in card_images:
            screen.blit(card_images[key], (x, y))
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))
            screen.blit(FONT.render("UNKNOWN CARD", True, BLACK), (x + 90, y + 50))

def red_no_set_screen():
    global selected_set, input_text, buttons

    #screen:
    screen.fill(RED)

    #button:
    buttons.clear()
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY, "Continue", continue_from_red_no_set)
    exit_game_button = Button((20, 20, 130, 40), GRAY, "Exit game", lambda: (change_state(END)))

    buttons= [continue_btn, exit_game_button]
    for button in buttons:
        button.draw(screen)
    
    #text:
    msg = BIG_FONT.render("Wrong set!", True, BLACK)
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 110))
    text = BIG_FONT.render(f"There was no set possible", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 320))
    text = FONT.render(f"Your incorrect set:", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 160))
    if fastest_set>0:
        text = FONT.render(f"Fastest set: {round(fastest_set, 1)}s", True, BLACK)
    else:
        text = FONT.render(f"Fastest set: -", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    text = FONT.render(f"Time used: {round(get_timer_for_difficulty()-round_timer, 1)}s", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 560))
    text = FONT.render(f"Deck: {len(S.cards_on_deck)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 460))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 430))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 400))

    #cards:
    for i, card in enumerate(selected_set): #display the wrong set from the user
        x = SCREEN_WIDTH//2 + (i % 4) * 220 -320
        y = 200
        key = str(card)
        if key in card_images:
            screen.blit(card_images[key], (x, y))
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))
            screen.blit(FONT.render("UNKNOWN CARD", True, BLACK), (x + 90, y + 50))

def time_screen(gevonden_set):
    global buttons

    #screen:
    screen.fill(ORANGE)

    #buttons:
    buttons.clear()
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY, "Continue", continue_from_time)
    exit_game_button = Button((20, 20, 130, 40), GRAY, "Exit game", lambda: (change_state(END)))

    buttons = [continue_btn, exit_game_button]
    for button in buttons:
        button.draw(screen)

    #text:
    msg = BIG_FONT.render("TIME IS OVER!", True, BLACK)
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 170))
    text = FONT.render(f"The computer found this set:", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 220))
    if fastest_set>0:
        text = FONT.render(f"Fastest set: {round(fastest_set, 1)}s", True, BLACK)
    else:
        text = FONT.render(f"Fastest set: -", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    text = FONT.render(f"Deck: {len(S.cards_on_deck)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 460))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 430))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 400))

    #cards:
    for i, card in enumerate(gevonden_set): #display the set the computer found
        x = SCREEN_WIDTH//2 + (i % 4) * 220 -320
        y = 260
        key = str(card)
        if key in card_images:
            screen.blit(card_images[key], (x, y))
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))
            screen.blit(FONT.render("UNKNOWN CARD", True, BLACK), (x + 90, y + 50))

def grey_screen():
    global buttons

    #screen:
    screen.fill(GRAY)

    #buttons:
    buttons.clear()
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 400, 200, 50), BLUE,  "Continue", continue_from_grey)
    exit_game_button = Button((20, 20, 130, 40), WHITE, "Exit game", lambda: (change_state(END)))

    buttons = [continue_btn, exit_game_button]
    for button in buttons:
        button.draw(screen)

    #text:
    msg = BIG_FONT.render("Time over: No sets possible!", True, BLACK)
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))
    if fastest_set>0:
        text = FONT.render(f"Fastest set: {round(fastest_set, 1)}s", True, BLACK)
    else:
        text = FONT.render(f"Fastest set: -", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 280))
    text = FONT.render(f"Cards 1, 2 and 3 will be replaced. ", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250))
    text = FONT.render(f"Deck: {len(S.cards_on_deck)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 340))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 310))

def no_set_correct_screen():
    global buttons

    #screen:
    screen.fill(GREEN2)

    #buttons:
    buttons.clear()
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY,  "Continue", continue_from_no_set_correct)
    exit_game_button = Button((20, 20, 130, 40), GRAY, "Exit game", lambda: (change_state(END)))

    buttons = [continue_btn, exit_game_button]
    for button in buttons:
        button.draw(screen)

    #text:
    msg = BIG_FONT.render("You are correct, no sets possible!", True, BLACK)
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 160))
    msg2 = FONT.render("You get 5 points!", True, BLACK)
    screen.blit(msg2, (SCREEN_WIDTH // 2 - msg2.get_width() // 2, 200))
    if fastest_set>0:
        text = FONT.render(f"Fastest set: {round(fastest_set, 1)}s", True, BLACK)
    else:
        text = FONT.render(f"Fastest set: -", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 280))
    text = FONT.render(f"Cards 1, 2 and 3 will be replaced. ", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250))
    text = FONT.render(f"Deck: {len(S.cards_on_deck)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 340))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 310))

def no_set_incorrect_screen(gevonden_set):
    global buttons

    #screen:
    screen.fill(RED2)

    #buttons:
    buttons.clear()
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY, "Continue", continue_from_time)
    exit_game_button = Button((20, 20, 130, 40), GRAY, "Exit game", lambda: (change_state(END)))

    buttons = [continue_btn, exit_game_button]
    for button in buttons:
        button.draw(screen)

    #text:
    msg = BIG_FONT.render("You are wrong, there is a set possible!", True, BLACK)
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 170))
    text = FONT.render(f"The computer found this set:", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 220))
    if fastest_set>0:
        text = FONT.render(f"Fastest set: {round(fastest_set, 1)}s", True, BLACK)
    else:
        text = FONT.render(f"Fastest set: -", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 370))
    text = FONT.render(f"Deck: {len(S.cards_on_deck)} cards", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 460))
    text = FONT.render(f"Computer Score: {computer_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 430))
    text = FONT.render(f"Player Score: {player_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 400))

    #cards:
    for i, card in enumerate(gevonden_set): #display the by the computer found correct set
        x = SCREEN_WIDTH//2 + (i % 4) * 220 -320
        y = 260
        key = str(card)
        if key in card_images:
            screen.blit(card_images[key], (x, y))
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))
            screen.blit(FONT.render("UNKNOWN CARD", True, BLACK), (x + 90, y + 50))

def end_screen():
    global buttons
    
    #screen:
    screen.fill(WHITE)

    #buttons:
    buttons.clear()
    continue_btn = Button((SCREEN_WIDTH // 2 - 100, 500, 200, 50), GRAY, "Back to Menu", lambda: (init_game(), change_state(START)))

    buttons = [continue_btn]
    for button in buttons:
        button.draw(screen)

    #text:
    if automative_end: #the computer decided it is over
            title = BIG_FONT.render("Game ended: no sets possible anymore!", True, BLACK)
    else: #the player decided the game is over
        title = BIG_FONT.render("Game ended!", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
    #determine the winner:
    if player_score>computer_score:
        winner="You won!"
    elif player_score<computer_score:
        winner="The computer won!"
    else:
        winner="Draw!"
    under_title = BIG_FONT.render(winner, True, BLACK)
    screen.blit(under_title, (SCREEN_WIDTH // 2 - under_title.get_width() // 2, 210))
    score_text = FONT.render(f"Final Score — Player: {player_score} | Computer: {computer_score}", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))
    time_text = FONT.render(f"Total Time: {int(total_elapsed_time)//60} minutes and {int(total_elapsed_time)-60*(int(total_elapsed_time)//60)} seconds", True, BLACK)
    screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, 360))
    if fastest_set>0:
        fasttime_text = FONT.render(f"Fastest set in {round(fastest_set,1)} seconds", True, BLACK)
    else:
        fasttime_text = FONT.render(f"Fastest set: -", True, BLACK)
    screen.blit(fasttime_text, (SCREEN_WIDTH // 2 - fasttime_text.get_width() // 2, 280))
    

'''
CONTINUE FUNCTIONS

These functions will be used when the corresponding screen is ended and we move towards the next screen. (for example, when moving from a red screen to game, we run "continue from red")
In general, these functions are aimed at updating the cards on table, deleting a set from table, adding cards, etc, because this should only be done once in stead of every time the screen is displayed
For further explanaition, see the notitions in the functions itself.
'''
def continue_from_start():
    change_state(RULES)

def continue_from_green():
    S.verwijder_set(*choosen_indices) #delete the set from the user from the table, and therefore use the indices of these cards
    S.voeg_kaarten_toe_op_tafel() #add extra cards on table (if possible, see documentation of this function in "classes" file)
    change_state(GAME)

def continue_from_red():
    S.voeg_kaarten_toe_op_tafel() #the set is already deleted by giving the computer set, so only add extra cards
    change_state(GAME)

def continue_from_red_no_set():
    S.verwijder_eerste_3_kaarten() #delete first three cards from table and add three extra ones
    change_state(GAME)

def continue_from_time():
    S.voeg_kaarten_toe_op_tafel() #the set is already deleted by giving the computer set, so only add extra cards
    change_state(GAME)

def continue_from_grey():
    S.verwijder_eerste_3_kaarten() #delete first three cards from table and add three extra ones
    change_state(GAME)

def continue_from_no_set_correct():
    S.verwijder_eerste_3_kaarten() #delete first three cards from table and add three extra ones
    change_state(GAME)

def continue_from_no_set_incorrect():
    S.voeg_kaarten_toe_op_tafel() #the set is already deleted by giving the computer set, so only add extra cards
    change_state(GAME)


'''
MAIN LOOP

This is the main loop of the code. We first init the first game, then start the loop where we investigate, using the users input, which STATE we should go to. In the end we display this state
For further information, see notitions in the loop
'''

# Main loop
init_game()
running = True
while running:
    #basics:
    clock.tick(FPS)
    screen.fill(WHITE)

    #If in game: update times and timer, check corner case to end the game and check the timer
    if state==GAME:
        # if with all possible cards on table and in the deck together there are no sets possible, we should end the game by computer. So automatice_end because True (which could be used to 
        #determine the text on the end_game screen). THere has been prooven that this could only be the case with lower than 20 cards.
        if len(S.cards_on_deck+S.cards_on_table)<=20:
            if len(all_possible_sets)==0: #helpfull to already use the checked sets on table if there is a set possible. If not, incorporate also the cards in deck
                if len(S.controleer_sets(S.cards_on_deck+S.cards_on_table))==0:
                    automative_end=True
                    change_state(END)
        #update the wait_times for pauze and cheat if neccesary
        if wait_pauze>0:
            wait_pauze-= 1/FPS
        if wait_cheat>0:
            wait_cheat-=1 / FPS
        #update the time in game and total elapsed time in game, only when not pauzed
        if Pauze == False:
            round_timer -= 1 / FPS
            total_elapsed_time += 1 / FPS
        # if time is over, depended on whether there are possible sets on table or not, change to TIME_OVER or GREY_SCREEN
        if round_timer <= 0:
            if len(all_possible_sets)!=0:
                update_score("computer")
                computer_set=find_set_by_computer()
                change_state(TIME_OVER)
            else:
                change_state(GREY_SCREEN)

    #handle input of user
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.handle_event(event)
        #only when in game, use input to determine the input_string
        if event.type == pygame.KEYDOWN and state == GAME:
            warning=""
            #check pauze
            if event.key == pygame.K_b:
                pauze_change()
            #only use input when game is not pauzed
            if not Pauze:
                #n = no set button
                if event.key == pygame.K_n:
                    no_set_button.callback()
                #h = hide cards button
                elif event.key == pygame.K_h:
                    if len(not_in_set_cards)>0 and cheat_amount<6: #only go to cheat when allowed
                        cheat()
                #backspace
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                #add to string (in other cases)
                elif event.key != pygame.K_BACKSPACE and event.key != pygame.K_RETURN and event.key != pygame.K_b :
                    input_text += event.unicode
                #if space, enter or backspace, updat the selected cards to display on screen
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_BACKSPACE:
                    try:
                        indices = list(map(int, input_text.strip().split()))
                        selected_cards = [index-1 for index in indices] #list of choosen indices, input is from 1 to 12, in python from 0 to 11
                        if max(selected_cards)>12 or min(selected_cards)<0:
                            print_warning("Index not in range!")
                    except:
                        print_warning("No integer!")
                # if users enters final input with return:
                if event.key == pygame.K_RETURN:
                    try:
                        if len(indices) == 3 and len(set(indices)) == 3: #are there 3 different indices
                            selected_set = [S.cards_on_table[i] for i in selected_cards] #make a list of all the selected cards as cards (selected_cards are the indices)
                            if selected_set[0].check_3_cards_if_set(selected_set[1], selected_set[2]): #check if set is correct
                                choosen_indices = indices
                                update_score("player")
                                set_fastest_time() #there is a new time, so update the fastest time if possible
                                change_state(GREEN_SCREEN)
                                
                            else:
                                update_score("computer")
                                if len(all_possible_sets)==0: #if no sets possible at all
                                    change_state(RED_NO_SET_SCREEN)
                                else:
                                    computer_set=find_set_by_computer()  #let the computer find a set
                                    change_state(RED_SCREEN)
                        else:
                            if len(indices) < 3:
                                print_warning("Not enough cards!")
                            elif len(indices) >3:
                                print_warning("Too many cards!")
                            else:
                                print_warning("Same cards selected!")
                    except:
                        pass

    #display the correct state using the dictionary
    if state in state_functions:
        state_functions[state]()

    pygame.display.flip()

pygame.quit()
sys.exit()