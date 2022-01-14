from pymysql import *

connection = connect(host='localhost',
                     user='root',
                     password='1234321',
                     database='hotel')

mycursor = connection.cursor()


# TREBA
# PROMENA BROJA RASPOLOZIVIH SOBA U KATEGORIJI (MENJA VREDNOST raspolozivo U TABELI kategorija_sobe)
def br_rasp_u_kategoriji():
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
#     return "Osvezen broj raspolozivih soba po kategorijama"


# TREBA
# ZAUZMI/OSLOBODI SOBU (MENJA VREDNOST raspoloziva U TABELI sobe), PROVERA RASPOLOZIVOSTI SOBE
# POZIVA I FUNKCIJU br_rasp_u_kategoriji KOJA OSVEZI/PROMENI VREDNOST raspolozivo U kategorija_sobe
def promeni_rasp_sobe(id_sobe, zahtev):
    mycursor.execute("SELECT id_sobe FROM sobe")
    for i in mycursor:
        if i[0] != id_sobe:
            pass
        elif i[0] == id_sobe and zahtev.lower() == "zauzmi":
            mycursor.execute("SELECT raspoloziva FROM sobe WHERE id_sobe = %s", id_sobe)
            for j in mycursor:
                if j[0] == 0:
                    return "vec_zauzeta"
                else:
                    mycursor.execute("UPDATE sobe SET raspoloziva = 0 WHERE id_sobe = %s", id_sobe)
                    connection.commit()
                    br_rasp_u_kategoriji()
                    return "Zauzeo"
        elif i[0] == id_sobe and zahtev.lower() == "oslobodi":
            mycursor.execute("SELECT raspoloziva FROM sobe WHERE id_sobe = %s", id_sobe)
            for j in mycursor:
                if j[0] == 1:
                    return "vec_slobodna"
                else:
                    mycursor.execute("UPDATE sobe SET raspoloziva = 1 WHERE id_sobe = %s", id_sobe)
                    connection.commit()
                    br_rasp_u_kategoriji()
                    return "Oslobodio"
        else:
            return -1
#
#
# print(promeni_rasp_sobe(3, 'zauzmi'))


# TREBA
# PROVERA KAPACITETA SOBE I BROJ ZAHTEVANIH OSOBA U SOBI


def provera_kapaciteta(id_sobe,osobe):
    mycursor.execute(f"SELECT broj_kreveta "
                     "FROM sobe AS s LEFT JOIN kategorija_sobe AS k "
                     "ON s.id_kategorije = k.id_kategorije WHERE s.id_sobe = %s", id_sobe)
    kapacitet = mycursor.fetchone()[0]
    return osobe <= kapacitet


# PROVERA DA LI SE ZELJENI DATUM ZA REZERVACIJU SOBE NALAZI U OPSEGU VEC REZERVISANIH SOBA
# ako je soba zauzeta tokom zeljenog termina vraca False
# ako je soba slobodna tokom zeljenog termina vraca True


def proveri_termine_sobe(id_sobe, datum_pocetka, datum_zavrsetka):
    mycursor.execute("SELECT id_rezervacije, zakazani_datum_pocetka, zakazani_datum_zavrsetka FROM rezervacija"
                     " WHERE zakazani_datum_pocetka BETWEEN %s"
                     " AND %s AND id_sobe = %s OR zakazani_datum_zavrsetka BETWEEN"
                     " %s AND %s AND id_sobe = %s"
                     , (datum_pocetka, datum_zavrsetka, id_sobe, datum_pocetka, datum_zavrsetka, id_sobe))
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


# proveri_termine_sobe(3, '2020-5-13', '2020-5-26')


# ZAVISNOST RASPOLOZIVOSTI SOBE U ODNOSU NA TO DA LI JE id_sobe U rezervacija
def raspolozivost_po_rezervacijama():
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
    br_rasp_u_kategoriji()
    connection.commit()
    # print(nerezervisane)
    print("Nerezervisane oslobodjene.")
    print("Rezervisane zauzete.")


# raspolozivost_po_rezervacijama()

# DODAVANJE REZERVACIJE NAKON ISPUNJENIH USLOVA
def dodaj_rezervaciju(id_sobe, broj_osoba, datum_pocetka, datum_zavrsetka):
    if provera_kapaciteta(id_sobe, broj_osoba) is True:
        if promeni_rasp_sobe(id_sobe, "zauzmi") != "vec_zauzeta" or\
                promeni_rasp_sobe(id_sobe, "zauzmi") == "vec_zauzeta" and\
                proveri_termine_sobe(id_sobe, datum_pocetka, datum_zavrsetka) is True:
            mycursor.execute("INSERT INTO rezervacija(id_sobe, datum_rezervacije, broj_osoba,"
                             " zakazani_datum_pocetka, zakazani_datum_zavrsetka,"
                             " realni_datum_pocetka, realni_datum_zavrsetka)"
                             "VALUES (%s,'2020-5-15',%s,'2020-5-15','2020-5-25','2020-5-15','2020-5-25')",
                             (id_sobe, broj_osoba))
            print("Rezervacija dodata.")
            br_rasp_u_kategoriji()
            raspolozivost_po_rezervacijama()
            connection.commit()
        else:
            print("Rezervacije odbijena.")
    else:
        print("nema mesta u sobi.")


# dodaj_rezervaciju(10, 2, '2020-5-13', '2020-5-26')


def obrisi_rezervaciju(id_rezervacije):
    id_sobe = None
    mycursor.execute("SELECT id_sobe FROM rezervacija WHERE id_rezervacije=%s", id_rezervacije)
    for i in mycursor:
        id_sobe = i[0]
    promeni_rasp_sobe(id_sobe, "oslobodi")
    mycursor.execute("DELETE FROM rezervacija WHERE id_rezervacije=%s", id_rezervacije)
    br_rasp_u_kategoriji()
    connection.commit()
    print("Rezervacija obrisana.")

# obrisi_rezervaciju(9)
