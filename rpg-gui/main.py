import tkinter as tk
from tkinter import ttk
from time import sleep
from classes.game import Person
from classes.magic import Spell
from classes.inventory import Item


class Interface:
    def __init__(self):
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
        self.btn_tr.configure(text="Potion (x" + str(player.items[0]["quantity"]) + ")")
        self.btn_l.configure(text="Hi-Potion (x" + str(player.items[1]["quantity"]) + ")")
        self.btn_r.configure(text="Elixer (x" + str(player.items[2]["quantity"]) + ")")
        self.btn_bl.configure(text="Splash Elixer (x" + str(player.items[3]["quantity"]) + ")")
        self.btn_br.configure(text="Bomb (x" + str(player.items[4]["quantity"]) + ")")

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
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            self.player_attack_anim()
            self.update_health(enemy)
            self.check_health(enemy)
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
            player.heal(heal.dmg)
            spell_cost = player.magic[4].cost
        else:
            magic_dmg = player.magic[self.player_choice - 2].generate_spell_damage()
            spell_cost = player.magic[self.player_choice - 2].cost
            name = player.magic[self.player_choice - 2].name
            self.magic_animation(name)

        player.reduce_mp(spell_cost)
        self.update_mp()
        enemy.take_damage(magic_dmg)
        self.update_health(enemy)

        self.check_health(enemy)
        self.enemy_attack()

    def choose_item(self):
        if self.player_choice == 1:
            self.display_menu()
            return
        else:
            item = player.items[self.player_choice - 2]["item"]
            if player.items[self.player_choice - 2]["quantity"] > 0:
                dmg = item.prop
                if item.type == "potion":
                    player.heal(dmg)
                    print(player.get_hp())
                elif item.type == "elixer":
                    player.mp += dmg
                    print(player.get_mp())
                elif item.type == "attack":
                    enemy.take_damage(dmg)
                    self.update_health(enemy)
                    self.check_health(enemy)

                player.items[self.player_choice - 2]["quantity"] -= 1
            else:
                pass

        self.enemy_attack()

    def enemy_attack(self):
        if enemy.get_hp() > 0:
            enemy_dmg = enemy.generate_damage()
            self.enemy_attack_anim()
            player.take_damage(enemy_dmg)
            self.update_health(player)
            self.check_health(player)
        else:
            pass

    def update_health(self, character):
        hp = character.get_hp()
        max_hp = character.get_maxhp()
        if character == player:
            health['value'] = hp
            health_lbl.configure(text="Player HP:" + str(hp) + "/" + str(max_hp))
            health.update()
        else:
            enemy_health['value'] = hp / 2.5  # this makes the enemy hp(250) equal to 100% of the progress bar
            enemy_health_lbl.configure(text="Enemy HP:" + str(hp) + "/" + str(max_hp))
            enemy_health.update()

    def update_mp(self):
        mp = player.get_mp()
        max_mp = player.get_maxmp()

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
            canvas.move(boss, -400, 0)
            canvas.update()
            sleep(0.3)
            canvas.move(boss, 400, 0)
            canvas.update()
        else:
            pass

    def check_health(self, character):
        hp = character.get_hp()
        if character == enemy:
            if hp == 0:
                canvas.create_image(200, 100, image=win_pic, anchor=tk.NW)
                self.running = False
                canvas.delete(boss)
        elif character == player:
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

        # spell = canvas.create_rectangle(675, 215, 690, 235, fill="red")


# Create Black spells
fire = Spell("Fire", 10, 50, "black")
ice = Spell("Ice", 15, 70, "black")
quake = Spell("Quake", 8, 30, "black")
lighting = Spell("Lightning", 25, 125, "black")


# Create White spell
heal = Spell("Heal", 20, 100, "white")


# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
elixer = Item("Elixer", "elixer", "Fully restores MP", 9999)
splashelixer = Item("Splash Elixer", "elixer", "Fully restores MP for all party members", 9999)

bomb = Item("Bomb", "attack", "Deals 250 damage to all enemies", 250)

player_spells = [fire, ice, quake, lighting, heal]
player_items = [{"item": potion, "quantity": 5},
                {"item": hipotion, "quantity": 1},
                {"item": elixer, "quantity": 3},
                {"item": splashelixer, "quantity": 1},
                {"item": bomb, "quantity": 3}]

# Instantiate Player and enemy
player = Person(100, 100, 25, 50, player_spells, player_items)
enemy = Person(250, 20, 33, 0, [fire, quake, heal], [])

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

background = tk.PhotoImage(file="assets/back.png")
sprite_pic = tk.PhotoImage(file="assets/player.png")
boss_pic = tk.PhotoImage(file="assets/orc.png")
fire_pic = tk.PhotoImage(file="assets/fire.png")
lightning_pic = tk.PhotoImage(file="assets/lightning2.png")
win_pic = tk.PhotoImage(file="assets/WIN.png")
lose_pic = tk.PhotoImage(file="assets/LOSE.png")
canvas.create_image(2, 0, image=background, anchor=tk.NW)

boss = canvas.create_image(600, 100, image=boss_pic, anchor=tk.NW)
sprite = canvas.create_image(100, 175, image=sprite_pic, anchor=tk.NW)


health = ttk.Progressbar(root, style="green.Horizontal.TProgressbar",
                         orient=tk.HORIZONTAL, length=100, mode="determinate")
health['value'] = 100
health.grid(column=0, row=2, sticky=tk.W)
health_lbl = tk.Label(root, text="Player HP:" + str(player.get_hp()) + "/" + str(player.get_maxhp()))
health_lbl.grid(column=0, row=1, sticky=tk.W)

magic_points = ttk.Progressbar(root, style="blue.Horizontal.TProgressbar",
                               orient=tk.HORIZONTAL, length=100, mode="determinate")
magic_points['value'] = 100
magic_points.grid(column=0, row=4, sticky=tk.W)
mp_lbl = tk.Label(root, text="Player MP:" + str(player.get_mp()) + "/" + str(player.get_maxmp()))
mp_lbl.grid(column=0, row=3, sticky=tk.W)

enemy_health = ttk.Progressbar(root, style="red.Horizontal.TProgressbar",
                               orient=tk.HORIZONTAL, length=250, mode="determinate")
enemy_health['value'] = 250
enemy_health.grid(column=1, row=2, sticky=tk.E)
enemy_health_lbl = tk.Label(root, text="Enemy HP:" + str(enemy.get_hp()) + "/" + str(enemy.get_maxhp()))
enemy_health_lbl.grid(column=1, row=1, sticky=tk.E)

buttons = Interface()
# endregion


root.mainloop()
