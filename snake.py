import math
import random
import pygame
import tkinter as tk
import numpy as np
from tkinter import messagebox

DIRECTIONS = np.array([ #움직이기편하게 디렉션만들어줌 (이거수정좀)
    (0, -1), #UP     0
    (0, 1),  #DOWN   1
    (-1, 0), #LEFT   2
    (1, 0)   #RIGHT  3
])

class Cube(object):
    rows = 20
    width = 500
    def __init__(self,start,color=(255,0,0)):
        self.pos = start
        self.color = color
        self.score = 0
        
    def move(self, x, y):
        self.pos = (self.pos[0] + x, self.pos[1] + y)  # change our position

    def getpos(self):
        return self.pos
    
    def draw(self, surface):
        dis = self.width // self.rows  # Width/Height of each Cube
        i = self.pos[0] # Current row
        j = self.pos[1] # Current Column

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        # By multiplying the row and column value of our Cube by the width and height of each Cube we can determine where to draw it


def move(cube1, cube2):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            if __name__ == '__main__': 
            #Key Event
                for key in keys:
                    if keys[pygame.K_LEFT]:
                        cube1.move(DIRECTIONS[2])
                        break

                    if keys[pygame.K_RIGHT]:
                        cube1.move(DIRECTIONS[3])
                        break
                    
                    if keys[pygame.K_UP]:
                        cube1.move(DIRECTIONS[0])
                        break

                    if keys[pygame.K_DOWN]:
                        cube1.move(DIRECTIONS[1])
                        break

                    if keys[pygame.K_a]:
                        cube2.move(-1, 0)
                        break

                    if keys[pygaame.K_d]:
                        cube2.move(1, 0)
                        break

                    if keys[pygame.K_w]:
                        cube2.move(0, -1)
                        break

                    if keys[pygame.K_s]:
                        cube2.move(0, 1)
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
    cube1.draw(surface)
    cube2.draw(surface)
    snack1.draw(surface)
    snack2.draw(surface)
    pygame.display.update()  # Updates the screen

def randomSnack(rows):
    x = random.randrange(rows)
    y = random.randrange(rows)
    return x, y

def sensor(self, Cube1, Cube2):     #센서 달아주는부분
    self.cube_pos = Cube1.getpos
    self.item_pos = Cube2.getpos

    input_layer = [0.0, 0.0, 0.0, 0.0]  #입력층
    output_layer = [0.0, 0.0, 0.0, 0.0] #출력층

    for i in range(5):                  #먹이찾기
        if cube_pos[0] + i == item_pos:
            input_layer[0] *= 0.2 * i
        if cube_pos[0] - i == item_pos:
            input_layer[1] *= 0.2 * i
        if cube_pos[1] + i == item_pos:
            input_layer[2] *= 0.2 * i
        if cube_pos[1] - i == item_pos:
            input_layer[3] *= 0.2 * i


    


def main(): 
    global width, rows, cube1, cube2, snack1, snack2
    width = 500  # Width of our screen
    height = 500  # Height of our screen
    rows = 20  # Amount of rows

    win = pygame.display.set_mode((width, height))  # Creates our screen object

    cube1 = Cube((10,10), (255,0,0))  # Creates a snake object which we will code later
    cube2 = Cube((10,12), (0,0,255))  
    snack1 = Cube(randomSnack(rows), color=(255,0,255))
    snack2 = Cube(randomSnack(rows), color=(0,255,255))
  
    clock = pygame.time.Clock() # creating a clock object

    flag = True
    # STARTING MAIN LOOP
    while flag:
        pygame.time.delay(50)  # This will delay the game so it doesn't run too quickly
        clock.tick(10)  # Will ensure our game runs at 10 FPS
        move(cube1, cube2)
        redrawWindow(win)  # This will refresh our screen

        #Collision Check
        if cube1.pos == snack1.pos:
            snack1 = Cube(randomSnack(rows), color=(255,0,255))
            cube1.score += 1
            print("Cube 1",cube1.score,"Point!")
        if cube2.pos == snack2.pos:
            snack2 = Cube(randomSnack(rows), color=(0,255,255))
            cube2.score += 1
            print("Cube 2",cube2.score,"Point!")
        if cube1.pos == snack2.pos:
            snack2 = Cube(randomSnack(rows), color=(0,255,255))
            cube1.score -= 2
            print("Cube 1",cube1.score,"Point!")
        if cube2.pos == snack1.pos:
            snack1 = Cube(randomSnack(rows), color=(0,255,255))
            cube2.score -= 2
            print("Cube 2",cube2.score,"Point!")

#if __name__ != '__main__': # 활성화부분 아직뺌
main()
