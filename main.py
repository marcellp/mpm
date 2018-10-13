from IOStream import io
from Room import Room
from Entity import Entity, Human
from Item import Item, Weapon, Clothing
from Parser import Parser
import json
import pickle
import copy
import pprint


class Game(object):
    def __init__(self):
        self.parser = Parser(self)
        # self.assets #filled in load assets
        self.load_assets()
        self.load_rooms()

    def save_rooms(self):
        if not self.rooms:
            raise Exception("rooms not loaded boi")

        with open("rooms.bin", "wb") as rooms:
            pickle.dump(self.rooms, rooms)

    def load_rooms(self):
        with open("areas.json") as f:
            raw_file_data = json.load(f)
            room_dict = {}

            for room_data in raw_file_data:
                room = Room(room_data["name"], room_data["desc"])
                room.interior = room_data["interior"]
                room.items = room_data["items"]
                room.entities = [self.get_entity(entity) for entity in room_data["entities"]]
                print(room.entities)
                room.paths = room_data["exits"]

                room_dict[room_data["name"]] = room

            for room in room_dict.values():
                for path, exit in room.paths.items():
                    room.paths[path] = room_dict[exit]

            self.rooms = tuple([room for room in room_dict.values()])

    def load_assets(self):
        """read from json file parse to tuples as types, copy into rooms from here"""
        with open("weapons.json") as f:
            raw_file_data = json.load(f)
        weapons = tuple(Weapon(x) for x in raw_file_data)

        with open("clothing.json") as f:
            raw_file_data = json.load(f)
        clothing = tuple(Clothing(x) for x in raw_file_data)
        self.assets = clothing + weapons

        self.entities = {}

        with open("entites.json") as f:
            raw_file_data = json.load(f)

        for entity in raw_file_data:
            temp = Entity(name = entity["name"])
            for item in entity["inventory"]:
                temp.add_item(self.get_item(item))
            temp.equipped = entity["equipped"]

            self.entities[entity["name"]] = temp

    def create_character(self):
        while True:
            name = io.send_in('By what name should I call you? > ').strip()
            if name:
                break

        while True:
            sex = io.send_in("Okay, " + name + ", what is your sex? (male, female) > ").strip()

            if sex == "male" or sex == "female":
                break

        p = Human(name, sex, local_player=True)
        io.out("Good job, {}. To create your character, assign some skills to your character.\n".format(name))

        """
		Here be dragons.
		"""
        while True:
            assignable_points = Entity.MAX_SPECIAL_POINTS
            total_points = 0
            i = 1
            out_of = len(p.stats) - 1

            for stat in p.stats.keys():
                if stat == "level":
                    continue

                while True:
                    try:
                        points = io.send_in(
                            "[{}/{}] Assign points for {} (default: 5, minimum: 1, maximum: 10 {}/{} assigned). > ".format(
                                i, out_of, stat.upper(), total_points, assignable_points))
                        points = int(points)
                    except ValueError:
                        io.out("I'll take that as 5.")
                        points = 5

                    if points < 1 or points > 10:
                        io.out('Points must be between 1 and 10.')
                        continue

                    if total_points == assignable_points and i <= out_of:
                        break

                    if total_points + points > assignable_points:
                        io.out('You cannot assign this many points.')
                        continue

                    p.stats[stat] = points
                    total_points += points
                    i += 1
                    break

                if total_points == assignable_points and i <= out_of:
                    io.out('You used up your points a bit too fast there. Let us try again....\n')
                    break

            if i > out_of:
                break

        # Character stats created, let us put the character into the first available room.
        p.move_to(self.rooms[0])

        return p

    def get_item(self, searchStr):
        """looks in assets for the specified search key
			returns none if not found"""
        for item in self.assets:
            if searchStr == item.name:
                return copy.deepcopy(item)

    def get_entity(self, searchStr):
        """looks in assets for the specified search key
			returns none if not found"""
        
        entity = self.entities.get(searchStr)
        return copy.deepcopy(entity)

    def show_intro(self):
        with open("title.txt") as f:
            for line in f:
                print(line, end="")

            print("\n")

        with open("intro.txt") as f:
            for line in f:
                print(line, end="")
            print("\n")

    def run(self):
        self.show_intro()
        self.p = self.create_character()
        c = self.get_item("Kevlar vest")
        d = self.get_item("Baseball bat")
        self.p.add_item(c)
        self.p.add_item(d)

        io.out('')

        # Game loop
        self.p.at.describe(who_for=self.p)

        while True:
            words = io.send_in()
            self.parser.parse(words)


g = Game()

g.run()
