import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    width = 500
    def __init__(self,start,color=(255,0,0)):
        self.pos = start
        self.color = color
        
    def move(self, x, y):
        self.pos = (self.pos[0] + x, self.pos[1] + y)  # change our position
    
    def draw(self, surface):
        dis = self.width // self.rows  # Width/Height of each cube
        i = self.pos[0] # Current row
        j = self.pos[1] # Current Column

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        # By multiplying the row and column value of our cube by the width and height of each cube we can determine where to draw it


def move(cube_list):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            #Key Event
            if keys[pygame.K_UP]:
                cube_list[0].move(0, -1)
                
            if keys[pygame.K_LEFT]:
                cube_list[0].move(-1, 0)

            if keys[pygame.K_DOWN]:
                cube_list[0].move(0, 1)

            if keys[pygame.K_RIGHT]:
                cube_list[0].move(1, 0)
                    
            if keys[pygame.K_w]:
                cube_list[1].move(0, -1)
                
            if keys[pygame.K_a]:
                cube_list[1].move(-1, 0)

            if keys[pygame.K_s]:
                cube_list[1].move(0, 1)
            
            if keys[pygame.K_d]:
                cube_list[1].move(1, 0)
            


def drawGrid(surface):
    sizeBtwn = width // rows  # Gives us the distance between the lines

    x = 0  # Keeps track of the current x
    y = 0  # Keeps track of the current y
    for l in range(rows):  # We will draw one vertical and one horizontal line each loop
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,width))
        pygame.draw.line(surface, (255,255,255), (0,y),(width,y))
        

def redrawWindow(surface):
    global width, rows
    surface.fill((0,0,0))  # Fills the screen with black

    drawGrid(surface)  # Will draw our grid lines
    for i in range(len(cube_list)):
        cube_list[i].draw(surface)
        snack_list[i].draw(surface)
    pygame.display.update()  # Updates the screen

def randomSnack(rows):
    x = random.randrange(rows)
    y = random.randrange(rows)
    return x, y

def item_sensor(cube, item):     #Sensor

    input_layer = [0,0,0,0]
    output_layer = ["Up","Left","Down","Right"]

    for i in range(1, 6):                  #find_item
        if cube.pos[1] > item.pos[1]:
            input_layer[0] = cube.pos[1] - item.pos[1]
        if cube.pos[0] > item.pos[0]:
            input_layer[1] = cube.pos[0] - item.pos[0]
        if cube.pos[1] < item.pos[1]:
            input_layer[2] = item.pos[1] - cube.pos[1]
        if cube.pos[0] < item.pos[0]:
            input_layer[3] = item.pos[0] - cube.pos[0]

    
    if output_layer[input_layer.index(max(input_layer))] == "Up":
        cube.move(0, -1)
    elif output_layer[input_layer.index(max(input_layer))] == "Left":
        cube.move(-1, 0)
    elif output_layer[input_layer.index(max(input_layer))] == "Down":
        cube.move(0, 1)
    elif output_layer[input_layer.index(max(input_layer))] == "Right":
        cube.move(1, 0)
    


def main(): 
    global width, rows, cube_list, snack_list
    width = 500  # Width of our screen
    height = 500  # Height of our screen
    rows = 20  # Amount of rows

    win = pygame.display.set_mode((width, height))  # Creates our screen object
    cube_list = []
    snack_list = []

    cube1 = cube((10,10), (255,0,0))  # Creates a snake object which we will code later
    cube2 = cube((10,11), (0,255,0))
    cube3 = cube((10,12), (0,0,255))
    cube4 = cube((10,13), (255,255,0))
    cube_list.append(cube1)
    cube_list.append(cube2)
    cube_list.append(cube3)
    cube_list.append(cube4)
    snack1 = cube(randomSnack(rows), color=(150,0,0))
    snack2 = cube(randomSnack(rows), color=(0,150,0))
    snack3 = cube(randomSnack(rows), color=(0,0,150))
    snack4 = cube(randomSnack(rows), color=(150,150,0))
    snack_list.append(snack1)
    snack_list.append(snack2)
    snack_list.append(snack3)
    snack_list.append(snack4)
    clock = pygame.time.Clock() # creating a clock object

    
    flag = True
    
    # STARTING MAIN LOOP
    while flag:
        pygame.time.delay(50)  # This will delay the game so it doesn't run too quickly
        clock.tick(10)  # Will ensure our game runs at 10 FPS
        move(cube_list)
        redrawWindow(win)  # This will refresh our screen
        for i in range(len(cube_list)):
            item_sensor(cube_list[i], snack_list[i])
        #Collision Check
        if cube_list[0].pos == snack_list[0].pos:
            snack_list[0] = cube(randomSnack(rows), color=(150,0,0))
        if cube_list[1].pos == snack_list[1].pos:
            snack_list[1] = cube(randomSnack(rows), color=(0,150,0))
        if cube_list[2].pos == snack_list[2].pos:
            snack_list[2] = cube(randomSnack(rows), color=(0,0,150))
        if cube_list[3].pos == snack_list[3].pos:
            snack_list[3] = cube(randomSnack(rows), color=(150,150,0))

main()
