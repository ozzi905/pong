import pygame as pg
import sys
from pygame.locals import *
import random, time

playerScore = 0
aiScore = 0

mode = "menu"
 
pg.init()
 
FPS = 60
FramePerSec = pg.time.Clock()
 
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
ballList = []

window = pg.display.set_mode((width,height))
window.fill(BLUE)
pg.display.set_caption("Pong")


def getNearestBall(balls):
    if(balls.count == 0): return
    closestBall = balls[0]
    for ball in balls:
        if (ball.rect.x > closestBall.rect.x): closestBall = ball
    return closestBall


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("images/classic/paddle.png").convert()
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
        self.image = pg.image.load("images/classic/enemy_paddle.png").convert()
        self.rect = self.image.get_rect(midright = (width, 360))
        self.score = 0
        self.speed = 13
        if(len(ballList) > 0): self.nearestBall = getNearestBall(ballList)

    def update_pos(self):
        if(len(ballList) > 0):
            self.nearestBall = getNearestBall(ballList)
            if(abs(self.rect.y - self.nearestBall.rect.y) < 40): pass
            elif(self.rect.y < self.nearestBall.rect.y): self.rect.y += self.speed
            else: self.rect.y -= self.speed

    def update(self):
        self.update_pos()
    
class Ball(pg.sprite.Sprite):
    def __init__(self, init_vel_x, init_vel_y):
        super().__init__()
        self.vel_x = init_vel_x
        self.vel_y = init_vel_y
        self.image = pg.image.load("images/classic/ball.png").convert_alpha(window)
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height/2)
        ballList.append(self)

    def update_pos(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if(pg.sprite.spritecollide(self, paddle, False)or pg.sprite.spritecollide(self, opponents, False)):
            self.vel_x = -(self.vel_x*1.1)
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

    def update(self):
        self.update_pos()

class Ui(pg.sprite.Sprite):
    def __init__(self, type, topleft):
        super().__init__()
        global mode
        self.type = type
        self.topleft = topleft
        self.image = pg.image.load(f"images/{mode}/{type}.png")
        self.rect = self.image.get_rect(topleft = topleft)

    def test_for_click(self):
        if(pg.mouse.get_pressed(num_buttons=5)[0] and self.rect.collidepoint(pg.mouse.get_pos())):
            if(self.type == "play_classic"): loadClassic()
            elif(self.type == "menu"): menu()
            elif(self.type == "resume"): unpause()
            else: pass

    def update(self):
        self.test_for_click()

small_font = pg.font.Font(None, 50)
large_font = pg.font.Font(None, 100)

paddle = pg.sprite.GroupSingle()

opponents = pg.sprite.Group()

balls = pg.sprite.Group()

ui = pg.sprite.Group()

bricks = pg.sprite.Group()



bg = pg.image.load(f"images/menu/background.png").convert()



playerScoreRect = pg.rect.Rect(200, 150, 100, 100)
aiScoreRect = pg.rect.Rect(1000, 150, 100, 100)


def emptyScreen():
    paddle.empty()
    opponents.empty()
    balls.empty()
    ballList.clear()
    ui.empty()

def loadClassic():
    emptyScreen()
    global active
    global bg
    bg = pg.image.load("images/classic/background.png")
    active = True
    aiScore = 0
    playerScore = 0
    global mode
    mode = "classic"

    unpause()
    ui.empty()
    pg.display.set_caption("classic mode!")
    paddle.add(Player())
    opponents.add(Ai())
    balls.add((Ball(4, 6)))


def menu():
    global mode, active, bg
    mode = "menu"
    active = False
    bg = pg.image.load(f"images/menu/background.png").convert()
    pause()
    pg.display.set_caption("pong")
    emptyScreen()
    play_classic= Ui("play_classic", (600, 300))
    ui.add(play_classic)

def lose():
    global active
    active = False
    emptyScreen()

    lose_screen = Ui("lose", (0,0))
    menu_button = Ui("menu", (400, 200))
    play_classic= Ui("play_classic", (600, 300))

    ui.add(lose_screen)
    ui.add(play_classic)
    ui.add(menu_button)

def win():
    global active
    active = False
    emptyScreen()
    menu_button = Ui("menu", (400, 200))
    play_classic= Ui("play_classic", (600, 300))
    win_screen = Ui("win", (0,0))
    ui.add(win_screen)
    ui.add(play_classic)
    ui.add(menu_button)

def pause():
    global paused
    paused = True

    menu_button = Ui("menu", (400, 200))
    resume_buttom = Ui("resume", (400, 275))

    ui.add(menu_button)
    ui.add(resume_buttom)
    # PONG LOGO?

def unpause():
    global paused
    paused = False
    ui.empty()


paused = False
active = False

menu()

while True:
    pg.display.update()
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYUP:
            if(event.key == K_SPACE):
                pass
            elif(event.key == K_p):
                pause()

    window.blit(bg, (0,0))

    if(not paused):
        paddle.update()
        opponents.update()
        balls.update()
        if(mode != "menu"):
            playerScoreText = large_font.render(str(playerScore), False, BLUE)
            window.blit(playerScoreText, playerScoreRect)

        if(mode == "classic"):
            aiScoreText = large_font.render(str(aiScore), False, GREEN)
            window.blit(aiScoreText, aiScoreRect)
            if(active):
                if(aiScore == 7):
                    aiScore = 0
                    playerScore = 0
                    lose()
                elif(playerScore == 7):
                    aiScore = 0
                    playerScore = 0
                    win()


    ui.update()
        
    paddle.draw(window)
    opponents.draw(window)
    balls.draw(window)
    ui.draw(window)

    FramePerSec.tick(FPS)