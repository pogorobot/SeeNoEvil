# Haunted Cave
# Meant to be a prototype for See No Evil
# Exploring monster AI
# Rough concept:
# You are a ghost, haunting a cave
# This cave is full of monsters
# Some of these monsters will chase you, but they cannot hurt you in any way
# Get them to murder each other !!

import pygame, random, math, sys, os
from pygame.locals import *

FPS = 30
WIDTH = 640
HEIGHT = 480

GRAVITY = (math.pi, 0.8)

UP = (0, 1)
RIGHT = (math.pi / 2, 1)
DOWN = (math.pi, 1)
LEFT = (3 * math.pi / 2, 1)
directions = [UP, DOWN, LEFT, RIGHT]

#utility function, for example to fall add current velocity to GRAVITY
def addVectors((angle1, length1), (angle2, length2)):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)

def chance(percent):
    return random.randint(0, 100) < percent

#depends on both things having a 'center'
def distanceBetween(firstThing, target):
    (x, y) = firstThing.center
    (otherX, otherY) = target.center
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

#Game objects store all the fiddly bits that make everything run
class Game(object):
    def __init__(self):
        pygame.display.set_caption('Haunted Cave')
        self.cave = Cave()
        self.player = Ghost()
        self.cave.population.append(self.player)
        self.running = True
        self.Run()
    def Run(self):
        while self.running:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.flap(RIGHT)
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.flap(LEFT)
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.flap(UP)
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player.flap(DOWN)
            self.cave.update()
            self.cave.draw()
            pygame.display.flip()
            fpsclock.tick(FPS)
        
#Ghost objects, player-controlled, float through everything and are very simple.
class Ghost(object):
    def __init__(self):
        self.width = 25
        self.height = 25
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.color = (120, 200, 250)
        self.center = (self.x, self.y)
        self.rectangle = Rect(0, 0, self.width, self.height)
        self.rectangle.center = self.center
        self.angle = 0
        self.speed = 0
    #change velocity in a direction
    def flap(self, (angle, speed)): 
        (self.angle, self.speed) = addVectors((self.angle, self.speed), (angle, speed))
    #continue with present momentum
    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
    #master function, entry point to everything done in every loop
    def update(self):
        self.move()
        self.center = (self.x, self.y)
        self.rectangle.center = self.center
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rectangle)

#Cave object, holds everything else within it. Scrolls across multiple screens
class Cave(object):
    def __init__(self):
        self.width = WIDTH #just one screen size for now
        self.height = HEIGHT
        self.backgroundColor = (100, 67, 68)
        self.terrain = []
        self.population = []
    def update(self):
        for creature in self.population:
            creature.update()
    def draw(self):
        screen.fill(self.backgroundColor)
        for item in self.terrain:
            item.draw()
        for creature in self.population:
            creature.draw()

#Wall object, really just a big fat obstacle. Can be floated through by player

    
def main():
    pygame.init()
    global screen, fpsclock
    fpsclock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game()
    
if __name__ == '__main__':
    main()