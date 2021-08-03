import tkinter as tk
from tkinter import ttk
from time import sleep


class Interface:
    def __init__(self, game):
        self.game = game
        self.player_choice = 0
        self.menu_level = 0
        self.animation_progress = False
        self.running = True

        self.root = tk.Tk()
        self.health = ttk.Progressbar(self.root, style="green.Horizontal.TProgressbar",
                                      orient=tk.HORIZONTAL, length=100, mode="determinate")
        self.enemy_health = ttk.Progressbar(self.root, style="red.Horizontal.TProgressbar",
                                            orient=tk.HORIZONTAL, length=250, mode="determinate")
        self.style = ttk.Style()
        self.canvas = tk.Canvas(self.root, width=800, height=350, bg="red")
        self.mp_lbl = tk.Label(self.root,
                               text="Player MP:" + str(self.game.player.get_mp()) + "/" + str(
                                   self.game.player.get_max_mp()))
        self.health_lbl = tk.Label(self.root, text="Player HP:" + str(self.game.player.get_hp()) + "/"
                                                   + str(self.game.player.get_max_hp()))
        self.enemy_health_lbl = tk.Label(self.root,
                                         text="Enemy HP:" + str(self.game.enemy.get_hp()) + "/" + str(
                                             self.game.enemy.get_max_hp()))
        self.magic_points = ttk.Progressbar(self.root, style="blue.Horizontal.TProgressbar",
                                            orient=tk.HORIZONTAL, length=100, mode="determinate")

        self.background = tk.PhotoImage(file=self.game.dir + "back.png")
        self.sprite_pic = tk.PhotoImage(file=self.game.dir + "player.png")
        self.boss_pic = tk.PhotoImage(file=self.game.dir + "orc.png")
        self.win_pic = tk.PhotoImage(file=self.game.dir + "WIN.png")
        self.lose_pic = tk.PhotoImage(file=self.game.dir + "LOSE.png")

        self.canvas.create_image(2, 0, image=self.background, anchor=tk.NW)
        self.sprite = self.canvas.create_image(100, 175, image=self.sprite_pic, anchor=tk.NW)
        self.boss = self.canvas.create_image(600, 100, image=self.boss_pic, anchor=tk.NW)

        self.entity_hp_lbls = {game.player: self.health_lbl, game.enemy: self.enemy_health_lbl}
        self.entity_mp_lbls = {game.player: self.mp_lbl}
        self.entity_hp_bars = {game.player: self.health, game.enemy: self.enemy_health}
        self.entity_mp_bars = {game.player: self.magic_points}
        self.entity_graphics = {game.player: self.sprite, game.enemy: self.boss}

        self.menu = ["Melee", "Magic", "Items", "", "", ""]
        self.buttons = []

        for i in range(6):
            self.buttons.append(
                ttk.Button(self.root, style="TButton", text=self.menu[i]))
            self.buttons[i].grid(column=i % 2, row=5 + (i // 2))

        self.buttons[0].configure(command=lambda: self.get_choice(1))
        self.buttons[1].configure(command=lambda: self.get_choice(2))
        self.buttons[2].configure(command=lambda: self.get_choice(3))
        self.buttons[3].configure(command=lambda: self.get_choice(4))
        self.buttons[4].configure(command=lambda: self.get_choice(5))
        self.buttons[5].configure(command=lambda: self.get_choice(6))

    def update_btns(self, labels, menu_level):
        self.menu_level = menu_level
        for i in range(len(self.buttons)):
            self.buttons[i].configure(text=labels[i])

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
            self.attack(self.game.player, self.game.enemy)
        elif self.player_choice == 2:
            self.update_btns(["Go Back", "Fire", "Ice", "Quake", "Lightning", "Heal"], 1)
        elif self.player_choice == 3:
            self.update_btns(["Go Back", "Potion (x" + str(self.game.get_item_quantity(0)) + ")",
                              "Hi-Potion (x" + str(self.game.get_item_quantity(1)) + ")",
                              "elixir (x" + str(self.game.get_item_quantity(2)) + ")",
                              "Splash elixir (x" + str(self.game.get_item_quantity(3)) + ")",
                              "Bomb (x" + str(self.game.get_item_quantity(4)) + ")"], 2)

    def choose_magic(self):
        magic_dmg = 0

        if self.player_choice == 1:
            self.update_btns(self.menu, 0)
            return
        elif self.player_choice == 6:
            self.game.player.heal(self.game.heal.dmg)
            spell_cost = self.game.player.magic[4].cost
        else:
            magic_dmg = self.game.player.magic[self.player_choice - 2].generate_spell_damage()
            spell_cost = self.game.player.magic[self.player_choice - 2].cost
            self.magic_animation(self.game.player.magic[self.player_choice - 2])

        self.game.player.reduce_mp(spell_cost)
        self.game.enemy.take_damage(magic_dmg)
        self.update_stats()

        self.check_health()
        self.attack(self.game.enemy, self.game.player)

    def choose_item(self):
        if self.player_choice == 1:
            self.update_btns(self.menu, 0)
            return

        item = self.game.player.items[self.player_choice - 2]["item"]
        if self.game.player.items[self.player_choice - 2]["quantity"] > 0:
            dmg = item.prop
            if item.form == "potion":
                self.game.player.heal(dmg)
            elif item.form == "elixir":
                self.game.player.mp += dmg
                if self.game.player.mp > self.game.player.get_max_mp():
                    self.game.player.mp = self.game.player.get_max_mp()
            elif item.form == "attack":
                self.game.enemy.take_damage(dmg)

            self.update_stats()
            self.check_health()
            self.game.player.items[self.player_choice - 2]["quantity"] -= 1
            self.buttons[self.player_choice - 1].configure(
                text=item.name + "(x" + str(self.game.get_item_quantity(self.player_choice - 2)) + ")")

        self.attack(self.game.enemy, self.game.player)

    def attack(self, src, target):
        if src == target:
            return

        if src.get_hp() > 0:
            dmg = src.generate_damage()
            self.melee_anim(src)
            target.take_damage(dmg)
            self.update_stats()
            self.check_health()

            if src.get_team() == "good":
                if target.get_hp() > 0:
                    self.attack(target, src)

    def update_stats(self):
        for player in self.game.entities:
            hp = player.get_hp()
            max_hp = player.get_max_hp()
            mp = player.get_mp()
            max_mp = player.get_max_mp()

            if player in self.entity_hp_lbls:
                self.entity_hp_lbls[player].configure(text="Player HP:" + str(hp) + "/" + str(max_hp))
                self.entity_hp_bars[player]['value'] = hp / (max_hp / 100)
                self.entity_hp_bars[player].update()

            if player in self.entity_mp_lbls:
                self.entity_mp_lbls[player].configure(text="MP:" + str(mp) + "/" + str(max_mp))
                self.entity_mp_bars[player]['value'] = mp / (max_mp / 100)
                self.entity_mp_bars[player].update()

    def check_health(self):
        for character in self.game.entities:
            hp = character.get_hp()
            if hp <= 0:
                if character.get_team() == "evil":
                    img = self.win_pic
                    dead = self.boss
                else:
                    img = self.lose_pic
                    dead = self.sprite

                self.running = False
                self.canvas.create_image(200, 100, image=img, anchor=tk.NW)
                self.canvas.delete(dead)
                self.canvas.update()
                break

    def melee_anim(self, character):
        movement = 450
        if character.get_team() == "evil":
            movement = -450

        graphic = self.entity_graphics[character]
        if not self.animation_progress:
            sleep(0.1)
            self.animation_progress = True
            self.canvas.move(graphic, movement, 0)
            self.canvas.update()
            sleep(0.3)
            self.canvas.move(graphic, -movement, 0)
            self.canvas.update()
            self.animation_progress = False

    def magic_animation(self, spell):
        start = 225
        end = 675
        speed = 30

        pic = spell.get_graphic()
        img = tk.PhotoImage(file=self.game.dir + "anim_default.png")
        if pic:
            img = tk.PhotoImage(file=self.game.dir + pic)

        animation = self.canvas.create_image(start, 215, image=img, anchor=tk.NW)

        while start <= end:
            self.canvas.update()
            self.canvas.move(animation, speed, 0)
            sleep(0.05)
            start += speed
        self.canvas.delete(animation)

    def run(self):
        self.root.geometry("805x650")
        self.root.title("Dungeon Quest")
        self.root.configure(bg="darkgrey")

        self.style.theme_use('clam')
        self.style.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        self.style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
        self.style.configure("blue.Horizontal.TProgressbar", foreground='blue', background='blue')

        self.style.configure('TButton',
                             font=('calibri', 10),
                             borderwidth='4',
                             background="#002366",
                             foreground="white",
                             height=4, width=54)

        self.style.map('TButton',
                       foreground=[('active', 'white')],
                       background=[('active', "#021A44")])

        self.canvas.grid(column=0, row=0, columnspan=2)

        self.health['value'] = 100
        self.health.grid(column=0, row=2, sticky=tk.W)
        self.health_lbl.grid(column=0, row=1, sticky=tk.W)

        self.magic_points['value'] = 100
        self.magic_points.grid(column=0, row=4, sticky=tk.W)
        self.mp_lbl.grid(column=0, row=3, sticky=tk.W)

        self.enemy_health['value'] = 250
        self.enemy_health.grid(column=1, row=2, sticky=tk.E)
        self.enemy_health_lbl.grid(column=1, row=1, sticky=tk.E)

        self.root.mainloop()
