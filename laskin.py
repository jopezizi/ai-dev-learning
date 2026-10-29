alv = 0.255

def lisaa_alv(netto, kanta=alv):
    return round(netto + netto*alv,3)

def veroton(brutto, kanta=alv):
    return round(brutto / (1 + kanta), 2)

print(lisaa_alv(100))