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
        self.running = True
        self.Run()
    def Run(self):
        while self.running:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False            
            pygame.display.flip()
            fpsclock.tick(FPS)
        
#Ghost objects, player-controlled, float through everything and are very simple.

#Cave object, holds everything else within it. Scrolls across multiple screens

#Wall object, really just a big fat obstacle. Can be floated through by player

    
def main():
    pygame.init()
    global screen, fpsclock
    fpsclock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game()
    
if __name__ == '__main__':
    main()