CREATE DATABASE hotel;
USE hotel;

CREATE TABLE rezervacija(
	id_rezervacije INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_sobe INT NOT NULL,
    datum_rezervacije DATE NOT NULL,
    broj_osoba INT NOT NULL,
    zakazani_datum_pocetka DATE NOT NULL,
    zakazani_datum_zavrsetka DATE NOT NULL,
    realni_datum_pocetka DATE,
    realni_datum_zavrsetka DATE,
    FOREIGN KEY (id_sobe) REFERENCES sobe(id_sobe)
);

SELECT id_kategorije FROM sobe WHERE id_sobe = 2;
SELECT broj_kreveta FROM kategorija_sobe WHERE id_kategorije = 3;
SELECT * FROM rezervacija;

SELECT broj_kreveta
FROM sobe AS s
LEFT JOIN kategorija_sobe AS k
ON s.id_kategorije = k.id_kategorije
WHERE s.id_sobe = 2;

CREATE TABLE sobe(
	id_sobe INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    sprat INT NOT NULL,
    id_kategorije INT NOT NULL,
    raspoloziva BOOL NOT NULL,
    FOREIGN KEY (id_kategorije) REFERENCES kategorija_sobe(id_kategorije)
);

CREATE TABLE kategorija_sobe(
	id_kategorije INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    broj_kreveta INT NOT NULL,
    apartman BOOL NOT NULL,
    pogled ENUM('more','parking','park','tereni'),
    cena FLOAT NOT NULL,
    ukupan_broj_soba INT NOT NULL,
    raspolozivo INT
);

CREATE TABLE gosti(
	id_gosta INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    broj_pasosa INT NOT NULL UNIQUE,
    ime VARCHAR(50) NOT NULL,
    prezime VARCHAR(50) NOT NULL
);

CREATE TABLE osobe_u_rezervaciji(
	kontakt_osoba INT NOT NULL,
    telefon VARCHAR(20) NOT NULL,
    FOREIGN KEY (kontakt_osoba) REFERENCES gosti(broj_pasosa)
);


ALTER TABLE sobe DROP foreign key id_kategorije;
ALTER TABLE rezervacija ADD FOREIGN KEY (id_sobe) REFERENCES sobe(id_sobe);
ALTER TABLE rezervacija ADD id_sobe INT NOT NULL;
DROP TABLE sobe;
SELECT * FROM sobe;
SELECT * FROM kategorija_sobe;
SELECT * FROM gosti;
SELECT * FROM rezervacija;
DELETE FROM rezervacija WHERE id_sobe = 0;
SELECT id_kategorije FROM sobe;
SELECT id_sobe FROM sobe;
SELECT * FROM rezervacija;
ALTER TABLE rezervacija DROP COLUMN id_sobe;
SELECT sobe.id_sobe,sobe.id_kategorije
FROM sobe
WHERE sobe.id_kategorije = 3;

SELECT sobe.id_sobe
FROM sobe
WHERE sobe.id_kategorije = 3;

ALTER TABLE sobe ADD COLUMN raspoloziva BOOL NOT NULL;

DELETE FROM rezervacija WHERE id_sobe = 7;

SELECT sobe.id_sobe
FROM sobe
WHERE sobe.raspoloziva = 0;

SELECT id_sobe FROM rezervacija;

SELECT id_kategorije FROM sobe WHERE id_sobe = 5;
INSERT INTO sobe(sprat,id_kategorije,raspoloziva) VALUES(1,2,1);

UPDATE hotel.kategorija_sobe
 SET broj_kreveta = 4
    ,apartman =  1
    ,pogled = "more"
    ,cena = 100
    ,ukupan_broj_soba = 5
    ,raspolozivo = 5
 WHERE id_kategorije = 1;

 UPDATE hotel.kategorija_sobe
 SET broj_kreveta = 3
    ,apartman =  0
    ,pogled = "tereni"
    ,cena = 60
    ,ukupan_broj_soba = 15
    ,raspolozivo = 15
 WHERE id_kategorije = 3;