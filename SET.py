class kaart:
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
def main():
    pass
if __name__=="__main__":
    main()

    

    