import tkinter as tk
from tkinter import ttk
from classes.game import Bcolours, Person
from classes.magic import Spell
from classes.inventory import Item
from time import sleep


# region "Interface class"
class Interface:
    def __init__(self, game_obj):
        self.game_obj = game_obj
        self.player_choice = 0
        self.menu_level = 0
        self.animation_progress = False
        self.running = True

        self.btn_tl = ttk.Button(root, style="TButton", text="Melee", command=lambda: self.get_choice(1))
        self.btn_tl.grid(column=0, row=5)

        self.btn_tr = ttk.Button(root, style="TButton", text="Magic", command=lambda: self.get_choice(2))
        self.btn_tr.grid(column=1, row=5)

        self.btn_l = ttk.Button(root, style="TButton", text="Items", command=lambda: self.get_choice(3))
        self.btn_l.grid(column=0, row=6)

        self.btn_r = ttk.Button(root, style="TButton", command=lambda: self.get_choice(4))
        self.btn_r.grid(column=1, row=6)

        self.btn_bl = ttk.Button(root, style="TButton", command=lambda: self.get_choice(5))
        self.btn_bl.grid(column=0, row=7)

        self.btn_br = ttk.Button(root, style="TButton", command=lambda: self.get_choice(6))
        self.btn_br.grid(column=1, row=7)

    def display_menu(self):
        self.menu_level = 0
        self.btn_tl.configure(text="Melee")
        self.btn_tr.configure(text="Magic")
        self.btn_l.configure(text="Items")
        self.btn_r.configure(text="")
        self.btn_bl.configure(text="")
        self.btn_br.configure(text="")

    def display_magic(self):
        self.menu_level = 1
        self.btn_tl.configure(text="Go back")
        self.btn_tr.configure(text="Fire")
        self.btn_l.configure(text="Ice")
        self.btn_r.configure(text="Quake")
        self.btn_bl.configure(text="Lighting")
        self.btn_br.configure(text="Heal")

    def display_items(self):
        self.menu_level = 2
        self.btn_tl.configure(text="Go back")
        self.btn_tr.configure(text="Potion (x" + str(self.game_obj.player.items[0]["quantity"]) + ")")
        self.btn_l.configure(text="Hi-Potion (x" + str(self.game_obj.player.items[1]["quantity"]) + ")")
        self.btn_r.configure(text="elixir (x" + str(self.game_obj.player.items[2]["quantity"]) + ")")
        self.btn_bl.configure(text="Splash elixir (x" + str(self.game_obj.player.items[3]["quantity"]) + ")")
        self.btn_br.configure(text="Bomb (x" + str(self.game_obj.player.items[4]["quantity"]) + ")")

    def get_choice(self, i):
        if self.running:
            self.player_choice = i
            if self.menu_level == 0:
                self.choose_action()
            elif self.menu_level == 1:
                self.choose_magic()
            elif self.menu_level == 2:
                self.choose_item()

    def choose_action(self):
        if self.player_choice == 1:
            dmg = self.game_obj.player.generate_damage()
            self.game_obj.enemy.take_damage(dmg)
            self.player_attack_anim()
            self.update_health(self.game_obj.enemy)
            self.check_health(self.game_obj.enemy)
            self.enemy_attack()
        elif self.player_choice == 2:
            self.display_magic()
        elif self.player_choice == 3:
            self.display_items()

    def choose_magic(self):
        magic_dmg = 0

        if self.player_choice == 1:
            self.display_menu()
            return
        elif self.player_choice == 6:
            self.game_obj.player.heal(self.game_obj.heal.dmg)
            spell_cost = self.game_obj.player.magic[4].cost
        else:
            magic_dmg = self.game_obj.player.magic[self.player_choice - 2].generate_spell_damage()
            spell_cost = self.game_obj.player.magic[self.player_choice - 2].cost
            name = self.game_obj.player.magic[self.player_choice - 2].name
            self.magic_animation(name)

        self.game_obj.player.reduce_mp(spell_cost)
        self.update_mp()
        self.game_obj.enemy.take_damage(magic_dmg)
        self.update_health(self.game_obj.enemy)

        self.check_health(self.game_obj.enemy)
        self.enemy_attack()

    def choose_item(self):
        if self.player_choice == 1:
            self.display_menu()
            return
        else:
            item = self.game_obj.player.items[self.player_choice - 2]["item"]
            if self.game_obj.player.items[self.player_choice - 2]["quantity"] > 0:
                dmg = item.prop
                if item.type == "potion":
                    self.game_obj.player.heal(dmg)
                    print(self.game_obj.player.get_hp())
                elif item.type == "elixir":
                    self.game_obj.player.mp += dmg
                    print(self.game_obj.player.get_mp())
                elif item.type == "attack":
                    self.game_obj.enemy.take_damage(dmg)
                    self.update_health(self.game_obj.enemy)
                    self.check_health(self.game_obj.enemy)

                self.game_obj.player.items[self.player_choice - 2]["quantity"] -= 1
            else:
                pass

        self.enemy_attack()

    def enemy_attack(self):
        if self.game_obj.enemy.get_hp() > 0:
            enemy_dmg = self.game_obj.enemy.generate_damage()
            self.enemy_attack_anim()
            self.game_obj.player.take_damage(enemy_dmg)
            self.update_health(self.game_obj.player)
            self.check_health(self.game_obj.player)
        else:
            pass

    def update_health(self, character):
        hp = character.get_hp()
        max_hp = character.get_maxhp()
        if character == self.game_obj.player:
            health['value'] = hp
            health_lbl.configure(text="Player HP:" + str(hp) + "/" + str(max_hp))
            health.update()
        else:
            enemy_health['value'] = hp / 2.5  # this makes the enemy hp(250) equal to 100% of the progress bar
            enemy_health_lbl.configure(text="Enemy HP:" + str(hp) + "/" + str(max_hp))
            enemy_health.update()

    def update_mp(self):
        mp = self.game_obj.player.get_mp()
        max_mp = self.game_obj.player.get_maxmp()

        magic_points['value'] = mp
        mp_lbl.configure(text="Player MP:" + str(mp) + "/" + str(max_mp))

    def player_attack_anim(self):
        if not self.animation_progress:
            self.animation_progress = True
            canvas.move(sprite, 450, 0)
            canvas.update()
            sleep(0.3)
            canvas.move(sprite, -450, 0)
            canvas.update()
            self.animation_progress = False
        else:
            pass

    def enemy_attack_anim(self):
        if not self.animation_progress:
            sleep(1)
            canvas.move(boss, -450, 0)
            canvas.update()
            sleep(0.3)
            canvas.move(boss, 450, 0)
            canvas.update()
        else:
            pass

    def check_health(self, character):
        hp = character.get_hp()
        if character == self.game_obj.enemy:
            if hp == 0:
                canvas.create_image(200, 100, image=win_pic, anchor=tk.NW)
                self.running = False
                canvas.delete(boss)
        elif character == self.game_obj.player:
            if hp == 0:
                canvas.create_image(200, 100, image=lose_pic, anchor=tk.NW)
                self.running = False
                canvas.delete(sprite)

    def magic_animation(self, name):
        x1 = 225
        x2 = 675
        spell = canvas.create_rectangle(x1, 215, x1 + 15, 235, fill="red")
        if name == "Fire":
            spell = canvas.create_image(x1, 215, image=fire_pic, anchor=tk.NW)
        elif name == "Ice":
            # insert ice picture
            pass
        elif name == "Lightning":
            spell = canvas.create_image(x1, 215, image=lightning_pic, anchor=tk.NW)
        elif name == "Quake":
            # insert quake animation
            pass
        canvas.update()
        sleep(0.1)
        while x1 <= x2:
            if x1 == x2:
                canvas.delete(spell)
            else:
                canvas.move(spell, 30, 0)
                canvas.update()
                sleep(0.05)
            x1 += 30

# endregion


class Setup:
    def __init__(self):
        # Create Black spells
        self.fire = Spell("Fire", 10, 50, "black", Bcolours.FAIL)
        self.ice = Spell("Ice", 15, 70, "black", Bcolours.OKBLUE)
        self.quake = Spell("Quake", 8, 30, "black", Bcolours.BROWN)
        self.lightning = Spell("Lightning", 25, 125, "black", Bcolours.PURPLE)

        # Create White spells
        self.heal = Spell("Heal", 10, 50, "white", Bcolours.YELLOW)
        self.mega = Spell("Mega Heal", 20, 100, "white", Bcolours.LIGHT_CYAN)

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

        # Instantiate Player and enemy
        self.player = Person(100, 100, 25, 50, self.player_spells, self.player_items)
        self.enemy = Person(250, 20, 33, 0, [self.fire, self.quake, self.heal], [])


game = Setup()
valid = False
game_modes = [1, 2]
mode_select = 0

while not valid:
    try:
        # int() already strips whitespace
        mode_select = int(input("Select a mode in which you would like to play?:\n1: Text-based\n2: Graphical\n"))
    except ValueError as e:
        print("Invalid input Try Again")
        continue

    if mode_select in game_modes:
        valid = True
    else:
        print("Invalid game mode Try Again")

if mode_select == 1:
    running = True

    print(Bcolours.FAIL + Bcolours.BOLD + 'AN ENEMY ATTACKS!' + Bcolours.ENDC)

    while running:
        print("=================================")
        game.player.choose_action()
        choice = input("Choose action: ")
        try:
            index = int(choice) - 1
        except ValueError as e:
            continue

        print("You chose", game.player.get_action_name(index))

        if index == 0:
            dmg = game.player.generate_damage()
            game.enemy.take_damage(dmg)
        elif index == 1:
            game.player.choose_magic_spell()
            try:
                magic_choice = int(input("Choose spell: ")) - 1
            except ValueError as e:
                continue

            if magic_choice == -1:
                continue

            magic_dmg = game.player.magic[magic_choice].generate_spell_damage()
            spell = game.player.magic[magic_choice]

            current_mp = game.player.get_mp()

            if spell.cost > current_mp:
                print(Bcolours.FAIL + "Not enough MP" + Bcolours.ENDC)
                continue

            game.player.reduce_mp(spell.cost)

            if spell.type == "black":
                game.enemy.take_damage(magic_dmg)
                print(spell.colour + "\n" + spell.name + " deals", str(magic_dmg) + " points of damage" + Bcolours.ENDC)
            elif spell.type == "white":
                game.player.heal(magic_dmg)
                print(spell.colour + "\n" + spell.name + " heals", str(magic_dmg) + " HP" + Bcolours.ENDC)

        elif index == 2:
            game.player.choose_item()
            try:
                item_choice = int(input("Choose Item: ")) - 1
            except ValueError as e:
                continue

            if item_choice == -1:
                continue

            item = game.player.items[item_choice]["item"]

            if game.player.items[item_choice]["quantity"] == 0:
                print(Bcolours.FAIL + "DAMMIT I ran out" + Bcolours.ENDC)
                continue

            game.player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                game.player.heal(item.prop)
                print(Bcolours.OKGREEN + "Player heals for " + str(item.prop) + " HP" + Bcolours.ENDC)

            elif item.type == "elixir":
                game.player.mp = game.player.maxmp
                print(Bcolours.OKGREEN + "Fully restored player MP" + Bcolours.ENDC)

            elif item.type == "attack":
                game.enemy.take_damage(item.prop)
                print(item.name, "deals " + str(item.prop) + " points of damage")

        enemy_choice = 1
        enemy_dmg = game.enemy.generate_damage()
        game.player.take_damage(enemy_dmg)
        print("Enemy attacks for:", enemy_dmg)
        print("--------------------")

        print("Enemy Health: " + Bcolours.FAIL + str(game.enemy.get_hp()) + "/"
              + str(game.enemy.get_maxhp()) + Bcolours.ENDC)
        print("Your Health: " + Bcolours.OKGREEN + str(game.player.get_hp()) + "/"
              + str(game.player.get_maxhp()) + Bcolours.ENDC)
        print("Your MP" + Bcolours.OKBLUE + str(game.player.get_mp()) + "/"
              + str(game.player.get_maxmp()) + Bcolours.ENDC)

        if game.enemy.get_hp() == 0:
            print(Bcolours.BOLD + Bcolours.OKGREEN + "CONGRATS You defeated the enemy :)" + Bcolours.ENDC)
            running = False
        elif game.player.get_hp() == 0:
            print(Bcolours.BOLD + Bcolours.FAIL + "YOU DIED!" + Bcolours.ENDC)
            running = False


elif mode_select == 2:
    root = tk.Tk()
    root.geometry("805x650")
    root.title("Dungeon Quest")
    root.configure(bg="darkgrey")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
    style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
    style.configure("blue.Horizontal.TProgressbar", foreground='blue', background='blue')

    style.configure('TButton',
                    font=('calibri', 10),
                    borderwidth='4',
                    background="#002366",
                    foreground="white",
                    height=4, width=54)

    style.map('TButton',
              foreground=[('active', 'white')],
              background=[('active', "#021A44")])

    # region "canvas + buttons"
    canvas = tk.Canvas(root, width=800, height=350, bg="red")
    canvas.grid(column=0, row=0, columnspan=2)
    dir = "docs/assets/"
    background = tk.PhotoImage(file=dir+"back.png")
    sprite_pic = tk.PhotoImage(file=dir+"player.png")
    boss_pic = tk.PhotoImage(file=dir+"orc.png")
    fire_pic = tk.PhotoImage(file=dir+"fire.png")
    lightning_pic = tk.PhotoImage(file=dir+"lightning2.png")
    win_pic = tk.PhotoImage(file=dir+"WIN.png")
    lose_pic = tk.PhotoImage(file=dir+"LOSE.png")
    canvas.create_image(2, 0, image=background, anchor=tk.NW)

    boss = canvas.create_image(600, 100, image=boss_pic, anchor=tk.NW)
    sprite = canvas.create_image(100, 175, image=sprite_pic, anchor=tk.NW)

    health = ttk.Progressbar(root, style="green.Horizontal.TProgressbar",
                             orient=tk.HORIZONTAL, length=100, mode="determinate")
    health['value'] = 100
    health.grid(column=0, row=2, sticky=tk.W)
    health_lbl = tk.Label(root, text="Player HP:" + str(game.player.get_hp()) + "/" + str(game.player.get_maxhp()))
    health_lbl.grid(column=0, row=1, sticky=tk.W)

    magic_points = ttk.Progressbar(root, style="blue.Horizontal.TProgressbar",
                                   orient=tk.HORIZONTAL, length=100, mode="determinate")
    magic_points['value'] = 100
    magic_points.grid(column=0, row=4, sticky=tk.W)
    mp_lbl = tk.Label(root, text="Player MP:" + str(game.player.get_mp()) + "/" + str(game.player.get_maxmp()))
    mp_lbl.grid(column=0, row=3, sticky=tk.W)

    enemy_health = ttk.Progressbar(root, style="red.Horizontal.TProgressbar",
                                   orient=tk.HORIZONTAL, length=250, mode="determinate")
    enemy_health['value'] = 250
    enemy_health.grid(column=1, row=2, sticky=tk.E)
    enemy_health_lbl = tk.Label(root, text="Enemy HP:" + str(game.enemy.get_hp()) + "/" + str(game.enemy.get_maxhp()))
    enemy_health_lbl.grid(column=1, row=1, sticky=tk.E)

    buttons = Interface(game)
    # endregion

    root.mainloop()
