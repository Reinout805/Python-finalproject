from SET import Spel, Kaart
def willekeurige_set_verwijderen():
    SET=Spel([1,2,3], ["rood", "groen", "paars"], ["leeg", "gestreept", "vol"], ["ovaal", "ruit", "golf"])
    huidige_tafel=SET.maak_start_tafel()
    print("vooraf tafel")
    SET.print_kaarten(huidige_tafel)
    print("\n alle kaarten:")
    SET.print_kaarten(SET.alle_kaarten)
    SET.verwijder_random_kaarten_op_tafel(huidige_tafel)
    print("\n tafel na verwijderen")
    SET.print_kaarten(huidige_tafel)
    print("\n alle kaarten (na verwijderen):")
    SET.print_kaarten(SET.alle_kaarten)
def main():
    willekeurige_set_verwijderen()
    

if __name__=="__main__":
    main()

