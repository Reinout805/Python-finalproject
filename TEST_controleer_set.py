from SET import kaart
a = kaart(3, "rood", "leeg", "ruit")
b = kaart(3, "groen", "leeg", "ruit")
c = kaart(3, "blauw", "leeg", "ruit")

d = kaart(1, "rood", "vol", "ovaal")
e = kaart(2, "rood", "vol", "ovaal")
f = kaart(3, "rood", "vol", "ovaal")

g = kaart(1, "rood", "leeg", "golf")
h = kaart(1, "rood", "leeg", "ruit")
i = kaart(1, "rood", "leeg", "golf")
def main():
    print(a.check_3_cards_if_set(b,c)==True)
    print(d.check_3_cards_if_set(e,f)==True)
    print(g.check_3_cards_if_set(h,i)==False)
if __name__=="__main__":
    main()