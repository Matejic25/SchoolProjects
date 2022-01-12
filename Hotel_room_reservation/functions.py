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
# print(promeni_rasp_sobe(7, 'oslobodi'))



# TREBA
# PROVERA KAPACITETA SOBE I BROJ ZAHTEVANIH OSOBA U SOBI


def provera_kapaciteta(id_sobe,osobe):
    mycursor.execute(f"SELECT broj_kreveta "
                     "FROM sobe AS s LEFT JOIN kategorija_sobe AS k "
                     "ON s.id_kategorije = k.id_kategorije WHERE s.id_sobe = %s", id_sobe)
    kapacitet = mycursor.fetchone()[0]
    return osobe <= kapacitet


# Problem sa argumentima, ostalo radi
# DODAVANJE REZERVACIJE NAKON ISPUNJENIH USLOVA


def dodaj_rezervaciju(id_sobe, broj_osoba):
    if provera_kapaciteta(id_sobe, broj_osoba) is True:
        if promeni_rasp_sobe(id_sobe, "zauzmi") != "vec_zauzeta":
            mycursor.execute("INSERT INTO rezervacija(id_sobe, datum_rezervacije, broj_osoba, zakazani_datum_pocetka, zakazani_datum_zavrsetka, realni_datum_pocetka, realni_datum_zavrsetka)"
                             "VALUES (%s,'2020-5-15',%s,'2020-5-15','2020-5-25','2020-5-15','2020-5-25')", (id_sobe, broj_osoba))
            print("Rezervacija dodata!")
            br_rasp_u_kategoriji()
            connection.commit()
        else:
            print("soba vec zauzeta!")
    else:
        print("nema mesta u sobi!")



# dodaj_rezervaciju(7, 2)


# DODAVANJE U TABELU OSOBE_U_REZERVACIJI I ISPIS REDOVA
# mycursor.execute("INSERT INTO osobe_u_rezervaciji(kontakt_osoba, telefon) VALUES "
#                  "(123456789,'063/555-333'),"
#                  "(123456789,'063/555-333')")
# connection.commit()
# mycursor.execute("SELECT * FROM osobe_u_rezervaciji")
# for i in mycursor:
#     print(i)


# DODAVANJE U TABELU GOSTI I ISPIS REDOVA
# mycursor.execute("INSERT INTO gosti(broj_pasosa, ime, prezime) VALUES "
#                  "(123456789,'Nikola','Matejic'),"
#                  "(9876543,'Nemanja','Nemanjic'),"
#                  "(25252525,'Marko','Markovic'),"
#                  "(19191919,'Petar','Petrovic')")
# connection.commit()
# mycursor.execute('SELECT * FROM gosti')
# for i in mycursor:
#     print(i)


# DODAVANJE U TABELU SOBE I ISPIS REDOVA
# for i in range(5):
#     mycursor.execute('INSERT INTO sobe(sprat, id_kategorije, raspoloziva) VALUES (3, 1, 1)')
#     connection.commit()
# mycursor.execute('SELECT * FROM sobe')
# for i in mycursor:
#     print(i)


# DODAVANJE U TABELU KATEGORIJA_SOBA I ISPIS REDOVA
# mycursor.execute("INSERT INTO kategorija_sobe(broj_kreveta, apartman, pogled, cena, ukupan_broj_soba, raspolozivo) "
#                  "VALUES (4,TRUE,'more',100,5,5)")
# connection.commit()
#
# mycursor.execute('SELECT * FROM kategorija_sobe')
# for i in mycursor:
#     print(i)
