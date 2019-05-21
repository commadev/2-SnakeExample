import numpy as np
import time

#전역변수
rows = 18
period = 0
reward = 0
myItem = []
myDst = []

#맵 배열 생성
map_Matrix = np.zeros((rows,rows))


#큐브 개체
class cube(object):
    def __init__(self,num,pos):
        self.num = num
        self.pos = pos
        self.hp = 100
        map_Matrix[self.pos[0]][self.pos[1]] = self.num
        
    def move(self,x,y):
        map_Matrix[self.pos[0]][self.pos[1]] = 0
        self.pos = self.pos + np.array([x,y]) #행렬합
        if collisionCheck(myItem[i]) == True:
            for i in range(len(myItem)):
                period += 1
                myItem[i].pos = randomPos(rows)
                myDst[i].pos = randomPos(rows)
                print("1")
        else:
            map_Matrix[self.pos[0]][self.pos[1]] = self.num
            print("2")
        
        

#충돌
def collisionCheck(item_):
    if map_Matrix[item_.pos[0]][item_.pos[1]] + item_.num == 0: #겹치는 좌표와의 합이 0이면 본인목적지
        reward = 50
        return True
    elif map_Matrix[item_.pos[0]][item_.pos[1]] + item_.num == item_.num: #겹치는 좌표와의 합이 본인이 값과 같으면 충돌x
        return False
    else: #그외 나머지값은 장애물과 충돌
        reward = -100
        return True

        
#난수 생성
def randomPos(rows):
    
    x = np.random.randint(18)
    y = np.random.randint(18)
        
    return np.array([x,y])



#임시 센서
def item_sensor(item_, dst_):

    input_layer = [0,0,0,0]
    output_layer = ["Up","Left","Down","Right"]  

    if item_.pos[1] > dst_.pos[1]:
        input_layer[0] = (item_.pos[1] - dst_.pos[1])
    if item_.pos[0] > dst_.pos[0]:
        input_layer[1] = (item_.pos[0] - dst_.pos[0])
    if item_.pos[1] < dst_.pos[1]:
        input_layer[2] = (dst_.pos[1] - item_.pos[1])
    if item_.pos[0] < dst_.pos[0]:
        input_layer[3] = (dst_.pos[0] - item_.pos[0])

    if output_layer[input_layer.index(max(input_layer))] == "Up":
        item_.move(0, -1)
    elif output_layer[input_layer.index(max(input_layer))] == "Left":
        item_.move(-1, 0)
    elif output_layer[input_layer.index(max(input_layer))] == "Down":
        item_.move(0, 1)
    elif output_layer[input_layer.index(max(input_layer))] == "Right":
        item_.move(1, 0)
        


#메인
def main():
    global period

    for i in range(1,3):
        myItem.append(cube(i,randomPos(rows)))
    for i in range(-1,-3,-1):
        myDst.append(cube(i,randomPos(rows)))
    
    #메인루프
    flag = True
    while(flag == True):

        
        print(map_Matrix, end='\r')
        print("")
        
        for i in range(len(myItem)):
            item_sensor(myItem[i],myDst[i])
            
                
        print("Period = ", period, "Reward = ", reward , end='\r')

        time.sleep(1)
        

        
main()
