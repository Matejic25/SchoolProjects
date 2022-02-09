CREATE DATABASE hotel;
USE hotel;

CREATE TABLE `room_categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `num_of_beds` int NOT NULL,
  `apartment` tinyint(1) NOT NULL,
  `view` enum('more','parking','park','tereni') NOT NULL,
  `price` float NOT NULL,
  `num_of_rooms` int NOT NULL,
  `available` int NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO room_categories(num_of_beds, apartment, view, price, num_of_rooms, available)
VALUES (4, 1, 'more', 100, 5, 5),
       (2, 0, 'park', 80, 10, 10),
       (3, 0, 'tereni', 60, 15, 15);

CREATE TABLE `rooms` (
  `room_id` int NOT NULL AUTO_INCREMENT,
  `floor` int NOT NULL,
  `category_id` int NOT NULL,
  `available` tinyint(1) NOT NULL,
  PRIMARY KEY (`room_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `sobe_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `room_categories` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `reservations` (
  `reservation_id` int NOT NULL AUTO_INCREMENT,
  `reservation_date` date NOT NULL,
  `num_of_guests` int NOT NULL,
  `reservation_beginning_date` date NOT NULL,
  `reservation_ending_date` date NOT NULL,
  `check_in_date` date DEFAULT NULL,
  `checkout_date` date DEFAULT NULL,
  `room_id` int NOT NULL,
  PRIMARY KEY (`reservation_id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `rezervacija_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `guests` (
  `guest_id` int NOT NULL AUTO_INCREMENT,
  `passport_serial_number` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `surname` varchar(50) NOT NULL,
  PRIMARY KEY (`guest_id`),
  UNIQUE KEY `passport_serial_number` (`passport_serial_number`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `checked_in_reservations` (
  `checked_in_reservation_id` int NOT NULL AUTO_INCREMENT,
  `guest_id` int NOT NULL,
  `contact_person` int NOT NULL,
  `reservation_id` int NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  PRIMARY KEY (`checked_in_reservation_id`),
  KEY `osobe_u_rezervaciji_ibfk_2_idx` (`guest_id`),
  KEY `osobe_u_rezervaciji_ibfk_3_idx` (`reservation_id`),
  KEY `osobe_u_rezervaciji_ibfk_1_idx` (`contact_person`),
  CONSTRAINT `osobe_u_rezervaciji_ibfk_1` FOREIGN KEY (`contact_person`) REFERENCES `guests` (`passport_serial_number`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `osobe_u_rezervaciji_ibfk_2` FOREIGN KEY (`guest_id`) REFERENCES `guests` (`guest_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `osobe_u_rezervaciji_ibfk_3` FOREIGN KEY (`reservation_id`) REFERENCES `reservations` (`reservation_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
