import tkinter as tk
from tkinter import ttk
from time import sleep


class Interface:
    def __init__(self, game_obj, root, health, enemy_health, style, canvas, mp_lbl, health_lbl, enemy_health_lbl,
                 magic_points, sprite, boss, win_pic, lose_pic, fire_pic, lightning_pic):

        self.root = root
        self.health = health
        self.enemy_health = enemy_health
        self.style = style
        self.canvas = canvas
        self.mp_lbl = mp_lbl
        self.health_lbl = health_lbl
        self.enemy_health_lbl = enemy_health_lbl
        self.magic_points = magic_points
        self.sprite = sprite
        self.boss = boss
        self.win_pic = win_pic
        self.lose_pic = lose_pic
        self.fire_pic = fire_pic
        self.lightning_pic = lightning_pic

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
                if item.form == "potion":
                    self.game_obj.player.heal(dmg)
                    print(self.game_obj.player.get_hp())
                elif item.form == "elixir":
                    self.game_obj.player.mp += dmg
                    print(self.game_obj.player.get_mp())
                elif item.form == "attack":
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
        max_hp = character.get_max_hp()
        if character == self.game_obj.player:
            self.health['value'] = hp
            self.health_lbl.configure(text="Player HP:" + str(hp) + "/" + str(max_hp))
            self.health.update()
        else:
            self.enemy_health['value'] = hp / 2.5  # this makes the enemy hp(250) equal to 100% of the progress bar
            self.enemy_health_lbl.configure(text="Enemy HP:" + str(hp) + "/" + str(max_hp))
            self.enemy_health.update()

    def update_mp(self):
        mp = self.game_obj.player.get_mp()
        max_mp = self.game_obj.player.get_max_mp()

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
        if character == self.game_obj.enemy:
            if hp == 0:
                self.canvas.create_image(200, 100, image=self.win_pic, anchor=tk.NW)
                self.running = False
                self.canvas.delete(self.boss)
        elif character == self.game_obj.player:
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
