import random
from itertools import combinations
from classes import Kaart, Spel

def game():
    punten_speler = 0
    punten_computer = 0
    SET = Spel(["green", "purple", "red"], ["oval", "diamand", "squiggle"], ["empty", "shaded", "filled"], ["1", "2", "3"])
    SET.maak_start_tafel()
    x = True
    while x:
        print("\nDe kaarten op tafel zijn:")
        SET.print_kaarten(SET.cards_on_table)
        print(f"Er zijn nog {len(SET.alle_kaarten)} kaarten in de pot.")
        print("Type 'geen set gevonden' of drie kaartnummers gescheiden door spaties (bijv. '1 2 3'):")
        inputs = input()

        if inputs.lower() == "geen set gevonden":
            if SET.controleer_sets():
                if SET.alle_kaarten:
                    SET.verwijder_willekeurige_set()
                    SET.voeg_kaarten_toe_op_tafel()
                else:
                    SET.verwijder_willekeurige_set()
                punten_computer += 1
            else:
                print("Geen set gevonden, 3 kaarten worden vervangen.")
                SET.verwijder_eerste_3_kaarten(SET.cards_on_table)
        elif len(inputs.split()) == 3:
            try:
                index1, index2, index3 = map(int, inputs.split())
                if len(set([index1, index2, index3])) == 3 and all(1 <= idx <= len(SET.cards_on_table) for idx in [index1, index2, index3]):
                    kaart1 = SET.cards_on_table[index1 - 1]
                    kaart2 = SET.cards_on_table[index2 - 1]
                    kaart3 = SET.cards_on_table[index3 - 1]
                    if kaart1.check_3_cards_if_set(kaart2, kaart3):
                        print("de set is goed")
                        SET.verwijder_set(index1, index2, index3)
                        if SET.alle_kaarten:
                            SET.voeg_kaarten_toe_op_tafel()
                        punten_speler += 1
                    else:
                        print("de set is fout")
                else:
                    print("ongeldig: dubbele of ongeldige indices")
            except ValueError:
                print("ongeldig: invoer bevat geen geldige getallen")
        else:
            print("ongeldig: verkeerde input")

        if len(SET.alle_kaarten + SET.cards_on_table) <= 20 and not SET.controleer_sets(SET.alle_kaarten + SET.cards_on_table):
            print("er zijn geen sets meer mogelijk")
            x = False
        print("druk op enter om door te gaan")
        input()

    print(f"Spel afgelopen: speler {punten_speler}, computer {punten_computer}")

def main():
    game()

if __name__ == "__main__":
    main()