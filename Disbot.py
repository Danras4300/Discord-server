import discord

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

client = discord.Client(intents=intents)

TOK_FILE = "token.txt"

def get_token():
  tokfile = open(TOK_FILE, 'r')
  token = tokfile.read()
  tokfile.close()
  return token

@client.event
async def on_ready():
    print("Connected!")

### Helper functions for displaying rooms ###

Items = {
    "key" : "1",
    "flashlight" : "0"
}

def show_room_0():
    """Display the contents of room 0."""
    reply = ["You are in an empty room with white walls.",
    "Theres a door to your west.",
    'if you need help type "help"',
    "Items available in this room",
    list(Items.keys())[list(Items.values()).index("0")]]
    return reply
     
      

    
    

def show_room_1():
    """Display the contents of room 1."""
    reply = ["You are in an empty hallway, but you see a shiny key laying in the corner",
    "There's a staircase to your north"
    (list(Items.keys())[list(Items.values()).index("1")])]
    return reply
    

def show_room_2():
    reply = ["""Display the contents of room 2.""",
    "You are in an empty hallway on the second floor.",
    "There's a locked room to your east",
    list(Items.keys())[list(Items.values()).index("2")]]
    return reply

def show_room_3():
    """Display the contents of room 3"""
    reply = ["You've unlocked the door.",
    "In front of you there is a table, chairs and security cameras",
    "There's an open window to your east",
    list(Items.keys())[list(Items.values()).index("3")]]
    return reply



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
        "You have climbed the stairs to the 2nd floor",
        "You are in an empty hallway on the second floor.",
        "There's a locked room to your east"
        return 2
    elif direction == "east":  
        "You returned to your cell",
        "You are in an empty room with white walls.",
        "Theres a door to your west."
        return 0
    else: 
        print("It is not possible to go in that direction")
        return 1
    
def move_from_room_2(direction):
    if direction == "east":
        "You have unlocked the door to the security room",
        "In front of you there is a table, chairs and security cameras"
        "There's an open window to your east"
        return 3
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
        ["you have returnd to the halway",
        "You are in an empty hallway on the second floor.",
        "There's a locked room to your east"]
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
        reply = "You are out of bounds. Room", room_num, "does not exist."
        return reply
        

def get_room_items(current_room):
    """Find the list of items in the room."""
    if current_room == 0:
        return list(Items.keys())[list(Items.values()).index("0")]
    elif current_room == 1:
        return list(Items.keys())[list(Items.values()).index("1")]
    elif current_room == 2: 
        return list(Items.keys())[list(Items.values()).index("2")]
    elif current_room == 3:
        return list(Items.keys())[list(Items.values()).index("3")]

### The main game loop ###

@client.event
async def on_message(message):
    contents = message.content
    user = message.author.id
  
    current_room = 0
    if contents.startswith("!look"):
      await message.channel.send(show_room(current_room)) #kig på den næste gang (fejl besked)
    elif contents.startswith("!help"):
      reply = ['"!look" gives a short presentation of the current room',
               '"!grab" u can use the grab command to grab an item',
               '"!walk" lets you walk the direction you want (North, west, east, south)',
               '"!east" you move east from your current position',
               '"!south" you move south from your current position',
               '"!west" you move west from your current position',
               '"!north" you move north from your current position',
               '"!quit" you can only use quit if you wish to exit the game',
               '"!items" view the items that are available in your current room']
      await message.channel.send("\n".join(reply))
    elif contents.startswith("!grab"):
      item = contents[6:]
      print(item)
      if item in Items:
        if item == "flashlight":
          Items[item] = "inventory"
          print("You have grabbed this item:", item)
          await message.channel.send(reply)
        elif Items[item] == "inventory":
          print("You already have this item:", item)
        elif Items["flashlight"] != "inventory": 
          print("It's too dark to see without flashlight")
      elif Items[item] == "inventory":
          print("You already have this item:", item)
      else:
        print("unable to find:", item)
    elif contents.startswith("!drop"):
      item = contents[5:]
      Items[item] = str(current_room)
      print("You have dropped the", item)
    elif contents.startswith("!inventory"):
      print(list(Items.keys())[list(Items.values()).index("inventory")])
    elif contents.startswith("!walk"):
      direction = contents[6:]
      print(direction)
      if Items["flashlight"] == "inventory":
        if current_room == 0:
          current_room = move_from_room_0(direction)
        elif current_room == 1:
          current_room = move_from_room_1(direction)
        elif current_room == 2: 
          if direction == "east":
            if Items["key"] == "inventory":
              current_room = move_from_room_2(direction)
            else: 
              print("You can't unlock the door without the key")
          else: 
            current_room = move_from_room_2(direction)
        elif current_room == 3: 
          current_room = move_from_room_3(direction)
          if direction == "east":
            print("You have escaped prison!")
      else: 
        print("It's too dark to move")
    else:
      print("I don't understand..")


token = get_token()
client.run(token)