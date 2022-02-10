from pymysql import *

connection = connect(host='localhost',
                     user='root',
                     password='1234321',
                     database='hotel')

mycursor = connection.cursor()


def add_guest(passport_serial_number, name, surname):
    mycursor.execute("INSERT INTO guests(passport_serial_number, name, surname)"
                     "VALUES (%s, %s, %s)", (passport_serial_number, name, surname))
    connection.commit()
    print(f"Guest {name} {surname} added successfully.")


# PROMENA BROJA RASPOLOZIVIH SOBA U KATEGORIJI (MENJA VREDNOST raspolozivo U TABELI room_categories)
def refresh_available_in_category():
    list3 = []
    list2 = []
    list1 = []
    mycursor.execute("SELECT room_id FROM rooms WHERE available = 1 AND category_id = 3")
    for i in mycursor:
        list3.append(i)
    free_rooms3 = len(list3)
    mycursor.execute("SELECT room_id FROM rooms WHERE available = 1 AND category_id = 2")
    for i in mycursor:
        list2.append(i)
    free_rooms2 = len(list2)
    mycursor.execute("SELECT room_id FROM rooms WHERE available = 1 AND category_id = 1")
    for i in mycursor:
        list1.append(i)
    free_rooms1 = len(list1)
    mycursor.execute("UPDATE room_categories SET available = %s WHERE category_id = 3", free_rooms3)
    mycursor.execute("UPDATE room_categories SET available = %s WHERE category_id = 2", free_rooms2)
    mycursor.execute("UPDATE room_categories SET available = %s WHERE category_id = 1", free_rooms1)
    connection.commit()


# ZAUZMI/OSLOBODI SOBU (MENJA VREDNOST raspoloziva U TABELI sobe), PROVERA RASPOLOZIVOSTI SOBE
# POZIVA I FUNKCIJU refresh_available_in_category KOJA OSVEZI/PROMENI VREDNOST raspolozivo U room_categories
def occupy_free_the_room(room_id, request):
    mycursor.execute("SELECT room_id FROM rooms")
    for i in mycursor:
        if i[0] != room_id:
            pass
        elif i[0] == room_id and request.lower() == "occupy":
            mycursor.execute("SELECT available FROM rooms WHERE room_id = %s", room_id)
            for j in mycursor:
                if j[0] == 0:
                    print("Room already occupied")
                    return "already_occupied"
                else:
                    mycursor.execute("UPDATE rooms SET available = 0 WHERE room_id = %s", room_id)
                    connection.commit()
                    refresh_available_in_category()
                    return "occupation_successful"
        elif i[0] == room_id and request.lower() == "free":
            mycursor.execute("SELECT available FROM rooms WHERE room_id = %s", room_id)
            for j in mycursor:
                if j[0] == 1:
                    print("Room already free")
                    return "already_free"
                else:
                    mycursor.execute("UPDATE rooms SET available = 1 WHERE room_id = %s", room_id)
                    connection.commit()
                    refresh_available_in_category()
                    return "freeing_successful"
        else:
            return -1


# PROVERA KAPACITETA SOBE I BROJ ZAHTEVANIH OSOBA U SOBI
def check_capacity(room_id, num_of_guests):
    mycursor.execute(f"SELECT num_of_beds "
                     "FROM rooms AS r LEFT JOIN room_categories AS rc "
                     "ON r.category_id = rc.category_id WHERE r.room_id = %s", room_id)
    capacity = mycursor.fetchone()[0]
    print(f"This room contains {capacity} beds")
    return num_of_guests <= capacity


# PROVERA DA LI SE ZELJENI DATUM ZA REZERVACIJU SOBE NALAZI U OPSEGU VEC REZERVISANIH SOBA
# ako je soba zauzeta tokom zeljenog termina vraca False
# ako je soba slobodna tokom zeljenog termina vraca True
def check_occupied_dates(room_id, beginning_date, ending_date):
    mycursor.execute("SELECT reservation_id, reservation_beginning_date, reservation_ending_date FROM reservations "
                     "WHERE reservation_beginning_date BETWEEN %s AND %s AND room_id = %s "
                     "OR reservation_ending_date BETWEEN %s AND %s AND room_id = %s "
                     "OR %s BETWEEN reservation_beginning_date AND reservation_ending_date AND room_id = %s "
                     "OR %s BETWEEN reservation_beginning_date AND reservation_ending_date AND room_id = %s"
                     , (beginning_date, ending_date, room_id, beginning_date, ending_date, room_id, beginning_date,
                        room_id, ending_date, room_id))
    results = 0
    for i in mycursor:
        results += 1
        if results > 0:
            print(f"Room: {room_id} is occupied in period | OF: {i[1]} | TO: {i[2]} ---- Reservation ID: {i[0]}")
        else:
            print(f"The room: {room_id} is free in period | OF: {beginning_date} | TO: {ending_date}")
    if results > 0:
        return False
    else:
        return True


# ZAVISNOST RASPOLOZIVOSTI SOBE U ODNOSU NA TO DA LI JE room_id U rezervacija
def refresh_availability_of_rooms():
    rooms = []
    reserved = []
    non_reserved = []
    mycursor.execute("SELECT room_id FROM rooms ORDER BY room_id DESC")
    for i in mycursor:
        rooms.append(i[0])
    mycursor.execute("SELECT room_id FROM reservations ORDER BY room_id DESC")
    for i in mycursor:
        reserved.append(i[0])
    for room in rooms:
        if room in rooms and room not in reserved:
            non_reserved.append(room)
        else:
            for reserved_room in reserved:
                mycursor.execute("UPDATE rooms SET available = 0 WHERE room_id = %s", reserved_room)
    for non_reserved_room in non_reserved:
        mycursor.execute("UPDATE rooms SET available = 1 WHERE room_id = %s", non_reserved_room)
    refresh_available_in_category()
    connection.commit()
    print("Availabilities refreshed.")


# DODAVANJE REZERVACIJE NAKON ISPUNJENIH USLOVA
def add_reservation(room_id, num_of_guests, beginning_date, ending_date):
    if check_capacity(room_id, num_of_guests) is True:
        if occupy_free_the_room(room_id, "occupy") != "already_occupied" or \
                occupy_free_the_room(room_id, "occupy") == "already_occupied" and \
                check_occupied_dates(room_id, beginning_date, ending_date) is True:
            mycursor.execute("INSERT INTO reservations(room_id, reservation_date, num_of_guests,"
                             " reservation_beginning_date, reservation_ending_date)"
                             "VALUES (%s,CURRENT_DATE(),%s,%s,%s)",
                             (room_id, num_of_guests, beginning_date, ending_date))
            print("Reservation added successfully.")
            refresh_available_in_category()
            refresh_availability_of_rooms()
            connection.commit()
        else:
            print("Reservation declined")
    else:
        print("Not enough beds in the room for reservation")


def remove_reservation(reservation_id):
    mycursor.execute("SELECT room_id FROM reservations WHERE reservation_id=%s", reservation_id)
    mycursor.execute("DELETE FROM reservations WHERE reservation_id=%s", reservation_id)
    refresh_availability_of_rooms()
    refresh_available_in_category()
    connection.commit()
    print("Reservation removed successfully")


def all_reservations():
    mycursor.execute("SELECT * FROM reservations")
    for reservation in mycursor:
        for data in range(8):
            print(reservation[data], end="       ")
        print("\n")


def check_in(passport_serial_number, room_id, phone_number):
    mycursor.execute("SELECT * FROM guests WHERE passport_serial_number = %s", passport_serial_number)
    guest_id = None
    reservation_id = None
    name = ""
    surname = ""
    for data in mycursor:
        guest_id = data[0]
        name = data[2]
        surname = data[3]
        for i in data:
            print(i, end="           ")
    mycursor.execute("SELECT reservation_id FROM reservations WHERE room_id = %s", room_id)
    for i in mycursor:
        print(i[0], "       ", phone_number)
        reservation_id = i[0]
    if guest_id is not None and reservation_id is not None:
        mycursor.execute("INSERT INTO checked_in_reservations(guest_id, contact_person, reservation_id, phone_number)"
                         " VALUES(%s, %s, %s, %s)", (guest_id, passport_serial_number, reservation_id, phone_number))
        mycursor.execute("UPDATE reservations SET check_in_date = CURRENT_DATE()"
                         "WHERE reservation_id=%s", reservation_id)
        connection.commit()
        print(f"Reservation of guest {name} {surname} is checked-in successfully.")
    else:
        print("Invalid guest data.")


def checkout(reservation_id):
    mycursor.execute("SELECT reservation_id FROM checked_in_reservations")
    for reservation in mycursor:
        if reservation[0] == reservation_id:
            mycursor.execute("DELETE FROM checked_in_reservations WHERE reservation_id = %s", reservation_id)
            mycursor.execute("UPDATE reservations SET checkout_date = CURRENT_DATE()"
                             "WHERE reservation_id=%s", reservation_id)
            connection.commit()
        else:
            print("Reservation ID not found.")
    print("Reservation checked out successfully.")
