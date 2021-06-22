__author__ = "Sandeep Yadav"
__copyright__ = "Copyright 2019."
__credits__ = ["Sandeep Yadav"]
__license__ = "MIT License"
__version__ = "2.0.0"
__maintainer__ = "Sandeep Yadav"
__email__ = "sandeepyadav1478@gmail.com"
__status__ = "Working"

import pygame as pg
import re
from pygame.draw import circle
from pygame.transform import rotate
from pygame import NOFRAME

from genericpath import exists
from win32api import GetSystemMetrics
from os.path import exists

from packages.RecordCoordinates import recordcords
from packages.imagetocoordinates import imgtocord
from packages.cordinatearrange import cordsort, undo
from packages.coordinatetoImage import cordtoimage
from packages.DrawFFT import draw

#------------  Editable Content by User ------------------------

#image output method
out_img_type = "b&w"  # gray || b&w || edge
threshold_level = 255  #  50 || 255 || 255
#to change edge detect image thresholds, its range of filter
canny_pass =  [200, #threshold 1
               430, #threshold 2
               1 #apertureSize
               ]


cord_record = 'cords.txt'           #base file for cords saving
cord_record_bck = 'bck_cords.txt'   #backup file

comp = 0   # Compression percentage

circle = False      # want out in pixels or circles with 1 radius
rotate_stop_key = 'r'
draw_exit_key = 'q'

#-----------------------------------


running = True
win_active = 1
radio1 = 0
img_loc_status = 0
img_loc_status_sec = 0
img_exists = False
img_first_key = 0

icon_loc = "assets/icon.png"
font_loc = "assets/BAHNSCHRIFT.TTF"
bg_img = 'assets/sew.jpg'
img_loc = "sample1.jpg"

comp_status = 0
switch = 'Remove'
undo_status = 0

dfft_switch = 0

def main():
    
    global running, radio1, img_loc, img_loc_status, img_first_key, img_loc_status_sec, win_active, img_exists, comp, comp_status, switch, dfft_switch, undo_status
    # monitor resolution
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
    #
    perc_width = lambda x: int(x*width/100)
    perc_height = lambda x: int(x*height/100)

    colors = {'white':(255,255,255),
              'bck1':(70,194,181), 'bck2':(74,188,193),
              'black':(0,0,0), 'gray': (105,105,105),
              'dark_green':(153, 255, 51), 'green':(0,255,0),
              'dark_red':(190,0,0),'red':(255,0,0),
              'yellow':(255,255,0),'dark_yellow':(200,200,0),
              'blue':(0,0,255),'navy_blue':(0,0,128)}
    

    screen = pg.display.set_mode((perc_width(75), perc_width(33)),NOFRAME)

    pg.init()

    def base():
        bg = pg.image.load(bg_img)
        pg.display.set_caption("Joseoh Fourier")
        pg.display.set_icon(pg.image.load(icon_loc))

        #Change background with image
        screen.blit(bg, (0, 0))

        pg.draw.rect(screen,(255,255,255,1), [perc_width(75) - 35,perc_height(1),30, 30],1,1)

        # defining a font
        small_font = pg.font.Font(font_loc,11)
        medium_font = pg.font.Font(font_loc,20)
        large_font = pg.font.Font(font_loc,30)

        # rendering a text written in
        # this font
        quit_char = medium_font.render('X' , True , colors['red'])
        head_main = 'Fourier  Transform  X'

        head_text1 = 'Formula used'
        formula_text2 = 'F(x)=½ Ao + Σ An Cos(nx) ± Σ Bn Sin(nx)'
        formula_text3 = 'Where n --> [1, inf.] inclusive.'
        formula_text4 = 'Ao = 1/π Int.[π,-π] F(x) dx'
        formula_text5 = 'An = 1/π Int.[π,-π] F(x) Cos(nx) dx'
        formula_text6 = 'Bn = 1/π Int.[π,-π] F(x) Sin(nx) dx'

        head_text2 = 'Select input method'
        input_text1_opt1 = 'Image'
        input_text1_opt2 = 'Draw'
        go_icon1 = '>'

        head_text3 = 'Compression'
        h3t1 = 'Percentage: '
        h3t2 = '%'
        h3t3 = 'Undo'

        head_text4 = 'Ruff  Sketch'
        h4t1 = 'Try!'

        input_text5_opt1 = 'fftshift( X )'

        heading_main = large_font.render(head_main,True, colors['white'])

        heading1 = medium_font.render(head_text1,True,colors['white'])
        formula2 = medium_font.render(formula_text2,True,colors['black'])
        formula3 = medium_font.render(formula_text3,True,colors['yellow'])
        formula4 = medium_font.render(formula_text4,True,colors['dark_green'])
        formula5 = medium_font.render(formula_text5,True,colors['dark_green'])
        formula6 = medium_font.render(formula_text6,True,colors['dark_green'])


        heading2 = medium_font.render(head_text2,True,colors['white'])
        input1_opt1 = medium_font.render(input_text1_opt1,True,colors['white'])
        input1_opt2 = medium_font.render(input_text1_opt2,True,colors['white'])
        go1 = large_font.render(go_icon1,True,colors['white'])


        heading3 = medium_font.render(head_text3,True,colors['white'])
        h31 = medium_font.render(h3t1,True,colors['black'])
        h32 = medium_font.render(h3t2,True,colors['black'])
        h33 = medium_font.render(h3t3,True,colors['white'])
        comp_text = medium_font.render(str(comp),True,colors['white'])
        go2 = large_font.render(go_icon1,True,colors['black'])
        switch_opt1 = medium_font.render(switch,True,colors['white'])

        heading4 = medium_font.render(head_text4,True,colors['white'])
        h41 = medium_font.render(h4t1,True,colors['white'])


        input5_opt1 = medium_font.render(input_text5_opt1,True,colors['white'])


        # superimposing the text onto our button
        screen.blit(quit_char , (perc_width(73.2),perc_height(1.1)))
        screen.blit(heading_main,(perc_width(26.9),perc_height(1)))
        
        screen.blit(heading1,(perc_width(1),perc_height(5.6)))
        screen.blit(formula2,(perc_width(5),perc_height(10)))
        screen.blit(formula3,(perc_width(5),perc_height(13)))
        screen.blit(formula4,(perc_width(9.5),perc_height(16)))
        screen.blit(formula5,(perc_width(9.5),perc_height(19)))
        screen.blit(formula6,(perc_width(9.5),perc_height(22)))


        #radio button 1
        pg.draw.rect(screen,colors['black'], [perc_width(5),perc_height(35.5),90, 30])
        #radio button 2
        pg.draw.rect(screen,colors['black'], [perc_width(16),perc_height(35.5),90, 30])
        #go1 button ('>') 
        if img_loc_status:pg.draw.rect(screen,colors['black'], [perc_width(26),perc_height(45.4),perc_width(2.2), perc_width(2.2)],border_radius = 15)
        screen.blit(heading2,(perc_width(1),perc_height(30)))
        screen.blit(input1_opt1,(perc_width(6.2),perc_height(35.6)))
        screen.blit(input1_opt2,(perc_width(17.6),perc_height(35.6)))
        if img_loc_status:screen.blit(go1,(perc_width(26.75),perc_height(44.78)))
        


        screen.blit(heading3,(perc_width(40),perc_height(5.6)))
        screen.blit(h31,(perc_width(45),perc_height(10)))
        screen.blit(h32,(perc_width(63),perc_height(10)))
        screen.blit(comp_text,(perc_width(57.6),perc_height(10)))
        pg.draw.line(screen,colors['white'], [perc_width(54),perc_height(13)],[perc_width(62),perc_height(13)])
        #go2 button ('>') 
        pg.draw.rect(screen,colors['white'], [perc_width(67.2),perc_height(9.3),perc_width(2.2), perc_width(2.2)],border_radius = 15)
        screen.blit(go2,(perc_width(67.9),perc_height(8.7)))
        #switch button 1
        pg.draw.rect(screen,colors['black'], [perc_width(45),perc_height(16),90, 30])
        screen.blit(switch_opt1,(perc_width(45.5),perc_height(16.2)))
        #undo button
        if undo_status:
            pg.draw.rect(screen,colors['black'], [perc_width(55),perc_height(16),90, 30])
            screen.blit(h33,(perc_width(56.5),perc_height(16.2)))
        

        screen.blit(heading4,(perc_width(40),perc_height(30)))
        pg.draw.rect(screen,colors['black'], [perc_width(45),perc_height(35.5),90, 30])
        screen.blit(h41,(perc_width(47),perc_height(35.9)))

        # fftx button
        if dfft_switch:
            pg.draw.rect(screen,colors['green'], [perc_width(45),perc_height(49),perc_width(24.6), 30])
            screen.blit(input5_opt1,(perc_width(54),perc_height(49.3)))

        pg.display.flip()
        show_msg("*Tip: To load previous cords, compress data with 100% 'Keep'")

    def show_msg(message):
        pg.draw.rect(screen,colors['bck1'], [perc_width(5.2),perc_height(51),perc_width(22.5), 14])
        temp_font = pg.font.Font(font_loc,11)
        temp1 = temp_font.render(message, True, colors['dark_red'])
        screen.blit(temp1,(perc_width(5.2),perc_height(51)))
        pg.display.flip()

    #init screen
    base()
    while running:
        for event in pg.event.get():
            small_font = pg.font.Font(font_loc,11)
            medium_font = pg.font.Font(font_loc,20)
            large_font = pg.font.Font(font_loc,30)
            if (event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]):running = False
            if not win_active and event.type == pg.KEYDOWN:show_msg("currently in working process. You can use 'Esc' only")
            if win_active and (event.type == pg.MOUSEBUTTONUP):
                #undo button
                if undo_status and pg.mouse.get_pos()[0] >= perc_width(55) and pg.mouse.get_pos()[0] <= perc_width(61.56) and pg.mouse.get_pos()[1] >= perc_height(16) and pg.mouse.get_pos()[1] <= perc_height(20):
                    win_active = 0
                    img_loc_status = 0
                    show_msg("processing...")
                    show_msg(undo(file_path=cord_record,file_path_bck=cord_record_bck))
                    win_active = 1
                #try check
                if pg.mouse.get_pos()[0] >= perc_width(45) and pg.mouse.get_pos()[0] <= perc_width(51.8) and pg.mouse.get_pos()[1] >= perc_height(35.5) and pg.mouse.get_pos()[1] <= perc_height(39.5):
                    win_active = 0
                    img_loc_status = 0
                    comp_status = 0
                    show_msg("processing...")
                    show_msg(cordtoimage(file_path = cord_record))
                    win_active = 1
                #switch button check
                if pg.mouse.get_pos()[0] >= perc_width(45) and pg.mouse.get_pos()[0] <= perc_width(51) and pg.mouse.get_pos()[1] >= perc_height(16) and pg.mouse.get_pos()[1] <= perc_height(20):
                    img_loc_status = 0
                    comp_status = 1
                    if switch == 'Remove':switch = 'Keep'
                    else:switch = 'Remove'
                    switch_opt1 = medium_font.render(switch,True,colors['white'])
                    pg.draw.rect(screen,colors['black'], [perc_width(45),perc_height(16),90, 30])
                    screen.blit(switch_opt1,(perc_width(45.5),perc_height(16.2)))
                    pg.display.flip()
                # Percentage line check
                if pg.mouse.get_pos()[0] >= perc_width(54) and pg.mouse.get_pos()[0] <= perc_width(62) and pg.mouse.get_pos()[1] >= perc_height(10) and pg.mouse.get_pos()[1] <= perc_height(13):
                    pg.draw.line(screen,colors['gray'], [perc_width(54),perc_height(13)],[perc_width(62),perc_height(13)])
                    pg.display.flip()
                    img_loc_status = 0
                    comp_status = 1
                #
                #quit button
                if pg.mouse.get_pos()[0] >= perc_width(75) - 35 and pg.mouse.get_pos()[0] <= perc_width(75) - 5 and pg.mouse.get_pos()[1] >= perc_height(1.6) and pg.mouse.get_pos()[1] <= perc_height(5):
                    running = False
                #
                #radio1
                if pg.mouse.get_pos()[0] >= perc_width(5) and pg.mouse.get_pos()[0] <= perc_width(5) + 90 and pg.mouse.get_pos()[1] >= perc_height(35.5) and pg.mouse.get_pos()[1] <= perc_height(35.5) + 30:
                    radio1 = 1
                    img_loc_status = 1
                    comp_status = 0
                    pg.draw.rect(screen,colors['black'], [perc_width(16),perc_height(35.5),90, 30],1)
                    pg.draw.rect(screen,colors['white'], [perc_width(5),perc_height(35.5),90, 30],1)
                    #draw button
                    pg.draw.rect(screen,colors['black'], [perc_width(26),perc_height(45.4),perc_width(2.2), perc_width(2.2)],border_radius = 15)
                    go1 = large_font.render(">",True,colors['white'])
                    screen.blit(go1,(perc_width(26.75),perc_height(44.78)))
                    #
                    temp1 = small_font.render("path: ",True,colors['black'])
                    screen.blit(temp1,(perc_width(5.2),perc_height(42)))

                    pg.draw.line(screen,colors['white'], [perc_width(7),perc_height(49)],[perc_width(20),perc_height(49)])

                    temp1 = small_font.render(img_loc,True,colors['white'])
                    screen.blit(temp1,(perc_width(7.2),perc_height(47)))
                    pg.display.flip()
                #radio2
                if pg.mouse.get_pos()[0] >= perc_width(16) and pg.mouse.get_pos()[0] <= perc_width(16) + 90 and pg.mouse.get_pos()[1] >= perc_height(35.5) and pg.mouse.get_pos()[1] <= perc_height(35.5) + 30:
                    radio1 = 2
                    comp_status = 0
                    pg.draw.rect(screen,colors['black'], [perc_width(5),perc_height(35.5),90, 30],1)
                    pg.draw.rect(screen,colors['white'], [perc_width(16),perc_height(35.5),90, 30],1)
                    pg.display.flip()
                    img_loc_status = 0
                    img_loc_status_sec = 0
                    win_active = 0
                    show_msg('Drag your mouse on poped screen.')
                    temp = recordcords(circle=False, file_path = cord_record, font_loc=font_loc)
                    #creating window again
                    screen = pg.display.set_mode((perc_width(75), perc_width(33)), NOFRAME)
                    base()
                    #
                    #showing output
                    if 'temp' in locals():
                        if len(str(temp)):
                            show_msg(temp)
                            if bool(re.search(r'\d', temp)):
                                # creating fttx button
                                temp = medium_font.render('fftshift( X )',True,colors['white'])
                                pg.draw.rect(screen,colors['green'], [perc_width(45),perc_height(49),perc_width(24.6), 30])
                                screen.blit(temp,(perc_width(54),perc_height(49.3)))
                                pg.display.flip()
                                dfft_switch = 1
                                #
                            win_active = 1
                    #
                #activating image location bar
                if img_loc_status and pg.mouse.get_pos()[0] >= perc_width(6) and pg.mouse.get_pos()[0] <= perc_width(21) and pg.mouse.get_pos()[1] >= perc_height(45.9) and pg.mouse.get_pos()[1] <= perc_height(49) :
                    if not img_loc_status_sec:
                        pg.draw.rect(screen,colors['bck1'], [perc_width(4.5),perc_height(47),perc_width(21), 14])
                        temp1 = small_font.render(img_loc,True,colors['white'])
                        screen.blit(temp1,(perc_width(5.2),perc_height(47)))
                        pg.draw.line(screen,colors['gray'], [perc_width(5.2),perc_height(49)],[perc_width(22.5),perc_height(49)])
                        img_loc_status_sec = 1
                        pg.display.flip()
                #clicking on go1 button
                if pg.mouse.get_pos()[0] >= perc_width(26) and pg.mouse.get_pos()[0] <= perc_width(28.2) and pg.mouse.get_pos()[1] >= perc_height(45.5) and pg.mouse.get_pos()[1] <= perc_height(49.2) :
                    if exists(img_loc):
                        show_msg("found file")
                        win_active = 0
                        temp = imgtocord(img_path = img_loc,type=out_img_type,threshold_level=threshold_level, file_loc= cord_record,canny_pass =canny_pass)
                        if 'temp' in locals():
                            if len(temp):
                                show_msg(str(temp)+' cords/pixels saved.')
                                # creating fttx button
                                temp = medium_font.render('fftshift ( X )',True,colors['white'])
                                pg.draw.rect(screen,colors['green'], [perc_width(45),perc_height(49),perc_width(24.6), 30])
                                screen.blit(temp,(perc_width(54),perc_height(49.3)))
                                pg.display.flip()
                                dfft_switch = 1
                                #
                        win_active = 1
                    else:
                        show_msg("image doesn't exist")
                #clicking on go2 button
                if pg.mouse.get_pos()[0] >= perc_width(67.2) and pg.mouse.get_pos()[0] <= perc_width(69.4) and pg.mouse.get_pos()[1] >= perc_height(9.3) and pg.mouse.get_pos()[1] <= perc_height(13) :
                    img_loc_status = 0
                    comp_status = 1
                    win_active = 0
                    show_msg('Arranging...')
                    temp = cordsort(file_path = cord_record, perc = comp, format = switch, file_path_bck= cord_record_bck)
                    if 'temp' in locals():
                            if len(temp)>0:
                                show_msg(temp)
                                # creating fttx button
                                if bool(re.search(r'\d', temp)):
                                    temp = medium_font.render('fftshift ( X )',True,colors['white'])
                                    pg.draw.rect(screen,colors['green'], [perc_width(45),perc_height(49),perc_width(24.6), 30])
                                    screen.blit(temp,(perc_width(54),perc_height(49.3)))
                                    pg.display.flip()
                                    dfft_switch = 1
                                #
                    win_active = 1
                    pg.draw.rect(screen,colors['black'], [perc_width(55),perc_height(16),90, 30])
                    temp = medium_font.render('Undo',True,colors['white'])
                    screen.blit(temp,(perc_width(56.5),perc_height(16.2)))
                    pg.display.flip()
                    undo_status = 1
                #clicking on fftx button
                if pg.mouse.get_pos()[0] >= perc_width(45) and pg.mouse.get_pos()[0] <= perc_width(69.6) and pg.mouse.get_pos()[1] >= perc_height(49) and pg.mouse.get_pos()[1] <= perc_height(52.85) :
                    if dfft_switch:
                        comp_status = 0
                        img_loc_status = 0
                        win_active = 0
                        temp = draw(file_path=cord_record,circle=circle,rotate_stop_key = rotate_stop_key,exit_key=draw_exit_key)
                        if 'temp' in locals():
                            if len(temp):
                                show_msg(temp)
                                # creating fttx button
                                if bool(re.search(r'\d', temp)):
                                    temp = medium_font.render('fftshift ( X )',True,colors['white'])
                                    pg.draw.rect(screen,colors['green'], [perc_width(45),perc_height(49),perc_width(24.6), 30])
                                    screen.blit(temp,(perc_width(54),perc_height(49.3)))
                                    pg.display.flip()
                                    dfft_switch = 1
                                #
                        #creating window again
                        screen = pg.display.set_mode((perc_width(75), perc_width(33)), NOFRAME)
                        base()
                        #
                        win_active = 1
            if win_active and event.type == pg.KEYDOWN:
                if img_loc_status:
                    if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                        if exists(img_loc):
                            show_msg("found image.")
                            win_active = 0
                            temp = imgtocord(img_path = img_loc,type=out_img_type,threshold_level=threshold_level, file_loc= cord_record,canny_pass =canny_pass)
                            if len(temp):
                                show_msg(temp)
                                if bool(re.search(r'\d', temp)):
                                    # creating fttx button
                                    temp = medium_font.render('fftshift( X )',True,colors['white'])
                                    pg.draw.rect(screen,colors['green'], [perc_width(45),perc_height(49),perc_width(24.6), 30])
                                    screen.blit(temp,(perc_width(54),perc_height(49.3)))
                                    pg.display.flip()
                                    dfft_switch = 1
                                    #
                                win_active = 1
                        else:
                            show_msg("image doesn't exist")
                    elif event.key == pg.K_BACKSPACE:
                        if len(img_loc) > 0:
                            if not img_first_key:
                                img_first_key = 1
                            img_loc = img_loc[:-1]
                            pg.draw.rect(screen,colors['bck1'], [perc_width(4.5),perc_height(47),perc_width(21), 14])
                            if len(img_loc) > 39:
                                temp1 = small_font.render(img_loc[-40:-1],True,colors['white'])
                            else:
                                temp1 = small_font.render(img_loc,True,colors['white'])
                            screen.blit(temp1,(perc_width(5.2),perc_height(47)))
                            pg.display.flip()
                    else:
                        try:temp = ord(event.unicode)
                        except:pass
                        if 'temp' in locals() and type(temp) == int:
                            if (temp >= 97 and temp <= 122) or (temp >= 65 and temp <= 90) or temp == 46 or (temp > 48 and temp < 57):    
                                if not img_first_key:
                                    img_first_key = 1
                                    img_loc = ''
                                img_loc += str(event.unicode)
                                pg.draw.line(screen,colors['gray'], [perc_width(5.2),perc_height(49)],[perc_width(22.5),perc_height(49)])
                                pg.draw.rect(screen,colors['bck1'], [perc_width(4.5),perc_height(47),perc_width(21), 14])
                                if len(img_loc) > 39:temp1 = small_font.render(img_loc[-40:-1],True,colors['white'])
                                else:temp1 = small_font.render(img_loc,True,colors['white'])
                                screen.blit(temp1,(perc_width(5.2),perc_height(47)))
                                pg.display.flip()
                if comp_status:
                    if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                        win_active = 0
                        show_msg('Arranging...')
                        temp = cordsort(file_path = cord_record, perc = comp, format = switch)
                        if len(str(temp)):
                            show_msg('Compressed: '+str(temp)+' cords/points left now.')
                            win_active = 1
                    elif event.key == pg.K_BACKSPACE:
                        if len(str(comp)) > 0:
                            comp = int(comp/10)
                            pg.draw.rect(screen,colors['bck2'], [perc_width(54),perc_height(10),perc_width(8), perc_height(3)])
                            medium_font = pg.font.Font(font_loc,20)
                            temp1 = medium_font.render(str(comp),True,colors['white'])
                            screen.blit(temp1,(perc_width(57.6),perc_height(10)))
                            pg.display.flip()
                    else:
                        try:temp2 = int(event.key)
                        except:pass
                        if 'temp2' in locals():
                            if temp2 > 1073741912  and temp2 < 1073741923:
                                if len(str(comp)) < 3:
                                    deff =  1073741912
                                    if temp2 == 1073741922:
                                        deff = 1073741922
                                    comp = (comp*10) + (temp2 - deff)
                                    if comp > 100:
                                        comp = 100
                                    pg.draw.rect(screen,colors['bck2'], [perc_width(54),perc_height(10),perc_width(8), perc_height(3)])
                                    medium_font = pg.font.Font(font_loc,20)
                                    temp1 = medium_font.render(str(comp),True,colors['white'])
                                    screen.blit(temp1,(perc_width(57.6),perc_height(10)))
                                    pg.display.flip()
                                else:
                                    show_msg("Can't go more then 100")
                            else:
                                show_msg('Use num keys')
    pg.quit()

if __name__== "__main__":main()