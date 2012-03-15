import pygame as pg
import sys
import time
import os
from pygame.locals import *

# Commandline flags
TXT = ("-txt" in sys.argv)
PNG = ("-png" in sys.argv)

# Pygame init
dataLen = 12
margin = 50
(width, height) = (1000, 700)
sep = (width-2*margin)/(dataLen-1)

pg.init()
window = pg.display.set_mode((width,height), RESIZABLE)
pg.display.set_caption("Graph")
canvas = pg.PixelArray(window)
white, black = Color(255,255,255), Color(0,0,0)
colors = [Color(175,0,0), Color(0,175,0), Color(0,0,175), Color(128,128,0)]

# Funcs
def screenshot():
    os.system("scrot --focused graphs/"+str(int(time.time()))+".png")
    #pg.image.save(pg.display.get_surface(), "graphs/"+str(int(time.time()))+".png")
    
def exit():
    if PNG: screenshot()
    sys.exit()

maxdata, data, mindata = [-50000]*dataLen, [0]*dataLen, [+50000]*dataLen
skip = 4
skipcnt = 1
lines = []
top = 200
cnt = top

# Offsets gathered empirically... (maxdata+mindata)/2
offsets=[113, -377, 11, 59, 185, 1, -42, 215, -11, 239, -236, 256]

while True:
    # Handle events
    for event in pg.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE: exit()
        if event.type == QUIT: exit()
        if event.type == VIDEORESIZE: 
            width, height = event.size
            window = pg.display.set_mode((width,height), RESIZABLE)
            sep = (width-2*margin)/(dataLen-1)
            pg.draw.rect(window, black, (0,0,width,height))

    # Read data
    read = sys.stdin.readline()[:-1]
    if(read==""): exit()
    if TXT: print read

    # Skip frames
    skipcnt += 1
    if not skipcnt%skip == 0: continue
        
    # Parse data
    exdata = list(data)
    data = [int(s) for s in read.split(" ")[1:]]

    # Clear lines
    clear = 10
    pg.draw.line(window, black, (0,cnt-1+clear/2),(width,cnt-1+clear/2), clear)
    for _,v1,v2 in lines: pg.draw.line(window, black, v1, v2, 1)
    
    # Normalize data somewhat
    for i in range(len(data)):
        maxdata[i], mindata[i] = max(data[i], maxdata[i]), min(data[i], mindata[i])

        # Offset
        if i<6: data[i] += offsets[i]

        # Multiply
        multi = 1
        if i/3 == 0: multi = 4
        if i/3 == 2: multi = 2
        data[i] *= multi

    # Draw data lines
    for i in range(len(data)):
        xorigin = margin+i*sep
        pg.draw.aaline(window, white, 
            (xorigin + (width/1000.0)*(exdata[i]/50.0), cnt-1),
            (xorigin + (width/1000.0)*(data[i]/50.0), cnt))
        pg.draw.line(window, colors[i/3], (xorigin,top-5),(xorigin,height), 1)

    # Axis lines
    lines = []
    for i in range(4):
        xx, yy = margin+sep+sep*i*3, 100
        div = 10
        lines += [
            (colors[0], (xx,yy), (xx+data[0+i*3]/div,yy+data[1+i*3]/div)),
            (colors[1], (xx,yy), (xx+data[1+i*3]/div,yy+data[2+i*3]/div)),
            (colors[2], (xx,yy), (xx+data[2+i*3]/div,yy+data[0+i*3]/div)),
        ]

    for c,v1,v2 in lines: pg.draw.line(window, c, v1, v2, 1)

    pg.display.flip()
    
    cnt += 1
    if cnt>=height-10:
        # Print min and max
        #sys.stderr.write( str(maxdata)+"\n" )
        #sys.stderr.write( str(mindata)+"\n" )

        cnt = top-5
        pg.draw.line(window, black, (0,cnt-1+clear/2),(width,cnt-1+clear/2), clear)
        cnt = top

        # Save screenshot
        if PNG: screenshot()

