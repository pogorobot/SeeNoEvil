import pygame, random, math, sys, os
from pygame.locals import *

# Constants
FPS = 30
WIDTH = 640
HEIGHT = 480
stoneColour = (135, 135, 135)
dragonColour = (42, 42, 95)
preyColour = (255, 255, 42)
charredPreyColour = (40, 10, 0)
smokeColour = (86, 46, 8)
wallColour = (98, 45, 12)

backgroundImage = pygame.image.load("Eye of the Coyote.jpg")
backgroundImage = pygame.transform.smoothscale(backgroundImage, (WIDTH, HEIGHT))
otherBackgroundImage = pygame.image.load("The Hall of Shortcuts.jpg")
otherBackgroundImage = pygame.transform.smoothscale(otherBackgroundImage, (WIDTH, HEIGHT))

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

def typeOfObject(thing):
    return thing.__class__.__name__

def isType(thing, label):
    return typeOfObject(thing) == label

class Map(object):
    def __init__(self, adventure):
        self.width = 8
        self.height = 6
        self.rooms = []
        red = 255
        green = 250
        blue = 232
        self.colourController = ColourCycler((red, green, blue), self.height, (red - 90, green - 90, blue - 90))
        self.shieldHP = 20
        self.totalShieldHP = self.shieldHP
        self.adventure = adventure
        for columnNumber in range(self.width):
            column = []
            for roomNumber in range(self.height):
                room = Room(self, (columnNumber, roomNumber))
                room.recalibrateColours(self.colourController.getColour())
                column.append(room)
                self.colourController.play()
            self.rooms.append(column)
            self.colourController.fastForward(-self.height)
        self.x = random.randint(1, self.width-1)
        self.y = random.randint(1, self.height-1)
        self.currentRoom = self.rooms[self.x][self.y]
        self.goalRoom = self.rooms[random.randint(1, self.width-1)][random.randint(1, self.height-1)]
        self.addWalls()
        self.goalRoom.numberOfObstacles = 0
        self.goalRoom.numberOfPrey = 100
        self.goalRoom.originalNumberOfPrey = 100
        self.goalRoom.recalibrateColours((255, 240, 232))
        self.contents = []
        for i in range(self.goalRoom.numberOfPrey):
            nugget = Prey(self.goalRoom)
            nugget.getColourUnderControl(ColourCycler(preyColour, 20, charredPreyColour))
    def addWalls(self):
        for column in self.rooms:
            for room in column:
                room.addWalls()
        for column in self.rooms:
            for room in column:
                room.makeWallsConsistent()
    def changeRooms(self, (x, y)):
        if self.currentRoom == self.goalRoom: #If you're leaving the goal room..
            (x, y) = self.pickARoom()
        if 0 <= x and x < len(self.rooms):
            if 0 <= y and y < len(self.rooms[1]):
                self.x = x
                self.y = y
                self.rooms[self.x][self.y].player = self.currentRoom.player
                self.currentRoom = self.rooms[self.x][self.y]
                self.currentRoom.contents.append(self.currentRoom.player)
    def changeRoomsRandomly(self):
        self.changeRooms(self.pickARoom())
    def pickARoom(self):
        x = random.randint(0, self.width-1)
        y = random.randint(0, self.height-1)
        return(x, y)
    def draw(self):
        self.currentRoom.visible = True
        margin = 45.0
        widthAvailable = WIDTH - (margin * 2)
        heightAvailable = HEIGHT - (margin * 2)
        x = margin
        y = margin
        pygame.draw.rect(screen, self.currentRoom.backgroundColour, (margin - 2, margin - 2, widthAvailable + 4, heightAvailable + 4))
        xSize = (WIDTH - (2 * margin)) / self.width
        ySize = (HEIGHT - (2 * margin)) / self.height
        for column in self.rooms:
            y = margin
            for room in column:
                if room.visible:
                    pygame.draw.rect(screen, room.backgroundColour, Rect(x, y, xSize, ySize))
                if room == self.currentRoom:
                    pygame.draw.rect(screen, dragonColour, Rect(x, y, xSize, ySize))
                if room == self.goalRoom:
                    pygame.draw.rect(screen, room.backgroundColour, Rect(x, y, xSize, ySize))
                if room.visible:
                    room.drawWallsSmall(x, y, xSize, ySize)
                y += ySize
            x += xSize
    def drawShield(self):
        windowWidth = int(self.shieldHP * WIDTH / self.totalShieldHP)
        windowHeight = int(self.shieldHP * HEIGHT / self.totalShieldHP)
        leftMargin = int((WIDTH - windowWidth) / 2)
        topMargin = int((HEIGHT - windowHeight) / 2)
        mask = pygame.Surface((windowWidth, windowHeight))
        mask.blit(screen, (0, 0, windowWidth, windowHeight), (leftMargin, topMargin, windowWidth, windowHeight))
        shield = pygame.Surface((WIDTH, HEIGHT))
        shield.blit(mask, (leftMargin, topMargin, windowWidth, windowHeight))
        shield.set_alpha(255 - int(self.shieldHP * 255 / self.totalShieldHP))
        screen.blit(shield, (0, 0, WIDTH, HEIGHT))

class Room(object):
    def __init__(self, world, (x, y)):
        red = 255
        green = 240
        blue = 232
        self.backgroundColour = (red, green, blue)
        self.completedBackgroundColour = (red - 30, green - 30, blue - 25)
        self.numberOfObstacles = random.randint(0, 12)
        self.contents = []
        self.numberOfPrey = random.randint(1, 2)
        self.originalNumberOfPrey = self.numberOfPrey
        self.colourController = ColourCycler(self.backgroundColour, self.numberOfPrey, self.completedBackgroundColour)
        self.walls = []
        self.world = world
        self.x = x
        self.y = y
        self.wallThickness = random.randint(5, 20)
        self.flame = 100
        self.fullBar = 100
        self.visible = False
        self.locked = self.allPossibleWalls()
        for i in range(self.numberOfObstacles):
            obstacle = Obstacle(self)
        for obstacle in self.contents:
            if chance(60):
                obstacle.flap(random.choice(directions))
        for i in range(self.numberOfPrey):
            nugget = Prey(self)
            nugget.getColourUnderControl(ColourCycler(preyColour, 20, charredPreyColour))
        #self.hunters = []
        while chance(80):
            hunter = Hunter(self) #initialize, which also adds to contents
        #self.nests = []
        while chance(45):
            nest = Nest(self)
        while chance(60):
            bomb = Bomb(self)
        self.tieTwoThingsTogetherAtRandom()
        self.background = backgroundImage
        self.backgroundRect = self.background.get_rect()
        self.otherBackground = otherBackgroundImage
        size = (width, height) = self.background.get_size() 
        self.backgroundMask = pygame.Surface((WIDTH, HEIGHT))
    def unlocked(self):
        for item in self.contents:
            if isType(item, 'Prey'): return False
            if isType(item, 'Nest'): return False
            if isType(item, 'Hunter'):
                if item.allegiance != self.player:
                    return False
        return True
    def update(self):
        if self.player.breathingFire:
            (mousex, mousey) = self.player.breathingFire
            newFlame = Flame(self, self.player, (mousex, mousey))
            newFlame.angle += random.uniform(-math.pi / 24, math.pi / 24)
            self.contents.append(newFlame)
            newFlame.angle += random.uniform(-math.pi / 24, math.pi / 24)
            self.contents.append(newFlame)
        else:
            self.player.refuel()
        for item in self.contents:
            item.update()
        #self.player.drawFlameGauge()
        #self.world.drawShield()
    def tieTwoThingsTogetherAtRandom(self):
        one = random.randint(0, len(self.contents) - 1)
        two = random.randint(0, len(self.contents) - 1)
        while one == two:
            two = random.randint(0, len(self.contents) - 1)
        Rope(self, self.contents[one], self.contents[two])
    def addWalls(self):
        self.walls = [Wall(self, random.choice(directions), 10)]
    def drawWallsSmall(self, x, y, xSize, ySize):
        thickness = 4
        for wall in self.walls:
            direction = wall.direction
            if direction == LEFT:
                pygame.draw.rect(screen, wallColour, (x, y, thickness, ySize))
            elif direction == RIGHT:
                pygame.draw.rect(screen, wallColour, (x + xSize - thickness, y, thickness, ySize))
            elif direction == UP:
                pygame.draw.rect(screen, wallColour, (x, y, xSize, thickness))
            elif direction == DOWN:
                pygame.draw.rect(screen, wallColour, (x, y + ySize - thickness, xSize, thickness))
    def makeWallsConsistent(self):
        for wall in self.walls:
            direction = wall.direction
            thickness = self.wallThickness
            if not self.neighbor(direction).hasWall(oppositeDirection(direction)):
                self.neighbor(direction).walls.append(Wall(self.neighbor(direction), oppositeDirection(direction), thickness))
    def neighbor(self, direction):
        if direction == UP:
            if self.y < 1:
                return self.world.rooms[self.x][len(self.world.rooms[1]) - 1]
            return self.world.rooms[self.x][self.y-1]
        if direction == DOWN:
            if self.y > len(self.world.rooms[1]) - 2:
                return self.world.rooms[self.x][0]
            return self.world.rooms[self.x][self.y+1]
        if direction == RIGHT:
            if self.x > len(self.world.rooms) - 2:
                return self.world.rooms[0][self.y]
            return self.world.rooms[self.x+1][self.y]
        if direction == LEFT:
            if self.x < 1:
                return self.world.rooms[len(self.world.rooms) - 1][self.y]
            return self.world.rooms[self.x-1][self.y]
        return self
    def hasWall(self, direction):
        for wall in self.walls:
            if wall.direction == direction:
                return True
        return False
    def write(self, someText):
        labelColour = (159, 182, 205)
        textColour = (0, 0, 0)
        self.writeWithOptions(someText, screen.get_rect().centerx, screen.get_rect().centery, labelColour, textColour)
    def writeWithOptions(self, someText, centerx, centery, labelColour, textColour):
        font = pygame.font.Font(None, 17)
        text = font.render(someText, True, textColour, labelColour)
        textRect = text.get_rect()
        textRect.centerx = centerx
        textRect.centery = centery
        screen.blit(text, textRect)
        
    def draw(self):
        screen.blit(self.background, self.backgroundRect)
        self.backgroundMask.blit(self.otherBackground, self.backgroundRect)
        self.backgroundMask.set_alpha(255 * self.flame / self.fullBar)
        screen.blit(self.backgroundMask, self.backgroundRect)
        if not self.unlocked():
            for wall in self.locked:
                wall.draw()
        else:
            for wall in self.walls:
                wall.draw()
    def allPossibleWalls(self):
        walls = []
        for direction in directions:
            wall = Wall(self, direction)
            walls.append(wall)
        return walls
        
    def recalibrateColours(self, (newRed, newGreen, newBlue)):
        self.backgroundColour = (newRed, newGreen, newBlue)
        self.completedBackgroundColour = (newRed - 30, newGreen - 30, newBlue - 25)
        self.colourController = ColourCycler(self.backgroundColour, self.originalNumberOfPrey, self.completedBackgroundColour)
    def selfDestruct(self):
        self.__init__(self.world)
        
class Wall(object):
    def __init__(self, currentRoom, direction, thickness = 10):
        self.currentRoom = currentRoom
        self.direction = direction
        self.colour = wallColour
        self.currentRoom.walls.append(self)
        if direction == UP:
            oppositeDirection = DOWN
            self.rectangle = Rect(0, 0, WIDTH, thickness)
        elif direction == DOWN:
            oppositeDirection = UP
            self.rectangle = Rect(0, HEIGHT - thickness, WIDTH, thickness)
        elif direction == RIGHT:
            oppositeDirection = LEFT
            self.rectangle = Rect(WIDTH - thickness, 0, thickness, HEIGHT)
        elif direction == LEFT:
            oppositeDirection = RIGHT
            self.rectangle = Rect(0, 0, thickness, HEIGHT)
            
    def draw(self):
        pygame.draw.rect(screen, self.colour, self.rectangle)
        
class Artifact(object):
    def __init__(self, world):
        self.world = world
        self.currentRoom = world.rooms[random.randint(0, len(world.rooms) - 1)][random.randint(0, len(world.rooms[1]) - 1)]
        self.currentRoom.artifacts.append(self)
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)

class GameObject(object):
    def __init__(self, currentRoom, colour = stoneColour, size = 40):
        self.colour = colour
        self.colourController = None
        self.size = size
        self.angle = 0
        self.speed = 0
        self.thrust = 3.5
        self.stuck = 0
        self.airResistance = 10
        self.hp = 400
        self.terrain = False
        self.onLand = False
        self.currentRoom = currentRoom
        self.borderSize = 2 #thickness of outline
        self.findClearPosition()
        currentRoom.contents.append(self)
    def findClearPosition(self):
        blocking = True
        while blocking:
            blocking = False
            self.x = random.randint(0, WIDTH - self.size)
            self.y = random.randint(0, HEIGHT - self.size)
            self.refreshRectangle()
            if self.somethingInTheWay(): blocking = True
    def somethingInTheWay(self):
        for obstacle in self.currentRoom.contents:
            if obstacle.rectangle.colliderect(self.rectangle):
                return obstacle
        self.stuck = 0
        return False
    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.x - self.borderSize, self.y - self.borderSize, self.size + self.borderSize * 2, self.size + self.borderSize * 2))
        pygame.draw.rect(screen, self.colour, self.rectangle)
    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.fall()
        if not self.terrain:
            self.speed *= drag
        self.bounce()
        self.refreshRectangle()
    def explode(self):
        Shockwave(self)
        self.die()
    def bounce(self):
        if self.x > WIDTH - self.size:
            self.bounceThisWay(RIGHT)
            self.x = WIDTH - self.size
        elif self.x < 0:
            self.bounceThisWay(LEFT)
            self.x = 0
        if self.y > HEIGHT - self.size:
            self.bounceThisWay(UP)
            self.y = HEIGHT - self.size
        elif self.y < 0:
            self.bounceThisWay(DOWN)
            self.y = 0
    def bounceThisWay(self, direction):
        self.bouncing = 2
        if direction == RIGHT:
            self.angle = -self.angle
            if not self.terrain:
                self.speed *= elasticity
        if direction == LEFT:
            self.angle = -self.angle
            if not self.terrain:
                self.speed *= elasticity
        if direction == UP:
            self.angle = math.pi - self.angle
            if not self.terrain:
                self.speed *= elasticity
        if direction == DOWN:
            self.angle = math.pi - self.angle
            if not self.terrain:
                self.speed *= elasticity            
    def fall(self):
        if self.terrain: return
        (angle, speed) = gravity
        speed /= self.airResistance
        (self.angle, self.speed) = addVectors((self.angle, self.speed), (angle, speed))
    def update(self):
        self.move()
        self.draw()
        self.findCollisions()
    def findCollisions(self):
        for potential in self.currentRoom.contents:
            if potential != self:
                if potential.rectangle.colliderect(self.rectangle):
                    self.collide(potential)
    def collide(self, otherThing):
        if self == otherThing: return None
    def burn(self, heat):
        self.getHurt(heat)
    def die(self):
        if self.currentRoom.contents.count(self):
            self.currentRoom.contents.remove(self)
    def getHurt(self, pain):
        self.hp -= pain
        if self.hp < 0:
            self.die()
    def flap(self, (angle, speed)):
        if self.stuck:
            self.slippery = 1
        (self.angle, self.speed) = addVectors((self.angle, self.speed), (angle, speed * self.thrust))
    def getPushed(self, (angle, speed)):
        self.flap((angle, speed))
    def refreshRectangle(self):      
        self.rectangle = Rect(self.x, self.y, self.size, self.size) 

class Obstacle(GameObject):
    def __init__(self, currentRoom, colour = stoneColour, size = 40):
        super(Obstacle, self).__init__(currentRoom, colour, size)
        self.slippery = 0
        self.stuck = 0
        self.terrain = True
        self.bouncing = 0
        self.onFire = False
    
    def bounceAgainst(self, otherThing):
        if self.bouncing: return
        brokenEdges = []
        if self.inThisOrder(otherThing.rectangle.top, self.rectangle.bottom, otherThing.rectangle.bottom):
            brokenEdges.append(DOWN)
        if self.inThisOrder(otherThing.rectangle.left, self.rectangle.left, otherThing.rectangle.right):
            brokenEdges.append(LEFT)
        if self.inThisOrder(otherThing.rectangle.top, self.rectangle.top, otherThing.rectangle.bottom):
            brokenEdges.append(UP)
        if self.inThisOrder(otherThing.rectangle.left, self.rectangle.right, otherThing.rectangle.right):
            brokenEdges.append(RIGHT)
        if brokenEdges.count(DOWN):
            if not brokenEdges.count(UP):
                self.bounceThisWay(DOWN)
                self.rectangle.bottom = otherThing.rectangle.top
        elif brokenEdges.count(UP):
            self.bounceThisWay(UP)
            self.rectangle.top = otherThing.rectangle.bottom
        if brokenEdges.count(LEFT):
            if not brokenEdges.count(RIGHT):
                self.bounceThisWay(LEFT)
                self.rectangle.left = otherThing.rectangle.right
        elif brokenEdges.count(RIGHT):
            self.bounceThisWay(RIGHT)
            self.rectangle.right = otherThing.rectangle.left
        self.angle, self.speed = addVectors((self.angle, self.speed), (otherThing.angle, otherThing.speed))
        self.refreshFromRectangle()
    
    def refreshFromRectangle(self):
        self.x = self.rectangle.left
        self.y = self.rectangle.top
                    
  


    def getColourUnderControl(self, colourController):
        self.colourController = colourController
    def rePigment(self):
        self.colour = self.colourController.getColour()       
        
    def inThisOrder(self, first, middle, last):
        return (first < middle) and (middle < last)
                
    def stick(self):
        if self.terrain: return
        if self.somethingInTheWay():
            if self.slippery:
                self.slippery -= 1
            else:
                self.speed = 0
                self.stuck += 1
        else:
            self.slippery = 0
            
            
    def land(self):
        self.speed = math.sin(self.angle) * self.speed
        self.angle = math.pi / 2
        
    def grabWall(self):
        self.speed = math.cos(self.angle) * self.speed
        self.angle = 0


    def wrapAround(self):
        halfway = -self.size / 2
        world = self.currentRoom.world
        if self.x > WIDTH + halfway:
            if self.currentRoom.hasWall(RIGHT):
                super(Dragon, self).bounce()
            else:
                self.x = halfway
                world.changeRooms((self.currentRoom.x + 1, self.currentRoom.y))
        elif self.x < halfway:
            if self.currentRoom.hasWall(LEFT):
                super(Dragon, self).bounce()
            else:
                self.x = WIDTH + halfway
                world.changeRooms((self.currentRoom.x - 1, self.currentRoom.y))
        if self.y > HEIGHT + halfway:
            if self.currentRoom.hasWall(DOWN):
                super(Dragon, self).bounce()
            else:
                self.y = halfway
                world.changeRooms((self.currentRoom.x, self.currentRoom.y + 1))
        elif self.y < halfway:
            if self.currentRoom.hasWall(UP):
                super(Dragon, self).bounce()
            else:
                self.y = HEIGHT + halfway
                world.changeRooms((self.currentRoom.x, self.currentRoom.y - 1))
                
class Nest(Obstacle):
    def __init__(self, currentRoom):
        super(Nest, self).__init__(currentRoom)
        self.colour = self.chooseColour()
        self.size = 25
        self.refreshRectangle()
        self.hp = 900
        self.totalHP = self.hp
        self.spawnTimer = 150
        self.occupants = []
        self.totalRoom = 4
        self.borderSize = 2
        for number in range(self.totalRoom):
            self.makeOne()
    def chooseColour(self):
        red = random.randint(100, 200)
        green = random.randint(50, 150)
        blue = random.randint(0, 100)
        return (red, green, blue)
    def move(self):
        self.spawnTimer -= 1
        self.spawn()
    def burn(self, heat):
        self.hp -= heat
        self.spawnTimer -= int(heat)
        self.spawn()
        if self.hp < 0:
            self.explode()
        if self.hp < len(self.occupants) * self.totalHP / self.totalRoom:
            self.letOneOut()
    def spawn(self):
        if self.hp < 0: return None
        if self.spawnTimer < 0:
            if len(self.occupants) < self.totalRoom:
                self.makeOne()
                self.spawnTimer += 300
            else:
                self.letOneOut()
                self.spawnTimer += 300
    def makeOne(self):
        newBug = Hunter(self.currentRoom)
        newBug.x = self.rectangle.centerx
        newBug.y = self.rectangle.centery
        newBug.allegiance = self
        newBug.setColour(self.colour)
        self.currentRoom.contents.remove(newBug)
        self.occupants.append(newBug)        
    def letOneOut(self):
        if len(self.occupants) == 0:
            return None
        self.currentRoom.contents.append(self.occupants[0])
        self.occupants.remove(self.occupants[0])
    def label(self):
        self.currentRoom.writeWithOptions(str(int(self.hp)), self.rectangle.centerx, self.rectangle.centery, self.colour, (0, 0, 0))
    def draw(self):
        super(Nest, self).draw()
        self.label()
        
class Dragon(Obstacle):
    def __init__(self, currentRoom):
        super(Dragon, self).__init__(currentRoom)
        self.colour = dragonColour
        self.size = 32
        self.terrain = False
        self.thrust = 1.25
        self.stomach = []
        self.fuelTank = 1000
        self.fullBar = 150
        self.flames = self.fullBar
        self.breathingFire = False
        self.armor = 3
        currentRoom.player = self
    def update(self):
        super(Dragon, self).update()
        self.breatheFireIfTarget()
    def collide(self, target):
        if isType(target, 'Hunter'):
            self.getHurt(10)
        elif isType(target, 'Prey'):
            self.nom(target)
        elif isType(target, 'Obstacle'):
            self.bounceAgainst(target)
    def breatheFireIfTarget(self):
        targetThreshold = self.size * 7
        originalTargetThreshold = targetThreshold #to know when to stop
        for item in self.currentRoom.contents:
            if isType(item, 'Hunter'):
                if item.allegiance != self:
                    if distanceBetween(self, item) < targetThreshold:
                        self.breathingFire = item.rectangle.center
                        targetThreshold = distanceBetween(self, item)
            if isType(item, 'Nest') or isType(item, 'Bomb'):
                if item.hp < 0: continue
                if distanceBetween(self, item) < targetThreshold:
                    self.breathingFire = item.rectangle.center
                    targetThreshold = distanceBetween(self, item)
        if targetThreshold == originalTargetThreshold:
            self.breathingFire = False
    def refuel(self):
        if self.flames < self.fullBar:
            if self.fuelTank > 0:
                self.flames += 0.5
                self.fuelTank -= 0.5
    def roar(self):
        Shockwave(self)
        
    def flap(self, (angle, speed)):
        newSpeed = speed * self.thrust
        super(Dragon, self).flap((angle, newSpeed))
    def bounce(self):
        if self.currentRoom.unlocked():
            super(Dragon, self).wrapAround()
            return None
        super(Dragon, self).bounce()   
    def bounceThisWay(self, direction):
        if direction == UP or direction == DOWN:
            self.land()
        else:
            self.grabWall()
        super(Dragon, self).bounceThisWay(direction)
    def nom(self, meal):
        meal.die()
        self.stomach.append(meal)
        #self.size = math.sqrt(math.pow(self.size, 2) + meal.nutrition)
        self.size += 1
        self.thrust += 0.01
        self.fullBar = math.sqrt(math.pow(self.fullBar, 2) + meal.hp)
        self.fuelTank += meal.hp / 10
        if self.currentRoom.world.shieldHP < self.currentRoom.world.totalShieldHP:
            self.currentRoom.world.shieldHP += 1
    def stick(self):
        if self.terrain: return
        if self.somethingInTheWay():
            self.bounceAgainst(self.somethingInTheWay())
    def drawFlameGauge(self):
        self.currentRoom.flame = self.flames
        self.currentRoom.fullBar = self.fullBar
    def getHurt(self, pain):
        if self.stomach == []: return None
        freedom = self.stomach.pop()
        freedom.currentRoom = self.currentRoom
        freedom.x, freedom.y = self.rectangle.center
        freedom.speed = 20
        freedom.angle = self.angle + math.pi
        freedom.move()
        self.currentRoom.contents.append(freedom)
        self.currentRoom.colourController.fastForward(-1)
        self.size -= 0.1
        
class Animation(object):
    def __init__(self, beginning, frames, end, looping = False):
        self.beginning = beginning
        self.end = end
        self.totalFrames = frames
        self.increment = float(end - beginning) / frames
        self.onFrame = 0
        self.value = beginning
        self.looping = looping
    def constrainTimeline(self):
        if self.looping:
            self.onFrame = self.onFrame % self.totalFrames
        else:
            if self.onFrame < 0:
                self.onFrame = 0
            if self.onFrame > self.totalFrames:
                self.onFrame = self.totalFrames
    def updateValue(self):
        self.constrainTimeline() #make sure we're in bounds
        self.value = self.beginning + self.increment * self.onFrame
        return self.value
    def moveToFrame(self, frame):
        self.onFrame = frame
        return self.updateValue()
    def fastForward(self, frames):
        return self.moveToFrame(self.onFrame + frames)
    def play(self):
        return self.fastForward(1)
    
            
class ColourCycler(object):
    def __init__(self, (firstRed, firstGreen, firstBlue), frames, (finalRed, finalGreen, finalBlue)):
        self.totalFrames = frames
        self.currentFrame = 0
        self.firstRed = firstRed
        self.firstGreen = firstGreen
        self.firstBlue = firstBlue
        self.lastRed = finalRed
        self.lastGreen =  finalGreen
        self.lastBlue =  finalBlue
        self.red = firstRed
        self.green = firstGreen
        self.blue = firstBlue
        self.dRed = float(finalRed - firstRed) / frames
        self.dGreen = float(finalGreen - firstGreen) / frames
        self.dBlue = float(finalBlue - firstBlue) / frames
    def updateColour(self):
        if self.currentFrame < 0:
            self.red = self.firstRed
            self.green = self.firstGreen
            self.blue = self.firstBlue
            return self.getColour()
        if self.currentFrame > self.totalFrames:
            self.red = self.lastRed
            self.green = self.lastGreen
            self.blue = self.lastBlue
            return self.getColour()
        self.red = self.firstRed + self.dRed * self.currentFrame
        self.green = self.firstGreen + self.dGreen * self.currentFrame
        self.blue = self.firstBlue + self.dBlue * self.currentFrame
    def play(self):
        self.currentFrame += 1
        if self.currentFrame < self.totalFrames:
            self.updateColour()
        return self.getColour()
    def fastForward(self, speed):
        self.currentFrame += speed
        self.updateColour()
        return self.getColour()
    def getColour(self):
        return (self.red, self.green, self.blue)
    
class SoundWave(GameObject):
    def __init__(self, monster):
        super(SoundWave, self).__init__(monster.currentRoom)
        self.currentRoom = monster.currentRoom
        self.monster = monster
        self.origin = monster.rectangle.center
        self.timer = 0
        self.speed = 5
        self.rectangle = Rect(monster.rectangle.centerx, monster.rectangle.centery, self.timer, self.timer)
        self.timeOut = 200
        self.colour = monster.colour
    def draw(self):
        pygame.draw.circle(screen, self.colour, self.origin, self.timer, 1)
    def move(self):
        self.timer += self.speed
        self.scare()
        if self.timer > self.timeOut:
            self.die()
    def scare(self):
        for item in self.monster.currentRoom.contents:
            if isType(item, 'Prey'):
                if distanceBetween(self, item) < self.timer:
                    item.flapAwayFrom(self)
            if isType(item, 'Hunter'):
                if int(distanceBetween(self, item)) - int(self.timer) < 5:
                    item.allegiance = self.monster
                    item.flapAwayFrom(self)
                    item.setColour(self.colour)

class Shockwave(SoundWave):
    def __init__(self, source, power = 9001, speed = 10):
        super(Shockwave, self).__init__(source)
        self.source = source
        self.power = power
        self.speed = speed
    def scare(self):
        for item in self.source.currentRoom.contents:
            if item != self.source:
                if item != self:
                    if distanceBetween(self, item) < self.timer:
                        self.push(item)
    def move(self):
        self.timer += self.speed
        self.scare()
        if math.pow(self.timer, 2) > self.power * 10:
            self.die()
    def push(self, block):
        if isType(block, 'Bomb'):
            block.explode()
        dy = block.rectangle.centery - self.rectangle.centery
        dx = block.rectangle.centerx - self.rectangle.centerx
        angle = math.atan2(dx, -dy)
        if distanceBetween(self, block) == 0:
            power = 0
        else:
            power = float(self.power) / math.pow(distanceBetween(self, block), 2)
        block.getPushed((angle, power))
        block.getHurt(power)
        
class Bomb(GameObject):
    def __init__(self, currentRoom):
        super(Bomb, self).__init__(currentRoom)
        self.size = 30
        self.colour = (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50))
        self.power = 5000
    def die(self):
        Shockwave(self)
        super(Bomb, self).die()
    def burn(self, heat):
        self.explode()
        
class Rope(GameObject):
    def __init__(self, currentRoom, mother, father):
        super(Rope, self).__init__(currentRoom)
        self.mother = mother
        self.father = father
        self.setColour()
    def draw(self):
        pygame.draw.line(screen, self.colour, self.mother.rectangle.center, self.father.rectangle.center, 3.4)
    def setColour(self):
        (mRed, mGreen, mBlue) = self.mother.colour
        (fRed, fGreen, fBlue) = self.father.colour
        self.colour = ((mRed + fRed) / 2, (mGreen + fGreen) / 2, (mBlue + fBlue) / 2)
                         
            
class Prey(Obstacle):
    def __init__(self, currentRoom):
        super(Prey, self).__init__(currentRoom, preyColour, 5)
        self.speed = 0.01
        self.angle = 0
        self.timer = 0
        self.thrust = 1
        self.terrain = False
        self.flapFrequency = 3 #how many frames go by before the next flap
        self.hp = 1066
        self.nutrition = self.hp / 100
        self.skewer = None
        self.escaping = True
        self.borderSize = 1
        self.getColourUnderControl(ColourCycler(preyColour, 20, charredPreyColour))
    def flapAwayFrom(self, fear):
        maximumDistance = 100
        if distanceBetween(self, fear) > maximumDistance: return None
        dy = self.rectangle.centery - fear.rectangle.centery
        dx = self.rectangle.centerx - fear.rectangle.centerx
        angle = math.atan2(-dx, dy)
        self.flap((angle, maximumDistance - distanceBetween(self, fear)))        
    def collide(self, other):
        if isType(other, 'Dragon') or isType(other, 'Hunter'):
            self.getSkewered(other)
        elif isType(other, 'Obstacle'):
            self.bounceAgainst(other)
    def die(self):
        super(Prey, self).die()
        self.currentRoom.backgroundColour = self.currentRoom.colourController.play()
    def flapRandomly(self):
        self.timer = self.timer + 1
        weightedDirections = [UP, UP, UP, UP, LEFT, LEFT, RIGHT, RIGHT, RIGHT, DOWN]
        if self.stuck:
            self.speed /= self.stuck
        if self.timer >= self.flapFrequency:
            self.flap(random.choice(weightedDirections))
            self.timer = 0
        if self.stuck > 30:
            self.die()
    def move(self):
        if self.skewer:
            self.angle = self.skewer.angle
            self.speed = self.skewer.speed
        super(Prey, self).move()
        self.flapRandomly()
    def burn(self, heat):
        self.hp -= heat
        self.flapFrequency += heat
        if self.colourController:
            self.colourController.fastForward(heat)
        if self.hp < 0:
            self.die()
        self.rePigment()
        if self.currentRoom.world.shieldHP < self.currentRoom.world.totalShieldHP:
            self.currentRoom.world.shieldHP += 1
    def getSkewered(self, skewer):
        skewer.stomach.append(self)
        #if self.currentRoom.world.shieldHP > 0:
            #self.currentRoom.world.shieldHP -= 1
        self.die()
    def bounce(self):        
        #if self.escaping:
            #self.escape()
            #return None
        super(Prey, self).bounce()
        
    def escape(self):
        halfway = -self.size / 2
        world = self.currentRoom.world
        if self.x > WIDTH + halfway:
            self.x = halfway
            world.addToRoom(self, (self.currentRoom.x + 1, self.currentRoom.y))
            self.die()
                    #self.currentRoom.selfDestruct()
        elif self.x < halfway:
            self.x = WIDTH + halfway
            world.addToRoom(self, (self.currentRoom.x - 1, self.currentRoom.y))
            self.die()
                    #self.currentRoom.selfDestruct()
        if self.y > HEIGHT + halfway:
            self.y = halfway
            world.addToRoom(self, (self.currentRoom.x, self.currentRoom.y + 1))
            self.die()
                    #self.currentRoom.selfDestruct()
        elif self.y < halfway:
            self.y = HEIGHT + halfway
            world.addToRoom(self, (self.currentRoom.x, self.currentRoom.y - 1))
            self.die()
    
class Hunter(Prey):
    def __init__(self, currentRoom):
        super(Hunter, self).__init__(currentRoom)
        self.allegiance = currentRoom
        self.target = None
        self.chooseTarget()
        self.beakLength = self.size * 3
        self.beakX = self.x
        self.beakY = self.y
        self.setColour((120, 29, 25)) #put colour under a cycler so it can change with burning
        self.hp = 42
        self.onFire = False
        self.escaping = False
        self.stomach = []
    def setColour(self, colour):
        self.colour = colour
        self.getColourUnderControl(ColourCycler(self.colour, self.hp, (64, 0, 0)))
    def setTarget(self, potential):
        dy = math.fabs(potential.y - self.y)
        dx = math.fabs(potential.x - self.x)
        newDistance = math.sqrt(math.pow(dy, 2) + math.pow(dx, 2))
        if newDistance < self.distance:
            self.target = potential
            self.distance = newDistance
    def chooseTarget(self):
        #targetColour = (129, 220, 125, 100)
        self.distance = WIDTH * HEIGHT
        if self.allegiance == self.currentRoom:
            for potential in self.currentRoom.contents:
                if isType(potential, 'Prey'):
                    self.setTarget(potential)
        else:
            if self.allegiance == self:
                for potential in self.currentRoom.contents:
                    if isType(potential, 'Dragon'):
                        self.setTarget(potential)
            for potential in self.currentRoom.contents:
                if isType(potential, 'Hunter'):
                    if potential.allegiance != self.allegiance:
                        self.setTarget(potential)
        if self.distance == WIDTH * HEIGHT:
            self.allegiance = self
            return self.chooseTarget()
                    
        #pygame.draw.circle(screen, targetColour, self.target.rectangle.center, self.target.size * 2)
        return self.target
    def draw(self):
        self.beakX = self.x + (math.sin(self.angle) * self.beakLength)
        self.beakY = self.y - (math.cos(self.angle) * self.beakLength)
        pygame.draw.line(screen, self.colour, (self.x, self.y), (self.beakX, self.beakY))
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), int(self.size))
        if len(self.stomach) > 0:
            bug = self.stomach[0]
            bug.rectangle.center = self.rectangle.center
            bug.refreshFromRectangle()
            bug.draw()
    def chase(self):
        if not self.chooseTarget(): return None
        dy = self.target.y - self.beakY
        dx = self.target.x - self.beakX
        angle = math.atan2(dx, -dy)
        self.flap((angle, self.thrust))
    def move(self):
        super(Hunter, self).move()
        self.chase()
    def die(self):
        super(Hunter, self).die()
        #for bug in self.stomach:
            #(bug.x, bug.y) = self.rectangle.center
            #self.currentRoom.contents.append(bug)

class Flame(Obstacle):
    def __init__(self, currentRoom, player, (mousex, mousey)):
        super(Flame, self).__init__(currentRoom)
        self.x, self.y = player.rectangle.center
        dx = mousex - self.x
        dy = mousey - self.y
        self.angle = math.atan2(dx, -dy)
        self.size = float(player.size) / 4
        self.rectangle.center = (self.x, self.y)
        self.speed = 7 + self.size
        self.heat = self.size * 2
        self.source = player
        flameColour = (random.randint(175, 230), random.randint(100, 175), random.randint(0, 10))
        super(Flame, self).getColourUnderControl(ColourCycler(flameColour, self.heat, smokeColour))
        self.colour = self.colourController.getColour()
        #player.flames -= 1
        if player.flames < 1:
            player.breathingFire = False
    def move(self):
        super(Flame, self).move()
        self.heat -= 1
        if self.heat < 1:
            self.die()
        self.colourController.play()
        self.rePigment()
    def draw(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size)
    def collide(self, other):
        if other != self:
            if other != self.source:
                if not isinstance(other, SoundWave):
                    other.burn(self.heat)
            

class GameInstance(object):
    def __init__(self):
        self.mousex = 0
        self.mousey = 0
        pygame.display.set_caption('Dragon vs. Coyote')
        self.running = True
        self.mouseClicked = False
        self.world = Map(self)
        self.startingX = random.randint(0, self.world.width - 1)
        self.startingY = random.randint(0, self.world.height - 1)
        self.currentRoom = self.world.currentRoom
        self.player = Dragon(self.currentRoom)
        self.Run()
    def Run(self):
        while self.running:
            self.runMountainMode()
            pygame.display.flip()
            fpsclock.tick(FPS)
    def runMountainMode(self):
        self.currentRoom = self.world.currentRoom
        self.player.currentRoom = self.world.currentRoom
        self.currentRoom.draw()
        self.world.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.flap(RIGHT)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.flap(LEFT)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.flap(UP)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.flap(DOWN)
                if event.key == pygame.K_r:
                    self.player.roar()
            #elif event.type == MOUSEBUTTONUP:
            #    self.player.breathingFire = pygame.mouse.get_pos()
            #elif event.type == MOUSEMOTION:
            #    self.player.breathingFire = pygame.mouse.get_pos()
        self.currentRoom.update()

def main():
    pygame.init()
    global screen, fpsclock
    fpsclock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = GameInstance()

if __name__ == '__main__':
    main()