import pygame as pg
import sys
from pygame.locals import *
import random, time

# HELLO THIS IS A COMMENT

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

playerScore = 0
aiScore = 0
mode = "menu"
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
    def __init__(self, left = True):
        super().__init__()
        self.image = pg.image.load("images/classic/paddle.png").convert()
        if(left): self.rect = self.image.get_rect(midleft = (0, 360))
        else: self.rect = self.image.get_rect(midright = (width, 360))
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
        self.init_vel_x = init_vel_x
        self.vel_x = init_vel_x
        self.vel_y = init_vel_y
        self.image = pg.image.load("images/classic/ball.png")
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height/2)
        ballList.append(self)

    def update_pos(self):
        global mode
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if(pg.sprite.spritecollide(self, paddle, False)or pg.sprite.spritecollide(self, opponents, False)):
            self.vel_x = -(self.vel_x*1.1)
            self.rect.x += self.vel_x

        elif(self.rect.left >= width):
            global playerScore
            if(mode == "classic"):
                playerScore += 1
                time.sleep(1)
                self.vel_x = self.init_vel_x
                self.rect.center = (width/2, height/2)
            elif(mode == "single"):
                 lose()

        elif(self.rect.right <= 0):
            global aiScore
            if(mode == "classic"):
                aiScore += 1
                time.sleep(1)
                self.vel_x = self.init_vel_x
                self.rect.center = (width/2, height/2)
            elif(mode == "single"):
                lose()

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
            elif(self.type == "play_single"): loadSingle()
            elif(self.type == "menu"): menu()
            elif(self.type == "resume"): unpause()
            else: pass

    def update(self):
        self.test_for_click()

small_font = pg.font.Font(None, 50)
large_font = pg.font.Font(None, 400)

paddle = pg.sprite.Group()

opponents = pg.sprite.Group()
balls = pg.sprite.Group()
ui = pg.sprite.Group()
bricks = pg.sprite.Group()
powers = pg.sprite.Group()

bg = pg.image.load(f"images/menu/background.png").convert()

playerScoreRect = pg.rect.Rect(200, 225, 100, 100)
aiScoreRect = pg.rect.Rect(950, 225, 100, 100)


def emptyScreen():
    paddle.empty()
    opponents.empty()
    balls.empty()
    ballList.clear()
    ui.empty()
    bricks.empty()

def loadClassic():
    global bg, mode
    emptyScreen()
    bg = pg.image.load("images/classic/background.png")
    aiScore = 0
    playerScore = 0
    mode = "classic"

    unpause()
    ui.empty()
    pg.display.set_caption("classic mode!")
    paddle.add(Player())
    opponents.add(Ai())
    balls.add((Ball(4, 6)))

def loadSingle():
    global bg, mode
    mode = "single"
    emptyScreen()
    bg = pg.image.load(f"images/{mode}/background.png")
    pg.display.set_caption("single mode!")
    global playerScoreRect
    playerScoreRect = pg.rect.Rect(560, 225, 100, 100)
    paddle.add(Player())
    paddle.add(Player(left = False))
    balls.add(Ball(4, 6))
    unpause()



def menu():
    global mode, bg
    mode = "menu"
    bg = pg.image.load(f"images/menu/background.png").convert()
    pause()
    pg.display.set_caption("pong")
    emptyScreen()
    play_classic= Ui("play_classic", (600, 300))
    play_single = Ui("play_single", (400, 300))
    ui.add(play_classic)
    ui.add(play_single)

def lose():
    global mode
    emptyScreen()

    lose_screen = Ui("lose", (0,0))
    menu_button = Ui("menu", (400, 200))
    play = Ui(f"play_{mode}", (600, 300))

    ui.add(lose_screen)
    ui.add(play)
    ui.add(menu_button)

def win():
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

            if(aiScore == 7):
                aiScore = 0
                playerScore = 0
                lose()
            elif(playerScore == 7):
                aiScore = 0
                playerScore = 0
                win()

        if(mode == "single"):
            pass

    ui.update()
        
    paddle.draw(window)
    opponents.draw(window)
    balls.draw(window)
    ui.draw(window)

    FramePerSec.tick(FPS)