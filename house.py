# Intro to programming game tutorial.

class Room:

    # place holder values to demonstrate what kind of data we will hold here
    # normally use enums, but python doesn't have enums.
    # this is a dictionary (aka hashmap)
    # doors = {
    #     "north": False,
    #     "east": False,
    #     "south": False,
    #     "west": False
    # }
    #
    # items are stored in a dictionary
    # e.g.
    # items = {
    #     "lamp": Lamp(),
    #     "dresser": Dresser()
    # }

    def __init__(self, name, description, doors, items):
        self.name = name
        self.description = description
        self.doors = doors
        self.items = items

    def check(self, item_name):
        if not (item_name in self.items):
            print "Checked [" + item_name + "], but found nothing."
            return

        else:  # item must be in the room
            self.items[item_name].check()


class Player:

    def __init__(self):
        self.name = 'Kenny'
        self.hp = 2
        self.x = 0
        self.y = 0
        self.items = {} # dictionary of items

    def is_alive(self):
        return self.hp > 0


# Item & Item Implementations
class Item:

    def __init__(self):
        pass

    def check(self):
        print "default check, do nothing."


class Lamp(Item):

    def __init__(self):
        self.is_on = False

    def check(self):
        if self.is_on:
            self.is_on = False
            print "Turning off the light."
        else:
            self.is_on = True
            print "You turned on the light and it begins to flicker. You notice a lock on the dresser."


class Dresser(Item):

    def __init__(self, player):
        self.is_locked = True
        self.has_underwear = True
        self.player = player

    def check(self):
        if self.is_locked:
            if "dresser_key" in self.player.items:
                self.is_locked = False
                print "Used key to unlock dresser."

            else:
                print "You try and open the dresser, but it appears to be locked."

        else:  # it's now unlocked
            if self.has_underwear:
                self.player.items["dirty_underwear"] = True
                self.has_underwear = False
                print "You found shit stained underwear that need to be washed. It could be useful."
            else:
                print "The dresser is empty, but you can still see the shit outline from the dirty underwear."


class Bed(Item):

    def __init__(self, player):
        self.has_key = True
        self.player = player

    def check(self):
        if self.has_key:
            self.has_key = False
            self.player.items["dresser_key"] = True
            print "Found key under the pillow. Placed it in pocket."
        else:
            print "There is nothing left on the bed except splooge stains."


class DirtyToilet(Item):

    def __init__(self, player):
        self.player = player

    def check(self):
        self.player.hp -= 1
        print "You open the toilet and see chopped up body parts and shit. You don't know which is more gross. You begin puking uncontrollably. Aftwards you are in extreme pain."


class BathTub(Item):

    def __init__(self, player):
        self.player = player
        self.has_liver = True

    def check(self):
        print "There is a rotting corpse in the bathtub. It appears to be missing it's limbs. Upon closer look it is Steve!? OMG What happened?!"

        if self.has_liver:
            if "knife" in self.player.items:
                self.player.items["raw_liver"] = True
                self.has_liver = False
                print "You use your knife to cut into the body's abdomen and after several minutes and a lot of blood and puss, you pull out a fresh liver, it looks tasty, but a bit undercooked."
            else:  # we don't have gloves
                self.player.hp -= 1
                print "As you press your hand into the rotten corpse, maggots and mice begin biting your hand. You jump back in pain."


class BreakerBox(Item):

    def __init__(self, house):
        self.house = house
        self.is_on = True

    def check(self):
        if self.is_on:
            print "Everything looks fine"

        else:
            self.is_on = True
            # change state in kitchen

            print "The breaker is off, you flip it on, and the power comes back on."

            if "puppy" in house.rooms[2][2].itemsc:
                print "You see a starving puppy whimpering in the corner. It looks hungry."



class Washer(Item):

    def __init__(self, player, breakerBox):
        self.player = player
        self.breakerBox = breakerBox

    def check(self):
        if "dirty_underwear" in self.player.items:
            self.breakerBox.is_on = False
            del self.player.items["dirty_underwear"]
            print "You place the soiled underwear in the washer and turn it on. Immediately all the lights flicker and go off. It appears that you blew a breaker."

        else:
            print "You don't have anything to wash, yet"


class Puppy(Item):

    def __init__(self, house):
        self.house = house
        self.player = house.player
        self.is_eat_meat = False

    def check(self):
        if not self.is_eat_meat:  # the dog should be in the garage
            if "cooked_liver" in self.player.items:
                del self.player.items["cooked_liver"]
                self.is_eat_meat = True
                del house.rooms[2][2].items["puppy"]     # remove puppy from current room
                house.rooms[2][1].items["puppy"] = self  # add puppy to living room
                house.rooms[2][1].items["remote"] = Remote(self.house)
                house.rooms[2][1].description += " The puppy found the remote and brought it to you."  # update the room description to mention the dog
                print "You give the liver to the puppy. It devours the meat instantly and then runs to the living room."

            else:
                self.player.hp -= 1
                print "You pet the starving puppy and it bites you. It is really hungry."

        else:  # the dog should be in the living room
            print "The puppy barks and nudges the remote towards you."


class Floor(Item):

    def __init__(self, player):
        self.player = player
        self.has_knife = True

    def check(self):
        if self.has_knife:
            self.has_knife = False
            self.player.items["knife"] = True
            print "You found a dull, rusty knife covered in human blood. This should be useful."


class Stove(Item):

    def __init__(self, player):
        self.player = player

    def check(self):
        if "raw_liver" in self.player.items:
            del self.player.items["raw_liver"]
            self.player.items["cooked_liver"] = True
            print "After adding spices and cooking for 30 minutes the liver turned out perfect. Someone is dying to eat this."

        else:
            print "The perfect oven to cook a feast."


class FrontDoor(Item):

    def __init__(self, house):
        self.house = house
        self.player = house.player

    def check(self):
        if "house_key" in self.player.items:
            print "You place the key into the front door. Why on Earth it's locked from the inside? You'll never know. You step outside, finally escaping your nightmare."
            print "Once outside, you see lights flashing, blue and red. It's the police. You suddenly remember all the gory details of last night."
            print "It was you."
            print "You're a terrible person and will rot in prison."
            house.is_playing = False

        else:
            print "The door as a padlock on it. It is oddly locked from the inside."


class Remote(Item):

    def __init__(self, house):
        self.house = house
        self.player = house.player

    def check(self):
        house.rooms[2][2].items["car"].is_saw_video = True
        print "The TV turns on. It is a first person recording of what seems to be a brutal murder in the house. The details seem vaguely familiar."
        print "The scene cuts to a scene in the garage where the recorder is stuffing body parts into the car and tub. You see the house keys under the driver's seat."
        print "Another scene shows the person stashing a bloody axe, knives, and a chainsaw in the attic in the middle hallway. You wonder if they are still there."


class Car(Item):

    def __init__(self, player):
        self.player = player
        self.is_saw_video = False

    def check(self):
        print "After gagging at the foul oder, you see your other friends, Andrew and Danny. Or parts of them at least. The carpet is soaked in blood."

        if self.is_saw_video:
            self.player.items["house_key"] = True
            print "In addition, you find the house keys under the driver seat. You should probably leave the house as soon as possible."


class Attic(Item):
    def __init__(self, player):
        self.player = player

    def check(self):
        self.player.hp -= 1000
        print "Why on Earth did you open the attic?! The bloody murder axe falls down along with several knives."
        print "The axe lands directly in your head, and your last memory is you falling to the ground and blood squirting out of your head."
        print "No amount of Tylenol is going to help your headache."


# The main game class
class House:

    def __init__(self):
        self.player = Player()
        self.rooms = []
        self.is_playing = True

    def build_rooms(self):
        # shared items
        breaker_box = BreakerBox(self)
        stove = Stove(self.player)
        floor = Floor(self.player)

        kitchen = Room(name="Kitchen",
                       description="It is a dirty kitchen, with food spilled all over the floor and walls. The sound of bugs crawling is everywhere. The is an old stove on the wall. Knives lay on the floor." ,
                       doors={"north": False, "south": True, "east": False, "west": False},
                       items={"floor": floor, "knife": floor, "knives": floor, "stove": stove, "oven": stove})
        bathroom = Room(name="Bathroom",
                        description="The smell of feces and maggots fills the air. The smell appears to be coming from the toilet and tub.",
                        doors={"north": False, "south": True, "east": True, "west": False},
                        items={"toilet": DirtyToilet(self.player), "tub": BathTub(self.player)})
        laundry_room = Room(name="Laundry Room",
                            description="One wonders why there is even a laundry room here. All the clothes are soiled in shit and piss. The washer is plugged in.",
                            doors={"north": False, "south": False, "east": False, "west": True},
                            items={"washer": Washer(self.player, breaker_box)})
        hallway = Room(name="Hallway",
                       description="The end of the hallway. There is a broken window where it looks like someone jumped out. You peer out the window and see a dead body.",
                       doors={"north": True, "south": True, "east": True, "west": False},
                       items={})
        hallway2 = Room(name="Hallway",
                        description="The middle of a long and dark hallway. You can only see a few feet ahead due to cobwebs.",
                        doors={"north": True, "south": True, "east": True, "west": True},
                        items={"attic": Attic(self.player)})
        entrance = Room(name="Entrance",
                        description="You are standing in the doorway of the most disgusting house in the world. The door out is locked, perhaps we can find another way out.",
                        doors={"north": False, "south": True, "east": False, "west": True},
                        items={"door": FrontDoor(self)})
        kennys_room = Room(name="Kenny's Room",
                           description="The only clean room in the house. Emaculate. Filled with games and very comfy bed. ;) Though it is a bit dark. Perhaps you should turn on the lamp?",
                           doors={"north": True, "south": False, "east": False, "west": False},
                           items={"lamp": Lamp(), "dresser": Dresser(self.player), "bed": Bed(self.player)})
        living_room = Room(name="Living Room",
                           description="The living room is a swimming pool of beer cans. There is a nice tv but you can't find the remote.",
                           doors={"north": True, "south": False, "east": False, "west": False},
                           items={})
        garage = Room(name="Garage",
                      description="The garage has a broke down car in it. You can't see in because of what seems to be blood on the windows. There is also a breakerbox on the back wall",
                      doors={"north": True, "south": False, "east": False, "west": False},
                      items={"breaker": breaker_box, "breakerbox": breaker_box, "box": breaker_box, "puppy": Puppy(self), "car": Car(self.player)})

        self.rooms = [
            [kitchen, bathroom, laundry_room],
            [hallway, hallway2, entrance],
            [kennys_room, living_room, garage]
        ]


    def new_game(self):
        self.player = Player()

        # start in entrance
        self.player.y = 2
        self.player.x = 0

        self.build_rooms()
        self.is_playing = True
        print "Initializing new game"


    def describe_room(self):
        print self.get_current_room().description


    def print_room_name(self):
        print "You are in the " + self.get_current_room().name


    def get_current_room(self):
        return self.rooms[self.player.y][self.player.x]


    def handle_input(self):
        # get user input
        input = raw_input("Enter command: ")

        # decide what to do based on user input
        if input == "help" or input == "h":
            self.help()

        if input == "me" or input == "m":
            print "HP: " + str(self.player.hp)
            print "Your location: (" + str(self.player.x) + ", " + str(self.player.y) + ")"
            print "Doors: " + str(self.get_current_room().doors)
            print "Inventory: " + str(self.player.items)

        elif input == "describe" or input == "d":
            self.describe_room()

        elif input == "north" or input == "n":
            if self.get_current_room().doors["north"]:
                print "Walking North"
                self.player.y -= 1

            else:
                print "There is no door in that direction"

        elif input == "south" or input == "s":
            if self.get_current_room().doors["south"]:
                print "Walking South"
                self.player.y += 1

            else:
                print "There is no door in that direction"

        elif input == "west" or input == "w":
            if self.get_current_room().doors["west"]:
                print "Walking West"
                self.player.x -= 1

            else:
                print "There is no door in that direction"

        elif input == "east" or input == "e":
            if self.get_current_room().doors["east"]:
                print "Walking East"
                self.player.x += 1

            else:
                print "There is no door in that direction"

        # command syntax is "check <item_name>" or "c <item_name>"
        elif input.startswith("check ") or input.startswith("c "):
            pieces = input.split(" ")
            item_name = pieces[1]  # 0th item is "check or c" the 1st item is the item name
            self.get_current_room().check(item_name)

        elif input == "exit":
            self.is_playing = False

        else:
            print "Unknown command [" + input + "]"
            self.help()


    # print out help/commands
    def help(self):
        print "No help for you"


    def play(self):
        self.new_game()

        print "Starting game"
        print "You wake up from what was the most drunk, wild party of your life."
        print "Your last memory was playing Dungeons & Dragons but it seemed awfully real."
        while self.is_playing:
            self.print_room_name()
            self.handle_input()

            if not self.player.is_alive():
                print "You are dead"
                self.is_playing = False

        print "Exiting game"
        exit()


# start game
house = House()
house.play()
