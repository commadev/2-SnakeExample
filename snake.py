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
            for key in keys:
                if keys[pygame.K_LEFT]:
                    cube_list[0].move(-1, 0)
                    break

                if keys[pygame.K_RIGHT]:
                    cube_list[0].move(1, 0)
                    break
                    
                if keys[pygame.K_UP]:
                    cube_list[0].move(0, -1)
                    break

                if keys[pygame.K_DOWN]:
                    cube_list[0].move(0, 1)
                    break

                if keys[pygame.K_a]:
                    cube_list[1].move(-1, 0)
                    break

                if keys[pygame.K_d]:
                    cube_list[1].move(1, 0)
                    break
                    
                if keys[pygame.K_w]:
                    cube_list[1].move(0, -1)
                    break

                if keys[pygame.K_s]:
                    cube_list[1].move(0, 1)
                    break


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
    cube_list[0].draw(surface)
    cube_list[1].draw(surface)
    snack_list[0].draw(surface)
    snack_list[1].draw(surface)
    pygame.display.update()  # Updates the screen

def randomSnack(rows):
    x = random.randrange(rows)
    y = random.randrange(rows)
    return x, y

def item_sensor(cube, item_need, item_avoid):     #먹이센서
    cube_pos = cube
    item_need_pos = item_need
    item_avoid_pos = item_avoid
    input_layer = [0.0, 0.0, 0.0, 0.0]  #입력층

    for i in range(1, 6):                  #먹이찾기
        if (cube_pos[0] + i, cube_pos[1]) == item_need_pos:
            input_layer[0] = 1.2 - 0.2 * i
        if (cube_pos[0] - i, cube_pos[1]) == item_need_pos:
            input_layer[1] = 1.2 - 0.2 * i
        if (cube_pos[0], cube_pos[1] + i) == item_need_pos:
            input_layer[2] = 1.2 - 0.2 * i
        if (cube_pos[0], cube_pos[1] - i) == item_need_pos:
            input_layer[3] = 1.2 - 0.2 * i
                                            #다른먹이회피
        if (cube_pos[0] + i, cube_pos[1]) == item_avoid_pos:
            input_layer[0] = - 1.2 + 0.2 * i
        if (cube_pos[0] - i, cube_pos[1]) == item_avoid_pos:
            input_layer[1] = - 1.2 + 0.2 * i
        if (cube_pos[0], cube_pos[1] + i) == item_avoid_pos:
            input_layer[2] = - 1.2 + 0.2 * i
        if (cube_pos[0], cube_pos[1] - i) == item_avoid_pos:
            input_layer[3] = - 1.2 + 0.2 * i

    return input_layer

def cube_sensor(cube1, cube2):     #딴놈이랑 충돌센서
    cube1_pos = cube1
    cube2_pos = cube2

    input_layer = [0.0, 0.0, 0.0, 0.0]  #입력층

    for i in range(1, 6): 
        if (cube1_pos[0] + i, cube1_pos[1]) == cube2_pos:
            input_layer[0] = - 1.2 + 0.2 * i
        if (cube1_pos[0] - i, cube1_pos[1]) == cube2_pos:
            input_layer[1] = - 1.2 + 0.2 * i
        if (cube1_pos[0], cube1_pos[1] + i) == cube2_pos:
            input_layer[2] = - 1.2 + 0.2 * i
        if (cube1_pos[0], cube1_pos[1] - i) == cube2_pos:
            input_layer[3] = - 1.2 + 0.2 * i

    return input_layer

def main(): 
    global width, rows, cube_list, snack_list
    width = 500  # Width of our screen
    height = 500  # Height of our screen
    rows = 20  # Amount of rows

    win = pygame.display.set_mode((width, height))  # Creates our screen object
    cube_list = []
    snack_list = []

    cube1 = cube((10,10), (255,0,0))  # Creates a snake object which we will code later
    cube2 = cube((10,12), (0,0,255))
    cube_list.append(cube1)
    cube_list.append(cube2)
    snack1 = cube(randomSnack(rows), color=(255,0,255))
    snack2 = cube(randomSnack(rows), color=(0,255,255))
    snack_list.append(snack1)
    snack_list.append(snack2)
    clock = pygame.time.Clock() # creating a clock object

    
    flag = True
    # STARTING MAIN LOOP
    while flag:
        pygame.time.delay(50)  # This will delay the game so it doesn't run too quickly
        clock.tick(10)  # Will ensure our game runs at 10 FPS
        move(cube_list)
        redrawWindow(win)  # This will refresh our screen
        print(item_sensor(cube_list[0].pos, snack_list[0].pos, snack_list[1].pos))
        print(cube_sensor(cube_list[0].pos, cube_list[1].pos))
        #Collision Check
        if cube1.pos == snack_list[0].pos:
            snack_list[0] = cube(randomSnack(rows), color=(255,0,255))
        if cube2.pos == snack_list[1].pos:
            snack_list[1] = cube(randomSnack(rows), color=(0,255,255))

main()
