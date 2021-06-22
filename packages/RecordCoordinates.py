import pygame as pg1
import json
from pygame import gfxdraw
import random

success = True

def recordcords(size = (700,700), 
                file_path = "coordinate.txt", 
                show_text = "Draw something with mouse",
                font_loc = "BAHNSCHRIFT.TTF", 
                font_size = 14, 
                font_color = (0, 255, 0), 
                background_color = (0,0,0), 
                random_color = True, 
                circle = True, 
                circle_radious = 1):
    
    
    global success
    new_coords = []
    bckp_coords = []
    reversed = False
    switch = True
    saved = False

    # pg1.init()
    pg1.display.set_caption("Co-ordinates feed")
    screen = pg1.display.set_mode(size)
    #changing color
    screen.fill(background_color)
    #
    #adding a test line
    font = pg1.font.Font(font_loc, font_size)
    text = font.render(show_text, True, font_color)
    textRect = text.get_rect()
    # textRect.center = (len(show_text)*(font_size/4), 10) #for movement of text center
    screen.blit(text, textRect)
    #
    while switch:
        for event in pg1.event.get():
            coord = (0,0)
            if event.type == pg1.QUIT or pg1.key.get_pressed()[pg1.K_ESCAPE]:
                switch = False
            elif pg1.mouse.get_pressed()[0] :
                if reversed:
                    bckp_coords = new_coords
                    reversed = False
                coord = pg1.mouse.get_pos()
                new_coords.append(coord)
                bckp_coords.append(coord)
                if random_color:
                    if circle:
                        pg1.draw.circle(screen, (random.randint(50,255), random.randint(50,255), random.randint(50,255)),coord, circle_radious)
                    else:
                        gfxdraw.pixel(screen,coord[0],coord[1], (random.randint(50,255), random.randint(50,255), random.randint(50,255)))
                else:
                    if circle:
                        pg1.draw.circle(screen, (255, 255, 255),coord, circle_radious)
                    else:
                        gfxdraw.pixel(screen,coord[0],coord[1],(255, 255, 255))
            elif pg1.key.get_pressed()[pg1.K_x]:
                if len(bckp_coords) == len(new_coords):
                    print("No cords for redo")
                else:
                    reversed = True
                    new_coords.append(bckp_coords[len(new_coords)])
                    if random_color:
                        if circle:
                            pg1.draw.circle(screen, (random.randint(50,255), random.randint(50,255), random.randint(50,255)),new_coords[-1], circle_radious)
                        else:
                            gfxdraw.pixel(screen,new_coords[-1][0],new_coords[-1][1], (random.randint(50,255), random.randint(50,255), random.randint(50,255)))
                    else:
                        if circle:
                            pg1.draw.circle(screen, (255, 255, 255),new_coords[-1], circle_radious)
                        else:
                            gfxdraw.pixel(screen,new_coords[-1][0],new_coords[-1][1],(255, 255, 255))
            elif pg1.key.get_pressed()[pg1.K_z]:
                if len(new_coords) > 0:
                    reversed = True
                    if circle:
                        pg1.draw.circle(screen, background_color, new_coords[-1], 1)
                    else:
                        gfxdraw.pixel(screen,new_coords[-1][0],new_coords[-1][1],background_color)
                    new_coords.pop(-1)
                else:
                    print("No cords for undo")
            elif pg1.key.get_pressed()[pg1.K_s]:
                file = open(file_path, "w")
                json.dump(new_coords,file)
                file.close()
                if len(new_coords) > 0:
                    success = 1
                switch = False
                saved = True
        pg1.display.flip()
    print("Total numbers of cords :",len(new_coords))
    # pg1.quit()
    if saved:
        print("saved to file.")
        return  str(len(new_coords))+' cords/pixels drawn.'
    else:
        print("not saved to file.")
        return  'cords not saved. Draw again.'