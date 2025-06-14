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
        

    def __eq__(self, other):
        return (self.aantal == other.aantal and self.kleur == other.kleur and self.vulling == other.vulling and self.vorm == other.vorm)
    

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
        self.gevonden_sets=[]
    
    def print_kaarten(self, kaarten_lijst):
        x=1
        for kaart in kaarten_lijst:
            print(f"{x}e kaart:", kaart)
            x+=1
    
    def print_gevonden_sets(self):
        for item in self.gevonden_sets:
            self.print_kaarten(item)
    
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
    
    def verwijder_set(self, index1, index2, index3, huidige_tafel):
        new_set=[]
        for index in [index1, index2, index3]:
            new_set.append(huidige_tafel[index-1])
            huidige_tafel[index-1]=False
        self.gevonden_sets.append(new_set)
        for i in range(len(huidige_tafel)-1,-1,-1):
            if type(huidige_tafel[i])!=Kaart:
                huidige_tafel.pop(i) 
        
    def voeg_kaarten_toe_op_tafel(self, huidige_tafel):
        print("de kaarten die nu zijn toegevoegd:")
        for _ in range(3):
            new_kaart_index=random.choice(range(0,len(self.alle_kaarten)))
            print(self.alle_kaarten[new_kaart_index])
            huidige_tafel.append(self.alle_kaarten[new_kaart_index])
            self.alle_kaarten.pop(new_kaart_index)
    
    def verwijder_willekeurige_set(self, huidige_tafel):
        random_set=random.choice(self.controleer_sets(huidige_tafel))
        print("de gevonden set is: ")
        for kaart in random_set:
            print(kaart)
        index1=huidige_tafel.index(random_set[0])+1
        index2=huidige_tafel.index(random_set[1])+1
        index3=huidige_tafel.index(random_set[2])+1
        self.verwijder_set(index1, index2, index3, huidige_tafel)
        
    def verwijder_random_kaarten_op_tafel(self, huidige_tafel):
        gekozen_indices=[]
        mogelijke_index=list(range(12))
        verwijderde_kaarten_lijst=[]
        for _ in range(3):
            new_index=random.choice(mogelijke_index)
            gekozen_indices.append(new_index)
            verwijderde_kaarten_lijst.append(huidige_tafel[new_index])
            mogelijke_index.remove(new_index)
        for index in gekozen_indices:
            huidige_tafel[index]=False
        for i in range(11,-1,-1):
            if type(huidige_tafel[i])!=Kaart:
                huidige_tafel.pop(i) 
        print("de verwijderde kaarten zijn: ") 
        self.print_kaarten(verwijderde_kaarten_lijst)
        self.voeg_kaarten_toe_op_tafel(huidige_tafel)
        for kaart in verwijderde_kaarten_lijst:
            self.alle_kaarten.append(kaart)

    def verwijder_eerste_3_kaarten(self, huidige_tafel):
        gekozen_indices=[0,1,2]
        verwijderde_kaarten_lijst=[]
        for index in gekozen_indices:
            verwijderde_kaarten_lijst.append(huidige_tafel[index])
            huidige_tafel[index]=False
        for i in range(2,-1,-1):
            if type(huidige_tafel[i])!=Kaart:
                huidige_tafel.pop(i) 
        print("de verwijderde kaarten zijn: ") 
        self.print_kaarten(verwijderde_kaarten_lijst)
        self.voeg_kaarten_toe_op_tafel(huidige_tafel)
        for kaart in verwijderde_kaarten_lijst:
            self.alle_kaarten.append(kaart)

def game():
    punten_speler=0
    punten_computer=0
    SET=Spel([1,2,3], ["rood", "groen", "paars"], ["leeg", "gestreept", "vol"], ["ovaal", "ruit", "golf"])
    start_tafel=SET.maak_start_tafel()
    x=True
    while x:
        print("\n \n \n De kaarten op tafel zijn:")
        SET.print_kaarten(start_tafel)
        print(f"Er zijn nog {len(SET.alle_kaarten)} kaarten in de pot.")
        print("type hieronder 'geen set gevonden' als je geen set gevonden hebt. type anders 'kaartnummer1 kaartnummer2 kaartnummer3' ald je denkt dat deze kaartnummers een set vormen(bijvorbeeld '8 4 6' als kaarten 8, 4 en 6 een set vormen)")
        inputs=input()
        if inputs=="geen set gevonden":
            print("\n \n ")
            if len(SET.controleer_sets(start_tafel))!=0:
                if len(SET.alle_kaarten)>0:
                    SET.verwijder_willekeurige_set(start_tafel)
                    SET.voeg_kaarten_toe_op_tafel(start_tafel)
                    punten_computer+=1
                    print("\n")
                    print(f"punten speler= {punten_speler} & punten computer= {punten_computer}")
                else:
                    SET.verwijder_willekeurige_set(start_tafel)
                    punten_computer+=1
                    print("\n")
                    print(f"punten speler= {punten_speler} & punten computer= {punten_computer}")
      

            else:
                print("ik heb geen set gevonden, ik verwijder 3 random kaarten op tafel")
                SET.verwijder_eerste_3_kaarten(start_tafel)
                print("\n")
                print(f"puntenspeler= {punten_speler} & punten computer= {punten_computer}")
        elif len(inputs.split(" "))==3:
            try:
                int(inputs.split(" ")[0]) and int(inputs.split(" ")[1]) and int(inputs.split(" ")[2])
                if (int(inputs.split(" ")[0]) in range(12)) and (int(inputs.split(" ")[1]) in range(12)) and (int(inputs.split(" ")[2]) in range(12)):
                    if int(inputs.split(" ")[0])!=int(inputs.split(" ")[1]) and int(inputs.split(" ")[2])!=int(inputs.split(" ")[1]) and int(inputs.split(" ")[0])!=int(inputs.split(" ")[2]):
                        inputslist=inputs.split(" ")
                        index1=int(inputslist[0])
                        index2=int(inputslist[1])
                        index3=int(inputslist[2])
                        kaart1=start_tafel[index1 - 1]
                        kaart2=start_tafel[index2 - 1]
                        kaart3=start_tafel[index3 - 1]
                        if kaart1.check_3_cards_if_set(kaart2, kaart3):
                            print("de set is goed")
                            SET.verwijder_set(index1, index2,index3, start_tafel)
                            if len(SET.alle_kaarten)>0:
                                SET.voeg_kaarten_toe_op_tafel(start_tafel)
                            print("\n")
                            punten_speler+=1
                            print(f"punten speler= {punten_speler} & punten computer= {punten_computer}")
                        else:
                            print("de set is fout")
                            print("\n")
                            print(f"punten speler= {punten_speler} & punten computer= {punten_computer}")  
                    else:
                        print("ongeldig: getallen dubbel genoemd")
                else:
                    print("ongeldig: getallen buiten bereik van 1 tot en met 12")
            except:
                print("er zit een letter of een decimaal getal bij")
        else:
            print("ongeldig: verkeerde input, misschien bedoel je 'geen set gevonden?'")
        if len(SET.alle_kaarten+start_tafel)<=20:
            if len(SET.controleer_sets(SET.alle_kaarten+start_tafel))==0:
                print("er zijn dit spel geen sets meer mogelijk")
                x=False
        print("klik op enter om door te gaan")
        input()
    print(f"het spel is klaar, de uislag is: punten speler= {punten_speler} & punten computer= {punten_computer}")

def main():
    game()
if __name__=="__main__":
    main()

    

  