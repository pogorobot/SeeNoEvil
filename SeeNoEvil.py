import pygame, random, math, sys, os
from pygame.locals import *

# Constants
fps = 30
width = 660
height = 480
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
                elif event.type == KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.environment.player.walkRight()
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.environment.player.walkLeft()
            self.environment.draw()
            pygame.display.flip()
            fpsclock.tick(fps)
        
class Cave(object):
    def __init__(self):
        self.width = width
        self.height = height
        self.ceiling = [] #ceiling is a list of points that we'll use to create an irregular cave
        self.floor = []   #floor will cover the bottom
        self.backgroundColor = (0, 0, 0)
        self.tileSize = 15 #how many stalactites we draw
        for i in range((self.width / self.tileSize) + 1):
            self.ceiling.append((i * self.tileSize, random.randint(0, self.height / 4)))
        for i in range((self.width / self.tileSize) + 1):
            self.floor.append((i * self.tileSize, random.randint(self.height * 3 / 4, self.height)))        
        self.player = Explorer(self)
    def draw(self):
        screen.fill(self.backgroundColor)
        oldPoint = (0, 0)
        for point in self.ceiling:
            self.drawStalactiteHalf(point, oldPoint)
            oldPoint = point
        oldPoint = (0, 0)
        for point in self.floor:
            self.drawStalagmiteHalf(point, oldPoint)
            oldPoint = point
        self.player.draw()
    def drawStalactiteHalf(self, point, oldPoint):
        (x, y) = point
        if oldPoint == (0, 0):
            oldPoint = point
            return
        (leftX, leftY) = oldPoint
        if y > leftY:
            lower = leftY
            slope = 1
        else:
            lower = y
            slope = 0
        pygame.draw.rect(screen, wallColor, (leftX, 0, self.tileSize, lower))
        if slope:
            pygame.draw.polygon(screen, wallColor, [(leftX, leftY), (x, y), (x, leftY)])
        else:
            pygame.draw.polygon(screen, wallColor, [(leftX, leftY), (x, y), (leftX, y)])
    def drawStalagmiteHalf(self, point, oldPoint):
        (x, y) = point                   #set local x and y variables
        if oldPoint == (0, 0):           #load the leftmost point first
            return                       #do nothing until we have a range
        (leftX, leftY) = oldPoint        #set individual variables for the left side coordinates
        if y < leftY:                    #determine whether slope is positive or negative
            lower = leftY                #if y-coord on the right is less
            slope = 0                    #our triangle will point left
        else:
            lower = y                    #if y-coord on the right is greater or equal
            slope = 1                    #our triangle will point right
        #draw the bottom of the stalagmite - the part underneath both points
        pygame.draw.rect(screen, wallColor, (leftX, lower, self.tileSize, self.height - lower))
        #draw the triangle connecting to the next point
        if slope:                        #the triangle points right
            pygame.draw.polygon(screen, wallColor, [(leftX, leftY), (x, y), (leftX, y)])
        else:                            #the triangle points left
            pygame.draw.polygon(screen, wallColor, [(leftX, leftY), (x, y), (x, leftY)])
    def floorLevel(self, x):
        index = int(x / self.tileSize)   
        offset = x % self.tileSize
        heightDifference = self.floor[index+1][1] - self.floor[index][1]
        if offset == 0:
            height = self.floor[index][1]
        else:
            height = self.floor[index][1] + heightDifference * offset / self.tileSize
        return height
    
class Explorer(object):
    def __init__(self, cave):
        self.cave = cave
        self.x = random.randint(0, cave.width)
        self.y = cave.floorLevel(self.x)
        self.size = 10
    def draw(self):
        pygame.draw.circle(screen, dragonColor, (self.x, self.y), self.size)
    def walkLeft(self):
        self.x -= 1
        self.y = self.cave.floorLevel(self.x)
    def walkRight(self):
        slef.x += 1
        self.y = self.cave.floorLevel(self.x)

def main():
    pygame.init()
    global screen, fpsclock
    fpsclock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    game = GameInstance()

if __name__ == '__main__':
    main()