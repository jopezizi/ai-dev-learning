alv = 0.255

def lisaa_alv(netto, kanta=alv):
    return round(netto + netto*alv,3)

print(lisaa_alv(100))