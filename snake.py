import math
import random
import pygame
import copy
import threading
from socket import *

width = 500  # Width of our screen
height = 500  # Height of our screen
rows = 20  # Amount of rows

f = open("result.txt", "w")
f.write("")
f.close()

#Socket Creator

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', 8080))
serverSock.listen(1)

connectionSock, addr = serverSock.accept()
print('Connect from ',str(addr))

#Create List
snake_list = []
snack_list = []
block_list = [] #Global block pos

count_genome = 0
max_genome = 20

generation = 1
fitness = 0

best_genome = 0
best_fitness = 0
sum_fitness = 0
avg_fitness = 0

genome_list = [[0,[0,0,0,0],[0,0,0,0,0,0]] for i in range(max_genome)]

avoid_power = 1
snack_power = 10

for i in range(max_genome):
    for j in range(4):
        genome_list[i][1][j] = round(random.random() * snack_power,4)
    for j in range(6):
        genome_list[i][2][j] = round(random.random() * avoid_power,4)

print(str(generation)+" : "+str(genome_list))



#Color DB
color_snack = [(92, 37, 13),(70, 98, 33),(14, 55, 85),(125, 96, 8)]
color_snake = [(183, 73, 15),(139, 193, 69),(29, 111, 169),(241, 192, 25)]


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
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis, dis))
        # By multiplying the row and column value of our cube by the width and height of each cube we can determine where to draw it

        #debug
        #pygame.draw.rect(surface, (0,0,0), (20,20,-10,-10))
 
def drawGrid(surface):
    sizeBtwn = width // rows  # Gives us the distance between the lines

    x = 0  # Keeps track of the current x
    y = 0  # Keeps track of the current y
    for l in range(rows):  # We will draw one vertical and one horizontal line each loop
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (128,128,128), (x,0),(x,width))
        pygame.draw.line(surface, (128,128,128), (0,y),(width,y))
        
def redrawWindow(surface):
    surface.fill((255,255,255))  # Fills the screen with black

    drawGrid(surface)  # Will draw our grid lines
    for i in range(len(snake_list)):
        snake_list[i].draw(surface)
        snack_list[i].draw(surface)
    pygame.display.update()  # Updates the screen

def randomPos(rows):
    x = random.randrange(rows)
    while x in block_list:
        x = random.randrange(rows)
        
    y = random.randrange(rows)
    while y in block_list:
        y = random.randrange(rows)
        
    return x, y

def item_sensor(snake_, snack_):     #Sensor
    global block_list
    global count_genome

    myBlocklist = []
    input_layer = [0,0,0,0]
    output_layer = ["Up","Left","Down","Right"]
    myBlocklist[:] = block_list[:]
    myBlocklist.remove(snake_.pos)
    myBlocklist.remove(snack_.pos)
    #print(myBlocklist)
    #print(block_list)

    genome_manage()

    #Find_item
    if snake_.pos[1] > snack_.pos[1]:
        input_layer[0] = (snake_.pos[1] - snack_.pos[1])# * genome_list[count_genome][1][0]
    if snake_.pos[0] > snack_.pos[0]:
        input_layer[1] = (snake_.pos[0] - snack_.pos[0])# * genome_list[count_genome][1][1]
    if snake_.pos[1] < snack_.pos[1]:
        input_layer[2] = (snack_.pos[1] - snake_.pos[1])# * genome_list[count_genome][1][2]
    if snake_.pos[0] < snack_.pos[0]:
        input_layer[3] = (snack_.pos[0] - snake_.pos[0])# * genome_list[count_genome][1][3]

    #Avoid_block
    for i in range(len(myBlocklist)):
        for j in range(0, 5):
            if abs(snake_.pos[0] - myBlocklist[i][0]) < 3 and snake_.pos[1] - j == myBlocklist[i][1]:
                input_layer[0] *= genome_list[count_genome][2][j]
                
            if abs(snake_.pos[1] - myBlocklist[i][1]) < 3 and snake_.pos[0] - j == myBlocklist[i][0]:
                input_layer[1] *= genome_list[count_genome][2][j]
                
            if abs(snake_.pos[0] - myBlocklist[i][0]) < 3 and snake_.pos[1] + j == myBlocklist[i][1]:
                input_layer[2] *= genome_list[count_genome][2][j]
                
            if abs(snake_.pos[1] - myBlocklist[i][1]) < 3 and snake_.pos[0] + j == myBlocklist[i][0]:
                input_layer[3] *= genome_list[count_genome][2][j]
                
                
            '''
            if abs(snake_.pos[0] - myBlocklist[i][0]) < 3 and snake_.pos[1] - j == myBlocklist[i][1]:
                input_layer[0] -= (snake_.pos[1] - myBlocklist[i][1]) * genome_list[count_genome][2][j]
                
            if abs(snake_.pos[1] - myBlocklist[i][1]) < 3 and snake_.pos[0] - j == myBlocklist[i][0]:
                input_layer[1] -= (snake_.pos[0] - myBlocklist[i][0]) * genome_list[count_genome][2][j]
                
            if abs(snake_.pos[0] - myBlocklist[i][0]) < 3 and snake_.pos[1] + j == myBlocklist[i][1]:
                input_layer[2] -= (myBlocklist[i][1] - snake_.pos[1]) * genome_list[count_genome][2][j]
                
            if abs(snake_.pos[1] - myBlocklist[i][1]) < 3 and snake_.pos[0] + j == myBlocklist[i][0]:
                input_layer[3] -= (myBlocklist[i][0] - snake_.pos[0]) * genome_list[count_genome][2][j]
            '''
    #print(count_genome)



    #break
    for i in range(len(myBlocklist)):
        if snake_.pos == myBlocklist[i]:
            return True


    if snake_.pos[1] - 1  > rows:
        input_layer[0] = - 1
        print(snake_.pos)
        print(input_layer)
    if snake_.pos[0] - 1  > rows:
        input_layer[1] = - 1
        print(snake_.pos)
        print(input_layer)
    if snake_.pos[1] + 1  < 0:
        input_layer[2] = - 1
        print(snake_.pos)
        print(input_layer)
    if snake_.pos[0] + 1  < 0:
        input_layer[3] = - 1
        print(snake_.pos)
        print(input_layer)

        
    
    # softmax
    input_layer_sum = 0
    for i in range(4):
        input_layer_sum += input_layer[i]
        
    if input_layer_sum == 0:
        input_layer_sum = 1
    
    for i in range(4):
        input_layer[i] = input_layer[i]/input_layer_sum
    

    #if snake_.color == (183, 73, 15):
    #    print(input_layer)
    
    
    if output_layer[input_layer.index(max(input_layer))] == "Up":
        snake_.move(0, -1)
    elif output_layer[input_layer.index(max(input_layer))] == "Left":
        snake_.move(-1, 0)
    elif output_layer[input_layer.index(max(input_layer))] == "Down":
        snake_.move(0, 1)
    elif output_layer[input_layer.index(max(input_layer))] == "Right":
        snake_.move(1, 0)
    
    return False

def genome_manage():
    global count_genome
    global generation
    global genome_list

    global sum_fitness
    global avg_fitness
    global best_genome
    global best_fitness

    if count_genome > max_genome - 1:
            avg_fitness = sum_fitness/max_genome
            print("best_genome = " + str(genome_list[best_genome]))
            print("avg_fitness = " + str(avg_fitness))

            f = open("result.txt", "a")
            f.write("Generation : " + str(generation)+" - best_genome = " + str(genome_list[best_genome]) + ", avg_fitness = " + str(avg_fitness) + '\n')
            f.close()
            
            sum_fitness = 0
            best_fitness = 0
            best_genome = 0

            genome_list.sort()
            genome_list.reverse()
            #print("Generation " + str(generation)+" : "+str(genome_list))
            #print("")

            new_genome_list = [[0,[0,0,0,0],[0,0,0,0,0,0]] for i in range(max_genome)]

            for i in range(max_genome):
                for j in range(4):
                    if random.random() < 0.1:
                        new_genome_list[i][1][j] = round(random.random() * snack_power,4)
                    else:
                        new_genome_list[i][1][j] = genome_list[random.randint(0,1)][1][j]
                for j in range(6):
                    if random.random() < 0.1:
                        new_genome_list[i][2][j] = round(random.random() * avoid_power,4)
                    else:
                        new_genome_list[i][2][j] = genome_list[random.randint(0,1)][2][j]
            genome_list[:] = new_genome_list[:]

            count_genome = 0
            generation += 1
            #print("Generation "  + str(generation)+" : "+str(genome_list))
            #print("")

def main(): 
    global fitness
    global count_genome
    global genome_list

    global sum_fitness
    global avg_fitness
    global best_genome
    global best_fitness

    temp_snake_list = []

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
        pygame.time.delay(100)  # This will delay the game so it doesn't run too quickly
        clock.tick(60)  # Will ensure our game runs at 10 FPS

        sendData = (
            str(snake_list[0].pos[0]) + ":" + str(snake_list[0].pos[1]) + ":" + str(snack_list[0].pos[0]) + ":" + str(snack_list[0].pos[1]) + ":" +
            str(snake_list[1].pos[0]) + ":" + str(snake_list[1].pos[1]) + ":" + str(snack_list[1].pos[0]) + ":" + str(snack_list[1].pos[1]) + ":" +
            str(snake_list[2].pos[0]) + ":" + str(snake_list[2].pos[1]) + ":" + str(snack_list[2].pos[0]) + ":" + str(snack_list[2].pos[1]) + ":" +
            str(snake_list[3].pos[0]) + ":" + str(snake_list[3].pos[1]) + ":" + str(snack_list[3].pos[0]) + ":" + str(snack_list[3].pos[1]))
        connectionSock.send(sendData.encode('utf-8'))
        temp_snake_list = copy.deepcopy(snake_list)

        
        #Create Sensor
        for i in range(len(snake_list)):
            if(item_sensor(snake_list[i], snack_list[i])):
                #fitness -= 100
                genome_list[count_genome][0] = fitness
                sum_fitness += fitness
                if best_fitness < fitness:
                    best_genome = count_genome
                    best_fitness = fitness
                count_genome += 1
                fitness = 0
                print("Generation " + str(generation)+" : "+str(count_genome)+" / "+str(max_genome))
                print("Fitness : "+str(genome_list[count_genome-1][0]))
                #print("Hidden 1 : "+str(genome_list[count_genome-1][1]))
                print("Hidden 2 : "+str(genome_list[count_genome-1][2]))
                print("")
                for j in range(4):
                    block_list.remove(snake_list[j].pos)
                    snake_list[j] = cube(randomPos(rows), color_snake[j])
                    block_list.remove(snack_list[j].pos)
                    snack_list[j] = cube(randomPos(rows), color_snack[j])
         
            
        #Collision Check
        for i in range(4):
            snake_list[i].hp -= 2
            if snake_list[i].hp <= 0:
                #fitness -= 200
                genome_list[count_genome][0] = fitness
                sum_fitness += fitness
                if best_fitness < fitness:
                    best_genome = count_genome
                    best_fitness = fitness
                count_genome += 1
                fitness = 0
                print("Generation " + str(generation)+" : "+str(count_genome)+" / "+str(max_genome))
                print("fitness : "+str(genome_list[count_genome-1][0]))
                #print("hidden 1 : "+str(genome_list[count_genome-1][1]))
                print("hidden 2 : "+str(genome_list[count_genome-1][2]))
                print("")
                for j in range(4):
                    block_list.remove(snake_list[j].pos)
                    snake_list[j] = cube(randomPos(rows), color_snake[j])
                    block_list.remove(snack_list[j].pos)
                    snack_list[j] = cube(randomPos(rows), color_snack[j])
            
            if snake_list[i].pos == snack_list[i].pos:
                fitness += 10
                snake_list[i].hp = 100
                block_list.remove(snack_list[i].pos)
                snack_list[i] = cube(randomPos(rows), color_snack[i])

        #fitness += 1
        if(abs(snake_list[0].pos[0] - temp_snake_list[0].pos[0]) == 1 or
        abs(snake_list[1].pos[0] - temp_snake_list[1].pos[0]) == 1 or
        abs(snake_list[2].pos[0] - temp_snake_list[2].pos[0]) == 1 or
        abs(snake_list[3].pos[0] - temp_snake_list[3].pos[0]) == 1 or
        abs(snake_list[0].pos[1] - temp_snake_list[0].pos[1]) == 1 or
        abs(snake_list[1].pos[1] - temp_snake_list[1].pos[1]) == 1 or
        abs(snake_list[2].pos[1] - temp_snake_list[2].pos[1]) == 1 or
        abs(snake_list[3].pos[1] - temp_snake_list[3].pos[1]) == 1):
            temp__list = [[.0,.0],[.0,.0],[.0,.0],[.0,.0]]
            for i in range(4):
                for j in range(2):
                    if(temp_snake_list[i].pos[j] < snake_list[i].pos[j]):
                        temp__list[i][j] = temp_snake_list[i].pos[j] + float(abs(snake_list[i].pos[j] - temp_snake_list[i].pos[j])/2)
                    else:
                        temp__list[i][j] = temp_snake_list[i].pos[j] - float(abs(snake_list[i].pos[j] - temp_snake_list[i].pos[j])/2)
            sendData = (
            str(temp__list[0][0]) + ":" + str(temp__list[0][1]) + ":" + str(snack_list[0].pos[0]) + ":" + str(snack_list[0].pos[1]) + ":" +
            str(temp__list[1][0]) + ":" + str(temp__list[1][1]) + ":" + str(snack_list[1].pos[0]) + ":" + str(snack_list[1].pos[1]) + ":" +
            str(temp__list[2][0]) + ":" + str(temp__list[2][1]) + ":" + str(snack_list[2].pos[0]) + ":" + str(snack_list[2].pos[1]) + ":" +
            str(temp__list[3][0]) + ":" + str(temp__list[3][1]) + ":" + str(snack_list[3].pos[0]) + ":" + str(snack_list[3].pos[1]))
            connectionSock.send(sendData.encode('utf-8'))

        redrawWindow(win)  # This will refresh our screen

        #End
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                pygame.quit()

main()
