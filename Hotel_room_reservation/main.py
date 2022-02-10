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
        passport_number = int(input("Passport serial number: "))
        name = str(input("Name: "))
        surname = str(input("Surname: "))
        add_guest(passport_number, name, surname)
    elif chosen_option == '2':
        print("Check room capacity")
        room_id = int(input("Room ID: "))
        num_of_guests = int(input("Passport serial number: "))
        check_capacity(room_id, num_of_guests)
    elif chosen_option == '3':
        print("Check occupied dates")
        room_id = input("Room ID: ")
        beginning_date = input("Reservation beginning date: ")
        ending_date = input("Reservation ending date: ")
        check_occupied_dates(room_id, beginning_date, ending_date)
    elif chosen_option == '4':
        print("Refresh availability of the rooms")
        refresh_availability_of_rooms()
    elif chosen_option == '5':
        print("Occupy/Free the room")
        room_id = int(input("Room ID: "))
        request = input("Occupy/Free: ")
        occupy_free_the_room(room_id, request)
    elif chosen_option == '6':
        print("Add reservation")
        room_id = int(input("Room ID: "))
        num_of_guests = int(input("Number of guests: "))
        beginning_date = input("Reservation beginning date: ")
        ending_date = input("Reservation ending date: ")
        add_reservation(room_id, num_of_guests, beginning_date, ending_date)
    elif chosen_option == '7':
        print("Remove reservation")
        reservation_id = int(input("Reservation ID: "))
        remove_reservation(reservation_id)
    elif chosen_option == '8':
        print("View all reservations")
        print("[Res_ID]  [Res_date]   [Num_of_guests] [Beginning_date]  [Ending_date]     [Check-in]    [Check-out] "
              "[Room_ID]")
        all_reservations()
    elif chosen_option == '9':
        print("Check-in")
        passport_number = int(input("Passport serial number: "))
        room_id = int(input("Room ID: "))
        phone_number = str(input("Phone number: "))
        print("[Guest_ID][Passport_num]      [Name]           [Surname]      [Room_id]      [Phone_number]")
        check_in(passport_number, room_id, phone_number)
    elif chosen_option == '10':
        print("Checkout")
        reservation_id = int(input("Reservation ID: "))
        checkout(reservation_id)
    else:
        print("Option does not exist!")
