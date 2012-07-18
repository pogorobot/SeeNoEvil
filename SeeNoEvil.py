import pygame, random, math, sys, os
from pygame.locals import *

# Constants
fps = 30
width = 540
height = 720
stoneColor = (135, 135, 135)
dragonColor = (42, 42, 95)
preyColor = (255, 255, 42)
charredPreyColor = (40, 10, 0)
smokeColor = (86, 46, 8)
wallColor = (98, 45, 12)


gravity = (math.pi, 0.8) #pixels per frame per frame
drag = 0.999
elasticity = 0.8


# Directions
UP = (0, 1)
RIGHT = (math.pi / 2, 1)
DOWN = (math.pi, 1)
LEFT = (3 * math.pi / 2, 1)

directions = [UP, DOWN, LEFT, RIGHT]

def addVectors((angle1, length1), (angle2, length2)):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)

def chance(percent):
    return random.randint(0, 100) < percent

def distanceBetween(firstThing, target):
    (x, y) = firstThing.rectangle.center
    (otherX, otherY) = target.rectangle.center
    return math.sqrt(math.pow(x - otherX, 2) + math.pow(y - otherY, 2))

def oppositeDirection(direction):
    if direction == UP:
        return DOWN
    if direction == DOWN:
        return UP
    if direction == RIGHT:
        return LEFT
    if direction == LEFT:
        return RIGHT
    return None 
    

class GameInstance(object):
    def __init__(self):
        self.mousex = 0
        self.mousey = 0
        self.environment = Cave()
        pygame.display.set_caption('See No Evil')
        self.running = True
        self.Run()
    def Run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.environment.draw()
            pygame.display.flip()
            fpsclock.tick(fps)
        
class Cave(object):
    def __init__(self):
        self.width = width
        self.height = height
        self.ceiling = [] #ceiling is a list of points that we'll use to create an irregular cave
        self.backgroundColor = (0, 0, 0)
        for i in range(self.width / 30):
            self.ceiling.append((i * 30, random.randint(0, self.height / 4)))
    def draw(self):
        screen.fill(self.backgroundColor)
        oldPoint = (0, 0)
        lower = 0
        for point in self.ceiling:
            (x, y) = point
            if oldPoint == (0, 0):
                oldPoint = point
                continue
            (leftX, leftY) = oldPoint
            if y > leftY:
                lower = leftY
                slope = 1
            else:
                lower = y
                slope = 0
            pygame.draw.rect(screen, wallColor, (leftX, 0, 30, lower))
            if slope:
                pygame.draw.polygon(screen, wallColor, [(leftX, leftY), (x, y), (x, leftY)])
            else:
                pygame.draw.polygon(screen, wallColor, [(leftX, leftY), (x, y), (leftX, y)])
            oldPoint = point
        

def main():
    pygame.init()
    global screen, fpsclock
    fpsclock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    game = GameInstance()

if __name__ == '__main__':
    main()