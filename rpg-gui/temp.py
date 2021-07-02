from tkinter import *
import random
import math
import time

class Game():

    # This __init__ will run first when you run Game()
    # Learn to always set up your programs this way.
    def __init__(self):

        test = random.randint(10,40)
        print(test)

        # Put self. before the name of every variable you might want to use outside this __init__ function.
        # this way you don't need to define them separately in every function

        # You defined these xs and ys by hand so of course it remains in the same position.
        # define them randomly and you'll be fine.
        self.fx0 = 20
        self.fy0 = 20
        self.fx1 = test + 20
        self.fy1 = test + 20
        self.x0 = -50
        self.y0 = -50
        self.x1 = 50
        self.y1 = 50
        self.speed = 1
        self.mouseX0 = 0
        self.mouseY0 = 0
        self.mouseX1 = 0
        self.mouseY1 = 0
        self.debug = "DEBUGGED"

        # Added these two variables
        self.tick_intervals = 10
        self.food_exists = True

        self.module = Tk()

        #Game is the name of your class don't use it here: (use game instead)
        self.game = Canvas(self.module, width=1000, height=1000)
        self.Player = self.game.create_oval(self.x0,self.y0,self.x1,self.y1,fill="blue")
        self.Food = self.game.create_oval(self.fx0, self.fy0, self.fx1, self.fy1, fill="red")
        self.rayCast = self.game.create_line(self.x0,self.y0,self.mouseX1,self.mouseY1)
        self.frayCast = self.game.create_line(self.x0,self.y0,self.mouseX1,self.mouseY1)
        self.game.pack()
        self.move()
        self.module.mainloop()


    def move(self):
        # To get mouse position on your whole screen: .winfo_pointerx() and .winfo_pointery()
        # To get position of widget (self.game) on screen .winfo_rootx()
        # x and y below are the same as mouse event.x and event.y without the need to bind anything to self.module
        x = self.game.winfo_pointerx()-self.game.winfo_rootx()
        y = self.game.winfo_pointery()-self.game.winfo_rooty()

        # If you have a value you use more than 1 time,
        # it's best to define it first then put that here
        # instead of writing it out every time.
        # this way you can change it very easily
        # better define these in __init__ function with self.something = ...
        self.mouseX0 = x - 10 # define var for 10
        self.mouseY0 = y - 10
        self.mouseX1 = x + 10
        self.mouseY1 = y + 10

        # You should also design a (visible or invisible) wall around the screen
        # so your Player and Food can't run off the screen.
        # Basically it's numbers and some if statements.

        # If you don't put elif here x and y might get resized then resized again.
        # but you only need to resize them once a tick.
        # You don't need != here. < > are enough.
        # Look up += -= *= /= functions.
        if self.x0 < self.mouseX0:
            self.x0 += self.speed
            self.x1 += self.speed
        elif self.x0 > self.mouseX0:
            self.x0 -= self.speed
            self.x1 -= self.speed
        if self.y0 < self.mouseY0:
            self.y0 += self.speed
            self.y1 += self.speed
        elif self.y0 > self.mouseY0:
            self.y0 -= self.speed
            self.y1 -= self.speed

        # Need to call these once a tick and not every time you change x or y
        self.game.coords(self.rayCast, self.x0, self.y0, self.mouseX1, self.mouseY1)
        self.game.coords(self.Player,self.x0,self.y0,self.x1,self.y1)

        # After you eat food this shouldn't run any more.
        # This is why Player kept getting bigger and bigger
        if self.food_exists:
            if self.fx0 > self.x0 and (self.fx0 - self.x0) < 20: # define var for 20
                self.fx0 += 0.5 # define var for 0.5
                self.fx1 += 0.5
            elif self.fx0 < self.x0 and (self.fx0 + self.x0) < 20:
                self.fx0 -= 0.5
                self.fx1 -= 0.5
            if self.fy0 > self.y0 and (self.fy0 - self.y0) < 20:
                self.fy0 += 0.5
                self.fy1 += 0.5
            elif self.fy0 < self.y0 and (self.fy0 - self.y0) < 20:
                self.fy0 -= 0.5
                self.fy1 -= 0.5
            if self.fx0 > self.x0 and (self.fx0 - self.x0) < 5: # define var for 5
                if self.fy0 > self.y0 and (self.fy0 - self.y0) <5:
                    self.game.delete(self.Food)
                    self.x0 -= self.fx1
                    self.y0 -= self.fy1
                    self.food_exists = False
            self.game.coords(self.Food,self.fx0,self.fy0,self.fx1,self.fy1)
            self.game.coords(self.frayCast, self.x0,self.y0, self.fx0,self.fy0)

        # This automatically runs self.move after (self.tick_intevals) miliseconds
        self.game.after(self.tick_intervals,self.move)

# This IF runs the Game() only if you run the script yourself.
# This way if you imported this script into another program it wouldn't run Game()
# Learn to always use this if for your programs
if __name__=='__main__':
    Game()