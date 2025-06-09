from SET import Spel, Kaart
def verwijder_set():
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
    print("vooraf alle kaarten")
    SET.print_kaarten(SET.alle_kaarten)
    SET.verwijder_set(1,2,3, start_tafel)
    print("na verwijderen tafel")
    SET.print_kaarten(start_tafel)
    print("na verwijderen alle kaarten")
    SET.print_kaarten(SET.alle_kaarten)
def main():
    verwijder_set()
    

if __name__=="__main__":
    main()
