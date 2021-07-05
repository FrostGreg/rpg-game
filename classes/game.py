import random
from .magic import Spell


class Bcolours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BROWN = "\033[0;33m"
    YELLOW = "\033[1;33m"
    PURPLE = "\033[0;35m"
    LIGHT_CYAN = "\033[1;36m"
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, hp, mp, atk, df, magic, items):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkh = atk + 10
        self.atkl = atk - 10
        self.df = df
        self.magic = magic
        self.items = items
        self.action = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp
        return self.hp

    def get_hp(self):
        return self.hp

    def get_maxhp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_maxmp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def get_action_name(self, i):
        return self.action[i]

    def choose_action(self):
        i = 1
        print(Bcolours.BOLD + Bcolours.HEADER + "ACTIONS" + Bcolours.ENDC)
        print("---------------------")
        for item in self.action:
            print("    " + str(i) + ": " + item)
            i += 1

    def choose_magic_spell(self):
        i = 1
        print("---------------------------------")
        print(Bcolours.BOLD + Bcolours.HEADER + "SPELLS" + Bcolours.ENDC)
        print("---------------------------------")
        print("    0: Back to menu")
        for spell in self.magic:
            print("    " + str(i) + ": " + spell.colour + spell.name + Bcolours.ENDC,
                  "(cost : " + str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("---------------------------------")
        print(Bcolours.BOLD + Bcolours.HEADER + "ITEMS" + Bcolours.ENDC)
        print("---------------------------------")
        print("    0: Back to menu")
        for item in self.items:
            print("    " + str(i) + ": " + item["item"].name + "(" + item["item"].description + ")" + "[x" +
                  str(item["quantity"]) + "]")
            i += 1
