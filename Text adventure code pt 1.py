### Helper functions for displaying rooms ###


def show_room_0():
    """Display the contents of room 0."""
    print("You are in an empty room with white walls.")
    print("Theres a door to your west.")
    print('if you need help type "help"')
 
def show_room_1():
    """Display the contents of room 1."""
    print("You are in an empty hallway, but you see a shiny key laying in the corner")
    print("There's a staircase to your north")

def show_room_2():
    """Display the contents of room 2."""
    print("You are in an empty hallway on the second floor.")
    print("There's a locked room to your east")

def show_room_3():
    """Display the contents of room 3"""
    print("You've unlocked the door.")
    print("In front of you there is a table, chairs and security cameras")
    print("There's an open window to your east")

def move_from_room_0(direction):
    """ Room 0 only has a single exit , which leads north to room 1. """
    if direction == "west": 
        print("You are in an empty hallway, but you see a shiny key laying in the corner")
        print("There's a staircase to your north")
        return 1
    else:
        print("It is not possible to go in that direction")
        return 0

def move_from_room_1(direction):
    if direction == "north": 
        print ("You have climbed the stairs to the 2nd floor")
        print ("You are in an empty hallway on the second floor.")
        print ("There's a locked room to your east")
        return 2
    elif direction == "east":  
        print("You returned to your cell")
        print ("You are in an empty room with white walls.")
        print ("Theres a door to your west.")
        return 0
    else: 
        print("It is not possible to go in that direction")
        return 1
    
def move_from_room_2(direction, has_key):
    if direction == "east": 
        if has_key == True:
            print("You have unlocked the door to the security room")
            print("In front of you there is a table, chairs and security cameras")
            print("There's an open window to your east")
            return 3
        else:
            print("You cannot go in that direction without the key")
            return 2
    elif direction == "west":
        print("You are in an empty hallway, but you see a shiny key laying in the corner")
        print("There's a staircase to your north-west")
        return 1
    else: 
        print("It is not possible to go in that direction")
        return 2

def move_from_room_3(direction):
    if direction == "east":
        print("Congratulations you have escaped from prison")
        return
    if direction == "west": 
        print("you have returnd to the halway")
        print("You are in an empty hallway on the second floor.")
        print("There's a locked room to your east")
        return 2
    else: 
        print("you can not go in that direction")
        return 3

def show_room(room_num):
    """Display the contents of the given room.
    Input:
    - room_num : int, the number of the room to show.
    """
    if room_num == 0:
        show_room_0()
    elif room_num == 1: 
        show_room_1()
    elif room_num == 2:
        show_room_2()
    elif room_num == 3:
        show_room_3()
    else:
        print("You are out of bounds. Room", room_num, "does not exist.")

### The main game loop ###

def game_loop():
    """Main loop of the game - this is where the fun happens."""

    # We start in room 0
    current_room = 0
    has_key = False
    key_count = 0

    # Display the room that we start in
    show_room(current_room)

    # Enter the main loop, where the user can input commands.
    while True:
        user_inp = input("> ")
        
        if user_inp == "look":
            show_room(current_room) 
        elif user_inp == "grab key":
            if has_key == True:
                print ("you have the key already")
            elif user_inp == "grab key":
                if current_room == 1: 
                    has_key = True
                    key_count = 1
                    print ("you have grabbed the key")
            else: 
                if current_room == 0 or current_room == 2 or current_room == 3:
                    print ("No key here.")
        elif user_inp == "help":
            print('"look" gives a short presentation of the current room')
            print('"grab" u can use the grab command to grab an item')
            print('"east" you move east from your current position')
            print('"south" you move south from your current position')
            print('"west" you move west from your current position')
            print('"north" you move north from your current position')
            print('"quit" you can only use quit if you wish to exit the game')
        elif user_inp == "west" or user_inp == "north" or user_inp == "east" or user_inp == "south":
            if current_room == 0:
                current_room = move_from_room_0(user_inp)
            elif current_room == 1:
                current_room = move_from_room_1(user_inp)    
            elif current_room == 2:
                current_room = move_from_room_2(user_inp, has_key)
            elif current_room == 3:
                current_room = move_from_room_3(user_inp)                
        elif user_inp == "quit":
            return
        else:
            print("I do not understand the command:", user_inp)

# Start the game!
game_loop()
