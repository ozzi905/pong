import pygame as pg
import sys
from pygame.locals import *
 
# Initialize program
pg.init()
 
# Assign FPS a value
FPS = 60
FramePerSec = pg.time.Clock()
 
# Setting up color objects
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
MAGENTA = (255,0,255)
CYAN = (0,255,255)
WHITE = (255,255,255)

# Setup a 300x300 pixel display with caption
window = pg.display.set_mode((800,800))
window.fill(BLUE)
pg.display.set_caption("Pong")

test_surface = pg.Surface((300,300))

class Paddle():
    def __init__(self, x, y, vertical):
        self.x = x
        self.y = y
        if(vertical == True): self.surface = pg.Surface((80, 20))
        else: self.surface = pg.Surface((20, 80))

while True:
    pg.display.update()
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    test_surface.fill(CYAN)
    window.blit(test_surface, (0,0))
    
   
    FramePerSec.tick(FPS)