from functions import *


opcije = """
        OPCIJE
        
1   --- Dodaj gosta
2   --- Provera kapaciteta sobe
3   --- Proveri termine za sobu
4   --- Osvezi raspolozivosti soba
5   --- Zauzmi/Oslobodi sobu
6   --- Dodaj rezervaciju
7   --- Obrisi rezervaciju
8   --- Uvid u rezervacije
9   --- Prijava rezervacije
10  --- Odjava rezervacije
0   --- Izlaz"""

while True:
    print(opcije)
    print("")
    izabrana_opcija = input("Izaberi opciju: ")
    if izabrana_opcija == '0':
        break
    elif izabrana_opcija == '1':
        print("Dodaj gosta")
        broj_pasosa = int(input("Broj pasosa: "))
        ime = str(input("Ime: "))
        prezime = str(input("Prezime: "))
        dodaj_gosta(broj_pasosa, ime, prezime)
    elif izabrana_opcija == '2':
        print("Provera kapaciteta sobe")
        id_sobe = int(input("ID sobe: "))
        osobe = int(input("Broj osoba: "))
        provera_kapaciteta(id_sobe, osobe)
    elif izabrana_opcija == '3':
        print("Proveri termine za sobu")
        id_sobe = input("ID sobe: ")
        datum_pocetka = input("Datum pocetka boravka: ")
        datum_zavrsetka = input("Datum kraja boravka: ")
        proveri_termine_sobe(id_sobe, datum_pocetka, datum_zavrsetka)
    elif izabrana_opcija == '4':
        print("Osvezi raspolozivosti soba")
        osvezi_raspolozivosti_soba()
    elif izabrana_opcija == '5':
        print("Zauzmi/Oslobodi sobu")
        id_sobe = int(input("ID sobe: "))
        zahtev = input("Zauzmi/Oslobodi: ")
        zauzmi_oslobodi_sobu(id_sobe, zahtev)
    elif izabrana_opcija == '6':
        print("Dodaj rezervaciju")
        id_sobe = int(input("ID sobe: "))
        broj_osoba = int(input("Broj osoba: "))
        datum_pocetka = input("Datum pocetka boravka: ")
        datum_zavrsetka = input("Datum kraja boravka: ")
        dodaj_rezervaciju(id_sobe, broj_osoba, datum_pocetka, datum_zavrsetka)
    elif izabrana_opcija == '7':
        print("Obrisi rezervaciju")
        id_rezervacije = int(input("ID rezervacije: "))
        obrisi_rezervaciju(id_rezervacije)
    elif izabrana_opcija == '8':
        print("Uvid u rezervacije")
        print("[ID_Rez]  [Dat_Rez]   [Br_Osoba] [Zak_Dat_Poc]  [Zak_Dat_Zav]     [Rea_Dat_Poc]    [Rea_Dat_Zav] "
              "[ID_Sobe]")
        sve_rezervacije()
    elif izabrana_opcija == '9':
        print("Prijava rezervacije")
        broj_pasosa = int(input("Broj pasosa: "))
        id_sobe = int(input("ID sobe: "))
        telefon = str(input("Telefon: "))
        print("[id_gosta][br_pasosa]      [Ime]           [Prezime]      [id_sobe]      [telefon]")
        prijava_rezervacije(broj_pasosa, id_sobe, telefon)
    elif izabrana_opcija == '10':
        print("Odjava rezervacije")
        id_rezervacije = int(input("ID rezervacije: "))
        odjava_rezervacije(id_rezervacije)
    else:
        print("Opcija ne postoji!")
