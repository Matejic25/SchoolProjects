from functions import *


options = """
        OPTIONS
        
1   --- Add guest
2   --- Check room capacity
3   --- Check occupied dates
4   --- Refresh availability of the rooms
5   --- Occupy/Free the room
6   --- Add reservation
7   --- Remove reservation
8   --- View all reservations
9   --- Check-in
10  --- Checkout
0   --- Exit"""

while True:
    print(options)
    print("")
    chosen_option = input("Choose option: ")
    if chosen_option == '0':
        break
    elif chosen_option == '1':
        print("Add guest")
        broj_pasosa = int(input("Broj pasosa: "))
        ime = str(input("Ime: "))
        prezime = str(input("Prezime: "))
        add_guest(broj_pasosa, ime, prezime)
    elif chosen_option == '2':
        print("Check room capacity")
        id_sobe = int(input("ID sobe: "))
        osobe = int(input("Broj osoba: "))
        check_capacity(id_sobe, osobe)
    elif chosen_option == '3':
        print("Check occupied dates")
        id_sobe = input("ID sobe: ")
        datum_pocetka = input("Datum pocetka boravka: ")
        datum_zavrsetka = input("Datum kraja boravka: ")
        check_occupied_dates(id_sobe, datum_pocetka, datum_zavrsetka)
    elif chosen_option == '4':
        print("Refresh availability of the rooms")
        refresh_availability_of_rooms()
    elif chosen_option == '5':
        print("Occupy/Free the room")
        id_sobe = int(input("ID sobe: "))
        zahtev = input("Zauzmi/Oslobodi: ")
        occupy_free_the_room(id_sobe, zahtev)
    elif chosen_option == '6':
        print("Add reservation")
        id_sobe = int(input("ID sobe: "))
        broj_osoba = int(input("Broj osoba: "))
        datum_pocetka = input("Datum pocetka boravka: ")
        datum_zavrsetka = input("Datum kraja boravka: ")
        add_reservation(id_sobe, broj_osoba, datum_pocetka, datum_zavrsetka)
    elif chosen_option == '7':
        print("Remove reservation")
        id_rezervacije = int(input("ID rezervacije: "))
        remove_reservation(id_rezervacije)
    elif chosen_option == '8':
        print("View all reservations")
        print("[ID_Rez]  [Dat_Rez]   [Br_Osoba] [Zak_Dat_Poc]  [Zak_Dat_Zav]     [Rea_Dat_Poc]    [Rea_Dat_Zav] "
              "[ID_Sobe]")
        all_reservations()
    elif chosen_option == '9':
        print("Check-in")
        broj_pasosa = int(input("Broj pasosa: "))
        id_sobe = int(input("ID sobe: "))
        telefon = str(input("Telefon: "))
        print("[id_gosta][br_pasosa]      [Ime]           [Prezime]      [id_sobe]      [telefon]")
        check_in(broj_pasosa, id_sobe, telefon)
    elif chosen_option == '10':
        print("Checkout")
        id_rezervacije = int(input("ID rezervacije: "))
        checkout(id_rezervacije)
    else:
        print("Option does not exist!")
