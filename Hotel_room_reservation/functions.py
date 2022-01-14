from pymysql import *

connection = connect(host='localhost',
                     user='root',
                     password='1234321',
                     database='hotel')

mycursor = connection.cursor()


# PROMENA BROJA RASPOLOZIVIH SOBA U KATEGORIJI (MENJA VREDNOST raspolozivo U TABELI kategorija_sobe)
def osvezi_raspolozive_u_kat():
    lista3 = []
    lista2 = []
    lista1 = []
    mycursor.execute("SELECT id_sobe FROM sobe WHERE raspoloziva = 1 AND id_kategorije = 3")
    for i in mycursor:
        lista3.append(i)
    slobodne3 = len(lista3)
    mycursor.execute("SELECT id_sobe FROM sobe WHERE raspoloziva = 1 AND id_kategorije = 2")
    for i in mycursor:
        lista2.append(i)
    slobodne2 = len(lista2)
    mycursor.execute("SELECT id_sobe FROM sobe WHERE raspoloziva = 1 AND id_kategorije = 1")
    for i in mycursor:
        lista1.append(i)
    slobodne1 = len(lista1)
    mycursor.execute("UPDATE kategorija_sobe SET raspolozivo = %s WHERE id_kategorije = 3", slobodne3)
    mycursor.execute("UPDATE kategorija_sobe SET raspolozivo = %s WHERE id_kategorije = 2", slobodne2)
    mycursor.execute("UPDATE kategorija_sobe SET raspolozivo = %s WHERE id_kategorije = 1", slobodne1)
    connection.commit()


# ZAUZMI/OSLOBODI SOBU (MENJA VREDNOST raspoloziva U TABELI sobe), PROVERA RASPOLOZIVOSTI SOBE
# POZIVA I FUNKCIJU osvezi_raspolozive_u_kat KOJA OSVEZI/PROMENI VREDNOST raspolozivo U kategorija_sobe
def zauzmi_oslobodi_sobu(id_sobe, zahtev):
    mycursor.execute("SELECT id_sobe FROM sobe")
    for i in mycursor:
        if i[0] != id_sobe:
            pass
        elif i[0] == id_sobe and zahtev.lower() == "zauzmi":
            mycursor.execute("SELECT raspoloziva FROM sobe WHERE id_sobe = %s", id_sobe)
            for j in mycursor:
                if j[0] == 0:
                    print("Soba je vec zauzeta!")
                    return "vec_zauzeta"
                else:
                    mycursor.execute("UPDATE sobe SET raspoloziva = 0 WHERE id_sobe = %s", id_sobe)
                    connection.commit()
                    osvezi_raspolozive_u_kat()
                    return "Zauzeo"
        elif i[0] == id_sobe and zahtev.lower() == "oslobodi":
            mycursor.execute("SELECT raspoloziva FROM sobe WHERE id_sobe = %s", id_sobe)
            for j in mycursor:
                if j[0] == 1:
                    print("Soba je vec slobodna!")
                    return "vec_slobodna"
                else:
                    mycursor.execute("UPDATE sobe SET raspoloziva = 1 WHERE id_sobe = %s", id_sobe)
                    connection.commit()
                    osvezi_raspolozive_u_kat()
                    return "Oslobodio"
        else:
            return -1


# PROVERA KAPACITETA SOBE I BROJ ZAHTEVANIH OSOBA U SOBI
def provera_kapaciteta(id_sobe, osobe):
    mycursor.execute(f"SELECT broj_kreveta "
                     "FROM sobe AS s LEFT JOIN kategorija_sobe AS k "
                     "ON s.id_kategorije = k.id_kategorije WHERE s.id_sobe = %s", id_sobe)
    kapacitet = mycursor.fetchone()[0]
    print(f"Ova soba poseduje {kapacitet} kreveta")
    return osobe <= kapacitet


# PROVERA DA LI SE ZELJENI DATUM ZA REZERVACIJU SOBE NALAZI U OPSEGU VEC REZERVISANIH SOBA
# ako je soba zauzeta tokom zeljenog termina vraca False
# ako je soba slobodna tokom zeljenog termina vraca True
def proveri_termine_sobe(id_sobe, datum_pocetka, datum_zavrsetka):
    mycursor.execute("SELECT id_rezervacije, zakazani_datum_pocetka, zakazani_datum_zavrsetka FROM rezervacija "
                     "WHERE zakazani_datum_pocetka BETWEEN %s AND %s AND id_sobe = %s "
                     "OR zakazani_datum_zavrsetka BETWEEN %s AND %s AND id_sobe = %s "
                     "OR %s BETWEEN zakazani_datum_pocetka AND zakazani_datum_zavrsetka AND id_sobe = %s "
                     "OR %s BETWEEN zakazani_datum_pocetka AND zakazani_datum_zavrsetka AND id_sobe = %s"
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
def osvezi_raspolozivosti_soba():
    sobe = []
    rezervisane = []
    nerezervisane = []
    mycursor.execute("SELECT id_sobe FROM sobe ORDER BY id_sobe DESC")
    for i in mycursor:
        sobe.append(i[0])
    mycursor.execute("SELECT id_sobe FROM rezervacija ORDER BY id_sobe DESC")
    for i in mycursor:
        rezervisane.append(i[0])
    for soba in sobe:
        if soba in sobe and soba not in rezervisane:
            nerezervisane.append(soba)
        else:
            for rezervisana in rezervisane:
                mycursor.execute("UPDATE sobe SET raspoloziva = 0 WHERE id_sobe = %s", rezervisana)
    for soba in nerezervisane:
        mycursor.execute("UPDATE sobe SET raspoloziva = 1 WHERE id_sobe = %s", soba)
    osvezi_raspolozive_u_kat()
    connection.commit()
    print("Raspolozivosti osvezene.")


# DODAVANJE REZERVACIJE NAKON ISPUNJENIH USLOVA
def dodaj_rezervaciju(id_sobe, broj_osoba, datum_pocetka, datum_zavrsetka):
    if provera_kapaciteta(id_sobe, broj_osoba) is True:
        if zauzmi_oslobodi_sobu(id_sobe, "zauzmi") != "vec_zauzeta" or \
                zauzmi_oslobodi_sobu(id_sobe, "zauzmi") == "vec_zauzeta" and \
                proveri_termine_sobe(id_sobe, datum_pocetka, datum_zavrsetka) is True:
            mycursor.execute("INSERT INTO rezervacija(id_sobe, datum_rezervacije, broj_osoba,"
                             " zakazani_datum_pocetka, zakazani_datum_zavrsetka,"
                             " realni_datum_pocetka, realni_datum_zavrsetka)"
                             "VALUES (%s,'2020-5-15',%s,%s,%s,'2020-5-15','2020-5-25')",
                             (id_sobe, broj_osoba, datum_pocetka, datum_zavrsetka))
            print("Rezervacija dodata.")
            osvezi_raspolozive_u_kat()
            osvezi_raspolozivosti_soba()
            connection.commit()
        else:
            print("Rezervacije odbijena.")
    else:
        print("nema mesta u sobi.")


def obrisi_rezervaciju(id_rezervacije):
    mycursor.execute("SELECT id_sobe FROM rezervacija WHERE id_rezervacije=%s", id_rezervacije)
    mycursor.execute("DELETE FROM rezervacija WHERE id_rezervacije=%s", id_rezervacije)
    osvezi_raspolozivosti_soba()
    osvezi_raspolozive_u_kat()
    connection.commit()
    print("Rezervacija obrisana.")


def sve_rezervacije():
    mycursor.execute("SELECT * FROM rezervacija")
    for rezervacija in mycursor:
        for data in range(8):
            print(rezervacija[data], end="       ")
        print("\n")
