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
DRAG = 0.99

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
        self.player = Ghost(self.cave)
        self.cave.population.append(self.player)
        self.cave.population.append(Flyer(self.cave, self.player)) #add an enemy
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
            self.cave.trackCamera(self.player)
            self.cave.draw()
            pygame.display.flip()
            fpsclock.tick(FPS)
        
#Ghost objects, player-controlled, float through everything and are very simple.
class Ghost(object):
    def __init__(self, cave):
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
        self.drag = 1 #drag coefficient. Ghosts are frictionless.
        self.cave = cave
    #change velocity in a direction
    def flap(self, (angle, speed)): 
        (self.angle, self.speed) = addVectors((self.angle, self.speed), (angle, speed))
    #continue with present momentum
    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        #bounce off walls
        if self.x < self.width / 2 or self.x > self.cave.width - self.width / 2:
            self.angle = -self.angle
        if self.y < self.height / 2 or self.y > self.cave.height - self.height / 2:
            self.angle = math.pi - self.angle
        #slow down
        self.speed *= self.drag
    #master function, entry point to everything done in every loop
    def update(self):
        self.move()
        self.center = (self.x, self.y)
        self.rectangle.center = self.center
    def draw(self):
        pygame.draw.rect(self.cave.canvas, self.color, self.rectangle)
        
class Flyer(Ghost):
    def __init__(self, cave, target):
        super(Flyer, self).__init__(cave)
        self.target = target
        self.topSpeed = 20
        self.turningRadius = math.pi / 18
    
    def update(self):
        #self.flap(random.choice(directions))
        self.chase(self.target)
        if self.speed > self.topSpeed:
            self.speed = self.topSpeed
        super(Flyer, self).update()
    def chase(self, target):        
        dy = self.target.y - self.y
        dx = self.target.x - self.x
        angle = math.atan2(dx, -dy)
        self.angle = angle
        self.flap((self.angle, 1))
        

#Cave object, holds everything else within it. Scrolls across multiple screens
class Cave(object):
    def __init__(self):
        self.width = WIDTH * 2
        self.height = HEIGHT * 2
        self.backgroundColor = (100, 67, 68)
        self.terrain = []
        self.population = []
        backgroundImage = pygame.image.load("Eye of the Coyote.jpg")
        self.backgroundImage = pygame.transform.smoothscale(backgroundImage, (self.width, self.height))
        self.camera = (WIDTH / 2, HEIGHT / 2)
        self.canvas = pygame.Surface((self.width, self.height))
    def update(self):
        for creature in self.population:
            creature.update()
    def trackCamera(self, target):
        (x, y) = self.camera
        if target.x < self.width - (WIDTH / 2):
            if target.x > WIDTH / 2:
                x = target.x
        if target.y < self.height - (HEIGHT / 2):
            if target.y > HEIGHT / 2:
                y = target.y
        self.camera = (x, y)
    def draw(self):
        self.canvas.blit(self.backgroundImage, (0, 0))
        for item in self.terrain:
            item.draw()
        for creature in self.population:
            creature.draw()
        screen.blit(self.canvas, (0, 0), (self.camera[0] - (WIDTH / 2), self.camera[1] - (HEIGHT / 2), WIDTH, HEIGHT))

#Wall object, really just a big fat obstacle. Can be floated through by player

    
def main():
    pygame.init()
    global screen, fpsclock
    fpsclock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game()
    
if __name__ == '__main__':
    main()