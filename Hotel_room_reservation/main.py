from functions import *


opcije = """
        OPCIJE
1   --- Provera kapaciteta sobe
2   --- Proveri termine za sobu
3   --- Osvezi raspolozivosti soba
4   --- Zauzmi/Oslobodi sobu
5   --- Dodaj rezervaciju
6   --- Obrisi rezervaciju
7   --- Uvid u rezervacije
0   --- Izlaz"""

while True:
    print(opcije)
    print("")
    izabrana_opcija = input("Izaberi opciju: ")
    if izabrana_opcija == '0':
        break
    elif izabrana_opcija == '1':
        print("Provera kapaciteta sobe")
        id_sobe = int(input("ID sobe: "))
        osobe = int(input("Broj osoba: "))
        provera_kapaciteta(id_sobe, osobe)
    elif izabrana_opcija == '2':
        print("Proveri termine za sobu")
        id_sobe = input("ID sobe: ")
        datum_pocetka = input("Datum pocetka boravka: ")
        datum_zavrsetka = input("Datum kraja boravka: ")
        proveri_termine_sobe(id_sobe, datum_pocetka, datum_zavrsetka)
    elif izabrana_opcija == '3':
        print("Osvezi raspolozivosti soba")
        osvezi_raspolozivosti_soba()
    elif izabrana_opcija == '4':
        print("Zauzmi/Oslobodi sobu")
        id_sobe = int(input("ID sobe: "))
        zahtev = input("Zauzmi/Oslobodi: ")
        zauzmi_oslobodi_sobu(id_sobe, zahtev)
    elif izabrana_opcija == '5':
        print("Dodaj rezervaciju")
        id_sobe = int(input("ID sobe: "))
        broj_osoba = int(input("Broj osoba: "))
        datum_pocetka = input("Datum pocetka boravka: ")
        datum_zavrsetka = input("Datum kraja boravka: ")
        dodaj_rezervaciju(id_sobe, broj_osoba, datum_pocetka, datum_zavrsetka)
    elif izabrana_opcija == '6':
        print("Obrisi rezervaciju")
        id_rezervacije = int(input("ID rezervacije: "))
        obrisi_rezervaciju(id_rezervacije)
    elif izabrana_opcija == '7':
        print("Uvid u rezervacije")
        print("[ID_Rez]  [Dat_Rez]   [Br_Osoba] [Zak_Dat_Poc]  [Zak_Dat_Zav]     [Rea_Dat_Poc]    [Rea_Dat_Zav] "
              "[ID_Sobe]")
        sve_rezervacije()
    else:
        print("Opcija ne postoji!")
