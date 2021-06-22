import pygame as pg3
import numpy as np
import keyboard as key
import json
from tqdm import tqdm
from pygame import gfxdraw, NOFRAME

#<--------------------------------------------------------------------------------->
load = True
rotate_switch = True
running = True

# these values are already defined in function draw defination

# size = (700, 700)
# position = (350,350)
# aqurcy = 100
# skip = 1
# file_path = "coordinate.txt"
# rotate_stop_key = "c"
# exit_key = "q"
#<--------------------------------------------------------------------------------->

def draw(size = (700, 700), 
         position = (350,350), 
         aqurcy = 100, 
         file_path = "coordinate.txt", 
         font_loc = "C:\Windows\Fonts\Arial.ttf",
         rotate_stop_key = "r", 
         exit_key = "q", 
         circle = True, 
         circle_radious = 1, 
         skip = 1):

    global running, load
    running = True
    load = True

    # pg3.init()
    pg3.display.set_caption("Arm drawing using FFT")
    screen = pg3.display.set_mode(size, 32)
    screen.fill((0, 0, 0))
    medium_font = pg3.font.Font(font_loc,20)
    loading_text = medium_font.render('Currently calculating Arms.....' , True , (0,255,255))
    screen.blit(loading_text,(0,0))
    pg3.display.flip()
    trail = pg3.Surface(size)
    epicircle = pg3.Surface(size)

    def FFT(coords):
        N = len(coords)
        phi = -np.pi/N
        A_F_P = []          #Amplitude, Frequency, Phase
        temp = 0            #Calculationg percentage for pg window
        for i in tqdm(range(1-N,N)):
            F = i
            ansX = 0
            ansY = 0
            for j in range(1-N,N):
                ansX += coords[j][0]*np.cos(phi*i*j) - coords[j][1]*np.sin(phi*i*j)
                ansY += coords[j][1]*np.cos(phi*i*j) + coords[j][0]*np.sin(phi*i*j)
                global running
                if not running:
                    break
            ansX /= 2*N
            ansY /= 2*N
            A = np.sqrt(ansY**2 + ansX**2)
            P = np.arctan2(ansY,ansX) + np.pi
            A_F_P.append([A,F,P])
            if key.is_pressed(exit_key):
                running = False
                break
            if temp != int((i+N)/(2*N)*100):
                temp = int((i+N)/(2*N)*100)
                screen.fill((0, 0, 0))
                medium_font = pg3.font.Font(font_loc,20)
                loading_text = medium_font.render('Completed : '+str(temp)+' %' , True , (0,255,255))
                screen.blit(loading_text,(0,0))
                pg3.display.flip()
        return A_F_P

    def control():
        for event in pg3.event.get():
            if event.type == pg3.QUIT:
                global running
                running = False
                pg3.quit()
                break

    class Arms:
        def __init__(self,pos,amp,color,phase,fre):
            self.pos = pos
            self.amp = amp
            self.color = color
            self.phase = phase
            self.time = 0
            self.fre = fre
            self.dt = 0.001
        def rotate(self,pos):
                self.c = pg3.draw.circle(epicircle, self.color, pos, self.amp, 1)
                self.l = pg3.draw.line(epicircle, self.color, pos, (pos[0] + np.cos(self.phase + self.fre*self.time) * self.amp,pos[1] + np.sin(self.phase + self.fre*self.time) * self.amp))
                self.time += self.dt
                self.pos = pos

        def position(self):
            return ((self.pos[0] + np.cos(self.phase + self.fre*(self.time-self.dt)) * self.amp,self.pos[1] + np.sin(self.phase + self.fre*(self.time-self.dt)) * self.amp))

    def Loading(coords,position):
        A_F_P = FFT(coords)
        A_F_P.sort(reverse=True)
        color = (220,220,0,255)
        for i in range(len(A_F_P)):
            globals()["arm"+str(i)] = Arms(position,A_F_P[i][0],color,A_F_P[i][2],A_F_P[i][1])
            if i > 0:
                position = globals()["arm"+str(i-1)].position()
            if not running:
                break
        return len(A_F_P)

    def rotator(arm_no,aqurcy):
        global rotate_switch
        if rotate_switch:
            for i in range(arm_no-aqurcy):
                if i > 0:
                    globals()["arm"+str(i)].rotate(globals()["arm"+str(i-1)].position())
                    if i == arm_no - aqurcy - 1:
                        if circle:
                            pg3.draw.circle(trail,(0,200,220),globals()["arm"+str(i)].position(), circle_radious)
                        else:
                            gfxdraw.pixel(trail,int(globals()["arm"+str(i)].position()[0]),int(globals()["arm"+str(i)].position()[1]),(0,200,220))
                else:
                    globals()["arm"+str(i)].rotate(position)
                if not rotate_switch or not running:
                    break
        if key.is_pressed(rotate_stop_key):
            rotate_switch = not rotate_switch
            

    while running:
        global rotate_switch

        if key.is_pressed(exit_key):
            running = False
            break

        
        control()
        # beginning position
        if load:
            new_coord = []
            coord = []
            file = open(file_path ,"r")
            coord = json.load(file)
            file.close()
            #coord.resize((200,2))
            print("No. of coordinates : "+str(len(coord)))
            for i in range(0,len(coord),skip):new_coord.append((250 - coord[i][0],250 - coord[i][1]))
            arm_no = Loading(new_coord,position)
            aqurcy = int(arm_no*(100-aqurcy)/100)
            print("No. of circles "+str(arm_no - aqurcy))
            load = False


        
        # update rotation
        screen.fill((0, 0, 0))
        epicircle.fill((0,0,0))
        epicircle.set_alpha(110)
        #calling rotation start function
        rotator(arm_no,aqurcy)
        #
        screen.blit(trail, (0, 0))
        screen.blit(epicircle,(0,0))
        pg3.display.flip()
    
    if not running:
        return "Interrupted"
    else:
        return "Drawing"
# draw()
