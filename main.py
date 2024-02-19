import numpy as np
import tkinter as tk
import customtkinter as ctk
import networkx as nx
import time
import threading
import math

from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 

from tkinter import filedialog

from ant import Ant,AntSim
from distance_matrix import Mat
from pheromone_matrix import PMat
from file_loader import Loader
from tsp import TSP
from frames import StartFrame,TSPFrame

def mainSim() -> None:

    WIDTH, HEIGHT = 320, 320
    global SIMWIDTH
    SIMWIDTH = 64

    global window
    window = tk.Tk()
    global canvas
    canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="#000000")
    canvas.pack()
    global img
    img = tk.PhotoImage(width=WIDTH, height=HEIGHT,file='IMG_0069.png')
    # canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

    global antMap
    antMap = [[0] * SIMWIDTH for i in range(SIMWIDTH)]

    foodTau = PMat(size=SIMWIDTH)
    nestTau = PMat(size=SIMWIDTH)
    for i in range(SIMWIDTH):
        for j in range(SIMWIDTH):
            if(img.get(i,j)[1] == 255):
                foodTau.set(i,j,1)
                foodTau.addPersistant([i,j])
            elif(img.get(i,j)[2] == 255):
                nestTau.set(i,j,1)
                nestTau.addPersistant([i,j])
            elif(img.get(i,j)[0] == 0):
                foodTau.set(i,j,0.01)
                nestTau.set(i,j,0.01)
            else:
                foodTau.set(i,j,-1)
                nestTau.set(i,j,-1)

    ants = []
    spawn = nestTau.persist[0]
    for i in range(1000):
        ant = AntSim(spawn,1,2,SIMWIDTH)
        antMap[spawn[0]][spawn[1]] += 1
        ants.append(ant)

    alphaFrame = tk.Frame()

    alphaLabel = tk.Label(master=alphaFrame, text="Value of pheromone impact: ", width=40)
    alphaLabel.pack(side=tk.LEFT)

    alphaScale = tk.Scale(master=alphaFrame, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, tickinterval=1, width=20)
    alphaScale.set(1)
    alphaScale.pack(side=tk.RIGHT)

    alphaFrame.pack()

    betaFrame = tk.Frame()

    betaLabel = tk.Label(master=betaFrame, text="Value of proximity impact: ", width=40)
    betaLabel.pack(side=tk.LEFT)

    betaScale = tk.Scale(master=betaFrame, from_=0, to=4, resolution=0.1, orient=tk.HORIZONTAL, tickinterval=1, width=20)
    betaScale.set(2)
    betaScale.pack(side=tk.RIGHT)

    betaFrame.pack()

    evapFrame = tk.Frame()

    evapLabel = tk.Label(master=evapFrame, text="Evaporation Coefficient: ", width=40)
    evapLabel.pack(side=tk.LEFT)

    evapScale = tk.Scale(master=evapFrame, from_=0, to=0.5, resolution=0.01, orient=tk.HORIZONTAL, width=20)
    evapScale.set(0.1)
    evapScale.pack(side=tk.RIGHT)

    evapFrame.pack()

    startButton = tk.Button(
        text="Run Sim", 
        width=25, 
        command=lambda:runSimThread(
            foodTau=foodTau,
            nestTau=nestTau,
            ants=ants,
            alpha=float(alphaScale.get()),
            beta=float(betaScale.get()),
            evap=float(evapScale.get())
        )
    )
    startButton.pack()

    window.after(0, lambda:redrawPixels(foodTau,nestTau))
    window.mainloop()

def runSimThread(foodTau, nestTau, ants, alpha, beta, evap):
    for ant in ants:
        ant.alpha = alpha
        ant.beta = beta
    t = threading.Thread(target=lambda:runSim(foodTau=foodTau, nestTau=nestTau, ants=ants, evaporation=evap))
    t.start()

def runSim(foodTau, nestTau, ants, evaporation):
    population = len(ants)
    # evaporation = 0.02
    pheromone = 1
    for i in range(5000):
        for ant in ants:
            antMap[ant.x][ant.y] -= 1
            ant.move(foodTau,nestTau)
            if(ant.foundFood):
                foodTau.add(ant.x,ant.y,(pheromone/population))
            else:
                nestTau.add(ant.x,ant.y,(pheromone/population))
            antMap[ant.x][ant.y] += 1
        foodTau.evaporate(evaporation)
        nestTau.evaporate(evaporation)
        if(i % 50 == 0):
            redrawPixels(foodTau,nestTau)

def redrawPixels(foodTau,nestTau):
    canvas.delete("all")
    colourMap = [["#"] * SIMWIDTH for i in range(SIMWIDTH)]
    highestPher = foodTau.highest()
    pherMap = foodTau.all()
    for i,row in enumerate(pherMap):
        for j,item in enumerate(row):
            if(item>0 and [i,j] not in foodTau.persist):
                val = (item/highestPher)
            else:
                val = 0
            r = str(hex(int(255*val))[2:])
            if(len(r) == 1):
                r = "0" + r
            colourMap[i][j] += r
    highestPher2 = nestTau.highest()
    pherMap2 = nestTau.all()
    for i,row in enumerate(pherMap2):
        for j,item in enumerate(row):
            if(item>0 and [i,j] not in nestTau.persist):
                val = (item/highestPher2)
            else:
                val = 0
            g = str(hex(int(255*val))[2:])
            if(len(g) == 1):
                g = "0" + g
            colourMap[i][j] += g
                # colour = '#'+str(hex(int(255*val))[2:])+str(hex(int(1))[2:])+str(hex(int(1))[2:])
                # canvas.create_rectangle(i*10,j*10,(i*10)+10,(j*10)+10,fill=colour,width=0)
    highestAnt = 0
    for row in antMap:
        if(max(row)>highestAnt):
            highestAnt = max(row)
    for i,row in enumerate(antMap):
        for j,item in enumerate(row):
            if(item > 0):
                val = (item/highestAnt)
            else:
                val = 0
            b = str(hex(int(255*val))[2:])
            if(len(b) == 1):
                b = "0" + b
            colourMap[i][j] += b
                # colour = '#'+str(hex(int(255*val))[2:])+str(hex(int(255*val))[2:])+str(hex(int(1))[2:])
                # canvas.create_rectangle(i*10,j*10,(i*10)+10,(j*10)+10,fill=colour,width=0)
    for i,row in enumerate(colourMap):
        for j,item in enumerate(row):
            if item != '#000000':
                canvas.create_rectangle(i*5,j*5,(i*5)+5,(j*5)+5,fill=item,width=0)
    # window.after(50,redrawPixels)

def drawAnt(x,y,val):
    colour = '#'+str(hex(int(255*val))[2:])+str(hex(int(255*val))[2:])+str(hex(int(255*val))[2:])
    # colour = '#ffffff'
    for i in range(10):
        # data.extend('{' + ' '.join('#ffffff' for j in range(10)) + '}')
        for j in range(10):
        #     print(x+i,y+j)
            
            img.put(colour, (x+i,y+j))
    # image_array = np.array(img)
    # image_array[y:y+10, x:x+10] = '#ffffff'
    # img.put(" ".join(data), to=(x, y))
    # img.put(data)

def draw_rectangle(x, y, color):
    pixel_data = []
    for i in range(10):
        for j in range(10):
            pixel_data.extend((x + i, y + j, color))
    img.put(pixel_data)

def progressBar(data:float,string:str="") -> None:
    '''
        data: float between 0-1
        string: a string to be displayed after the progress bar
    '''
    # Gets position of index in list over list length as a floored percentage
    percent = int(np.floor(data*100))
    # Calculates half the percentage, this provides only 50 characters and a less excessive progress bar
    percentOver4 = int(percent/4)
    # Prints out the progress bar, ending in an escape character "\r" so that it keeps printing on the same line everytime
    print(string+"Training Progress: "+str(percent)+"% "+("█"*(percentOver4))+("▒"*(25-percentOver4)), end="\r")

class App(tk.Tk):
    def __init__(self,screenName:str|None=None,baseName:str|None=None,className:str="Tk",useTk:bool=True,sync:bool=False,use:str|None=None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        # self.attributes('-fullscreen', True)
        # self.state('zoomed') 

        self.fs = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartFrame, TSPFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartFrame")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

        menuBar = frame.menuBar(self)
        self.configure(menu=menuBar)

    def toggle_fullscreen(self,even=None):
        self.fs = not self.fs
        self.attributes("-fullscreen", self.fs)

    def end_fullscreen(self,event=None):
        self.fs = False
        self.attributes("-fullscreen", False)

if __name__ == "__main__":
    app = App()
    app.mainloop()
    # mainSim()