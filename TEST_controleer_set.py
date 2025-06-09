from SET import Kaart
a = Kaart(3, "rood", "leeg", "ruit")
b = Kaart(3, "groen", "leeg", "ruit")
c = Kaart(3, "blauw", "leeg", "ruit")

d = Kaart(1, "rood", "vol", "ovaal")
e = Kaart(2, "rood", "vol", "ovaal")
f = Kaart(3, "rood", "vol", "ovaal")

g = Kaart(1, "rood", "leeg", "golf")
h = Kaart(1, "rood", "leeg", "ruit")
i = Kaart(1, "rood", "leeg", "golf")
def main():
    print(a.check_3_cards_if_set(b,c)==True)
    print(d.check_3_cards_if_set(e,f)==True)
    print(g.check_3_cards_if_set(h,i)==False)
if __name__=="__main__":
    main()