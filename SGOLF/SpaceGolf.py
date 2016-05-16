"""Space Golf Version 0.03 (Added SFX)
Programmer: Anthony Waterman
Project Start Date: 12/15/2015
Project Build Date: 2/18/2016
"""
from tkinter import *
from tkinter import ttk
from math import *
import functools
import os
import time
import winsound

class Hole: 
    def __init__(self, no_planets, spawn_x, spawn_y, hole_x, hole_y, par):
        self.no_planets = no_planets
        self.planets = []
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.hole_x = hole_x
        self.hole_y = hole_y
        self.hole_size = 25
        self.hole_gravity = -4
        self.bound_x = 1500
        self.bound_y = 800
        self.par = par

class Planet:
    def __init__(self, size, x, y):
        self.size = size 
        self.loc_x = x
        self.loc_y = y
        self.gravity = -4    
        
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.stroke = 0
        self.size = 5
        self.initial_x = 0
        self.initial_y = 0
        self.loc_x = 0
        self.loc_y = 0
        self.vel_x = 0
        self.vel_y = 0
        self.power = 50
        self.angle = 0
        self.controls = 0
        self.score = [0,0,0,0,0,0,0,0,0]

class Homescreen:
    def __init__(self, master):
        master.title("Space Golf")
        master.resizable(FALSE, FALSE)
        s = ttk.Style()
        s.theme_use("vista")
        f = Frame(master, width = 40, bg = "firebrick2", padx = 4, pady = 4)
        f.pack()
        
        self.label1 = Label(
            f, text = "Welcome to Space Golf v0.02!",
            fg = "white", bg = "firebrick2")
        self.label1.pack()
        
        self.label2 = Label(f, text = "How many players?", bg = "firebrick2")
        self.label2.pack()
        
        self.no_players = Scale(
            f, from_ = 1, to = 8, orient = HORIZONTAL, bg = "darkorange1")
        self.no_players.pack()
        
        self.label3 = Label(f, text = "Select a course", bg = "firebrick2")
        self.label3.pack()
        
        self.selected_course = StringVar()
        self.courselist = os.listdir("Courses")  # Courses folder
        self.courses = ttk.Combobox(
            f, width = 38, textvariable = self.selected_course, 
            values = self.courselist, state = "readonly")
        self.courses.current(0)
        self.courses.pack()

        self.player_select = Button(
            f, text = "Name & Ball Select", command = self.name_ball, 
            bg = "darkorange1", pady = 4)
        self.player_select.pack()
        
        # Lists needed for added widgets
        self.pf = []
        self.pname = []
        self.plabel = []
        self.pballcolor = []     
        self.holes = []
        
        
    def name_ball(self):
        """Dynamically show players based on number selected
        
        :param Homescreen self: Homescreen object stores all the current
        players, course, hole information 

        :return: None
        """
        self.num_players = int(self.no_players.get())
        self.no_players.config(state = DISABLED)
        self.courses.config(state = DISABLED)
        self.player_select.config(state = DISABLED)
        self.f2 = Frame(width = 40, bg = "firebrick2", padx = 4, pady = 4)
        self.f2.pack()
        for i in range(self.num_players):
            self.pf.append(Frame(
                self.f2, relief = RAISED, width = 40, 
                pady = 4, borderwidth = 4))
            self.plabel.append(Label(
                self.pf[i], text = "Player #" + str(i + 1) + "'s name:"))
            self.pname.append(Entry(self.pf[i], width = 40))
            self.pballcolor.append(Spinbox(
                self.pf[i], width = 20, state = "readonly", bg = "firebrick2",
                wrap = 1, justify = CENTER,
                command = functools.partial(self.color_change, k = i), 
                values=(
                    "blue", "red", "green", "yellow",
                    "orange", "white", "purple", "brown")))
            self.pf[i].config(bg = str(self.pballcolor[i].get()))
            self.plabel[i].config(bg = str(self.pballcolor[i].get()))
            self.plabel[i].pack()
            self.pname[i].pack()
            self.pballcolor[i].pack()
            self.pf[i].pack()            
        self.bback = Button(
            self.f2, text = "Go Back", command = self.go_back, 
            bg = "darkorange1", pady = 4, fg = "white")
        self.bback.pack(side = LEFT)
        self.bgame = Button(
            self.f2, text = "Start Game", command = self.start_game,
            bg = "darkorange1", pady = 4)
        self.bgame.pack(side = RIGHT)
    
    def color_change(self, k):
        """Dynamically change label color based on color selected
        
        :param Homescreen self: Homescreen object stores all the current
        players, course, hole information 

        :return: None
        """
        self.pf[k].config(bg=self.pballcolor[k].get())
        self.plabel[k].config(bg=self.pballcolor[k].get())
        
        
    def go_back(self):
        """Destroys player name and color select options and re-enables 
        previous menu options
        
        :param Homescreen self: Homescreen object stores all the current
        players, course, hole information 

        :return: None
        """
        for i in range(self.num_players):
            self.pf[i].destroy()
            self.plabel[i].destroy()
            self.pname[i].destroy()
            self.pballcolor[i].destroy()
        self.bback.destroy()
        self.bgame.destroy()
        self.f2.destroy()
        self.pf = []
        self.pname = []
        self.plabel = []
        self.pballcolor = []   
        self.no_players.config(state=ACTIVE)
        self.courses.config(state=ACTIVE)
        self.player_select.config(state=ACTIVE)        

    
    def start_game(self):
        """Initialize game window, canvas, and starting hole information
        
        :param Homescreen self: Homescreen object stores all the current
        players, course, hole information 

        :return: None
        """
        print("Players:", self.num_players) 
        print("Course:", self.selected_course.get())
        self.players = []
        self.playerball = []
        for i in range(self.num_players):
            self.players.append(Player(
                self.pname[i].get(), self.pballcolor[i].get()))
            if(self.players[i].name == ""):  # Sets player name if none entered
                self.players[i].name = "Player " + str(i+1)
            self.playerball.append(None)  # Placeholder for ball display
        self.gamewindow = Toplevel()
        self.gamewindow.title("It's an adventure in space...")
        self.current_hole = 1
        self.holes = []        
        self.course_file = open("Courses/" + self.selected_course.get())
        self.current_player = 0

        #Control Key-Bindings
        self.gamewindow.bind("<Up>", self.power_up)
        self.gamewindow.bind("<Down>", self.power_down)
        self.gamewindow.bind("<Left>", self.angle_up)
        self.gamewindow.bind("<Right>", self.angle_down)
        self.gamewindow.bind("<space>", self.shoot)
        self.gamewindow.bind("r", self.reset_ball)       

        # Displaying the game
        self.canv = Canvas(
            self.gamewindow, width = 1500, height = 800, bg = "black")
        self.canv.pack()
        bkg = PhotoImage(file = "images/starbg.gif")
        self.canv.background = bkg
        self.canv.create_image(750, 400, image = bkg)
        self.load_hole(self.current_hole)
        self.disp_planets = []
        self.display_hole(self.current_hole)
        self.current_player = 0 #1st player always starts hole
        print("Hole:", self.current_hole)
        print("Par:", self.holes[self.current_hole-1].par)
        self.gameplay()

        
    def load_hole(self, h):
        """Loads hole information from course file
        
        :param Homescreen self: Homescreen object stores all the current
        players, course, hole information 
        :param int h: Integer of hole to be loaded
        
        :return: None
        """        
        while self.course_file.readline()!="hole " + str(h) + "\n":
            pass  # searching for correct hole
        tempstr = self.course_file.readline().split() #  Hole Info
        self.holes.append(Hole(
            int(tempstr[0]), int(tempstr[1]), int(tempstr[2]),
            int(tempstr[3]), int(tempstr[4]), int(tempstr[5])))
        for i in range(0, self.holes[h - 1].no_planets, 1):  # Planet Info
            tempstr = self.course_file.readline().split()
            self.holes[h-1].planets.append(Planet(
                int(tempstr[0]), int(tempstr[1]), int(tempstr[2])))


    def display_hole(self, h):
        """Display hole information on canvas
        
        :param Homescreen self: Homescreen object stores all the current
        players, course, hole information 
        :param int h: Integer of hole to be displayed

        :return: None
        """        
        planet_colors = ["DarkGoldenrod2", "DeepSkyBlue3", "maroon",
            "dark orchid", "OliveDrab2", "seashell2", "thistle3",
            "RosyBrown3", "tomato2", "khaki"]
        self.disp_planets = []
        j = 0  # Secondary LCV for planet colors
        for i in self.holes[h - 1].planets:
            j+=1
            self.disp_planets.append(self.canv.create_oval(
                i.loc_x - i.size,
                i.loc_y - i.size,
                i.loc_x + i.size,
                i.loc_y + i.size,
                fill = planet_colors[j % 10], outline = "cyan"))
        black_hole = PhotoImage(file = "images/blackhole.gif")
        self.canv.image = black_hole
        self.canv.create_image(
            self.holes[h - 1].hole_x, 
            self.holes[h - 1].hole_y,
            image = black_hole)

            
    #Aiming, Power, Shooting Events        
    def power_up(self, event):
        """Increase player's current shot's power
        
        :param Homescreen self: Homescreen object stores all the current
        players, course, hole information 
        :param Event event: Calling event 

        :return: None
        """      
        cp = self.players[self.current_player]
        if cp.controls == 0:
            return
        if cp.power < 100:
            cp.power += 1
        self.canv.coords(
            self.reticle, cp.loc_x, cp.loc_y, 
            cp.loc_x + cp.power * cos(radians(cp.angle)),
            cp.loc_y - cp.power * sin(radians(cp.angle)))
        
    def power_down(self, event):
        """Decrease player's current shot's power
        
        :param Homescreen self: Homescreen object stores all the current
        players, course, hole information 
        :param Event event: Calling event 

        :return: None
        """      
        cp = self.players[self.current_player]
        if cp.controls == 0:
            return
        if cp.power > 1:
            cp.power -= 1
        self.canv.coords(
            self.reticle, cp.loc_x, cp.loc_y, 
            cp.loc_x + cp.power * cos(radians(cp.angle)),
            cp.loc_y - cp.power * sin(radians(cp.angle)))
            
    def angle_up(self, event):
        """Increase player's current shot's angle
        
        :param Homescreen self: Homescreen object stores all the current
        players, course, hole information 
        :param Event event: Calling event 

        :return: None
        """    
        cp = self.players[self.current_player]
        if cp.controls == 0:
            return
        if cp.angle == 359:
            cp.angle = 0        
        else: 
            cp.angle += 1
        self.canv.coords(
            self.reticle, cp.loc_x, cp.loc_y, 
            cp.loc_x + cp.power * cos(radians(cp.angle)),
            cp.loc_y - cp.power * sin(radians(cp.angle)))
            
    def angle_down(self, event):
        """Decrease player's current shot's angle
        
        :param Homescreen self: Homescreen object stores all the current
        players, course, hole information 
        :param Event event: Calling event 

        :return: None
        """    
        cp = self.players[self.current_player]
        if cp.controls == 0:
            return
        if cp.angle == 0:
            cp.angle = 359        
        else:
            cp.angle -= 1
        self.canv.coords(
            self.reticle, cp.loc_x, cp.loc_y, 
            cp.loc_x + cp.power * cos(radians(cp.angle)),
            cp.loc_y - cp.power * sin(radians(cp.angle)))

    def reset_ball(self, event):
        """Reset player's ball back to previous position
        
        :param Homescreen self: Homescreen object stores all the current
        players, course, hole information 
        :param Event event: Calling event 

        :return: None
        """    
        cp = self.players[self.current_player]
        if cp.controls == 1:
            return
        self.moving = False
        cp.vel_x = 0
        cp.vel_y = 0
        cp.loc_x = cp.initial_x
        cp.loc_y = cp.initial_y
        self.canv.coords(
            self.playerball[self.current_player], 
            cp.loc_x - cp.size, 
            cp.loc_y - cp.size,
            cp.loc_x + cp.size,
            cp.loc_y + cp.size,)
        self.canv.update()
        
    def shoot(self, event):
        """Shoot the player's ball, loop until ball stops moving, proceed to
        next player
        
        :param Homescreen self: Homescreen object stores all the current
        players, course, hole information 
        :param Event event: Calling event 

        :return: None
        """    
        cp = self.players[self.current_player]
        ch = self.holes[self.current_hole-1]
        if cp.controls == 0:
            self.timer_delay = 0  # Skips to shot at rest
            return
        self.sfx('golf')
        self.canv.delete(self.reticle)
        self.timer_delay = .05
        cp.initial_x = cp.loc_x  # Save initial position
        cp.initial_y = cp.loc_y  
        cp.vel_x = cos(radians(cp.angle)) * cp.power
        cp.vel_y = sin(radians(cp.angle)) * cp.power * -1  # Y axis is reversed
        cp.controls = 0
        self.moving = True
        friction = .5  # Const percentage of velocity to continue after bounce
        bnc = 1  # Decrementing percntage of velocity to continue after bounces
        
        # Physics loop:  while ball is moving
        while self.moving: 
            acc_x = 0
            acc_y = 0
            # Effects of each planet on ball
            for i in ch.planets: 
                distance = sqrt(
                    ((cp.loc_x - i.loc_x)**2) + ((cp.loc_y - i.loc_y)**2))
                dist_x = cp.loc_x - i.loc_x
                dist_y = cp.loc_y - i.loc_y
                current_vel = sqrt((cp.vel_x ** 2) + (cp.vel_y ** 2))
                # Inside gravity field for planet
                if distance < 3 * i.size and distance >= i.size:
                    gravity_factor = ((3 * i.size) - distance) / (2 * i.size) 
                    acc_x += gravity_factor * i.gravity * (dist_x) / distance
                    acc_y += gravity_factor * i.gravity * (dist_y) / distance
                # Hitting planet surface and slow 
                if distance <= i.size and current_vel < 5:
                    self.moving = False
                    cp.vel_x = 0
                    cp.vel_y = 0
                    self.sfx('rest')
                    break
                # Hitting planet surface but not slow enough to stop
                elif distance <= i.size:
                    if dist_x == 0:
                        cp.vel_y = friction * bnc * abs(cp.vel_y) * (
                            abs(dist_y) / dist_y)
                        cp.vel_x = friction * cp.vel_x * bnc
                        bnc -= .01  # Decrements ensure the ball will stop
                        self.sfx('bounce')
                    elif dist_y == 0:
                        cp.vel_x = friction * bnc * abs(cp.vel_x) * (
                            abs(dist_x) / dist_x)
                        cp.vel_y = friction * cp.vel_y * bnc
                        bnc -= .01
                        self.sfx('bounce')
                    else:
                        """Trig equations to use a set of secondary axes that 
                        are perpindicular / parallel to the planets surface.
                        """
                        theta = atan2(dist_x, dist_y)
                        vel_out = cp.vel_x * sin(theta) + cp.vel_y * cos(theta)
                        if vel_out < 0:
                            self.sfx('bounce')
                            vel_para = friction * (
                                cp.vel_x * cos(theta) - cp.vel_y * sin(theta))
                            vel_perp = friction * abs(vel_out)  
                            cp.vel_x = (
                                bnc * (
                                (vel_para * cos(theta)) + 
                                (vel_perp * sin(theta))))
                            cp.vel_y =(
                                bnc * (
                                (vel_para * sin(theta) * -1) +  # Neg y-axis
                                (vel_perp * cos(theta))))
                            bnc -= .01
            # Effects of hole on ball
            distance = sqrt(
                ((cp.loc_x - ch.hole_x)**2) + ((cp.loc_y - ch.hole_y)**2))
            if distance < 2 * ch.hole_size: 
                gravity_factor = ((2 * ch.hole_size) - distance) / ch.hole_size 
                acc_x = (
                    gravity_factor * ch.hole_gravity * 
                    (cp.loc_x - ch.hole_x) / distance)
                acc_y = (
                    gravity_factor * ch.hole_gravity * 
                    (cp.loc_y - ch.hole_y) / distance)
                if distance < ch.hole_size:  # Ball in hole
                    acc_x = 0
                    acc_y = 0
                    cp.vel_x = 0
                    cp.vel_y = 0
                    self.moving = False
                    self.sfx('clap')
            
            # Finalize velocity, position
            cp.vel_x += acc_x
            cp.vel_y += acc_y
            cp.loc_x += cp.vel_x * .2  # .2 value normalizes velocity
            cp.loc_y += cp.vel_y * .2
            
            # Tests if ball is out of bounds
            if (int(cp.loc_x) not in range(ch.bound_x) or 
                int(cp.loc_y) not in range(ch.bound_y)):
                self.moving = False
                cp.vel_x = 0
                cp.vel_y = 0
                cp.loc_x = cp.initial_x
                cp.loc_y = cp.initial_y
                self.sfx('fail')
            
            # Update display of ball
            time.sleep(self.timer_delay)
            self.canv.coords(self.playerball[self.current_player], 
                cp.loc_x - cp.size, 
                cp.loc_y - cp.size,
                cp.loc_x + cp.size,
                cp.loc_y + cp.size,)
            self.canv.update()
        
        # Score
        if distance < ch.hole_size:
            cp.score[self.current_hole-1] = cp.stroke
            print("Score:", cp.stroke)
            cp.stroke = 0
        
        # Player change
        if self.current_player == self.num_players - 1: 
            self.current_player = 0
        else:
            self.current_player += 1
        
        # Next shot
        self.gameplay()
        
    def gameplay(self):
        """Checks if all players have finished the hole, if not it gives 
        control to the current player. If the current player has scored, 
        the next player is selected and this function is called again.
        
        :param Homescreen self: Homescreen object stores all the current
        players, course, hole information 

        :return: None
        """            
        cp = self.players[self.current_player]
        finished = True  # Default value before check
        for i in self.players:  # If everyone is finished move to next hole
            if i.score[self.current_hole-1] == 0:
                finished = False
                break
        else:
            self.canv.destroy()
            if self.current_hole <= 9:  # Proceed to next hole
                time.sleep(2)
                self.sfx('laser')
                self.canv = Canvas(
                    self.gamewindow, width = 1500, height = 800, bg = "black")
                self.canv.pack()
                bkg = PhotoImage(file = "images/starbg.gif")
                self.canv.background = bkg
                self.canv.create_image(750, 400, image = bkg)
                self.current_hole += 1
                self.load_hole(self.current_hole)
                self.disp_planets.clear()
                self.display_hole(self.current_hole)
                self.current_player = 0  # 1st player always starts hole
                print("Hole:", self.current_hole)
                print("Par:", self.holes[self.current_hole-1].par)
                self.gameplay()
            else:  # All holes are finished
                for i in self.players:  # final scoreboard and cleanup        
                    print(i.name, ":", i.score)
                self.gamewindow.destroy()
                return
        
        # If player has scored, continue to next player
        if cp.score[self.current_hole-1] == 0 and not finished:
            if cp.stroke == 0:  # Spawn player
                cp.loc_x = self.holes[self.current_hole-1].spawn_x
                cp.loc_y = self.holes[self.current_hole-1].spawn_y
                self.playerball[self.current_player] = self.canv.create_oval(
                    cp.loc_x - cp.size, cp.loc_y - cp.size,
                    cp.loc_x + cp.size, cp.loc_y + cp.size,
                    fill = cp.color, outline = "gray")
            cp.stroke += 1
            cp.controls = 1  # player can control power/angle               
            self.reticle = self.canv.create_line(
                cp.loc_x, cp.loc_y, 
                cp.loc_x + cp.power * cos(radians(cp.angle)), 
                cp.loc_y - cp.power * sin(radians(cp.angle)), 
                arrow = LAST ,fill = "white", dash = (1, 1))
            print("Stroke:", cp.stroke)
        elif not finished:
            if self.current_player == self.num_players - 1:  # Player change
                self.current_player = 0
            else:
                self.current_player += 1
            self.gameplay()

            
    def sfx(self, sound):
        """Play a sound effect
        
        :param Homescreen self: Homescreen object stores all the current
        players, course, hole information 
        :param string sound: name of sound to play
        
        :return: None 
        """
        if sound == 'bounce':
            winsound.PlaySound('sounds/bounce.wav', winsound.SND_ASYNC)
        elif sound == 'rest':
            winsound.PlaySound('sounds/rest.wav', winsound.SND_ASYNC)
        elif sound == 'fail':
            winsound.PlaySound('sounds/fail.wav', winsound.SND_ASYNC)
        elif sound == 'laser':
            winsound.PlaySound('sounds/laser.wav', winsound.SND_ASYNC)
        elif sound == 'golf':
            winsound.PlaySound('sounds/golf.wav', winsound.SND_ASYNC)
        elif sound == 'clap':
            winsound.PlaySound('sounds/clap.wav', winsound.SND_ASYNC)
        else:
            print("Invalid sound name")

root = Tk()

hs = Homescreen(root)

root.mainloop()


