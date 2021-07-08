import random


class Spell:
    def __init__(self, name, cost, dmg, form, colour, graphic=None):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.form = form
        self.colour = colour
        self.graphic = graphic

    def get_graphic(self):
        return self.graphic

    def generate_spell_damage(self):
        high = self.dmg + 15
        low = self.dmg - 15
        return random.randrange(low, high)
