CREATE DATABASE hotel;
USE hotel;

CREATE TABLE `room_categories` (
  `id_kategorije` int NOT NULL AUTO_INCREMENT,
  `broj_kreveta` int NOT NULL,
  `apartman` tinyint(1) NOT NULL,
  `pogled` enum('more','parking','park','tereni') NOT NULL,
  `cena` float NOT NULL,
  `ukupan_broj_soba` int NOT NULL,
  `raspolozivo` int NOT NULL,
  PRIMARY KEY (`id_kategorije`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO room_categories(broj_kreveta, apartman, pogled, cena, ukupan_broj_soba, raspolozivo)
VALUES (4, 1, 'more', 100, 5, 5),
       (2, 0, 'park', 80, 10, 10),
       (3, 0, 'tereni', 60, 15, 15);

CREATE TABLE `rooms` (
  `id_sobe` int NOT NULL AUTO_INCREMENT,
  `sprat` int NOT NULL,
  `id_kategorije` int NOT NULL,
  `raspoloziva` tinyint(1) NOT NULL,
  PRIMARY KEY (`id_sobe`),
  KEY `id_kategorije` (`id_kategorije`),
  CONSTRAINT `sobe_ibfk_1` FOREIGN KEY (`id_kategorije`) REFERENCES `room_categories` (`id_kategorije`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `reservations` (
  `id_rezervacije` int NOT NULL AUTO_INCREMENT,
  `datum_rezervacije` date NOT NULL,
  `broj_osoba` int NOT NULL,
  `zakazani_datum_pocetka` date NOT NULL,
  `zakazani_datum_zavrsetka` date NOT NULL,
  `realni_datum_pocetka` date DEFAULT NULL,
  `realni_datum_zavrsetka` date DEFAULT NULL,
  `id_sobe` int NOT NULL,
  PRIMARY KEY (`id_rezervacije`),
  KEY `id_sobe` (`id_sobe`),
  CONSTRAINT `rezervacija_ibfk_1` FOREIGN KEY (`id_sobe`) REFERENCES `rooms` (`id_sobe`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `guests` (
  `id_gosta` int NOT NULL AUTO_INCREMENT,
  `broj_pasosa` int NOT NULL,
  `ime` varchar(50) NOT NULL,
  `prezime` varchar(50) NOT NULL,
  PRIMARY KEY (`id_gosta`),
  UNIQUE KEY `broj_pasosa` (`broj_pasosa`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `checked_in_reservations` (
  `id_OuR` int NOT NULL AUTO_INCREMENT,
  `id_gosta` int NOT NULL,
  `kontakt_osoba` int NOT NULL,
  `id_rezervacije` int NOT NULL,
  `telefon` varchar(20) NOT NULL,
  PRIMARY KEY (`id_OuR`),
  KEY `osobe_u_rezervaciji_ibfk_2_idx` (`id_gosta`),
  KEY `osobe_u_rezervaciji_ibfk_3_idx` (`id_rezervacije`),
  KEY `osobe_u_rezervaciji_ibfk_1_idx` (`kontakt_osoba`),
  CONSTRAINT `osobe_u_rezervaciji_ibfk_1` FOREIGN KEY (`kontakt_osoba`) REFERENCES `guests` (`broj_pasosa`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `osobe_u_rezervaciji_ibfk_2` FOREIGN KEY (`id_gosta`) REFERENCES `guests` (`id_gosta`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `osobe_u_rezervaciji_ibfk_3` FOREIGN KEY (`id_rezervacije`) REFERENCES `reservations` (`id_rezervacije`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;