import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


width = 500  # Width of our screen
height = 500  # Height of our screen
rows = 20  # Amount of rows

odd = random.random() / 2 + 0.5

#Create List
snake_list = []
snack_list = []
block_list = [] #Global block pos

#Color DB
color_snack = [(127,0,0),(0,127,0),(0,0,127),(127,127,0)]
color_snake = [(255,0,0),(0,255,0),(0,0,255),(255,255,0)]



class cube(object):
    def __init__(self,start,color):
        self.pos = start
        self.color = color
        self.hp = 100
        block_list.append(start)
        
    def move(self, x, y):
        block_list.remove(self.pos)
        #print(block_list)
        self.pos = (self.pos[0] + x, self.pos[1] + y)  # change our position
        block_list.append(self.pos)
        #print(block_list)
    
    def draw(self, surface):
        dis = width // rows  # Width/Height of each cube
        i = self.pos[0] # Current row
        j = self.pos[1] # Current Column

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        # By multiplying the row and column value of our cube by the width and height of each cube we can determine where to draw it



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
    surface.fill((0,0,0))  # Fills the screen with black

    drawGrid(surface)  # Will draw our grid lines
    for i in range(len(snake_list)):
        snake_list[i].draw(surface)
        snack_list[i].draw(surface)
    pygame.display.update()  # Updates the screen

def randomPos(rows):
    x = random.randrange(rows)
    y = random.randrange(rows)
    return x, y

def item_sensor(cube, item):     #Sensor

    input_layer = [0,0,0,0]
    output_layer = ["Up","Left","Down","Right"]

    #Find_item
    if cube.pos[1] > item.pos[1]:
        input_layer[0] = cube.pos[1] - item.pos[1]
    if cube.pos[0] > item.pos[0]:
        input_layer[1] = cube.pos[0] - item.pos[0]
    if cube.pos[1] < item.pos[1]:
        input_layer[2] = item.pos[1] - cube.pos[1]
    if cube.pos[0] < item.pos[0]:
        input_layer[3] = item.pos[0] - cube.pos[0]

    
    for i in range(len(block_list)):
        if cube.pos[1] + 1 == block_list[i][1]:
            input_layer[0] -= (cube.pos[1] - block_list[i][1]) * odd
        if cube.pos[0] + 1 == block_list[i][0]:
            input_layer[1] -= (cube.pos[0] - block_list[i][0]) * odd
        if cube.pos[1] - 1 == block_list[i][1]:
            input_layer[2] -= (block_list[i][1] - cube.pos[1]) * odd
        if cube.pos[0] - 1 == block_list[i][0]:
            input_layer[3] -= (block_list[i][0] - cube.pos[0]) * odd
    '''
    for i in range(len(block_list)):
        if cube.pos == block_list[i]:
    '''

    #print(input_layer)
    
    


    if output_layer[input_layer.index(max(input_layer))] == "Up":
        cube.move(0, -1)
    elif output_layer[input_layer.index(max(input_layer))] == "Left":
        cube.move(-1, 0)
    elif output_layer[input_layer.index(max(input_layer))] == "Down":
        cube.move(0, 1)
    elif output_layer[input_layer.index(max(input_layer))] == "Right":
        cube.move(1, 0)
    


def main(): 
    global odd
    # Creates Screen
    win = pygame.display.set_mode((width, height))  

    #Snack
    for i in range(4):
        snake_list.append(cube(randomPos(rows),color_snake[i]))
    #Snake
    for i in range(4):
        snack_list.append(cube(randomPos(rows),color_snack[i]))


    #Creating a clock object
    clock = pygame.time.Clock() 
    
    flag = True

    
    ### STARTING MAIN LOOP ###
    
    while flag:
        pygame.time.delay(50)  # This will delay the game so it doesn't run too quickly
        clock.tick(10)  # Will ensure our game runs at 10 FPS


        
        
        #Create Sensor
        for i in range(len(snake_list)):
            item_sensor(snake_list[i], snack_list[i])
            
        #Collision Check
        for i in range(4):
            snake_list[i].hp -= 1
            if snake_list[i].hp <= 0:
                print(odd)
                odd = random.random() / 2 + 0.5
                snake_list[i] = cube(randomPos(rows), color_snake[i])
            if snake_list[i].pos == snack_list[i].pos:
                snake_list[i].hp = 100
                snack_list[i] = cube(randomPos(rows), color_snack[i])
                block_list.remove(snack_list[i].pos)

        redrawWindow(win)  # This will refresh our screen

        #End
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                pygame.quit()


main()
