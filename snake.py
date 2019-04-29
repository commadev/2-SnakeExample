import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


width = 500  # Width of our screen
height = 500  # Height of our screen
rows = 20  # Amount of rows



#Create List
snake_list = []
snack_list = []
block_list = [] #Global block pos

#Color DB
color_snack = [(127,0,0),(0,127,0),(0,0,127),(127,127,0)]
color_snake = [(255,0,0),(0,255,0),(0,0,255),(255,255,0)]



class cube(object):
    def __init__(self,start,color, odd):
        self.pos = start
        self.color = color
        self.hp = 100
        self.odd = odd
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

def item_sensor(snake_, snack_):     #Sensor
    global block_list
    myBlocklist = []
    input_layer = [0,0,0,0]
    output_layer = ["Up","Left","Down","Right"]
    myBlocklist[:] = block_list[:]
    myBlocklist.remove(snake_.pos)
    myBlocklist.remove(snack_.pos)
    #print(myBlocklist)
    #print(block_list)

    #Find_item
    if snake_.pos[1] > snack_.pos[1]:
        input_layer[0] = snake_.pos[1] - snack_.pos[1]
    if snake_.pos[0] > snack_.pos[0]:
        input_layer[1] = snake_.pos[0] - snack_.pos[0]
    if snake_.pos[1] < snack_.pos[1]:
        input_layer[2] = snack_.pos[1] - snake_.pos[1]
    if snake_.pos[0] < snack_.pos[0]:
        input_layer[3] = snack_.pos[0] - snake_.pos[0]

    #Avoid_block
    for i in range(len(myBlocklist)):
        if snake_.pos[1] + 1 == myBlocklist[i][1]:
            input_layer[0] -= (snake_.pos[1] - myBlocklist[i][1]) * snake_.odd
        if snake_.pos[0] + 1 == myBlocklist[i][0]:
            input_layer[1] -= (snake_.pos[0] - myBlocklist[i][0]) * snake_.odd
        if snake_.pos[1] - 1 == myBlocklist[i][1]:
            input_layer[2] -= (myBlocklist[i][1] - snake_.pos[1]) * snake_.odd
        if snake_.pos[0] - 1 == myBlocklist[i][0]:
            input_layer[3] -= (myBlocklist[i][0] - snake_.pos[0]) * snake_.odd
    #print(myBlocklist)
    print(snake_.odd)

    for i in range(len(myBlocklist)):
        if snake_.pos == myBlocklist[i]:
            return True


    #print(input_layer)
    

    if output_layer[input_layer.index(max(input_layer))] == "Up":
        snake_.move(0, -1)
    elif output_layer[input_layer.index(max(input_layer))] == "Left":
        snake_.move(-1, 0)
    elif output_layer[input_layer.index(max(input_layer))] == "Down":
        snake_.move(0, 1)
    elif output_layer[input_layer.index(max(input_layer))] == "Right":
        snake_.move(1, 0)
    

    return False

def main(): 
    # Creates Screen
    win = pygame.display.set_mode((width, height))  

    #Snack
    for i in range(4):
        snake_list.append(cube(randomPos(rows),color_snake[i], random.random()))
    #Snake
    for i in range(4):
        snack_list.append(cube(randomPos(rows),color_snack[i], random.random()))


    #Creating a clock object
    clock = pygame.time.Clock() 
    
    flag = True

    
    ### STARTING MAIN LOOP ###
    
    while flag:
        pygame.time.delay(50)  # This will delay the game so it doesn't run too quickly
        clock.tick(10)  # Will ensure our game runs at 10 FPS

        #Create Sensor
        for i in range(len(snake_list)):
            if(item_sensor(snake_list[i], snack_list[i])):
                print( str(i) + "   " + str(snake_list[i].odd))
                block_list.remove(snake_list[i].pos)
                snake_list[i] = cube(randomPos(rows), color_snake[i], random.random())
 
            
        #Collision Check
        for i in range(4):
            snake_list[i].hp -= 0
            if snake_list[i].hp <= 0:
                print( str(i) + "   " + str(snake_list[i].odd))
                block_list.remove(snake_list[i].pos)
                snake_list[i] = cube(randomPos(rows), color_snake[i], random.random())
            
            if snake_list[i].pos == snack_list[i].pos:
                snake_list[i].hp = 100
                block_list.remove(snack_list[i].pos)
                snack_list[i] = cube(randomPos(rows), color_snack[i], random.random())
            
                



            

        redrawWindow(win)  # This will refresh our screen

        #End
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                pygame.quit()


main()
