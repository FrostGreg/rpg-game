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

        self.win_pic = tk.PhotoImage(file=self.game.dir + "WIN.png")
        self.lose_pic = tk.PhotoImage(file=self.game.dir + "LOSE.png")
        self.fire_pic = tk.PhotoImage(file=self.game.dir + "fire.png")
        self.lightning_pic = tk.PhotoImage(file=self.game.dir + "lightning2.png")

        self.background = tk.PhotoImage(file=self.game.dir + "back.png")
        self.sprite_pic = tk.PhotoImage(file=self.game.dir + "player.png")
        self.boss_pic = tk.PhotoImage(file=self.game.dir + "orc.png")
        self.sprite = self.boss = None

        self.btn_tl = ttk.Button(self.root, style="TButton", text="Melee", command=lambda: self.get_choice(1))
        self.btn_tl.grid(column=0, row=5)

        self.btn_tr = ttk.Button(self.root, style="TButton", text="Magic", command=lambda: self.get_choice(2))
        self.btn_tr.grid(column=1, row=5)

        self.btn_l = ttk.Button(self.root, style="TButton", text="Items", command=lambda: self.get_choice(3))
        self.btn_l.grid(column=0, row=6)

        self.btn_r = ttk.Button(self.root, style="TButton", command=lambda: self.get_choice(4))
        self.btn_r.grid(column=1, row=6)

        self.btn_bl = ttk.Button(self.root, style="TButton", command=lambda: self.get_choice(5))
        self.btn_bl.grid(column=0, row=7)

        self.btn_br = ttk.Button(self.root, style="TButton", command=lambda: self.get_choice(6))
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
        self.btn_tr.configure(text="Potion (x" + str(self.game.player.items[0]["quantity"]) + ")")
        self.btn_l.configure(text="Hi-Potion (x" + str(self.game.player.items[1]["quantity"]) + ")")
        self.btn_r.configure(text="elixir (x" + str(self.game.player.items[2]["quantity"]) + ")")
        self.btn_bl.configure(text="Splash elixir (x" + str(self.game.player.items[3]["quantity"]) + ")")
        self.btn_br.configure(text="Bomb (x" + str(self.game.player.items[4]["quantity"]) + ")")

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
            dmg = self.game.player.generate_damage()
            self.game.enemy.take_damage(dmg)
            self.player_attack_anim()
            self.update_health(self.game.enemy)
            self.check_health(self.game.enemy)
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
            self.game.player.heal(self.game.heal.dmg)
            spell_cost = self.game.player.magic[4].cost
        else:
            magic_dmg = self.game.player.magic[self.player_choice - 2].generate_spell_damage()
            spell_cost = self.game.player.magic[self.player_choice - 2].cost
            name = self.game.player.magic[self.player_choice - 2].name
            self.magic_animation(name)

        self.game.player.reduce_mp(spell_cost)
        self.update_mp()
        self.game.enemy.take_damage(magic_dmg)
        self.update_health(self.game.enemy)

        self.check_health(self.game.enemy)
        self.enemy_attack()

    def choose_item(self):
        if self.player_choice == 1:
            self.display_menu()
            return
        else:
            item = self.game.player.items[self.player_choice - 2]["item"]
            if self.game.player.items[self.player_choice - 2]["quantity"] > 0:
                dmg = item.prop
                if item.form == "potion":
                    self.game.player.heal(dmg)
                    print(self.game.player.get_hp())
                elif item.form == "elixir":
                    self.game.player.mp += dmg
                    print(self.game.player.get_mp())
                elif item.form == "attack":
                    self.game.enemy.take_damage(dmg)
                    self.update_health(self.game.enemy)
                    self.check_health(self.game.enemy)

                self.game.player.items[self.player_choice - 2]["quantity"] -= 1
            else:
                pass

        self.enemy_attack()

    def enemy_attack(self):
        if self.game.enemy.get_hp() > 0:
            enemy_dmg = self.game.enemy.generate_damage()
            self.enemy_attack_anim()
            self.game.player.take_damage(enemy_dmg)
            self.update_health(self.game.player)
            self.check_health(self.game.player)
        else:
            pass

    def update_health(self, character):
        hp = character.get_hp()
        max_hp = character.get_max_hp()
        if character == self.game.player:
            self.health['value'] = hp
            self.health_lbl.configure(text="Player HP:" + str(hp) + "/" + str(max_hp))
            self.health.update()
        else:
            self.enemy_health['value'] = hp / 2.5  # this makes the enemy hp(250) equal to 100% of the progress bar
            self.enemy_health_lbl.configure(text="Enemy HP:" + str(hp) + "/" + str(max_hp))
            self.enemy_health.update()

    def update_mp(self):
        mp = self.game.player.get_mp()
        max_mp = self.game.player.get_max_mp()

        self.magic_points['value'] = mp
        self.mp_lbl.configure(text="Player MP:" + str(mp) + "/" + str(max_mp))

    def player_attack_anim(self):
        if not self.animation_progress:
            self.animation_progress = True
            self.canvas.move(self.sprite, 450, 0)
            self.canvas.update()
            sleep(0.3)
            self.canvas.move(self.sprite, -450, 0)
            self.canvas.update()
            self.animation_progress = False
        else:
            pass

    def enemy_attack_anim(self):
        if not self.animation_progress:
            sleep(1)
            self.canvas.move(self.boss, -450, 0)
            self.canvas.update()
            sleep(0.3)
            self.canvas.move(self.boss, 450, 0)
            self.canvas.update()
        else:
            pass

    def check_health(self, character):
        hp = character.get_hp()
        if character == self.game.enemy:
            if hp == 0:
                self.canvas.create_image(200, 100, image=self.win_pic, anchor=tk.NW)
                self.running = False
                self.canvas.delete(self.boss)
        elif character == self.game.player:
            if hp == 0:
                self.canvas.create_image(200, 100, image=self.lose_pic, anchor=tk.NW)
                self.running = False
                self.canvas.delete(self.sprite)

    def magic_animation(self, name):
        x1 = 225
        x2 = 675
        spell = self.canvas.create_rectangle(x1, 215, x1 + 15, 235, fill="red")
        if name == "Fire":
            spell = self.canvas.create_image(x1, 215, image=self.fire_pic, anchor=tk.NW)
        elif name == "Ice":
            # insert ice picture
            pass
        elif name == "Lightning":
            spell = self.canvas.create_image(x1, 215, image=self.lightning_pic, anchor=tk.NW)
        elif name == "Quake":
            # insert quake animation
            pass
        self.canvas.update()
        sleep(0.1)
        while x1 <= x2:
            if x1 == x2:
                self.canvas.delete(spell)
            else:
                self.canvas.move(spell, 30, 0)
                self.canvas.update()
                sleep(0.05)
            x1 += 30

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

        # region "canvas + buttons"

        self.canvas.grid(column=0, row=0, columnspan=2)

        self.canvas.create_image(2, 0, image=self.background, anchor=tk.NW)

        self.sprite = self.canvas.create_image(100, 175, image=self.sprite_pic, anchor=tk.NW)
        self.boss = self.canvas.create_image(600, 100, image=self.boss_pic, anchor=tk.NW)

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
