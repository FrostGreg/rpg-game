from .magic import Spell
from .colours import Colours
from .inventory import Item
from .person import Person


class Game:
    def __init__(self):
        # Create Black spells
        self.fire = Spell("Fire", 10, 50, "black", Colours.FAIL, "fire.png")
        self.ice = Spell("Ice", 15, 70, "black", Colours.OKBLUE)
        self.quake = Spell("Quake", 8, 30, "black", Colours.BROWN)
        self.lightning = Spell("Lightning", 25, 125, "black", Colours.PURPLE, "lightning.png")

        # Create White spells
        self.heal = Spell("Heal", 10, 50, "white", Colours.YELLOW)
        self.mega = Spell("Mega Heal", 20, 100, "white", Colours.LIGHT_CYAN)

        # Create Items
        self.potion = Item("Potion", "potion", "Heals 50 HP", 50)
        self.hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
        self.elixir = Item("elixir", "elixir", "Fully restores MP", 9999)
        self.splashelixir = Item("Splash elixir", "elixir", "Fully restores MP for all party members", 9999)

        self.bomb = Item("Bomb", "attack", "Deals 250 damage to all enemies", 250)

        self.player_spells = [self.fire, self.ice, self.quake, self.lightning, self.heal, self.mega]
        self.player_items = [{"item": self.potion, "quantity": 5},
                             {"item": self.hipotion, "quantity": 1},
                             {"item": self.elixir, "quantity": 3},
                             {"item": self.splashelixir, "quantity": 1},
                             {"item": self.bomb, "quantity": 3}]

        # Initiate Player and enemy
        self.player = Person(100, 100, 25, 50, self.player_spells, self.player_items, "good", "player.png")
        self.enemy = Person(250, 20, 33, 0, [self.fire, self.quake, self.heal], [], "evil", "orc.png")
        self.entities = [self.player, self.enemy]
        self.running = True
        self.dir = "docs/assets/"

    def get_item_quantity(self, item):
        return self.player_items[item]["quantity"]

    def run(self):
        running = True

        print(Colours.FAIL + Colours.BOLD + 'AN ENEMY ATTACKS!' + Colours.ENDC)

        while running:
            print("=================================")
            self.player.choose_action()
            choice = input("Choose action: ")
            try:
                index = int(choice) - 1
            except ValueError:
                continue

            print("You chose", self.player.get_action_name(index))

            if index == 0:
                dmg = self.player.generate_damage()
                self.enemy.take_damage(dmg)
            elif index == 1:
                self.player.choose_magic_spell()
                try:
                    magic_choice = int(input("Choose spell: ")) - 1
                except ValueError:
                    continue

                if magic_choice == -1:
                    continue

                magic_dmg = self.player.magic[magic_choice].generate_spell_damage()
                spell = self.player.magic[magic_choice]

                current_mp = self.player.get_mp()

                if spell.cost > current_mp:
                    print(Colours.FAIL + "Not enough MP" + Colours.ENDC)
                    continue

                self.player.reduce_mp(spell.cost)

                if spell.form == "black":
                    self.enemy.take_damage(magic_dmg)
                    print(spell.colour + "\n" + spell.name + " deals",
                          str(magic_dmg) + " points of damage" + Colours.ENDC)
                elif spell.form == "white":
                    self.player.heal(magic_dmg)
                    print(spell.colour + "\n" + spell.name + " heals", str(magic_dmg) + " HP" + Colours.ENDC)

            elif index == 2:
                self.player.choose_item()
                try:
                    item_choice = int(input("Choose Item: ")) - 1
                except ValueError:
                    continue

                if item_choice == -1:
                    continue

                item = self.player.items[item_choice]["item"]

                if self.player.items[item_choice]["quantity"] == 0:
                    print(Colours.FAIL + "DAMMIT I ran out" + Colours.ENDC)
                    continue

                self.player.items[item_choice]["quantity"] -= 1

                if item.form == "potion":
                    self.player.heal(item.prop)
                    print(Colours.OKGREEN + "Player heals for " + str(item.prop) + " HP" + Colours.ENDC)

                elif item.form == "elixir":
                    self.player.mp = self.player.max_mp
                    print(Colours.OKGREEN + "Fully restored player MP" + Colours.ENDC)

                elif item.form == "attack":
                    self.enemy.take_damage(item.prop)
                    print(item.name, "deals " + str(item.prop) + " points of damage")

            enemy_dmg = self.enemy.generate_damage()
            self.player.take_damage(enemy_dmg)
            print("Enemy attacks for:", enemy_dmg)
            print("--------------------")

            print("Enemy Health: " + Colours.FAIL + str(self.enemy.get_hp()) + "/"
                  + str(self.enemy.get_max_hp()) + Colours.ENDC)
            print("Your Health: " + Colours.OKGREEN + str(self.player.get_hp()) + "/"
                  + str(self.player.get_max_hp()) + Colours.ENDC)
            print("Your MP" + Colours.OKBLUE + str(self.player.get_mp()) + "/"
                  + str(self.player.get_max_mp()) + Colours.ENDC)

            if self.enemy.get_hp() == 0:
                print(Colours.BOLD + Colours.OKGREEN + "CONGRATS You defeated the enemy :)" + Colours.ENDC)
                running = False
            elif self.player.get_hp() == 0:
                print(Colours.BOLD + Colours.FAIL + "YOU DIED!" + Colours.ENDC)
                running = False
