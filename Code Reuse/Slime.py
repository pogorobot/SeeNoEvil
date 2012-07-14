import pygame
import random
import math
import sys
from pygame.locals import *

# Constants
FPS = 30
WIDTH = 640
HEIGHT = 480
BOXSIZE = 40
GAPSIZE = 10
BOARDWIDTH = 10
BOARDHEIGHT = 7
XMARGIN = int((WIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((HEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#colors
backgroundColour = (143, 157, 190)
boxColour = (98, 98, 98)
wallColour = (23, 0, 23)
slimedColour = (98, 255, 98)
highlightColour = (200, 200, 200)
playerColour = (240, 255, 98)


# Directions
UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)

directions = (UP, DOWN, RIGHT, LEFT)

def Chance(percent):
    return random.randint(0, 100) < percent

class Board(object):
    def __init__(self):
        self.width = BOARDWIDTH
        self.height = BOARDHEIGHT
        self.contents = []
        #Board state codes (To be replaced with Tile objects later)
        self.EMPTY = 0
        self.SLIMED = 1
        self.WALL = 2
        self.PLAYER = 7
        for rows in range(BOARDWIDTH):
            row = []
            for box in range(BOARDHEIGHT):
                if Chance(75):
                    row.append(self.EMPTY)
                else:
                    row.append(self.WALL)
            self.contents.append(row)
    def boxInRange(self, (boxx, boxy)):
        if boxx == None: return False
        if boxy == None: return False
        if boxx >= self.width: return False
        if boxy >= self.height: return False
        if boxx < 0: return False
        if boxy < 0: return False
        return True
    def empty(self, (boxx, boxy)):
        if not self.boxInRange((boxx, boxy)): return False
        return self.contents[boxx][boxy] == self.EMPTY
    def slimed(self, (boxx, boxy)):
        if not self.boxInRange((boxx, boxy)): return False
        return self.contents[boxx][boxy] == self.SLIMED
    def clear(self, (boxx, boxy)):
        self.contents[boxx][boxy] = self.EMPTY
    def draw(self):
        for boxx in range(self.width):
            for boxy in range(self.height):
                left, top = leftTopCoordsOfBox(boxx, boxy)
                if self.contents[boxx][boxy] == self.EMPTY:
                    pygame.draw.rect(screen, boxColour, (left, top, BOXSIZE, BOXSIZE))
                elif self.contents[boxx][boxy] == self.SLIMED:
                    pygame.draw.rect(screen, slimedColour, (left, top, BOXSIZE, BOXSIZE))
                elif self.contents[boxx][boxy] == self.WALL:
                    pygame.draw.rect(screen, wallColour, (left, top, BOXSIZE, BOXSIZE))
                elif self.contents[boxx][boxy] == self.PLAYER:
                    pygame.draw.rect(screen, playerColour, (left, top, BOXSIZE, BOXSIZE))
                else: assert False, 'WTF? Wrong input to Board.draw()'
    def slime(self, (boxx, boxy)):
        if boxx != None:
            if boxy != None:
                if self.empty((boxx, boxy)):
                    self.contents[boxx][boxy] = self.SLIMED
    def movePlayerTo(self, (boxx, boxy)):
        self.contents[boxx][boxy] = self.PLAYER
        
class Player(object):
    def __init__(self, board):
        self.board = board
        #Find a random empty spot on the board to spawn the Player.
        empty = False
        while not empty:
            self.xpos = random.randint(0, board.width-1)
            self.ypos = random.randint(0, board.height-1)
            empty = board.empty((self.xpos, self.ypos))
        board.movePlayerTo((self.xpos, self.ypos))
    def moveTo(self, (newX, newY)):
        if self.board.empty((newX, newY)):
            self.board.clear((self.xpos, self.ypos))
            self.board.slime((self.xpos, self.ypos))
            self.board.movePlayerTo((newX, newY))
            self.xpos, self.ypos = (newX, newY)
    def move(self, (dx, dy)):
        newX, newY = (self.xpos + dx, self.ypos + dy)
        if self.board.empty((newX, newY)):
            self.moveTo((newX, newY))
            return
        if self.board.slimed((newX, newY)):
            self.slide((dx, dy))
    def slide(self, (dx, dy)):
        newX, newY = (self.xpos + dx, self.ypos + dy)
        while self.board.slimed((newX, newY)):
            self.board.clear((newX, newY))
            self.moveTo((newX, newY))
            newX, newY = (newX + dx, newY + dy)
        self.moveTo((newX, newY))
        
class Enemy(Player):
    timeToNextMove = 1.0 # in seconds, variable
    timer = 0
    def tick(self):
        self.timer = self.timer + 1
        if self.timer / FPS >= self.timeToNextMove:
            self.moveAround()
            self.timer = 0
    def moveAround(self):
        self.move(random.choice(directions))
        
        
        

mainBoard = Board()
avatar = Player(mainBoard)
randomWalker = Enemy(mainBoard)

def drawBoard(board):
    board.draw()

def leftTopCoordsOfBox(boxx, boxy):
    #convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def main():
    global fpsclock, screen
    pygame.init()
    fpsclock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    mousex = 0
    mousey = 0
    pygame.display.set_caption('Sliiiime')
    
    running = True
    mouseClicked = False
    while running:
        screen.fill(backgroundColour)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            elif event.type == KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    avatar.move(RIGHT)
                if event.key == pygame.K_LEFT:
                    avatar.move(LEFT)
                if event.key == pygame.K_UP:
                    avatar.move(UP)
                if event.key == pygame.K_DOWN:
                    avatar.move(DOWN)
                    
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if mouseClicked:
            avatar.moveTo(getBoxAtPixel(mousex, mousey))
            mouseClicked = False
        randomWalker.tick()
        drawBoard(mainBoard)
        pygame.display.flip()
        fpsclock.tick(FPS)
    
if __name__ == '__main__':
    main()