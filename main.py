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

paddle_surf = pg.image.load("images/paddle.png").convert()
paddle_rect = paddle_surf.get_rect(midleft = (0, 360))
paddle_score = 0

ai_surf = pg.image.load("images/enemy_paddle.png").convert()
ai_rect = ai_surf.get_rect(midright = (width, 360))
ai_score = 0

ball_vel_y = 5 
ball_vel_x = 10
ball_surf = pg.image.load("images/ball.png")
ball_rect = ball_surf.get_rect()
ball_rect.center = (width/2, height/2)
    

while True:
    pg.display.update()
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    window.blit(bg, (0,0))

    mouse_y = pg.mouse.get_pos()[1]

    paddle_rect.midleft = (paddle_rect.x, mouse_y)

    window.blit(paddle_surf, paddle_rect)
    window.blit(ai_surf, ai_rect)
    window.blit(ball_surf, ball_rect)

    ball_rect.x += ball_vel_x
    ball_rect.y += ball_vel_y

    if(ball_rect.left >= width):
        paddle_score += 1
        ball_rect.center = (width/2, height/2)

    elif(ball_rect.right <= 0):
        ai_score += 1
        ball_rect.center = (width/2, height/2)

    elif(ball_rect.bottom >= height or ball_rect.top <= 0): ball_vel_y = -ball_vel_y
    
    elif(paddle_rect.colliderect(ball_rect) or ai_rect.colliderect(ball_rect)):
        ball_vel_x = -ball_vel_x*1.05

    elif(pg.mouse.get_pressed(3)[0]):
        ball_rect.center = (width/2, height/2)
        print(f"ai: {ai_score}")
        print(f"you: {paddle_score}")

    if(abs(ai_rect.y - ball_rect.y) < 60): pass
    elif(ai_rect.y < ball_rect.y): ai_rect.y += 6
    else: ai_rect.y -= 6



    FramePerSec.tick(FPS)