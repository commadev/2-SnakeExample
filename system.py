import pygame
import numpy as np

#전역변수
w_Width = 500
w_Height = 500
rows = 20

#맵 배열 생성
map_Matrix = np.zeros((rows,rows))
print(map_Matrix)


#pygame에 맵 격자 그리는 함수
def drawGrid(surface):
    w_Size = w_Height // rows  #간격 = 윈도우사이즈 / 줄수
    x = 0
    y = 0
    for l in range(rows): #파이게임에 격자 맵 그리는 함수
        x = x + w_Size
        y = y + w_Size

        pygame.draw.line(surface, (128,128,128), (x,0),(x,w_Width))
        pygame.draw.line(surface, (128,128,128), (0,y),(w_Width,y))

#pygame에 맵 갱신 하는 함수
def redrawWindow(surface):
    surface.fill((255,255,255))  #배경색

    drawGrid(surface)  #drawGrid 함수 호출

    ##여기에 draw함수 입력##
    
    pygame.display.update()  # 화면갱신

#메인
def main(): 
    win = pygame.display.set_mode((w_Width, w_Height)) 


    #메인루프
    flag = True
    while(flag == True):

        
        redrawWindow(win) #pygame 화면갱신





        #pygame 종료
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                pygame.quit()


main()
