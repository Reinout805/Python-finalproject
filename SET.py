import random
from itertools import combinations
class Kaart:
    def __init__(self, aantal, kleur, vulling, vorm):
        self.aantal=aantal
        self.kleur=kleur
        self.vulling=vulling
        self.vorm=vorm
    
    def __str__(self):
        return f"{self.aantal}, {self.kleur}, {self.vulling}, {self.vorm}"
    
    def check_1_eigenschap(self, other_1, other_2, eigenschap):
        kaart1=getattr(self, eigenschap)
        kaart2=getattr(other_1, eigenschap)
        kaart3=getattr(other_2, eigenschap)
        if (kaart1==kaart2==kaart3) or (kaart1!=kaart2 and kaart2!=kaart3 and kaart3!=kaart1):
            return True
        else:
            return False
    
    def check_3_cards_if_set(self, other_1, other_2):
        bool_list=[]
        for eigenschap in ["aantal", "kleur", "vulling", "vorm"]:
            bool_list.append(self.check_1_eigenschap(other_1, other_2, eigenschap))
        if bool_list==[True , True, True, True]:
            return True
        else:
            return False
class Spel:
    def __init__(self, aantallen, kleuren, vullingen, vormen):
        self.aantallen=aantallen
        self.kleuren=kleuren
        self.vullingen=vullingen
        self.vormen=vormen

        kaarten_list=[]
        for aantal in self.aantallen:
            for kleur in self.kleuren:
                for vulling in self.vullingen:
                    for vorm in self.vormen:
                        kaarten_list.append(Kaart(aantal, kleur, vulling, vorm))
        self.alle_kaarten=kaarten_list

    def maak_start_tafel(self):
        actieve_kaarten=[]
        for _ in range(12):
            new_kaart_index=random.choice(range(0,len(self.alle_kaarten)))
            actieve_kaarten.append(self.alle_kaarten[new_kaart_index])
            self.alle_kaarten.pop(new_kaart_index)
        return  actieve_kaarten
    
    def controleer_sets(self, huidige_tafel):
        gevonden_sets=[]
        mogelijke_sets=combinations(huidige_tafel,3)
        for combination in mogelijke_sets:
            if combination[0].check_3_cards_if_set(combination[1], combination[2]):
                gevonden_sets.append(combination)
        return gevonden_sets

def main():
    pass
if __name__=="__main__":
    main()

    

    