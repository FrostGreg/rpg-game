import random
from .colours import Colours


class Person:
    def __init__(self, hp, mp, atk, df, magic, items, graphic=None):
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atk_high = atk + 10
        self.atk_low = atk - 10
        self.df = df
        self.magic = magic
        self.items = items
        self.action = ["Attack", "Magic", "Items"]
        self.graphic = graphic

    def generate_damage(self):
        return random.randrange(self.atk_low, self.atk_high)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp

    def reduce_mp(self, cost):
        self.mp -= cost

    def get_action_name(self, i):
        return self.action[i]

    def choose_action(self):
        i = 1
        print(Colours.BOLD + Colours.HEADER + "ACTIONS" + Colours.ENDC)
        print("---------------------")
        for item in self.action:
            print("    " + str(i) + ": " + item)
            i += 1

    def choose_magic_spell(self):
        i = 1
        print("---------------------------------")
        print(Colours.BOLD + Colours.HEADER + "SPELLS" + Colours.ENDC)
        print("---------------------------------")
        print("    0: Back to menu")
        for spell in self.magic:
            print("    " + str(i) + ": " + spell.colour + spell.name + Colours.ENDC,
                  "(cost : " + str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("---------------------------------")
        print(Colours.BOLD + Colours.HEADER + "ITEMS" + Colours.ENDC)
        print("---------------------------------")
        print("    0: Back to menu")
        for item in self.items:
            print("    " + str(i) + ": " + item["item"].name + "(" + item["item"].description + ")" + "[x" +
                  str(item["quantity"]) + "]")
            i += 1
