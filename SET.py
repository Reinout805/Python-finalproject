import random
from itertools import combinations

class Kaart:
    def __init__(self, aantal, kleur, vulling, vorm):
        self.aantal=aantal
        self.kleur=kleur
        self.vulling=vulling
        self.vorm=vorm
    
    # om de eigenschappen van een kaart te kunnen printen
    def __str__(self):
        return f"{self.aantal}, {self.kleur}, {self.vulling}, {self.vorm}"
    
    #gegeven een eigenschap, controleer of alle drie de kaarten dezelfde of verschillende waardes hebben. 
    #Zo ja, dan kan dit een set vormen (return True) en anders geen set vormen (return False)
    def één_eigenschap_voldoet(self, other_1, other_2, eigenschap):
        kaart1=getattr(self, eigenschap)
        kaart2=getattr(other_1, eigenschap)
        kaart3=getattr(other_2, eigenschap)
        if (kaart1==kaart2==kaart3) or (kaart1!=kaart2 and kaart2!=kaart3 and kaart3!=kaart1):
            return True
        else:
            return False
    
    #gegeven een drietal kaarten, controleer of het een set vormt
    def controleer_set(self, other_1, other_2):
        eigenschappen = ["aantal", "kleur", "vulling", "vorm"]
        if self.één_eigenschap_voldoet(other_1, other_2, eigenschappen[0]):
            if self.één_eigenschap_voldoet(other_1, other_2, eigenschappen[0]):
                if self.één_eigenschap_voldoet(other_1, other_2, eigenschappen[0]):
                    return True
        return False        
    
    #gelijkheid tussen kaarten controleren
    def __eq__(self, other):
        return (self.aantal == other.aantal and self.kleur == other.kleur and self.vulling == other.vulling and self.vorm == other.vorm)

class Spel:
    def __init__(self, aantallen, kleuren, vullingen, vormen):
        self.aantallen=aantallen
        self.kleuren=kleuren
        self.vullingen=vullingen
        self.vormen=vormen
        
        #maak een lijst met alle kaarten, die in het begin in de stapel zitten
        stapel=[]
        for aantal in self.aantallen:
            for kleur in self.kleuren:
                for vulling in self.vullingen:
                    for vorm in self.vormen:
                        stapel.append(Kaart(aantal, kleur, vulling, vorm))
        self.stapel=stapel

        #lijst met kaarten op tafel en de gevonden sets
        self.tafel = []
        self.alle_sets = []

    #gegeven een lijst met daarin kaarten, print alle kaarten genummerd
    def print_kaarten(self, kaarten_lijst):
        x=1
        for kaart in kaarten_lijst:
            print(f"{x}e kaart:", kaart)
            x+=1
    
    #print alle gevonden sets
    def print_gevonden_sets(self):
        for set in self.alle_sets:
            self.print_kaarten(set)
    
    #maak de eerste tafel met 12 kaarten
    def initieer_tafel(self):
        for _ in range(12):
            #kies een index uit de lijst met alle kaarten op de stapel
            new_kaart_index=random.choice(range(0,len(self.stapel))) 
            #voeg deze kaart toe aan de tafel
            self.tafel.append(self.stapel[new_kaart_index])
            #verwijder deze kaart uit de stapel
            self.stapel.pop(new_kaart_index)
    
    #vind alle sets en geef deze terug in een lijst met tuples voor de sets, gegeven de huigdige tafel
    def vind_sets(self):
        gevonden_sets=[]
        #maak alle combinaties van kaarten die op tafel liggen
        alle_combinaties=combinations(self.tafel,3)
        for combination in alle_combinaties:
            #als de combinatie een set is, voeg hem toe aan de gevonden_sets lisjt
            if combination[0].controleer_set(combination[1], combination[2]):
                gevonden_sets.append(combination)
        return gevonden_sets
    
    #gegeven 3 kaarten die een set vormen, verwijder deze set van de tafel en voeg ze toe aan alle gevonden sets lijst
    def verwijder_set(self, index1, index2, index3):
        new_set=[]
        #voeg de kaarten toe aan een nieuwe lijst van deze set
        for index in [index1, index2, index3]:
            new_set.append(self.tafel[index])
            self.tafel[index]=False
        self.alle_sets.append(new_set)
        #ga van achter naar voren in de lijst om alle False te verwijderen, dus de kaarten die de set vormen verwijderen
        for i in range(len(self.tafel)-1,-1,-1):
            if type(self.tafel[i])!=Kaart:
                self.tafel.pop(i) 

    
    def voeg_kaarten_toe_op_tafel(self, huidige_tafel):
        print("de kaarten die nu zijn toegevoegd:")
        for _ in range(3):
            new_kaart_index=random.choice(range(0,len(self.stapel)))
            print(self.stapel[new_kaart_index])
            huidige_tafel.append(self.stapel[new_kaart_index])
            self.stapel.pop(new_kaart_index)
    
    def verwijder_willekeurige_set(self, huidige_tafel):
        random_set=random.choice(self.vind_sets(huidige_tafel))
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
            self.stapel.append(kaart)

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
            self.stapel.append(kaart)

def game():
    punten_speler=0
    punten_computer=0
    SET=Spel([1,2,3], ["rood", "groen", "paars"], ["leeg", "gestreept", "vol"], ["ovaal", "ruit", "golf"])
    start_tafel=SET.initieer_tafel()
    x=True
    while x:
        print("\n \n \n De kaarten op tafel zijn:")
        SET.print_kaarten(start_tafel)
        print(f"Er zijn nog {len(SET.alle_kaarten)} kaarten in de pot.")
        print("type hieronder 'geen set gevonden' als je geen set gevonden hebt. type anders 'kaartnummer1 kaartnummer2 kaartnummer3' ald je denkt dat deze kaartnummers een set vormen(bijvorbeeld '8 4 6' als kaarten 8, 4 en 6 een set vormen)")
        inputs=input()
        if inputs=="geen set gevonden":
            print("\n \n ")
            if len(SET.vind_sets(start_tafel))!=0:
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
                        if kaart1.controleer_set(kaart2, kaart3):
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
            if len(SET.vind_sets(SET.alle_kaarten+start_tafel))==0:
                print("er zijn dit spel geen sets meer mogelijk")
                x=False
        print("klik op enter om door te gaan")
        input()
    print(f"het spel is klaar, de uislag is: punten speler= {punten_speler} & punten computer= {punten_computer}")

def main():
    game()
if __name__=="__main__":
    main()
    

  