#!/usr/bin/env python

# IMPORTS
import pygame, sys, time, random, bres
from pygame.locals import *

# PREDEFINED COLOUR PALETTE 
black = (0, 0, 0)
grey = (200, 200, 200)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (55, 55, 255)
orange = (255, 140, 0)

# OBJECT SIZE GLOBALS
cWidth, cHeight = 0, 0 # City sizing ***set in main()***
bWidth, bHeight = 0, 0 # Missile battery sizing ***set in main()***
expRadius = 64 # Maximum explosion radius

# GAME GLOBALS
rX, rH = 0, 0 # Game resolution ***set in main()***
eventDelay = 16 # Number of milliseconds of delay before generating a USEREVENT
rateofAttack = 128 # Value for comparing against PRNG to decide when to launch a missile
attackNumber = 32 # Amount of attacks for the turn
maxAmmo = 32 # Amount of missiles the battery can hold

# OBJECTS + THEIR CONTAINERS
battery = None
cities = []

# CITY OBJECT
class city:
    def __init__(self, pos):
        # City constructor
        # Parametres: (pos) set position
        self._pos = pos
        self._top = [pos[0] + cWidth / 2, pos[1]] # Ref pos for other objects to use
        self.draw() # Draw on creation
    def draw(self):
        # Draws the city
        pygame.draw.rect(screen, grey, (self._pos[0], self._pos[1], cWidth, cHeight), 0)
    def update(self):
        # Polls for updates: NOT PRESENTLY NEEDED
        pass
    def check(self, e):
        # Checks if the city has been hit with by given explosion 
        # Parametres: (e) explosion to test bounds of
        if (sqr(e._radius) > sqr(e._pos[0] - self._top[0]) + sqr(e._pos[1] - self._top[1])):
            cities.remove(self)

# MISSILE BATTERY OBJECT
class battery:
    def __init__(self, pos):
        # Missile battery constructor
        # Parametres: (pos) set position
        self._ammo = maxAmmo
        self._pos = pos
        self._aperture = [pos[0] + bWidth / 2, pos[1]] # Ref pos for other objects to use
        self.draw() #draw object on creation
    def draw(self):
        # Draws the missile battery
        pygame.draw.rect(screen, blue, (self._pos[0], self._pos[1], bWidth, bHeight), 0)
    def update(self):
        # Polls for updates: request ammo count draw update
        drawText(str(self._ammo), (self._pos[0] + (bWidth / 3), self._pos[1] + (bHeight / 3)), 'Monospace', white) 
        pass
    def fire(self, pos):
        if (self._ammo > 0):
            self._ammo -= 1
            #createMissile(self._aperture, pos)
    def check(self, e):
        # Checks if the missile battery has been hit with by given explosion 
        # Parametres: (e) explosion to test bounds of
        if (sqr(e._radius) > sqr(e._pos[0] - self._aperture[0]) + sqr(e._pos[1] - self._aperture[1])):
            remove(self)

# UTILITY FUNCTIONS
def sqr(x):
    # Simple squaring (^2) function
    # Parametres: (x) no to square
    return x * x 

def drawText(txt, pos, font, col):
    # Attempts to draw text with given params 
    # Parametres: (txt) text contents, (pos) start pos, (font) text font, (col) text colour
    try: # Attempt to draw
        font = pygame.font.SysFont(font, 32)
        text = font.render(txt, False, col)
        screen.blit(text, pos)
    except: # Catch if desired font font is not present
        print "Cannot print text " + txt

# OBJECT CREATION FUNCTIONS
def createCities():
    # Creates 6 cities with relative to resolution positioning
    global cities
    cities += [city([((rX + cWidth) / 10) * 1, rH - cHeight])]
    cities += [city([((rX + cWidth) / 10) * 2, rH - cHeight])]
    cities += [city([((rX + cWidth) / 10) * 3, rH - cHeight])]
    cities += [city([((rX - cWidth) / 10) * 7, rH - cHeight])]
    cities += [city([((rX - cWidth) / 10) * 8, rH - cHeight])]
    cities += [city([((rX - cWidth) / 10) * 9, rH - cHeight])]

# GAME LOOP FUNCTIONS
def update():
    # Update per frame method

    # Poll for updates from game objects
    if (battery != None):
        battery.update()

    # Redraw display
    pygame.display.flip()
    pygame.time.set_timer(USEREVENT + 1, eventDelay)

def waitForEvent():
    # Actual game loop method
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            sys.exit(0)
            #firing(event.button, pygame.mouse.get_pos())
        if event.type == USEREVENT + 1:
            update()
            #createAttack() # Attempt to create an attack each turn

# MAIN
def main():
    global screen, rX, rH, cWidth, cHeight, bWidth, bHeight, battery
    pygame.init()
    random.seed()

    # Access display information to set resolution
    rX, rH = pygame.display.Info().current_w, pygame.display.Info().current_h

    # Set city and missile battery size based on resolution for scaling
    cWidth = cHeight = rX * 0.025
    bWidth = bHeight = rX * 0.05

    # Create game screen object
    screen = pygame.display.set_mode([rX, rH], pygame.FULLSCREEN)

    # Create game objects
    createCities()
    battery = battery([((rX + bWidth) / 10) * 4.5, rH - bHeight])

    # Begin game loop
    update()
    waitForEvent()

main()