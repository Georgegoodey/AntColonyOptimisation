import tkinter as tk
import networkx as nx
import threading
import numpy as np

from tkinter import filedialog
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg) 

from tkinter_objects import FrameObject
from file_loader import Loader
from tsp import TSP
from pheromone_matrix import PMat
from ant import AntSim

class StartFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Ant Colony Optimisation")
        label.pack(side="top", fill="x", pady=10)

        tspButton = tk.Button(self, text="Travelling Salesman Implementation",
                            command=lambda: controller.showFrame("TSPFrame"))
        simButton = tk.Button(self, text="ACO Simulation",
                            command=lambda: controller.showFrame("SimFrame"))
        tspButton.pack()
        simButton.pack()

    def menuBar(self,root):
        menuBar = tk.Menu(root)
        return menuBar

class TSPFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        titleFrame = tk.Frame(master=self, width=1000)

        label = tk.Label(master=titleFrame, text="Travelling Salesman using ACO")
        label.pack(side=tk.BOTTOM, pady=10)

        self.returnButton = tk.Button(master=titleFrame, text="Return to Main Menu",command=lambda: controller.showFrame("StartFrame"))
        self.returnButton.pack(side=tk.LEFT)

        titleFrame.pack(side=tk.TOP, fill=tk.X)
        
        self.coords = []
        self.loader = Loader()

        self.createWidgets()

        self.after(0, self.redrawGraph)

    def open_file_browser(self):
        filepath = filedialog.askopenfilename(initialdir="./",title="Select a File", filetypes=(("TSP files", "*.tsp"), ("All files", "*.*")))
        file = self.loader.loadFile(filepath=filepath)
        self.coords = file[0]
        # if(file[1] != None):
        #     self.tour = file[1]
        #     print(self.tour)
        #     print(self.tsp.getCost(self.tour))
        if(self.coords):
            self.tsp = TSP(self.coords)
        if(file[1] != None):
            self.tour = file[1]
            print(self.tour)
            print(self.tsp.getCost(self.tour))

    def menuBar(self,root):
        menuBar = tk.Menu(root)
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Open", command=self.open_file_browser)
        menuBar.add_cascade(label="File", menu=fileMenu)
        return menuBar

    def createWidgets(self):

        widgetFrame = tk.Frame(master=self)

        menuFrame = tk.Frame(master=widgetFrame)

        # limit = FrameObject(master=self,type="entry",text="How many nodes: ",val="20")

        count = FrameObject(master=menuFrame,type="entry",text="How many ants: ",val="30")

        iterations = FrameObject(master=menuFrame,type="entry",text="How many iterations: ",val="30")

        alpha = FrameObject(master=menuFrame,type="scale",text="Value of pheromone impact: ",val=1,size=(0,2),resolution=0.1)

        beta = FrameObject(master=menuFrame,type="scale",text="Value of proximity impact: ",val=2,size=(0,4),resolution=0.1)

        evap = FrameObject(master=menuFrame,type="scale",text="Evaporation Coefficient: ",val=0.1,size=(0,1),resolution=0.05)

        startButton = tk.Button(
            master=menuFrame,
            text="Run Sim", 
            width=25, 
            command=lambda:self.runThread(alpha.get(),beta.get(),evap.get(),1,int(count.get()),int(iterations.get()))
        )
        startButton.pack()

        solverButton = tk.Button(
            master=menuFrame,
            text="Run Solver", 
            width=25, 
            command=lambda:self.runSolver()
        )
        solverButton.pack()

        self.progressFrame = tk.Frame(master=menuFrame)

        self.progressLabel = tk.Label(master=self.progressFrame, text="", width=60)
        self.progressLabel.pack(side=tk.LEFT)
        self.progressBarLabel(0)

        self.progressFrame.pack()

        self.costFrame = tk.Frame(master=menuFrame)

        self.costLabel = tk.Label(master=self.costFrame, text="ACO Cost: 0", width=40)
        self.costLabel.pack(side=tk.LEFT)

        self.costFrame.pack()

        self.solverCostFrame = tk.Frame(master=menuFrame)

        self.solverCostLabel = tk.Label(master=self.solverCostFrame, text="Solver Cost: 0", width=40)
        self.solverCostLabel.pack(side=tk.LEFT)

        self.solverCostFrame.pack()

        menuFrame.pack(side=tk.LEFT)

        self.fig = Figure(figsize = (4, 4), dpi = 100) 

        # Trying to make this scale
        self.canvas = FigureCanvasTkAgg(self.fig,master=widgetFrame)
        self.canvas.draw() 

        self.canvas.get_tk_widget().pack(side=tk.RIGHT,fill=tk.BOTH)

        self.graph = nx.Graph()

        self.solverGraph = nx.Graph()

        widgetFrame.pack(fill=tk.BOTH)

    def runThread(self,alpha,beta,evap,q,count,iterations):
        t = threading.Thread(target=lambda:self.runTSP(alpha,beta,evap,q,count,iterations))
        t.start()

    def runTSP(self,α,β,evaporationCoeff,q,antCount,iterations) -> None:
        if(self.coords == []):
            return
        for i in range(iterations):
            bestRoute,bestCost = self.tsp.iterate(α,β,evaporationCoeff,q,antCount)
            self.updateGraph(bestRoute,coords=self.coords)
            self.progressBarLabel((i/iterations))
            self.costLabel.config(text="ACO Cost: "+str(bestCost))
        self.updateGraph(bestRoute,coords=self.coords)

    def updateGraph(self,route, coords):
        self.graph.clear()
        for r in range(len(route)-1):
            node = route[r]
            self.graph.add_node(node,pos=(coords[node][1], coords[node][0]))
            self.graph.add_edge(node, route[r+1])

    def redrawGraph(self): 
        self.fig.clf()
        plot1 = self.fig.add_subplot(111)

        pos = {node: coords for node, coords in nx.get_node_attributes(self.graph, "pos").items()}
        nx.draw(self.graph, pos, with_labels=False, node_size=50, node_color="#4169E1", ax=plot1)
        pos = {node: coords for node, coords in nx.get_node_attributes(self.solverGraph, "pos").items()}
        nx.draw(self.solverGraph, pos, with_labels=False, node_size=50, edge_color="#CC5500", ax=plot1)
        self.canvas.draw()
        self.after(100,self.redrawGraph)

    def runSolver(self) -> None:
        bestRoute,bestCost = self.tsp.useSolver()
        self.updateSolverGraph(bestRoute)
        self.solverCostLabel.config(text="Solver Cost: "+str(bestCost))

    def updateSolverGraph(self,route):
        self.solverGraph.clear()
        for r in range(len(route)-1):
            node = route[r]
            self.solverGraph.add_node(node,pos=(self.coords[node][1], self.coords[node][0]))
            self.solverGraph.add_edge(node, route[r+1])

    def progressBarLabel(self,data:float,string:str="") -> None:
        '''
            data: float between 0-1
            string: a string to be displayed after the progress bar
        '''
        # Gets position of index in list over list length as a floored percentage
        percent = int(np.floor(data*100))
        # Calculates half the percentage, this provides only 50 characters and a less excessive progress bar
        percentOver4 = int(percent/4)
        # Prints out the progress bar, ending in an escape character "\r" so that it keeps printing on the same line everytime
        self.progressLabel.config(text=string+"Training Progress: "+("█"*(percentOver4))+("▒"*(25-percentOver4)))#+str(percent)+"% "

class SimFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Virtual Simulation using ACO")
        label.pack(side="top", fill="x", pady=10)

        self.foodTau = None
        self.nestTau = None
        self.ants = []

        self.createWidgets()

        self.returnButton = tk.Button(master=self, text="Return to the main menu",command=lambda: controller.showFrame("StartFrame"))
        self.returnButton.pack()

    def menuBar(self,root):
        menuBar = tk.Menu(root)
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Open", command=self.open_file_browser)
        menuBar.add_cascade(label="File", menu=fileMenu)
        return menuBar
    
    def open_file_browser(self):
        filepath = filedialog.askopenfilename(initialdir="./",title="Select a File", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
        if(filepath):
            self.loadSim(filename=filepath)

    def createWidgets(self) -> None:

        self.WIDTH, self.HEIGHT = 320, 320
        
        self.SIMWIDTH = 64
        
        self.canvas = tk.Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg="#000000")
        self.canvas.pack()

        alphaFrame = tk.Frame(master=self)

        alphaLabel = tk.Label(master=alphaFrame, text="Value of pheromone impact: ", width=40)
        alphaLabel.pack(side=tk.LEFT)

        alphaScale = tk.Scale(master=alphaFrame, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, tickinterval=1, width=20)
        alphaScale.set(1)
        alphaScale.pack(side=tk.RIGHT)

        alphaFrame.pack()

        betaFrame = tk.Frame(master=self)

        betaLabel = tk.Label(master=betaFrame, text="Value of proximity impact: ", width=40)
        betaLabel.pack(side=tk.LEFT)

        betaScale = tk.Scale(master=betaFrame, from_=0, to=4, resolution=0.1, orient=tk.HORIZONTAL, tickinterval=1, width=20)
        betaScale.set(2)
        betaScale.pack(side=tk.RIGHT)

        betaFrame.pack()

        evapFrame = tk.Frame(master=self)

        evapLabel = tk.Label(master=evapFrame, text="Evaporation Coefficient: ", width=40)
        evapLabel.pack(side=tk.LEFT)

        evapScale = tk.Scale(master=evapFrame, from_=0, to=0.5, resolution=0.01, orient=tk.HORIZONTAL, width=20)
        evapScale.set(0.1)
        evapScale.pack(side=tk.RIGHT)

        evapFrame.pack()

        startButton = tk.Button(
            master=self,
            text="Run Sim", 
            width=25, 
            command=lambda:self.runSimThread(
                foodTau=self.foodTau,
                nestTau=self.nestTau,
                ants=self.ants,
                alpha=float(alphaScale.get()),
                beta=float(betaScale.get()),
                evap=float(evapScale.get())
            )
        )
        startButton.pack()

    def loadSim(self, filename):

        self.img = tk.PhotoImage(width=self.WIDTH, height=self.HEIGHT,file=filename)
        
        self.foodTau = PMat(size=self.SIMWIDTH)
        self.nestTau = PMat(size=self.SIMWIDTH)

        self.antMap = [[0] * self.SIMWIDTH for i in range(self.SIMWIDTH)]

        for i in range(self.SIMWIDTH):
            for j in range(self.SIMWIDTH):
                if(self.img.get(i,j)[1] == 255):
                    self.foodTau.set(i,j,1)
                    self.foodTau.addPersistant([i,j])
                elif(self.img.get(i,j)[2] == 255):
                    self.nestTau.set(i,j,1)
                    self.nestTau.addPersistant([i,j])
                elif(self.img.get(i,j)[0] == 0):
                    self.foodTau.set(i,j,0.01)
                    self.nestTau.set(i,j,0.01)
                else:
                    self.foodTau.set(i,j,-1)
                    self.nestTau.set(i,j,-1)

        self.ants = []
        spawn = self.nestTau.persist[0]
        for i in range(1000):
            ant = AntSim(spawn,1,2,self.SIMWIDTH)
            self.antMap[spawn[0]][spawn[1]] += 1
            self.ants.append(ant)

    def runSimThread(self,foodTau, nestTau, ants, alpha, beta, evap):
        for ant in ants:
            ant.alpha = alpha
            ant.beta = beta
        t = threading.Thread(target=lambda:self.runSim(foodTau=foodTau, nestTau=nestTau, ants=ants, evaporation=evap))
        t.start()

    def runSim(self,foodTau, nestTau, ants, evaporation):
        if(foodTau == None):
            return
        population = len(ants)
        # evaporation = 0.02
        pheromone = 1
        for i in range(5000):
            for ant in ants:
                self.antMap[ant.x][ant.y] -= 1
                ant.move(foodTau,nestTau)
                if(ant.foundFood):
                    foodTau.add(ant.x,ant.y,(pheromone/population))
                else:
                    nestTau.add(ant.x,ant.y,(pheromone/population))
                self.antMap[ant.x][ant.y] += 1
            foodTau.evaporate(evaporation)
            nestTau.evaporate(evaporation)
            if(i % 50 == 0):
                self.redrawPixels(foodTau,nestTau)

    def redrawPixels(self,foodTau,nestTau):
        self.canvas.delete("all")
        colourMap = [["#"] * self.SIMWIDTH for i in range(self.SIMWIDTH)]
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
        highestAnt = 0
        for row in self.antMap:
            if(max(row)>highestAnt):
                highestAnt = max(row)
        for i,row in enumerate(self.antMap):
            for j,item in enumerate(row):
                if(item > 0):
                    val = (item/highestAnt)
                else:
                    val = 0
                b = str(hex(int(255*val))[2:])
                if(len(b) == 1):
                    b = "0" + b
                colourMap[i][j] += b
        for i,row in enumerate(colourMap):
            for j,item in enumerate(row):
                if item != '#000000':
                    self.canvas.create_rectangle(i*5,j*5,(i*5)+5,(j*5)+5,fill=item,width=0)