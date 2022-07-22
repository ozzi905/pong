import pygame as pg
import sys
from pygame.locals import *
import random, time
playerScore = 0
aiScore = 0
 
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
        self.image = pg.image.load("images/paddle.png").convert()
        self.rect = self.image.get_rect(midleft = (0, 360))
        self.score = 0

    def update_pos(self):
        mouse_y = pg.mouse.get_pos()[1]
        self.rect.midleft = (self.rect.x, mouse_y)
 
    def update(self):
        self.update_pos()

class Ai(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("images/enemy_paddle.png").convert()
        self.rect = self.image.get_rect(midright = (width, 360))
        self.score = 0
        self.speed = 13
        if(len(ballList) > 0): self.nearestBall = getNearestBall(ballList)

    def update_pos(self):
        if(len(ballList) > 0):
            self.nearestBall = getNearestBall(ballList)
            if(abs(self.rect.y - self.nearestBall.rect.y) < 50): pass
            elif(self.rect.y < self.nearestBall.rect.y): self.rect.y += self.speed
            else: self.rect.y -= self.speed

    def update(self):
        self.update_pos()
    
class Ball(pg.sprite.Sprite):
    def __init__(self, init_vel_x, init_vel_y):
        super().__init__()
        self.vel_x = init_vel_x
        self.vel_y = init_vel_y
        self.image = pg.image.load("images/ball.png").convert_alpha(window)
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height/2)
        ballList.append(self)

    def update_pos(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if(pg.sprite.spritecollide(self, paddle, False)or pg.sprite.spritecollide(self, opponents, False)):
            self.vel_x = -(self.vel_x + 0.5)
            self.rect.x += self.vel_x

        elif(self.rect.left >= width):
            global playerScore
            playerScore += 1
            time.sleep(1)
            self.rect.center = (width/2, height/2)

        elif(self.rect.right <= 0):
            global aiScore
            aiScore += 1
            time.sleep(1)
            self.rect.center = (width/2, height/2)

        elif(self.rect.bottom >= height or self.rect.top <= 0):
            self.vel_y = -(self.vel_y + 0.5)
            self.rect.y += self.vel_y*1.5

        elif(self.rect.bottom >= 1000 or self.rect.bottom <= -300): self.rect.center = (width/2, height/2)

        

    def draw(self):
        window.blit(self.image, self.rect)

    def update(self):
        self.update_pos()


paddle = pg.sprite.GroupSingle()
paddle.add(Player())

opponents = pg.sprite.Group()
opponents.add(Ai())

balls = pg.sprite.Group()

while True:
    pg.display.update()
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            balls.add((Ball(4, 8)))

    window.blit(bg, (0,0))

    paddle.update()
    opponents.update()
    balls.update()
    
    paddle.draw(window)
    opponents.draw(window)
    balls.draw(window)

    FramePerSec.tick(FPS)