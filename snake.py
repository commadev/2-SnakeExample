import pygame
import random
import math
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    
    def __init__(self, start, dirnx = 1, dirny = 0, color = (255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2,dis-2))

        

class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)

        self.dirnx = 0
        self.dirny = 1

    '''
    def move(self,k1,k2,k3,k4):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            #키이벤트
            for key in keys:
                if keys[k1]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if keys[k2]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    
                if keys[k3]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if keys[k4]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            #맵끝으로 갔을때
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows -1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
                #else: c.move( c.dirnx, c.dirny) #자동이동
            '''


    def reset(self, pos):
        pass

    def addCube(self):
        pass

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid(surface):
    sizeBtwn = width // rows

    x = 0
    y = 0
    
    for l in range(rows):

        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,width))
        pygame.draw.line(surface, (255,255,255), (0,y),(width,y))
        

def redrawWindow(surface):
    global width, rows, s1, s2, snack1, snack2
    surface.fill((0,0,0))
    s2.draw(surface)
    s1.draw(surface)
    snack1.draw(surface)
    snack2.draw(surface)
    drawGrid(surface)
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x, y)

def message_box(subject, content):
    pass


def move(snake2,snake1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            #Key Event
            for key in keys:
                if keys[pygame.K_LEFT]:
                    snake1.dirnx = -1
                    snake1.dirny = 0
                    snake1.turns[snake1.head.pos[:]] = [snake1.dirnx, snake1.dirny]

                if keys[pygame.K_RIGHT]:
                    snake1.dirnx = 1
                    snake1.dirny = 0
                    snake1.turns[snake1.head.pos[:]] = [snake1.dirnx, snake1.dirny]
                    
                if keys[pygame.K_UP]:
                    snake1.dirnx = 0
                    snake1.dirny = -1
                    snake1.turns[snake1.head.pos[:]] = [snake1.dirnx, snake1.dirny]

                if keys[pygame.K_DOWN]:
                    snake1.dirnx = 0
                    snake1.dirny = 1
                    snake1.turns[snake1.head.pos[:]] = [snake1.dirnx, snake1.dirny]
                
                if keys[pygame.K_a]:
                    snake2.dirnx = -1
                    snake2.dirny = 0
                    snake2.turns[snake2.head.pos[:]] = [snake2.dirnx, snake2.dirny]

                if keys[pygame.K_d]:
                    snake2.dirnx = 1
                    snake2.dirny = 0
                    snake2.turns[snake2.head.pos[:]] = [snake2.dirnx, snake2.dirny]
                    
                if keys[pygame.K_w]:
                    snake2.dirnx = 0
                    snake2.dirny = -1
                    snake2.turns[snake2.head.pos[:]] = [snake2.dirnx, snake2.dirny]

                if keys[pygame.K_s]:
                    snake2.dirnx = 0
                    snake2.dirny = 1
                    snake2.turns[snake2.head.pos[:]] = [snake2.dirnx, snake2.dirny]



        for j, d in enumerate(snake2.body):
            q = d.pos[:]
            if q in snake2.turns:
                turn2 = snake2.turns[q]
                d.move(turn2[0], turn2[1])
                if j == len(snake2.body)-1:
                    snake2.turns.pop(q)
            #맵끝으로 갔을때
            else:
                if d.dirnx == -1 and d.pos[0] <= 0: d.pos = (d.rows -1, d.pos[1])
                elif d.dirnx == 1 and d.pos[0] >= d.rows-1: d.pos = (0, d.pos[1])
                elif d.dirny == 1 and d.pos[1] >= d.rows-1: d.pos = (d.pos[0], 0)
                elif d.dirny == -1 and d.pos[1] <= 0: d.pos = (d.pos[0], d.rows-1)
                #else: d.move( d.dirnx, d.dirny) #자동이동


        for i, c in enumerate(snake1.body):
            p = c.pos[:]
            if p in snake1.turns:
                turn1 = snake1.turns[p]
                c.move(turn1[0], turn1[1])
                if i == len(snake1.body)-1:
                    snake1.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows -1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)


def main():
    global width, rows, s1, s2, snack1, snack2
    width = 500
    height = 500
    rows = 20


    #pygame start
    win = pygame.display.set_mode((width, height))
    
    s1 = snake((255,0,0), (10,10))
    s2 = snake((255,0,0), (15,15))
    clock = pygame.time.Clock()
    snack1 = cube(randomSnack(rows, s1), color=(0,255,0))
    snack2 = cube(randomSnack(rows, s2), color=(0,0,255))
    flag = True

    
    #loop clock
    while flag:
        
        pygame.time.delay(50)
        clock.tick(100)
        move(s1, s2)
        
        

        
        #Collision Check
        if s1.body[0].pos == snack1.pos:
            s1.addCube()
            snack1 = cube(randomSnack(rows, s1), color=(0,255,0))
        if s2.body[0].pos == snack2.pos:
            s2.addCube()
            snack2 = cube(randomSnack(rows, s2), color=(0,0,255))

        redrawWindow(win)
main()
