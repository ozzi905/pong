import pygame as pg
import sys
from pygame.locals import *
import random
 
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

width = 1280
height = 720

# Setup a 300x300 pixel display with caption
window = pg.display.set_mode((width,height))
window.fill(BLUE)
pg.display.set_caption("Pong")

bg = pg.image.load("images/background.png").convert()

ballList = []

def getNearestBall(balls):
    if(balls.count == 0): return
    closestBall = balls[0]
    for ball in balls:
        if (ball.rect.x > closestBall.rect.x): closestBall = ball
    return closestBall


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pg.image.load("images/paddle.png").convert()
        self.rect = self.surf.get_rect(midleft = (0, 360))
        self.score = 0

    def update_pos(self):
        mouse_y = pg.mouse.get_pos()[1]
        self.rect.midleft = (self.rect.x, mouse_y)

    def draw(self):
        window.blit(self.surf, self.rect)

class Ai(pg.sprite.Sprite):
    def __init__(self):
        self.surf = pg.image.load("images/enemy_paddle.png").convert()
        self.rect = self.surf.get_rect(midright = (width, 360))
        self.score = 0
        self.speed = 13
        if(len(ballList) > 0): self.nearestBall = getNearestBall(ballList)

    def update_pos(self):
        if(len(ballList) > 0):
            self.nearestBall = getNearestBall(ballList)
            if(abs(self.rect.y - self.nearestBall.rect.y) < 60): pass
            elif(self.rect.y < self.nearestBall.rect.y): self.rect.y += self.speed
            else: self.rect.y -= self.speed
    
    def draw(self):   
        window.blit(self.surf, self.rect)
    
class Ball(pg.sprite.Sprite):
    def __init__(self, init_vel_x, init_vel_y):
        self.vel_x = init_vel_x
        self.vel_y = init_vel_y
        self.surf = pg.image.load("images/ball.png")
        self.rect = self.surf.get_rect()
        self.rect.center = (width/2, height/2)
        ballList.append(self)

    def update_pos(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if(paddle.rect.colliderect(self.rect) or ai.rect.colliderect(self.rect)):
            self.vel_x = -(self.vel_x + 0.05)
            self.rect.x += self.vel_x

        elif(self.rect.left >= width):
            paddle.score += 1
            self.rect.center = (width/2, height/2)

        elif(self.rect.right <= 0):
            ai.score += 1
            self.rect.center = (width/2, height/2)

        elif(self.rect.bottom >= height or self.rect.top <= 0):
            self.vel_y = -self.vel_y 
            self.rect.y += self.vel_y*1.5

        elif(self.rect.bottom >= 1000 or self.rect.bottom <= -300): self.rect.center = (width/2, height/2)

        

    def draw(self):
        window.blit(self.surf, self.rect)



paddle = Player()
#ball0 = Ball(8, 5)
#ball1 = Ball(4, 2)
ai = Ai()

while True:
    pg.display.update()
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            ballList.append(Ball(4, 8))
    window.blit(bg, (0,0))

    paddle.update_pos()
    ai.update_pos()
    
    for ball in ballList:
        ball.update_pos()
        ball.draw()

    ai.draw()
    paddle.draw()
    

#    if(pg.mouse.get_pressed(3)[0]):
#        ball.rect.center = (width/2, height/2)
#        print(f"ai: {ai.score}")
#        print(f"you: {paddle.score}")



    FramePerSec.tick(FPS)