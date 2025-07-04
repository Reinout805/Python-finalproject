from SET import Spel, Kaart
def verwijder_kaarten_van_tafel():
    SET=Spel([1,2,3], ["rood", "groen", "paars"], ["leeg", "gestreept", "vol"], ["ovaal", "ruit", "golf"])
    start_tafel = [
        # set (verander de eerste kaart in paars zodat er geen set te vinden is)
        Kaart(2, 'groen', 'vol', 'ruit'),
        Kaart(2, 'rood', 'leeg', 'golf'),
        Kaart(2, 'paars', 'gestreept', 'ovaal'),
        # geen set
        Kaart(3, 'rood', 'gestreept', 'golf'),        
        Kaart(3, 'rood', 'leeg', 'golf'),        
        Kaart(1, 'paars', 'gestreept', 'ruit'),
        Kaart(2, 'groen', 'leeg', 'golf'),
        Kaart(2, 'paars', 'vol', 'ruit'),
        Kaart(3, 'groen', 'gestreept', 'ovaal'),
        Kaart(3, 'paars', 'leeg', 'golf'),
        Kaart(1, 'rood', 'vol', 'ruit'),        
        Kaart(3, 'paars', 'vol', 'golf'),
            ]
    print("vooraf tafel")
    SET.print_kaarten(start_tafel)
    print("vooraf gevonden sets")
    SET.print_gevonden_sets()
    SET.verwijder_set(12,2,3, start_tafel)
    print("na verwijderen tafel")
    SET.print_kaarten(start_tafel)
    print("na verwijderen gevonden sets")
    SET.print_gevonden_sets()
def main():
    verwijder_kaarten_van_tafel()
    

if __name__=="__main__":
    main()
