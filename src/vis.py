import pygame
import math as m
from pygame import *
from heapq import heappush,heappop,heapify
pygame.init()
#setting the caption
pygame.display.set_caption("A* pathfinding")
#the grid will be 500x500 so the window height will be 800
screen = pygame.display.set_mode((500,650))
#setting up the font
myfont = pygame.font.SysFont('Times New Roman', 30)
run = True
algorun = False
start = 0
end = 0
d = 0
drag = 0
startt = []
endt = []
grid = [[0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]]
#classes that we made
class MinHeap():
    def __init__(self):
        self.heap = []
    def parent(self,i):
        return (i-1)/2
    def insert(self,k):
        heappush(self.heap,k)
    def decreaseKey(self, i, new_val): 
        self.heap[i]  = new_val  
        while(i != 0 and self.heap[self.parent(i)] > self.heap[i]): 
            # Swap heap[i] with heap[parent(i)] 
            self.heap[i] , self.heap[self.parent(i)] = ( 
            self.heap[self.parent(i)], self.heap[i]) 
    def extractMin(self):
        return heappop(self.heap)
    def deleteKey(self,i):
        self.decreaseKey(i,float("-inf"))
        self.extractMin()
    def getMin(self):
        return self.heap[0]
class Node():
    def __init__(self,x,y,g,f,h,parent,wall):
        self.x = x
        self.y = y
        self.g = g
        self.f = f
        self.h = h
        self.parent = parent
        self.wall = wall
    def find_children(self):
        a = []
        c = [[self.x,self.y + 1],[self.x,self.y-1],[self.x+1,self.y],[self.x-1,self.y]]
        for i in c:
            if (0<=i[0]<=9 and 0<=i[1]<=9):
                if (grid[i[1]][i[0]].wall == False):
                    a.append(Node(i[0],i[1],0,0,0,0,False))
            else:
                pass    
        return a
def distance(x,y,a,b):
    return abs(x-a) + abs(y-b)        
#main loop        
while run:
    pygame.time.delay(10)
    #draw the grid
    for y in range(0,500, 50):
        for x in range(0,500,50):
            pygame.draw.rect(screen,(255,140,0),(x,y,50,50),2)
    #drawing the buttons
    pygame.draw.rect(screen,(255,0,0),(50,550,180,50))
    pygame.draw.rect(screen,(0,255,0),(280,550,180,50))
    #objects for the text
    findpath = myfont.render('Find Path', False, (0, 0, 0))
    clear = myfont.render('Clear Grid', False, (0, 0, 0))
    #blitting the text on the buttons
    screen.blit(findpath,(70,570))
    screen.blit(clear,(300,570))
    pygame.display.update()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #detecting the keydown presses
            if event.type == pygame.KEYDOWN:
                #the keys we want to detect
                if event.key == pygame.K_s:
                    start = 1
                if event.key == pygame.K_e:
                    end = 1
                if event.key == pygame.K_d:
                    d = 1
            #mouse pressed
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = m.floor(pos[0]/50)*50
                y = m.floor(pos[1]/50)*50
                if (50<=x<=230 and 550<=y<=600):
                    algorun = True
                    for i in range(0,10):
                        for j in range(0,10):
                            if grid[i][j] == 0:
                                grid[i][j] = Node(i,j,0,0,0,0,False)
                            else:
                                grid[i][j] = Node(i,j,0,0,0,0,True)
                    openlist = []
                    closedlist = []
                    sx = int(startt[0][0]/50) 
                    sy = int(startt[0][1]/50) 
                    ex = int(endt[0][0]/50) 
                    ey = int(endt[0][1]/50) 
                    snode = Node(sx,sy,0,0,0,0,True)
                    openlist.append(snode)
                    while algorun == True and len(openlist)!=0:
                        pygame.time.delay(10)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                        temp = MinHeap()
                        temp2 = []
                        for i in openlist:
                            temp.insert(i.f)
                            temp2.append(i.f)
                        tq = temp.getMin()
                        index = temp2.index(tq)
                        q = openlist[index]
                        openlist.remove(q)
                        closedlist.append(q)
                        pygame.draw.rect(screen,(255,255,1),(q.x*50,q.y*50,50,50))
                        #drawing the lines
                        for i in range(0,500,50):
                            pygame.draw.line(screen,(255,140,0),(0,i),(500,i),5)
                            pygame.draw.line(screen,(255,140,0),(i,0),(i,500),5)
                        pygame.display.update() 
                        if q.x == ex and q.y == ey:
                            temp = q
                            path = []
                            path.append(temp)
                            while(temp.parent):
                                path.append([temp.parent.x,temp.parent.y])
                                temp = temp.parent 
                            del path[0]
                            for i in path:
                                pygame.draw.rect(screen, (255,255,255),(i[0]*50,i[1]*50,50,50))
                            pygame.draw.rect(screen,(255,0,0),(sx*50,sy*50,50,50))
                            pygame.draw.rect(screen,(0,255,0),(ex*50,ey*50,50,50))
                            for i in range(0,500,50):
                                pygame.draw.line(screen,(255,0,0),(0,i),(500,i),5)
                                pygame.draw.line(screen,(255,0,0),(i,0),(i,500),5)
                                pygame.display.update()
                            algorun = False
                        children = q.find_children()
                        for child in children:
                            if child in closedlist:
                                continue
                            child.g = q.g + 1
                            child.h = distance(child.x,child.y,ex,ey)
                            child.f = child.g + child.h
                            child.parent = q
                            tpos = []    
                            for i in openlist:
                                tpos.append([i.x,i.y])
                            if [child.x,child.y] in tpos:
                                if child.g > openlist[tpos.index([child.x,child.y])].g:
                                    continue
                                else:
                                    openlist.remove(openlist[tpos.index([child.x,child.y])])
                            openlist.append(child)
                elif (280<=x<=460 and 550<=y<=600):
                    grid = [[0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0]]
                    for y in range(0,500, 50):
                        for x in range(0,500,50):
                            pygame.draw.rect(screen,(0,0,0),(x,y,50,50))
                    startt = []
                    endt = []
                elif (0<=x<=450 and 0<=y<=450):
                    if start == 1:
                        if len(startt)>0:
                            pygame.draw.rect(screen,(0,0,0),(startt[0][0],startt[0][1],50,50))
                            startt.remove(startt[0])
                            startt.append([x,y])
                            pygame.draw.rect(screen,(255,0,0),(x,y,50,50))
                            start = 0
                        else:
                            pygame.draw.rect(screen,(255,0,0),(x,y,50,50))
                            startt.append([x,y])
                            start = 0
                    elif end ==1:
                        if len(endt)>0:
                            pygame.draw.rect(screen,(0,0,0),(endt[0][0],endt[0][1],50,50))
                            endt.remove(endt[0])
                            endt.append([x,y])
                            pygame.draw.rect(screen,(0,255,0),(x,y,50,50))
                            end = 0
                        else:
                            pygame.draw.rect(screen,(0,255,0),(x,y,50,50))
                            endt.append([x,y])
                            end = 0
                    elif d ==1:
                        pygame.draw.rect(screen,(0,0,0),(x,y,50,50))
                        grid[int(y/50)][int(x/50)] = 0
                        d = 0
                    else:
                        pygame.draw.rect(screen,(0,0,255),(x,y,50,50))
                        grid[int(y/50)][int(x/50)] = 2
                        drag = 1
            elif event.type == pygame.MOUSEMOTION:
                x = m.floor(pos[0]/50)*50
                y = m.floor(pos[1]/50)*50
                if drag == 1:
                    pygame.draw.rect(screen,(0,0,255),(x,y,50,50))
                    grid[int(y/50)][int(x/50)] = 2
            elif event.type == pygame.MOUSEBUTTONUP:
                drag = 0
                