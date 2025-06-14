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
            if self.één_eigenschap_voldoet(other_1, other_2, eigenschappen[1]):
                if self.één_eigenschap_voldoet(other_1, other_2, eigenschappen[2]):
                    if self.één_eigenschap_voldoet(other_1, other_2, eigenschappen[3]):
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
    
    #vind alle sets en geef deze terug in een lijst met tuples voor de sets 
    def vind_sets(self, kaarten):
        gevonden_sets=[]
        #maak alle combinaties van kaarten die op tafel liggen
        alle_combinaties=combinations(kaarten,3)
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

    #voeg 3 extra kaarten toe op tafel van de stapel
    def voeg_kaarten_toe_op_tafel(self):
        for _ in range(3):
            new_kaart_index=random.choice(range(0,len(self.stapel)))
            self.tafel.append(self.stapel[new_kaart_index])
            self.stapel.pop(new_kaart_index)
    
    #gegeven de lijst met gevonden sets op tafel, verwijder een willekeurige set
    def verwijder_willekeurige_set(self, gevonden_sets):
        random_set=random.choice(gevonden_sets)
        index1=self.tafel.index(random_set[0])
        index2=self.tafel.index(random_set[1])
        index3=self.tafel.index(random_set[2])
        self.verwijder_set(index1, index2, index3)

    #verwijder de eerste 3 kaarten op tafel
    def verwijder_eerste_3_kaarten_op_tafel(self):
        #we willen de kaarten die we verwijderen van de tafel opnieuw toevoegen 
        # aan de stapel, nadat we nieuwe kaarten hebben gepakt
        verwijderde_kaarten_lijst=[]
        #we willen de kaarten op indices 0,1,2 verwijderen
        for index in [2,1,0]:
            verwijderde_kaarten_lijst.append(self.tafel[index])
            self.tafel.pop(index) 
        #voeg nieuwe kaarten toe op tafel, aan het einde van de huidige tafel
        self.voeg_kaarten_toe_op_tafel()
        #voeg de verwijderde kaarten opnieuwe toe aan de stapel
        for kaart in verwijderde_kaarten_lijst:
            self.stapel.append(kaart)




def game():
    punten_speler=0
    punten_computer=0
    SET=Spel([1,2,3], ["rood", "groen", "paars"], ["leeg", "gestreept", "vol"], ["ovaal", "ruit", "golf"])
    SET.initieer_tafel()
    x=True
    while x:
        print("\n \n \n De kaarten op tafel zijn:")
        SET.print_kaarten(SET.tafel)
        print(f"Er zijn nog {len(SET.stapel)} kaarten in de pot.")
        print("type hieronder 'geen set gevonden' als je geen set gevonden hebt. type anders 'kaartnummer1 kaartnummer2 kaartnummer3' ald je denkt dat deze kaartnummers een set vormen(bijvorbeeld '8 4 6' als kaarten 8, 4 en 6 een set vormen)")
        inputs=input()
        if inputs=="geen set gevonden":
            print("\n \n ")
            gevonden_sets=SET.vind_sets(SET.tafel)
            if len(gevonden_sets)!=0:
                if len(SET.stapel)>0:
                    SET.verwijder_willekeurige_set(gevonden_sets)
                    SET.voeg_kaarten_toe_op_tafel()
                    punten_computer+=1
                    print("\n")
                    print(f"punten speler= {punten_speler} & punten computer= {punten_computer}")
                else:
                    SET.verwijder_willekeurige_set(gevonden_sets)
                    punten_computer+=1
                    print("\n")
                    print(f"punten speler= {punten_speler} & punten computer= {punten_computer}")
      

            else:
                print("ik heb geen set gevonden, ik verwijder 3 random kaarten op tafel")
                SET.verwijder_eerste_3_kaarten_op_tafel()
                print("\n")
                print(f"puntenspeler= {punten_speler} & punten computer= {punten_computer}")
        elif len(inputs.split(" "))==3:
            try:
                int(inputs.split(" ")[0]) and int(inputs.split(" ")[1]) and int(inputs.split(" ")[2])
                if (int(inputs.split(" ")[0]) in range(12)) and (int(inputs.split(" ")[1]) in range(12)) and (int(inputs.split(" ")[2]) in range(12)):
                    if int(inputs.split(" ")[0])!=int(inputs.split(" ")[1]) and int(inputs.split(" ")[2])!=int(inputs.split(" ")[1]) and int(inputs.split(" ")[0])!=int(inputs.split(" ")[2]):
                        inputslist=inputs.split(" ")
                        index1=int(inputslist[0])-1
                        index2=int(inputslist[1])-1
                        index3=int(inputslist[2])-1
                        kaart1=SET.tafel[index1]
                        kaart2=SET.tafel[index2]
                        kaart3=SET.tafel[index3]
                        if kaart1.controleer_set(kaart2, kaart3):
                            print("de set is goed")
                            SET.verwijder_set(index1, index2, index3)
                            if len(SET.stapel)>0:
                                SET.voeg_kaarten_toe_op_tafel()
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
        if len(SET.stapel+SET.tafel)<=20:
            if len(SET.vind_sets(SET.stapel+SET.tafel))==0:
                print("er zijn dit spel geen sets meer mogelijk")
                x=False
        print("klik op enter om door te gaan")
        input()
    print(f"het spel is klaar, de uislag is: punten speler= {punten_speler} & punten computer= {punten_computer}")

def main():
    game()
if __name__=="__main__":
    main()
    

  