import random
from itertools import combinations
import pygame
from constants import *

pygame.init()
pygame.font.init()


'''
This file "classes" incorporates the three different classes used in the game. We have:
    - Kaart: the class for the cards, with comparison of cards, printing cards and their properties
    - Spel: the class for the game logic, with initializing all the cards and all the functions needed to delete a set, add extra cards,
        find sets by computer, etc
    - Button: the class for the buttons, with draw, handle event and equaly
For more information, go to the section itself.
'''


'''
Kaart: This class represents a single card in the game. We have instance methods
    - __str__: to print the card properties toghether in the same name as the card images of the game
    - check_1_eigenschap: check whether a give property of the cards is correct regarding the rules of set
    - check_3_cards_if_set: check, given 3 cards, whether it is a set or not
    -__eq__: to check whether two Kaart objects are the same cards or not
'''

class Kaart:
    def __init__(self, kleur, vorm, vulling, aantal):
        self.aantal = str(aantal)
        self.kleur = str(kleur)
        self.vulling = str(vulling)
        self.vorm = str(vorm)

    def __str__(self):
        return f"{self.kleur}{self.vorm}{self.vulling}{self.aantal}"

    def check_1_eigenschap(self, other_1, other_2, eigenschap):
        kaart1 = getattr(self, eigenschap)
        kaart2 = getattr(other_1, eigenschap)
        kaart3 = getattr(other_2, eigenschap)
        return (kaart1 == kaart2 == kaart3) or (kaart1 != kaart2 and kaart2 != kaart3 and kaart3 != kaart1)

    def check_3_cards_if_set(self, other_1, other_2):
        return all(self.check_1_eigenschap(other_1, other_2, eigenschap) for eigenschap in ["aantal", "kleur", "vulling", "vorm"])

    def __eq__(self, other):
        return (self.aantal == other.aantal and self.kleur == other.kleur and self.vulling == other.vulling and self.vorm == other.vorm)


'''
Spel: This class represents a single game of set with all its logic and properties. We have instance methods
    - print_kaarten: given a list of cards, print the enumerated cards of the list
    - print_gevonden_set: print the sets the computer found itself
    - maak_start_tafel: initialize the cards on table for first time
    - controleer_sets: given a list of cards, find all the possible sets and return them in a list with sets (the set itself is also a list)
    - all_cards_not_in_set: given the cards on table, give a list with all the cards on table who are not in any possible set. 
    - verwijder_set: given three indices of cards on table, delete these cards
    - voeg_kaarten_toe_op_tafel: add three cards to the table (if there are still cards on the deck)
    - verwijder_willekeurige_set: delete a random set found by the computer and return this set as a list
    - verwijder_eerste_3_kaarten: delete the first three cards of the table and add three extra cards to the table if possible
For more information, see the notations at the functions itself.
'''

class Spel:
    def __init__(self, kleuren, vormen, vullingen, aantallen):
        self.kleuren = kleuren
        self.vormen = vormen
        self.vullingen = vullingen
        self.aantallen = aantallen
        #all sets currently found in the game
        self.gevonden_sets = [] 
        #all cards on the deck
        self.cards_on_deck = [Kaart(kleur, vorm, vulling, aantal)
                             for aantal in self.aantallen
                             for kleur in self.kleuren
                             for vulling in self.vullingen
                             for vorm in self.vormen]
        self.cards_on_table = []

    def print_kaarten(self, kaarten_lijst):
        for i, kaart in enumerate(kaarten_lijst, 1):
            print(f"{i}e kaart:", kaart)

    def print_gevonden_sets(self):
        for item in self.gevonden_sets:
            self.print_kaarten(item)

    def maak_start_tafel(self):
        #choose 12 random cards from deck
        actieve_kaarten = random.sample(self.cards_on_deck, 12)
        #remove these cards from the deck
        for kaart in actieve_kaarten:
            self.cards_on_deck.remove(kaart)
        #add these cards to the table
        self.cards_on_table = actieve_kaarten

    def controleer_sets(self, cards=""):
        #if no input is give, use the cards on table to determine the sets, else use the inputted list of cards
        if cards=="":
            return [combo for combo in combinations(self.cards_on_table, 3) if combo[0].check_3_cards_if_set(combo[1], combo[2])]
        else:
            return [combo for combo in combinations(cards, 3) if combo[0].check_3_cards_if_set(combo[1], combo[2])]
        
    def all_cards_not_in_sets(self):
        #find all possible sets
        found_sets=self.controleer_sets()
        cards=[] #all cards in sets
        index=[] #the indices of the cards in a set
        correct_index=list(range(12)) #list of all indices of cards on table
        #add the cards from the sets to the cards list if this cards is not in the list yet
        for i in range(len(found_sets)):
            for j in range(3):
                if found_sets[i][j] not in cards:
                    cards.append(found_sets[i][j])
        #add the indices of the cards from the sets to the index list                
        for card in cards:
            index.append(self.cards_on_table.index(card))
        #delete these indices from the indices of all the cards on table    
        for id in index:
            correct_index.remove(id)
        return correct_index #this list only possesses the indices of cards who are not in any set

    def verwijder_set(self, index1, index2, index3): #the indices as input are from 1 to 12
        new_set = [self.cards_on_table[i - 1] for i in [index1, index2, index3]] #the three cards in the set 
        self.gevonden_sets.append(new_set)
        for i in sorted([index1, index2, index3], reverse=True):
            del self.cards_on_table[i - 1] #delete the cards from the table

    def voeg_kaarten_toe_op_tafel(self):
        aantal_toevoegen = min(3, len(self.cards_on_deck)) #only add three cards if there are (more than) 3 cards in the deck
        for _ in range(aantal_toevoegen):
            kaart = random.choice(self.cards_on_deck) #choose random card from deck
            self.cards_on_table.append(kaart)
            self.cards_on_deck.remove(kaart)

    def verwijder_willekeurige_set(self):
        random_set = random.choice(self.controleer_sets()) #choose one random set from all possible sets
        indices = [self.cards_on_table.index(k) + 1 for k in random_set] #make a list of the corresponding indices to input in verwijder_set function
        self.verwijder_set(*indices)
        return random_set

    def verwijder_eerste_3_kaarten(self):
        verwijderde_kaarten = self.cards_on_table[:3] 
        del self.cards_on_table[:3] #delete first three cards
        self.voeg_kaarten_toe_op_tafel() #add extra cards
        self.cards_on_deck.extend(verwijderde_kaarten)


'''
Button: this class represents the buttons we create in the game. The ask for a rectangle, color, text and a callback function to call when the button is selected.
We have instance methods:
    - draw: to draw the button on the surface
    - handle_event: when to call the callback function
    - __eq__: to check whether buttons are the same
'''

class Button:
    def __init__(self, rect, color, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.color = color

    def draw(self, surface):
        from main import selected_button
        pygame.draw.rect(surface, self.color, self.rect)
        if self == selected_button: #if this button is the selected button, it should be highlighted
            pygame.draw.rect(surface, RED, self.rect, 4)
        txt = FONT.render(self.text, True, BLACK)
        surface.blit(txt, (self.rect.x + 10, self.rect.y + 10))
    
    def handle_event(self, event):
        #only when pressed on the button, call the callback function
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def __eq__(self, other): #use this in the draw function above
        #only check if other is a Button as well
        if isinstance(other, Button):
            return self.rect==other.rect and self.color==other.color and self.text==other.text
        return False

