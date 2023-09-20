import random
import pygame as pg
import tkinter as tk
debug = False

def draw_background():
    display.fill(background_color)
    pg.draw.line(display,gui_color,(0,20*tilesize),(displaysize[0],20*tilesize),2*tilesize)
    pg.draw.line(display,gui_color,(displaysize[0]-25*tilesize,5*tilesize),(displaysize[0]-15*tilesize,15*tilesize),2*tilesize)
    pg.draw.line(display,gui_color,(displaysize[0]-15*tilesize,5*tilesize),(displaysize[0]-25*tilesize,15*tilesize),2*tilesize)
    pg.draw.line(display,gui_color,(0,displaysize[1]-20*tilesize),(displaysize[0],displaysize[1]-20*tilesize),2*tilesize)
    display.blit(font.render(programname,False,gui_color),(2*tilesize,2*tilesize))
    
def draw_commands():
    display.blit(font.render(commandline,False,text_color),(2*tilesize,displaysize[1]-20*tilesize))
    currentline = 0
    for commandsus in reversed(commandlog):
        display.blit(font.render(commandsus,False,text_color),(2*tilesize,displaysize[1]-42*tilesize-linespacing*tilesize*currentline))
        currentline += 1



def cpu():
    global cpusage
    global cpucooldown
    if cpucooldown <= 0:
        cpusage = random.choice([cpusage-cpuinstability,cpusage+cpuinstability,cpusage,cpusage,cpusage,cpusage])
        if cpusage > 99:
            cpusage = 99
        if cpusage < 1 :
            cpusage = 1
        cpucooldown = cpucooldownm
    else:
        cpucooldown -= 1

    rectlen =((55*tilesize)/100)*cpusage
    pg.draw.rect(display,gui_color,(displaysize[0]-80*tilesize,30*tilesize,70*tilesize,40*tilesize),2*tilesize)
    display.blit(font.render("CPU:"+str(round(cpusage))+"%",False,text_color),(displaysize[0]-78*tilesize,32*tilesize))
    pg.draw.rect(display,gui_color,(displaysize[0]-76*tilesize,55*tilesize,rectlen,10*tilesize))

    global ramusage
    global ramcooldown
    if ramcooldown <= 0:
        ramusage = random.choice([ramusage-raminstability,ramusage+raminstability,ramusage,ramusage,ramusage,ramusage])
        if ramusage > 99:
            ramusage = 99
        if ramusage < 1 :
            ramusage = 1
        ramcooldown = ramcooldownm
    else:
        ramcooldown -= 1

    rectlen =((55*tilesize)/100)*ramusage
    pg.draw.rect(display,gui_color,(displaysize[0]-80*tilesize,80*tilesize,70*tilesize,40*tilesize),2*tilesize)
    display.blit(font.render("RAM:"+str(round(ramusage))+"%",False,text_color),(displaysize[0]-78*tilesize,82*tilesize))
    pg.draw.rect(display,gui_color,(displaysize[0]-76*tilesize,105*tilesize,rectlen,10*tilesize))

    

def select_command():
    global firstline
    global commandlist
    try:
        out = commandlist.pop(0)
    except:
        if debug:
            print("the file is over, looping")
        commandlist = open("commands.txt","r").read().splitlines()
        out = commandlist.pop(0)
    firstline = True
    return out







if not debug:
    root = tk.Tk()
    displaysize = (root.winfo_screenwidth(),root.winfo_screenheight())
    root.destroy()
else:
    displaysize = (255,255)

pg.init()
display = pg.display.set_mode(displaysize)

clock = pg.time.Clock()
pg.mouse.set_visible(False)

programname = "HACK1N4T0R V 1.5.33"
clockspeed = 1000
tilesize = round((displaysize[0]/1000))
try:
    font = pg.font.Font("SpaceMono-Regular.ttf",15*tilesize)
except:
    font = pg.font.SysFont("Courier",15*tilesize)
pg.display.set_caption(programname)

#import the text file

with open("commands.txt","r") as file:

    commandlist = file.read().splitlines()








typespeed =  1
commandpointer = ">> "
maxloglen = 45                  #pcpiccolo = 45
linespacing = 15
autoscrollspeed  = 4
cpuinstability = 1.2
raminstability = 1.2


background_color = (0,0,0)      #black
gui_color = (0,255,0)           #lime
text_color = (255,255,255)      #white


autoscrollcooldown = autoscrollspeed
autoscrollcooldownm = autoscrollcooldown
cpucooldown = 100
cpucooldownm = 100
ramcooldown  = 100
ramcooldownm = 100
commandlog = []
autoscroll = False
commandline = commandpointer
command = select_command()
cpusage = 20
ramusage = 35

dead = False
while not dead:
    already = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            dead = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                dead = True
            elif event.key == pg.K_F9:
                if autoscroll:
                    autoscroll =  False
                else:
                    autoscroll = True
            else:
                if not already:
                    for i in range(typespeed):
                        try:
        
                            while command[len(commandline)-len(commandpointer)] == " " and firstline:
                                commandline += command[len(commandline)-len(commandpointer)]
                            commandline += command[len(commandline)-len(commandpointer)]
                            firstline = False
                            already = True
                        except:
                            if debug:
                                print("error while adding the new character! is the typespeed too high?")

    if autoscroll:
        if autoscrollcooldown >0:
            autoscrollcooldown -= 1
        else:
            autoscrollcooldown = autoscrollcooldownm
            for i in range(typespeed):
                try:

                    while command[len(commandline)-len(commandpointer)] == " " and firstline:
                        commandline += command[len(commandline)-len(commandpointer)]
                    commandline += command[len(commandline)-len(commandpointer)]
                    firstline = False
                    already = True
                except:
                    if debug:
                        print("error while adding the new character! is the typespeed too high?")
               



    draw_background()
    if len(commandline) == len(command) + len(commandpointer):
        commandline = command
        if len(commandlog) <= maxloglen-1:
            commandlog.append(commandline)
        else:
            commandlog.pop(0)
            commandlog.append(commandline)
        command = select_command()
        commandline = commandpointer


    draw_commands()
    cpu()
    clock.tick(clockspeed)
    pg.display.update()
pg.quit()
quit()
