import random


class Spell:
    def __init__(self, name, cost, dmg, type, colour):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.type = type
        self.colour = colour

    def generate_spell_damage(self):
        high = self.dmg + 15
        low = self.dmg - 15
        return random.randrange(low, high)
