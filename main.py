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

def mainTSP() -> None:
    global window
    window = tk.Tk()

    limitFrame = tk.Frame()

    limitLabel = tk.Label(master=limitFrame, text="How many nodes: ", width=40)
    limitLabel.pack(side=tk.LEFT)

    limitEntry = tk.Entry(master=limitFrame, width=20)
    limitEntry.insert(0,"20")
    limitEntry.pack(side=tk.RIGHT)

    limitFrame.pack()

    antFrame = tk.Frame()

    antLabel = tk.Label(master=antFrame, text="How many ants: ", width=40)
    antLabel.pack(side=tk.LEFT)

    antEntry = tk.Entry(master=antFrame, width=20)
    antEntry.insert(0,"30")
    antEntry.pack(side=tk.RIGHT)

    antFrame.pack()

    iterationFrame = tk.Frame()

    iterationLabel = tk.Label(master=iterationFrame, text="How many iterations: ", width=40)
    iterationLabel.pack(side=tk.LEFT)

    iterationEntry = tk.Entry(master=iterationFrame, width=20)
    iterationEntry.insert(0,"30")
    iterationEntry.pack(side=tk.RIGHT)

    iterationFrame.pack()

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

    evapScale = tk.Scale(master=evapFrame, from_=0, to=1, resolution=0.05, orient=tk.HORIZONTAL, width=20)
    evapScale.set(0.1)
    evapScale.pack(side=tk.RIGHT)

    evapFrame.pack()

    startButton = tk.Button(
        text="Run Sim", 
        width=25, 
        command=lambda:runThread(
            float(alphaScale.get()),
            float(betaScale.get()),
            float(evapScale.get()),
            1,
            int(limitEntry.get()),
            int(antEntry.get()),
            int(iterationEntry.get())
        )
    )
    startButton.pack()

    progressFrame = tk.Frame()

    global progressLabel
    progressLabel = tk.Label(master=progressFrame, text="", width=60)
    progressLabel.pack(side=tk.LEFT)

    progressFrame.pack()

    global fig
    fig = Figure(figsize = (5, 5), dpi = 100) 
  
    global canvas
    canvas = FigureCanvasTkAgg(fig, 
                               master = window)   
    canvas.draw() 

    canvas.get_tk_widget().pack() 
 
    global graph
    graph = nx.Graph()

    window.after(0, redrawGraph)
    window.mainloop()
    # runTSP(1,2,0.1,1)

def runThread(alphaScale,betaScale,evapScale,q,limitEntry,antEntry,iterationEntry):
    t = threading.Thread(target=lambda:runTSP(
        float(alphaScale),
        float(betaScale),
        float(evapScale),
        q,
        int(limitEntry),
        int(antEntry),
        int(iterationEntry)
    ))
    t.start()

def redrawGraph(): 
    fig.clf()
    plot1 = fig.add_subplot(111)

    pos = {node: coords for node, coords in nx.get_node_attributes(graph, "pos").items()}
    nx.draw(graph, pos, with_labels=False, node_size=50, node_color="#4169E1", ax=plot1)
    canvas.draw()
    window.after(100,redrawGraph)

def updateGraph(route, coords):
    graph.clear()
    for r in range(len(route)-1):
        node = route[r]
        graph.add_node(node,pos=(coords[node][1], coords[node][0]))
        graph.add_edge(node, route[r+1])

def runTSP(α,β,evaporationCoeff,q,limit,antCount,iterations) -> None:
    # limit = int(input("Enter row limit for data: "))
    coords = loadCSV("gb.csv",1,2,True,limit=limit)
    # coords = loadTSP("datasets_tsp_att48_xy.txt",limit=limit)
    distMat = Mat(len(coords),β)
    distMat.formDistMat(coords,"haversine")
    tau  = np.ones(distMat.shape)
    # Python version of infinitely high cost
    bestCost = float("inf")
    bestRoute = []
    ants = []
    startTime = time.time()
    for i in range(iterations):
        ants = []
        tauChange = np.zeros(distMat.shape)
        for a in range(antCount):
            ants.append(Ant(nodes=list(range(distMat.size)),alpha=α,beta=β))
        for a, ant in enumerate(ants):
            ant.move(tau,distMat)
            if(ant.cost < bestCost):
                bestCost = ant.cost
                bestRoute = ant.route
                updateGraph(bestRoute,coords=coords)
            for r in range(len(ant.route)-1):
                tauChange[ant.route[r]][ant.route[r+1]] += q / ant.cost
            tau += tauChange / antCount
            tauChange = np.zeros(distMat.shape)
            # progressBar((i/iterations)+((a/(len(ants))/iterations)))
            progressBarLabel((i/iterations)+((a/(len(ants))/iterations)))
        tau *= (1-evaporationCoeff)
        
    endTime = time.time()
    totalTime = endTime - startTime
    # print("Best Route: "+str(bestRoute))
    # print("Cost of: "+str(bestCost))
    # print("Time taken: "+str(totalTime))
    # print("Time per ant: "+str(totalTime/(iterations*antCount)))
    updateGraph(bestRoute,coords=coords)

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

def progressBarLabel(data:float,string:str="") -> None:
    '''
        data: float between 0-1
        string: a string to be displayed after the progress bar
    '''
    # Gets position of index in list over list length as a floored percentage
    percent = int(np.floor(data*100))
    # Calculates half the percentage, this provides only 50 characters and a less excessive progress bar
    percentOver4 = int(percent/4)
    # Prints out the progress bar, ending in an escape character "\r" so that it keeps printing on the same line everytime
    progressLabel.config(text=string+"Training Progress: "+str(percent)+"% "+("█"*(percentOver4))+("▒"*(25-percentOver4)))

class App(tk.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.coords = []
        self.loader = Loader()

        self.create_widgets()

        self.after(0, self.redrawGraph)

    def open_file_browser(self):
        filepath = filedialog.askopenfilename(initialdir="./",title="Select a File")#, filetypes=(("all files", "*.*")))
        self.coords = self.loader.loadFile(filepath=filepath)

    def create_widgets(self):
        menuBar = tk.Menu(self)
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Open", command=self.open_file_browser)
        menuBar.add_cascade(label="File", menu=fileMenu)
        self.config(menu=menuBar)

        limitFrame = tk.Frame()

        limitLabel = tk.Label(master=limitFrame, text="How many nodes: ", width=40)
        limitLabel.pack(side=tk.LEFT)

        limitEntry = tk.Entry(master=limitFrame, width=20)
        limitEntry.insert(0,"20")
        limitEntry.pack(side=tk.RIGHT)

        limitFrame.pack()

        antFrame = tk.Frame()

        antLabel = tk.Label(master=antFrame, text="How many ants: ", width=40)
        antLabel.pack(side=tk.LEFT)

        antEntry = tk.Entry(master=antFrame, width=20)
        antEntry.insert(0,"30")
        antEntry.pack(side=tk.RIGHT)

        antFrame.pack()

        iterationFrame = tk.Frame()

        iterationLabel = tk.Label(master=iterationFrame, text="How many iterations: ", width=40)
        iterationLabel.pack(side=tk.LEFT)

        iterationEntry = tk.Entry(master=iterationFrame, width=20)
        iterationEntry.insert(0,"30")
        iterationEntry.pack(side=tk.RIGHT)

        iterationFrame.pack()

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

        evapScale = tk.Scale(master=evapFrame, from_=0, to=1, resolution=0.05, orient=tk.HORIZONTAL, width=20)
        evapScale.set(0.1)
        evapScale.pack(side=tk.RIGHT)

        evapFrame.pack()

        startButton = tk.Button(
            text="Run Sim", 
            width=25, 
            command=lambda:self.runThread(
                float(alphaScale.get()),
                float(betaScale.get()),
                float(evapScale.get()),
                1,
                int(limitEntry.get()),
                int(antEntry.get()),
                int(iterationEntry.get())
            )
        )
        startButton.pack()

        progressFrame = tk.Frame()

        global progressLabel
        progressLabel = tk.Label(master=progressFrame, text="", width=60)
        progressLabel.pack(side=tk.LEFT)

        progressFrame.pack()

        self.fig = Figure(figsize = (4, 4), dpi = 100) 
    
        # global canvas
        self.canvas = FigureCanvasTkAgg(self.fig, 
                                master = self)   
        self.canvas.draw() 

        self.canvas.get_tk_widget().pack() 
    
        # global graph
        self.graph = nx.Graph()

    def redrawGraph(self): 
        self.fig.clf()
        plot1 = self.fig.add_subplot(111)

        pos = {node: coords for node, coords in nx.get_node_attributes(self.graph, "pos").items()}
        nx.draw(self.graph, pos, with_labels=False, node_size=50, node_color="#4169E1", ax=plot1)
        self.canvas.draw()
        self.after(100,self.redrawGraph)

    def runThread(self,alphaScale,betaScale,evapScale,q,limitEntry,antEntry,iterationEntry):
        t = threading.Thread(target=lambda:self.runTSP(
            float(alphaScale),
            float(betaScale),
            float(evapScale),
            q,
            int(limitEntry),
            int(antEntry),
            int(iterationEntry)
        ))
        t.start()

    def updateGraph(self,route, coords):
        self.graph.clear()
        for r in range(len(route)-1):
            node = route[r]
            self.graph.add_node(node,pos=(coords[node][1], coords[node][0]))
            self.graph.add_edge(node, route[r+1])

    def runTSP(self,α,β,evaporationCoeff,q,limit,antCount,iterations) -> None:
        # limit = int(input("Enter row limit for data: "))
        # coords = loadCSV("gb.csv",limit=limit)
        # coords = loadTSP("datasets_tsp_att48_xy.txt",limit=limit)
        if(self.coords == []):
            return
        distMat = Mat(len(self.coords),β)
        distMat.formDistMat(self.coords,"haversine")
        tau  = np.ones(distMat.shape)
        # Python version of infinitely high cost
        bestCost = float("inf")
        bestRoute = []
        ants = []
        startTime = time.time()
        for i in range(iterations):
            ants = []
            tauChange = np.zeros(distMat.shape)
            for a in range(antCount):
                ants.append(Ant(nodes=list(range(distMat.size)),alpha=α,beta=β))
            for a, ant in enumerate(ants):
                ant.move(tau,distMat)
                if(ant.cost < bestCost):
                    bestCost = ant.cost
                    bestRoute = ant.route
                    self.updateGraph(bestRoute,coords=self.coords)
                for r in range(len(ant.route)-1):
                    tauChange[ant.route[r]][ant.route[r+1]] += q / ant.cost
                tau += tauChange / antCount
                tauChange = np.zeros(distMat.shape)
                # progressBar((i/iterations)+((a/(len(ants))/iterations)))
                progressBarLabel((i/iterations)+((a/(len(ants))/iterations)))
            tau *= (1-evaporationCoeff)
            
        endTime = time.time()
        totalTime = endTime - startTime
        # print("Best Route: "+str(bestRoute))
        # print("Cost of: "+str(bestCost))
        # print("Time taken: "+str(totalTime))
        # print("Time per ant: "+str(totalTime/(iterations*antCount)))
        self.updateGraph(bestRoute,coords=self.coords)

if __name__ == "__main__":
    app = App()
    app.mainloop()
    # mainSim()