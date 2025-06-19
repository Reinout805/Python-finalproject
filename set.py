import random
from itertools import combinations

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
        return actieve_kaarten

    def controleer_sets(self, huidige_tafel):
        return [combo for combo in combinations(huidige_tafel, 3) if combo[0].check_3_cards_if_set(combo[1], combo[2])]

    def all_cards_not_in_sets(self, huidige_tafel):
        found_sets=self.controleer_sets(huidige_tafel)
        cards=[]
        index=[]
        correct_index=list(range(12))
        if len(found_sets)>0:
            for i in range(len(found_sets)):
                for j in range(3):
                    if found_sets[i][j] not in cards:
                        cards.append(found_sets[i][j])
        for card in cards:
            index.append(huidige_tafel.index(card))
        for id in index:
            correct_index.remove(id)
        return correct_index

    def verwijder_set(self, index1, index2, index3, huidige_tafel):
        new_set = [huidige_tafel[i - 1] for i in [index1, index2, index3]]
        self.gevonden_sets.append(new_set)
        for i in sorted([index1, index2, index3], reverse=True):
            del huidige_tafel[i - 1]
        return huidige_tafel

    def voeg_kaarten_toe_op_tafel(self, huidige_tafel):
        aantal_toevoegen = min(3, len(self.alle_kaarten))
        for _ in range(aantal_toevoegen):
            kaart = random.choice(self.alle_kaarten)
            huidige_tafel.append(kaart)
            self.alle_kaarten.remove(kaart)
        return huidige_tafel

    def verwijder_willekeurige_set(self, huidige_tafel):
        random_set = random.choice(self.controleer_sets(huidige_tafel))
        indices = [huidige_tafel.index(k) + 1 for k in random_set]
        self.verwijder_set(*indices, huidige_tafel)
        return huidige_tafel, random_set

    def verwijder_eerste_3_kaarten(self, huidige_tafel):
        verwijderde_kaarten = huidige_tafel[:3]
        del huidige_tafel[:3]
        self.voeg_kaarten_toe_op_tafel(huidige_tafel)
        self.alle_kaarten.extend(verwijderde_kaarten)
        return huidige_tafel


def game():
    punten_speler = 0
    punten_computer = 0
    SET = Spel(["green", "purple", "red"], ["oval", "diamand", "squiggle"], ["empty", "shaded", "filled"], ["1", "2", "3"])
    start_tafel = SET.maak_start_tafel()
    x = True
    while x:
        print("\nDe kaarten op tafel zijn:")
        SET.print_kaarten(start_tafel)
        print(f"Er zijn nog {len(SET.alle_kaarten)} kaarten in de pot.")
        print("Type 'geen set gevonden' of drie kaartnummers gescheiden door spaties (bijv. '1 2 3'):")
        inputs = input()

        if inputs.lower() == "geen set gevonden":
            if SET.controleer_sets(start_tafel):
                if SET.alle_kaarten:
                    SET.verwijder_willekeurige_set(start_tafel)
                    SET.voeg_kaarten_toe_op_tafel(start_tafel)
                else:
                    SET.verwijder_willekeurige_set(start_tafel)
                punten_computer += 1
            else:
                print("Geen set gevonden, 3 kaarten worden vervangen.")
                SET.verwijder_eerste_3_kaarten(start_tafel)
        elif len(inputs.split()) == 3:
            try:
                index1, index2, index3 = map(int, inputs.split())
                if len(set([index1, index2, index3])) == 3 and all(1 <= idx <= len(start_tafel) for idx in [index1, index2, index3]):
                    kaart1 = start_tafel[index1 - 1]
                    kaart2 = start_tafel[index2 - 1]
                    kaart3 = start_tafel[index3 - 1]
                    if kaart1.check_3_cards_if_set(kaart2, kaart3):
                        print("de set is goed")
                        SET.verwijder_set(index1, index2, index3, start_tafel)
                        if SET.alle_kaarten:
                            SET.voeg_kaarten_toe_op_tafel(start_tafel)
                        punten_speler += 1
                    else:
                        print("de set is fout")
                else:
                    print("ongeldig: dubbele of ongeldige indices")
            except ValueError:
                print("ongeldig: invoer bevat geen geldige getallen")
        else:
            print("ongeldig: verkeerde input")

        if len(SET.alle_kaarten + start_tafel) <= 20 and not SET.controleer_sets(SET.alle_kaarten + start_tafel):
            print("er zijn geen sets meer mogelijk")
            x = False
        print("druk op enter om door te gaan")
        input()

    print(f"Spel afgelopen: speler {punten_speler}, computer {punten_computer}")


def main():
    game()

if __name__ == "__main__":
    main()
