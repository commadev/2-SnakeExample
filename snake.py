import math
import random
import pygame


width = 500  # Width of our screen
height = 500  # Height of our screen
rows = 20  # Amount of rows



#Create List
snake_list = []
snack_list = []
block_list = [] #Global block pos

count_genome = 0
max_genome = 100
generation = 1
fitness = 0

genome_list = [[0,[0,0,0,0],[0,0,0,0,0,0]] for i in range(max_genome)]

avoid_power = 1
snack_power = 1

for i in range(max_genome):
    for j in range(4):
        genome_list[i][1][j] = round(random.random(),4) * snack_power
    for j in range(6):
        genome_list[i][2][j] = round(random.random(),4) * avoid_power

print(str(generation)+" : "+str(genome_list))



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

    genome_manege()

    #Find_item
    if snake_.pos[1] > snack_.pos[1]:
        input_layer[0] = (snake_.pos[1] - snack_.pos[1]) * genome_list[count_genome][1][0]
    if snake_.pos[0] > snack_.pos[0]:
        input_layer[1] = (snake_.pos[0] - snack_.pos[0]) * genome_list[count_genome][1][1]
    if snake_.pos[1] < snack_.pos[1]:
        input_layer[2] = (snack_.pos[1] - snake_.pos[1]) * genome_list[count_genome][1][2]
    if snake_.pos[0] < snack_.pos[0]:
        input_layer[3] = (snack_.pos[0] - snake_.pos[0]) * genome_list[count_genome][1][3]

    #Avoid_block
    for i in range(len(myBlocklist)):
        for j in range(6):
            if snake_.pos[1] + j == myBlocklist[i][1]:
                input_layer[0] -= (snake_.pos[1] - myBlocklist[i][1]) * genome_list[count_genome][2][j]
            if snake_.pos[0] + j == myBlocklist[i][0]:
                input_layer[1] -= (snake_.pos[0] - myBlocklist[i][0]) * genome_list[count_genome][2][j]
            if snake_.pos[1] - j == myBlocklist[i][1]:
                input_layer[2] -= (myBlocklist[i][1] - snake_.pos[1]) * genome_list[count_genome][2][j]
            if snake_.pos[0] - j == myBlocklist[i][0]:
                input_layer[3] -= (myBlocklist[i][0] - snake_.pos[0]) * genome_list[count_genome][2][j]

    #print(myBlocklist)
    #print(count_genome)

    for i in range(len(myBlocklist)):
        if snake_.pos == myBlocklist[i]:
            return True

    # softmax
    input_layer_sum = 0
    for i in range(4):
        input_layer_sum += input_layer[i]
        
    if input_layer_sum == 0:
        input_layer_sum = 1
    
    for i in range(4):
        input_layer[i] = input_layer[i]/input_layer_sum

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

def genome_manege():
    global count_genome
    global generation
    global genome_list

    if count_genome > max_genome - 1:
            genome_list.sort()
            genome_list.reverse()
            print(str(generation)+" : "+str(genome_list))

            new_genome_list = [[0,[0,0,0,0],[0,0,0,0,0,0]] for i in range(max_genome)]
            
            for i in range(max_genome):
                for j in range(4):
                    if random.random() < 0.1:
                        new_genome_list[i][1][j] = round(random.random(),4) * snack_power
                    else:
                        new_genome_list[i][1][j] = genome_list[random.randint(0,1)][1][j]
                for j in range(6):
                    if random.random() < 0.1:
                        new_genome_list[i][2][j] = round(random.random(),4) * avoid_power
                    else:
                        new_genome_list[i][2][j] = genome_list[random.randint(0,1)][2][j]
            genome_list[:] = new_genome_list[:]

            count_genome = 0
            generation += 1
            print(str(generation)+" : "+str(genome_list))

def main(): 
    global fitness
    global count_genome
    global genome_list

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
        clock.tick(6000)  # Will ensure our game runs at 10 FPS

        #Create Sensor
        for i in range(len(snake_list)):
            if(item_sensor(snake_list[i], snack_list[i])):
                fitness -= 100
                genome_list[count_genome][0] = fitness
                count_genome += 1
                fitness = 0
                print(str(generation)+" : "+str(count_genome)+" / "+str(max_genome))
                print("fitness : "+str(genome_list[count_genome-1][0]))
                print("hidden 1 : "+str(genome_list[count_genome-1][1]))
                print("hidden 2 : "+str(genome_list[count_genome-1][2]))
                for j in range(4):
                    block_list.remove(snake_list[j].pos)
                    snake_list[j] = cube(randomPos(rows), color_snake[j])
                    block_list.remove(snack_list[j].pos)
                    snack_list[j] = cube(randomPos(rows), color_snack[j])
 
            
        #Collision Check
        for i in range(4):
            snake_list[i].hp -= 2
            if snake_list[i].hp <= 0:
                fitness -= 200
                genome_list[count_genome][0] = fitness
                count_genome += 1
                fitness = 0
                print(str(generation)+" : "+str(count_genome)+" / "+str(max_genome))
                print("fitness : "+str(genome_list[count_genome-1][0]))
                print("hidden 1 : "+str(genome_list[count_genome-1][1]))
                print("hidden 2 : "+str(genome_list[count_genome-1][2]))
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

        fitness += 1

            

        redrawWindow(win)  # This will refresh our screen

        #End
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                pygame.quit()


main()