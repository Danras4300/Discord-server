from pdb import Restart
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

#Lister

item_room_0 = ["flashlight"]
item_room_1 = ["key"]
item_room_2 = []
item_room_3 = []
item_inventory = []

#Dictionaries

Items = {
    "0" : item_room_0, 
    "1" : item_room_1,
    "2" : item_room_2,
    "3" : item_room_3,
    "inventory" : item_inventory
}

current_room = 0


class room:
    def __init__(self,name,surroundings,object):
        self.name = name
        self.surroundings = surroundings
        self.object = object
        

    def show(self):
        return self.name + "description: " + self.surroundings + str(self.object) 

#Klasser & objekter

room_0 = room("Cell ", "You are in an empty room with white walls. "
    "Theres a door to your west. "
    'If you need help type "!help" '
    "Items available in this room ", list(Items.values())[list(Items.keys()).index("0")])

room_1 = room("Hallway 1 ", "You are in an empty hallway, but you see a shiny key laying in the corner "
    "There's a staircase to your north ", list(Items.values())[list(Items.keys()).index("1")])

room_2 = room("Hallway 2 ", "Display the contents of room 2. "
    "You are in an empty hallway on the second floor. "
    "There's a locked room to your east ", list(Items.values())[list(Items.keys()).index("2")])

room_3 = room("Guard room ", "You've unlocked the door. "
    "In front of you there is a table, chairs and security cameras "
    "There's an open window to your east ", list(Items.values())[list(Items.keys()).index("3")])


def move_from_room_0(direction):
    """ Room 0 only has a single exit , which leads north to room 1. """
    if direction == "west": 
        return 1
    else:
        return 0

def move_from_room_1(direction):
    if direction == "north": 
        return 2
    elif direction == "east":  
        return 0
    else: 
        return 1
    
def move_from_room_2(direction):
    if direction == "east":
        return 3
    elif direction == "west":
        return 1
    else: 
        return 2

def move_from_room_3(direction):
    if direction == "east":
        return
    if direction == "west": 
        return 2
    else: 
        return 3

def show_room(room_num):
    """Display the contents of the given room.
    Input:
    - room_num : int, the number of the room to show.
    """
    if room_num == 0:
        return room_0.show()
    elif room_num == 1: 
        return room_1.show()
    elif room_num == 2:
        return room_2.show()
    elif room_num == 3:
        return room_3.show()
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
    global current_room
    contents = message.content
    user = message.author.id
    
    if contents.startswith("!look"):
      await message.channel.send(show_room(current_room)) 
    elif contents.startswith("!help"):
      reply = ['"!look" gives a short presentation of the current room',
               '"!grab" u can use the grab command to grab an item',
               '"!walk" lets you walk the direction you want (North, west, east, south)',
               '"!drop" lets you drop the items you dont want',
               '"!quit" you can only use quit if you wish to exit the game',
               '"!items" view the items that are available in your inventory']
      await message.channel.send("\n".join(reply))
    elif contents.startswith("!grab"):
      item = contents[6:]
      print(item)
      for n in range(0,len(Items[str(current_room)])):
        if item == Items[str(current_room)][n]:
            if item == "flashlight":
                Items[str(current_room)].remove(item) 
                Items["inventory"].append(item)
                reply = "You have grabbed this item: " + item
                await message.channel.send(reply)
            elif "flashlight" not in Items["inventory"]: 
                reply = "It's too dark to see without flashlight" 
                await message.channel.send(reply)
            elif item == Items[str(current_room)][n]:
                Items[str(current_room)].remove(item)
                Items["inventory"].append(item)
                reply = "You have grabbed this item: " + item
                await message.channel.send(reply)
        elif item in Items["inventory"]: 
            reply = "You already have this item: " + item
            await message.channel.send(reply)
        else:
          reply = "unable to find: ", item 
          await message.channel.send(reply)
    elif contents.startswith("!drop"):
      item = contents[6:]
      Items["inventory"].remove(item)
      Items[str(current_room)].append(item)
      reply = "You have dropped this item:" + item
      print(item)
      for n in range(0,len(Items["inventory"])):
        if item == Items["inventory"][n]:
            Items["inventory"].remove(item)
            Items[str(current_room)].append(item)
            reply = "You have dropped this item: " + item
            await message.channel.send(reply)
    elif contents.startswith("!inventory"):
      for n in Items["inventory"]:
        reply = n
        await message.channel.send(reply)
    elif contents.startswith("!walk"):
      direction = contents[6:]
      print(direction)
      if "flashlight" in Items["inventory"]:
        if current_room == 0:
            current_room = move_from_room_0(direction)
        elif current_room == 1:
            current_room = move_from_room_1(direction)
        elif current_room == 2:
            if direction == "east":
                if "key" in Items["inventory"]:
                    current_room = move_from_room_2(direction)
                else: 
                    reply = "You can't unlock the door without the key"
                    await message.channel.send(reply)
            else:
                current_room = move_from_room_2(direction)
        elif current_room == 3: 
            current_room = move_from_room_3(direction)
            if direction == "east":
                reply = "You have escaped prison!"
                await message.channel.send(reply)
                Restart
      else:
        reply = "Its too dark to move"
        await message.channel.send(reply)
    else:
      pass


token = get_token()
client.run(token)
