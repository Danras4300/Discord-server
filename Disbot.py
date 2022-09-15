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

item_room_0 = ["flashlight"]
item_room_1 = ["key"]
item_room_2 = [""]
item_room_3 = [""]
item_inventory = [""]


Items = {
    0 : item_room_0,
    1 : item_room_1,
    2 : item_room_2,
    3 : item_room_3,
    "inventory" : item_inventory
}

class room:
    def __init__(self,name,surroundings,object):
        self.name = name
        self.surroundings = surroundings
        self.object = object
        

    def show(self):
        print(self.name + "description:", self.surroundings, self.object )

room_0 = room("cell", "You are in an empty room with white walls."
    "Theres a door to your west."
    'if you need help type "help"'
    "Items available in this room", list(Items.values())[list(Items.keys()).index("0")])

room_1 = room("hallway 1", "You are in an empty hallway, but you see a shiny key laying in the corner"
    "There's a staircase to your north", list(Items.values())[list(Items.keys()).index("1")])

room_2 = room("hallway 2", "Display the contents of room 2."""
    "You are in an empty hallway on the second floor."
    "There's a locked room to your east", list(Items.values())[list(Items.keys()).index("2")])

room_3 = room("Guard room", "You've unlocked the door."
    "In front of you there is a table, chairs and security cameras"
    "There's an open window to your east", list(Items.values())[list(Items.keys()).index("3")])


def move_from_room_0(direction):
    """ Room 0 only has a single exit , which leads north to room 1. """
    if direction == "west": 
        print([room_1])
        return 1
    else:
        print("It is not possible to go in that direction")
        return 0

def move_from_room_1(direction):
    if direction == "north": 
        print([room_2])
        return 2
    elif direction == "east":  
        print([room_0])
        return 0
    else: 
        print("It is not possible to go in that direction")
        return 1
    
def move_from_room_2(direction):
    if direction == "east":
        print([room_3])
        return 3
    elif direction == "west":
        print([room_1])
        return 1
    else: 
        print("It is not possible to go in that direction")
        return 2

def move_from_room_3(direction):
    if direction == "east":
        print("Congratulations you have escaped from prison")
        return
    if direction == "west": 
        print([room_2])
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
        print([room_0])
    elif room_num == 1: 
        print([room_1])
    elif room_num == 2:
        print([room_2])
    elif room_num == 3:
        print([room_3])
    else:
        reply = "You are out of bounds. Room", room_num, "does not exist."
        return reply
        

def get_room_items(current_room):
    """Find the list of items in the room."""
    if current_room == 0:
        return list(Items.values())[list(Items.keys()).index(0)]
    elif current_room == 1:
        return list(Items.values())[list(Items.keys()).index(1)]
    elif current_room == 2: 
        return list(Items.values())[list(Items.keys()).index(2)]
    elif current_room == 3:
        return list(Items.values())[list(Items.keys()).index(3)]

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
      print(list(Items.values())[list(Items.keys()).index("inventory")])
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
