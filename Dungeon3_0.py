import pygame as pg
import numpy as np
import time,pickle,math,random,datetime,os
w,h=650,500
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
blue=(0,0,155)
cir=pg.draw.circle
lines=pg.draw.lines
line=pg.draw.line
rect=pg.draw.rect

class Dungeon:
    def __init__(self,resolution,w_h):
        self.win=pg.display.set_mode((w_h[0],w_h[1]))
        self.res=resolution
        self.w_h=w_h
        self.grid=np.empty((resolution,resolution,3))
        self.grid_copy=self.grid.copy()
        self.grid_color=(71,29,6)
        self.fill_color=(10,4,0)
        self.dimxy=[self.w_h[0]/self.res,self.w_h[1]/self.res]
        self.create_grid()
        self.pen=0
        self.mode=0
        self.fps=False
        self.max_score=0
        self.move_increment=1
        self.moves=10
        self.score=0
        self.character=None
        self.vision_depth=1
    def create_grid(self):
        dimxy=self.dimxy
        for x,r in enumerate(self.grid):
            for y,g in enumerate(r):
                self.grid[x][y]=[x*dimxy[0],y*dimxy[1],0]
    def draw(self):
        run=True
        clock=pg.time.Clock()
        while run:
            if self.fps:
                clock.tick(self.fps)
            self.win.fill(self.fill_color)
            dimxy=self.dimxy
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    run=False
            for x in self.grid:
                for g in x:
                    if g[2]==1:
                        rect(self.win,self.grid_color,(g[0],g[1],dimxy[0],dimxy[1]))
                    if g[2]==2:
                        rect(self.win,red,(g[0],g[1],dimxy[0],dimxy[1]))
            self.creator()
            self.save()
            self.pen_size()
            pg.display.update()
    def part_draw(self):
        run=True
        clock=pg.time.Clock()
        while run:
            if self.fps:
                clock.tick(self.fps)
            self.win.fill(self.fill_color)
            dimxy=self.dimxy
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    run=False
            view_depth=6
            v_r=(view_depth*2)+1
            mousex,mousey=pg.mouse.get_pos()
            gridx,gridy=int(mousex/(self.w_h[0]/self.res)),int(mousey/(self.w_h[1]/self.res))
            scale=v_r
            for v1,x in enumerate(range(v_r)):
                    for v2,y in enumerate(range(v_r)):
                        try:
                            g=self.grid[gridx+x-view_depth,gridy+y-view_depth]
                            if  g[2]==1:
                                rect(self.win,self.grid_color,(v1/scale*self.w_h[0],v2/scale*self.w_h[1],dimxy[0]/(dimxy[0]*v_r)*self.w_h[0],dimxy[1]/(dimxy[1]*v_r)*self.w_h[1]))
                            if g[2]==2:
                                rect(self.win,red,(g[0],g[1],dimxy[0],dimxy[1]))
                        except:
                            pass
            pg.display.update()
    def game_mode(self):
        if self.character==None:
            for x in range(self.res):
                for y in range(self.res):
                    if self.grid[x,y,2]!=1:
                        self.character=[x,y]
                        break

        run=True
        clock=pg.time.Clock()
        while run:
            if self.fps:
                clock.tick(self.fps)
            self.win.fill(self.fill_color)
            
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    run=False
            self.key_move()
            dimxy=self.dimxy
            view_depth=10
            v_r=(view_depth*2)+1
            gridx,gridy=int(self.character[0]),int(self.character[1])
            scale=v_r
            for v1,x in enumerate(range(v_r)):
                    for v2,y in enumerate(range(v_r)):
                        try:
                            g=self.grid[gridx+x-view_depth,gridy+y-view_depth]
                            if  g[2]==1:
                                rect(self.win,self.grid_color,(v1/scale*self.w_h[0],v2/scale*self.w_h[1],dimxy[0]/(dimxy[0]*v_r)*self.w_h[0],dimxy[1]/(dimxy[1]*v_r)*self.w_h[1]))
                            if g[2]==2:
                                rect(self.win,red,(v1/scale*self.w_h[0],v2/scale*self.w_h[1],dimxy[0]/(dimxy[0]*v_r)*self.w_h[0],dimxy[1]/(dimxy[1]*v_r)*self.w_h[1]))
                        except:
                            pass
            rect(self.win,blue,(view_depth/scale*self.w_h[0],view_depth/scale*self.w_h[1],dimxy[0]/(dimxy[0]*v_r)*self.w_h[0],dimxy[1]/(dimxy[1]*v_r)*self.w_h[1]))
            pg.display.update()
    
    
    def draw_ones(self):
        self.win.fill(self.fill_color)
        dimxy=self.dimxy
        for x in self.grid:
            for g in x:
                if g[2]==2:
                    rect(self.win,red,(g[0],g[1],dimxy[0],dimxy[1]))
        pg.display.update()
    
    
    def draw_char(self):
        dimxy=self.dimxy
        rect(self.win,blue,(self.grid[self.character[0]][self.character[1]][0],
                            self.grid[self.character[0]][self.character[1]][1],
                            dimxy[0],dimxy[1]))
        pg.display.update()
    
    
    def pen_size(self):
        key=pg.key.get_pressed()
        if key[pg.K_c] and self.pen<=5:
            self.pen+=0.5
            time.sleep(0.2)
            print(self.pen)
        if key[pg.K_v] and self.pen >=1:
            self.pen-=0.5
            time.sleep(0.2)
            print(self.pen)
    
    def creator(self):
        key=pg.key.get_pressed()
        mousex,mousey=pg.mouse.get_pos()
        gridx,gridy=int(mousex/(self.w_h[0]/self.res)),int(mousey/(self.w_h[1]/self.res))
        if key[pg.K_q]:
            self.mode=0
        if key[pg.K_1]:
            self.mode=1
        if key[pg.K_2]:
            self.mode=2
        if key[pg.K_e]:
            self.create_grid()
        if key[pg.K_w]:
            for x in self.grid:
                for g in x:
                    if g[2]==1:
                        g[2]=0
                    elif g[2]==0:
                        g[2]=1
            time.sleep(0.25)
        if pg.mouse.get_pressed()==(True,False,False):
            pen=int(self.pen)
            view_range=(pen*2)+1
            for v1 in range(view_range):
                    for v2 in range(view_range):
                        # if self.grid[(gridx+v1-pen),(gridy+v2-pen),2]:
                        self.grid[(gridx+v1-pen),(gridy+v2-pen),2]=self.mode
            if key[pg.K_a]:
                print([gridx,gridy])
    
    
    
    def cal_score(self):
        for x in self.grid:
            for g in x:
                if g[2]==2:
                    self.max_score+=1
        print(self.max_score)
    
    
    def save(self):
        key=pg.key.get_pressed()
        files=os.listdir()
        named=True
        name=1
        if key[pg.K_s]:
            while named:
                if f"dungeon{name}.pickle" not in files:
                    with open(f"dungeon{name}.pickle","wb") as f:
                        pickle.dump((self.grid,self.res,self.w_h),f)
                    named=False
                    print(f"Dungeon saved! dungeon{name}.pickle")
                    time.sleep(0.5)
                name+=1
    def load(self,name):
        with open(f"{name}.pickle","rb") as f:
            grid,res,w_h=pickle.load(f)
            self.__init__(res,w_h)
            self.grid=grid
            self.grid_copy=grid.copy()
        print(f"Dungeon loaded!")
    
    
    def view(self):
        state=[]
        view_range=(self.vision_depth*2)+1
        for x in range(view_range):
                for y in range(view_range):
                    state.append(self.grid[(self.character[0]+x-self.vision_depth)][(self.character[1]+y-self.vision_depth)][2])
        return state
    
    
    
    def reset(self):
        self.grid=self.grid_copy.copy()
        self.moves=10
        self.score=0
        return self.view()
    def set_char(self,pos):
        self.character=pos
    def move_char(self,action):
        done=False
        reward=0
        if action==0:
            self.character[1]-=1
        if action==1:
            self.character[1]+=1
        if action==2:
            self.character[0]+=1
        if action==3:
            self.character[0]-=1
        
        if self.grid[self.character[0]][self.character[1]][2]==2:
                self.grid[self.character[0]][self.character[1]][2]=0
                self.moves+=self.move_increment
                self.score+=1
                reward=1
        else:
            self.moves-=1
        
        if self.grid[self.character[0]][self.character[1]][2]==1 or self.moves<=0:
            done=True
        return self.view(),done,reward
    
    
    def key_move(self):
        key=pg.key.get_pressed()
        new_pos=self.character.copy()
        if key[pg.K_i]:
            new_pos[1]-=0.1
        if key[pg.K_k]:
            new_pos[1]+=0.1
        if key[pg.K_j]:
            new_pos[0]-=0.1
        if key[pg.K_l]:
            new_pos[0]+=0.1
        if self.grid[int(new_pos[0]),int(new_pos[1]),2]!=1:
            self.character=new_pos
        else:
            new_pos=self.character.copy()





