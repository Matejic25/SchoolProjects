from pymysql import *

connection = connect(host='localhost',
                     user='root',
                     password='1234321',
                     database='hotel')

mycursor = connection.cursor()


def add_guest(broj_pasosa, ime, prezime):
    mycursor.execute("INSERT INTO guests(passport_serial_number, name, surname)"
                     "VALUES (%s, %s, %s)", (broj_pasosa, ime, prezime))
    connection.commit()
    print(f"Gost {ime} {prezime} uspesno dodat.")


# PROMENA BROJA RASPOLOZIVIH SOBA U KATEGORIJI (MENJA VREDNOST raspolozivo U TABELI room_categories)
def refresh_available_in_category():
    lista3 = []
    lista2 = []
    lista1 = []
    mycursor.execute("SELECT room_id FROM rooms WHERE available = 1 AND category_id = 3")
    for i in mycursor:
        lista3.append(i)
    slobodne3 = len(lista3)
    mycursor.execute("SELECT room_id FROM rooms WHERE available = 1 AND category_id = 2")
    for i in mycursor:
        lista2.append(i)
    slobodne2 = len(lista2)
    mycursor.execute("SELECT room_id FROM rooms WHERE available = 1 AND category_id = 1")
    for i in mycursor:
        lista1.append(i)
    slobodne1 = len(lista1)
    mycursor.execute("UPDATE room_categories SET available = %s WHERE category_id = 3", slobodne3)
    mycursor.execute("UPDATE room_categories SET available = %s WHERE category_id = 2", slobodne2)
    mycursor.execute("UPDATE room_categories SET available = %s WHERE category_id = 1", slobodne1)
    connection.commit()


# ZAUZMI/OSLOBODI SOBU (MENJA VREDNOST raspoloziva U TABELI sobe), PROVERA RASPOLOZIVOSTI SOBE
# POZIVA I FUNKCIJU refresh_available_in_category KOJA OSVEZI/PROMENI VREDNOST raspolozivo U room_categories
def occupy_free_the_room(id_sobe, zahtev):
    mycursor.execute("SELECT room_id FROM rooms")
    for i in mycursor:
        if i[0] != id_sobe:
            pass
        elif i[0] == id_sobe and zahtev.lower() == "zauzmi":
            mycursor.execute("SELECT available FROM rooms WHERE room_id = %s", id_sobe)
            for j in mycursor:
                if j[0] == 0:
                    print("Soba je vec zauzeta!")
                    return "vec_zauzeta"
                else:
                    mycursor.execute("UPDATE rooms SET available = 0 WHERE room_id = %s", id_sobe)
                    connection.commit()
                    refresh_available_in_category()
                    return "Zauzeo"
        elif i[0] == id_sobe and zahtev.lower() == "oslobodi":
            mycursor.execute("SELECT available FROM rooms WHERE room_id = %s", id_sobe)
            for j in mycursor:
                if j[0] == 1:
                    print("Soba je vec slobodna!")
                    return "vec_slobodna"
                else:
                    mycursor.execute("UPDATE rooms SET available = 1 WHERE room_id = %s", id_sobe)
                    connection.commit()
                    refresh_available_in_category()
                    return "Oslobodio"
        else:
            return -1


# PROVERA KAPACITETA SOBE I BROJ ZAHTEVANIH OSOBA U SOBI
def check_capacity(id_sobe, osobe):
    mycursor.execute(f"SELECT num_of_beds "
                     "FROM rooms AS r LEFT JOIN room_categories AS rc "
                     "ON r.category_id = rc.category_id WHERE r.room_id = %s", id_sobe)
    kapacitet = mycursor.fetchone()[0]
    print(f"Ova soba poseduje {kapacitet} kreveta")
    return osobe <= kapacitet


# PROVERA DA LI SE ZELJENI DATUM ZA REZERVACIJU SOBE NALAZI U OPSEGU VEC REZERVISANIH SOBA
# ako je soba zauzeta tokom zeljenog termina vraca False
# ako je soba slobodna tokom zeljenog termina vraca True
def check_occupied_dates(id_sobe, datum_pocetka, datum_zavrsetka):
    mycursor.execute("SELECT reservation_id, reservation_beginning_date, reservation_ending_date FROM reservations "
                     "WHERE reservation_beginning_date BETWEEN %s AND %s AND room_id = %s "
                     "OR reservation_ending_date BETWEEN %s AND %s AND room_id = %s "
                     "OR %s BETWEEN reservation_beginning_date AND reservation_ending_date AND room_id = %s "
                     "OR %s BETWEEN reservation_beginning_date AND reservation_ending_date AND room_id = %s"
                     , (datum_pocetka, datum_zavrsetka, id_sobe, datum_pocetka, datum_zavrsetka, id_sobe, datum_pocetka,
                        id_sobe, datum_zavrsetka, id_sobe))
    rezultati = 0
    for i in mycursor:
        rezultati += 1
        if rezultati > 0:
            print(f"Soba: {id_sobe} je zauzeta | OD: {i[1]} | DO: {i[2]} ---- ID_Rezervacije: {i[0]}")
        else:
            print(f"Soba: {id_sobe} je slobodna za rezervaciju u terminu | OD: {datum_pocetka} | DO: {datum_zavrsetka}")
    if rezultati > 0:
        return False
    else:
        return True


# ZAVISNOST RASPOLOZIVOSTI SOBE U ODNOSU NA TO DA LI JE id_sobe U rezervacija
def refresh_availability_of_rooms():
    sobe = []
    rezervisane = []
    nerezervisane = []
    mycursor.execute("SELECT room_id FROM rooms ORDER BY room_id DESC")
    for i in mycursor:
        sobe.append(i[0])
    mycursor.execute("SELECT room_id FROM reservations ORDER BY room_id DESC")
    for i in mycursor:
        rezervisane.append(i[0])
    for soba in sobe:
        if soba in sobe and soba not in rezervisane:
            nerezervisane.append(soba)
        else:
            for rezervisana in rezervisane:
                mycursor.execute("UPDATE rooms SET available = 0 WHERE room_id = %s", rezervisana)
    for soba in nerezervisane:
        mycursor.execute("UPDATE rooms SET available = 1 WHERE room_id = %s", soba)
    refresh_available_in_category()
    connection.commit()
    print("Raspolozivosti osvezene.")


# DODAVANJE REZERVACIJE NAKON ISPUNJENIH USLOVA
def add_reservation(id_sobe, broj_osoba, datum_pocetka, datum_zavrsetka):
    if check_capacity(id_sobe, broj_osoba) is True:
        if occupy_free_the_room(id_sobe, "zauzmi") != "vec_zauzeta" or \
                occupy_free_the_room(id_sobe, "zauzmi") == "vec_zauzeta" and \
                check_occupied_dates(id_sobe, datum_pocetka, datum_zavrsetka) is True:
            mycursor.execute("INSERT INTO reservations(room_id, reservation_date, num_of_guests,"
                             " reservation_beginning_date, reservation_ending_date)"
                             "VALUES (%s,CURRENT_DATE(),%s,%s,%s)",
                             (id_sobe, broj_osoba, datum_pocetka, datum_zavrsetka))
            print("Rezervacija dodata.")
            refresh_available_in_category()
            refresh_availability_of_rooms()
            connection.commit()
        else:
            print("Rezervacije odbijena.")
    else:
        print("nema mesta u sobi.")


def remove_reservation(id_rezervacije):
    mycursor.execute("SELECT room_id FROM reservations WHERE reservation_id=%s", id_rezervacije)
    mycursor.execute("DELETE FROM reservations WHERE reservation_id=%s", id_rezervacije)
    refresh_availability_of_rooms()
    refresh_available_in_category()
    connection.commit()
    print("Rezervacija obrisana.")


def all_reservations():
    mycursor.execute("SELECT * FROM reservations")
    for rezervacija in mycursor:
        for data in range(8):
            print(rezervacija[data], end="       ")
        print("\n")


def check_in(broj_pasosa, id_sobe, telefon):
    mycursor.execute("SELECT * FROM guests WHERE passport_serial_number = %s", broj_pasosa)
    id_gosta = None
    id_rezervacije = None
    ime = ""
    prezime = ""
    for i in mycursor:
        id_gosta = i[0]
        ime = i[2]
        prezime = i[3]
        for j in i:
            print(j, end="           ")
    mycursor.execute("SELECT reservation_id FROM reservations WHERE room_id = %s", id_sobe)
    for i in mycursor:
        print(i[0], "       ", telefon)
        id_rezervacije = i[0]
    if id_gosta is not None and id_rezervacije is not None:
        mycursor.execute("INSERT INTO checked_in_reservations(guest_id, contact_person, reservation_id, phone_number)"
                         " VALUES(%s, %s, %s, %s)", (id_gosta, broj_pasosa, id_rezervacije, telefon))
        mycursor.execute("UPDATE reservations SET check_in_date = CURRENT_DATE()"
                         "WHERE reservation_id=%s", id_rezervacije)
        connection.commit()
        print(f"Rezervacija gosta {ime} {prezime} je uspesno prijavljena.")
    else:
        print("Nepravilno uneti podaci gosta")


def checkout(id_rezervacije):
    mycursor.execute("SELECT reservation_id FROM checked_in_reservations")
    for i in mycursor:
        if i[0] == id_rezervacije:
            mycursor.execute("DELETE FROM checked_in_reservations WHERE reservation_id = %s", id_rezervacije)
            mycursor.execute("UPDATE reservations SET checkout_date = CURRENT_DATE()"
                             "WHERE reservation_id=%s", id_rezervacije)
            connection.commit()
        else:
            print("ID rezervacije nije pronadjen.")
    print("Rezervacija uspesno odjavljena")
