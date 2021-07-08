import tkinter as tk
from tkinter import ttk
from classes.interface import Interface
from classes.game import Game

game = Game()
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
    game.run()

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
    background = tk.PhotoImage(file=dir + "back.png")
    sprite_pic = tk.PhotoImage(file=dir + "player.png")
    boss_pic = tk.PhotoImage(file=dir + "orc.png")
    fire_pic = tk.PhotoImage(file=dir + "fire.png")
    lightning_pic = tk.PhotoImage(file=dir + "lightning2.png")
    win_pic = tk.PhotoImage(file=dir + "WIN.png")
    lose_pic = tk.PhotoImage(file=dir + "LOSE.png")
    canvas.create_image(2, 0, image=background, anchor=tk.NW)

    boss = canvas.create_image(600, 100, image=boss_pic, anchor=tk.NW)
    sprite = canvas.create_image(100, 175, image=sprite_pic, anchor=tk.NW)

    health = ttk.Progressbar(root, style="green.Horizontal.TProgressbar",
                             orient=tk.HORIZONTAL, length=100, mode="determinate")
    health['value'] = 100
    health.grid(column=0, row=2, sticky=tk.W)
    health_lbl = tk.Label(root, text="Player HP:" + str(game.player.get_hp()) + "/" + str(game.player.get_max_hp()))
    health_lbl.grid(column=0, row=1, sticky=tk.W)

    magic_points = ttk.Progressbar(root, style="blue.Horizontal.TProgressbar",
                                   orient=tk.HORIZONTAL, length=100, mode="determinate")
    magic_points['value'] = 100
    magic_points.grid(column=0, row=4, sticky=tk.W)
    mp_lbl = tk.Label(root, text="Player MP:" + str(game.player.get_mp()) + "/" + str(game.player.get_max_mp()))
    mp_lbl.grid(column=0, row=3, sticky=tk.W)

    enemy_health = ttk.Progressbar(root, style="red.Horizontal.TProgressbar",
                                   orient=tk.HORIZONTAL, length=250, mode="determinate")
    enemy_health['value'] = 250
    enemy_health.grid(column=1, row=2, sticky=tk.E)
    enemy_health_lbl = tk.Label(root, text="Enemy HP:" + str(game.enemy.get_hp()) + "/" + str(game.enemy.get_max_hp()))
    enemy_health_lbl.grid(column=1, row=1, sticky=tk.E)

    buttons = Interface(game, root, health, enemy_health, style, canvas, mp_lbl, health_lbl, enemy_health_lbl,
                        magic_points, sprite, boss, win_pic, lose_pic, fire_pic, lightning_pic)
    # endregion

    root.mainloop()
