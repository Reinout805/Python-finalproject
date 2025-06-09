from SET import Spel
def main():
    SET=Spel([1,2,3], ["rood", "groen", "blauw"], ["leeg", "gestreept", "gevuld"], ["ovaal", "diamand", "kronkel"])
    x=0
    for kaart in SET.alle_kaarten:
        print(kaart)
        x+=1
    print(f"aantal kaarten in totaal is {x}")
if __name__=="__main__":
    main()