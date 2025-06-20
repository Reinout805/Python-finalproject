import random
from itertools import combinations
import pygame
from constants import *

pygame.init()
pygame.font.init()


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

class Spel:
    def __init__(self, kleuren, vormen, vullingen, aantallen):
        self.kleuren = kleuren
        self.vormen = vormen
        self.vullingen = vullingen
        self.aantallen = aantallen
        self.gevonden_sets = []

        self.alle_kaarten = [Kaart(kleur, vorm, vulling, aantal)
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
        actieve_kaarten = random.sample(self.alle_kaarten, 12)
        for kaart in actieve_kaarten:
            self.alle_kaarten.remove(kaart)
        self.cards_on_table = actieve_kaarten

    def controleer_sets(self, cards=""):
        if cards=="":
            return [combo for combo in combinations(self.cards_on_table, 3) if combo[0].check_3_cards_if_set(combo[1], combo[2])]
        else:
            return [combo for combo in combinations(cards, 3) if combo[0].check_3_cards_if_set(combo[1], combo[2])]
    def all_cards_not_in_sets(self):
        found_sets=self.controleer_sets()
        cards=[]
        index=[]
        correct_index=list(range(12))
        if len(found_sets)>0:
            for i in range(len(found_sets)):
                for j in range(3):
                    if found_sets[i][j] not in cards:
                        cards.append(found_sets[i][j])
        for card in cards:
            index.append(self.cards_on_table.index(card))
        for id in index:
            correct_index.remove(id)
        return correct_index

    def verwijder_set(self, index1, index2, index3):
        new_set = [self.cards_on_table[i - 1] for i in [index1, index2, index3]]
        self.gevonden_sets.append(new_set)
        for i in sorted([index1, index2, index3], reverse=True):
            del self.cards_on_table[i - 1]

    def voeg_kaarten_toe_op_tafel(self):
        aantal_toevoegen = min(3, len(self.alle_kaarten))
        for _ in range(aantal_toevoegen):
            kaart = random.choice(self.alle_kaarten)
            self.cards_on_table.append(kaart)
            self.alle_kaarten.remove(kaart)

    def verwijder_willekeurige_set(self):
        random_set = random.choice(self.controleer_sets())
        indices = [self.cards_on_table.index(k) + 1 for k in random_set]
        self.verwijder_set(*indices)
        return random_set

    def verwijder_eerste_3_kaarten(self):
        verwijderde_kaarten = self.cards_on_table[:3]
        del self.cards_on_table[:3]
        self.voeg_kaarten_toe_op_tafel()
        self.alle_kaarten.extend(verwijderde_kaarten)

class Button:
    def __init__(self, rect, color, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.color = color

    def draw(self, surface):
        from main import selected_button
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

