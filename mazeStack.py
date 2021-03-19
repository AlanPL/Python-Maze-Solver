#Author: Alan Palacios
# usage: py mazeStack dimension[optional] timeDelay[optional]
# 'py mazeStack' will run with the default 5x5 maze
import time
import os
import sys
import random
#colors
CGREYBG    = '\33[100m'
CYELLOW2 = '\33[93m'
CRED2    = '\33[91m'
CGREEN2  = '\33[92m'
CBLUE2   = '\33[94m'
CEND = '\033[0m'
#0: emptyCell, 1:wall, 2: start, 3: end
            #X:  0 1 2 3 4  
default_maze = [[2,1,0,1,0],#0
                [0,1,0,0,0],#1
                [0,0,0,1,0],#2
                [1,0,1,0,0],#3
                [1,0,1,3,0]]#4
stack = []
N = 5
timeDelay = 0.3
actualCoords=(0,0)
directions = [(-1,0),(0,-1),(1,0),(0,1)]          
treeshold = 0.7

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
#explore with a wall always on the right
#directions: 
#     1
# 0       2
#     3
def moveWallOnRight(xC, yC, dir):#new coords and direction    
    global stack
    global originPasses    
    global default_maze  
    stack.append((xC,yC,dir))        
    if(default_maze[yC][xC]==3):
        print(CGREEN2 + "Ha encontrado la salida!" + CEND)
        return
    rightDir = (dir+1)%4 #select right direction
    newX = xC+directions[rightDir][0]
    newY = yC+directions[rightDir][1]        
    #RIGHT: wall or limit 
    if(newX<0 or newX==N or newY<0 or newY==N or default_maze[newY][newX]==1): 
        #front coordinates
        frontX = xC+directions[dir][0]
        frontY = yC+directions[dir][1]            
        #FRONT: wall or limit
        if(frontX<0 or frontX==N or frontY<0 or frontY==N or default_maze[frontY][frontX]==1):             
            leftDir = (dir+3)%4 #turn to the left
            moveWallOnRight(xC, yC, leftDir)
        else:
            #give a step to front
            moveWallOnRight(frontX, frontY, dir)
    else:
        #turn to right and give a step
        moveWallOnRight(newX, newY, rightDir)        

def generateMaze():
    global default_maze
    default_maze = [[0 for y in range(N)] for x in range(N)] 
    for y in range(N):
        for x in range(N):
            rand = random.random()
            if(rand>treeshold):
                default_maze[y][x]=1
            else:                
                default_maze[y][x]=0    
    default_maze[0][0]=2
    default_maze[N-1][N-1]=3
    for y in range(N):
        for x in range(N):                  
                if(default_maze[y][x]==0):print( CGREEN2+ '^^'+CEND,'', end='')
                if(default_maze[y][x]==1):print(CYELLOW2+ '||'+ CEND,'', end='')
                if(default_maze[y][x]==2):print(CBLUE2+ '[]'+ CEND,'', end='')
                if(default_maze[y][x]==3):print(CBLUE2+ '[]'+ CEND,'', end='')                
        print('') 

def printPathway(arr):
    global actualCoords
    for coords in arr:
        actualCoords = coords    
        cls()    
        printMaze()
        print('------------')
        time.sleep(timeDelay)    
        
def printMaze():
    global actualCoords    
    for y in range(N):
        for x in range(N):
            if((x,y) == (actualCoords[0], actualCoords[1])):
                if(actualCoords[2]%2==0):print(CRED2+'--'+CEND,'', end='')
                else:print(CRED2+' |'+CEND,'', end='')
                
            else:        
                if(default_maze[y][x]==0):print( CGREEN2+ '^^'+CEND,'', end='')
                if(default_maze[y][x]==1):print(CYELLOW2+ '||'+ CEND,'', end='')
                if(default_maze[y][x]==2):print(CBLUE2+ '[]'+ CEND,'', end='')
                if(default_maze[y][x]==3):print(CBLUE2+ '[]'+ CEND,'', end='')                
        print('')    


if(len(sys.argv)>1):
    N = int(sys.argv[1])
    res='Y'
    while res.upper()=='Y' :
        generateMaze()
        res = input("Generate other maze? Y/N ")     
    if(len(sys.argv)>2):timeDelay=float(sys.argv[2])
start_time = time.time()
moveWallOnRight(0,0,3)
printPathway(stack)  

print("--- %s seconds ---" % (time.time() - start_time))