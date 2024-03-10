import tkinter as tk
import customtkinter as ctk
import networkx as nx
import threading
import numpy as np
import math

from tkinter import filedialog
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg) 

from tkinter_objects import FrameObject,GraphObject
from file_loader import Loader
from tsp import TSP
from pheromone_matrix import PMat
from ant import AntSim

class InfoFrame(ctk.CTkFrame):

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)
        label = ctk.CTkLabel(self, text="Ant Colony Optimisation", font=("Tw Cen MT", 50))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(self, text="This is a project using the Ant Colony Optimisation algorithm to solve travelling salesperson problems and simulate an ant colony", font=("Tw Cen MT", 20))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(self, text="It is intended to show how parameters affect the algorithm and hopefully give an understanding of how it works", font=("Tw Cen MT", 20))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(self, text="Travelling Salesperson Problem", font=("Bahnschrift", 30))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(self, text="This problem is about finding the shortest route around every point in a graph, this can be done using ACO to simulate ants travelling and just like real ants will eventually settle into a shortest route", font=("Bahnschrift", 16))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(self, text="There are a few parameters that can be changed and they'll be explained here to keep the UI clean so switch to the other when you're ready", font=("Bahnschrift", 16))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(self, text="Ant Count", font=("Bahnschrift", 18))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(self, text="This is the number of virtual ants running around the simulation, more ants mean more paths may be explored each pass but will increase the runtime as well", font=("Bahnschrift", 14))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(self, text="Pheromone Impact", font=("Bahnschrift", 18))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(self, text="How much the ants are affected by the pheromones they've laid, can encourage exploration when higher but will reinforce known paths too", font=("Bahnschrift", 14))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(self, text="Proximity Impact", font=("Bahnschrift", 18))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(self, text="How much the ants are affected by the distance to the next node when choosing a route, higher values give greedier solutions", font=("Bahnschrift", 14))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(self, text="Evaporation", font=("Bahnschrift", 18))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(self, text="This is how quickly the pheromones will evaporate, default is 10% per pass, increasing this forgets known routes faster but encourages exploration", font=("Bahnschrift", 14))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

    def menuBar(self,root):
        menuBar = tk.Menu(root)
        return menuBar

class TSPFrame(ctk.CTkFrame):

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        titleFrame = ctk.CTkFrame(master=self, width=1000)

        label = ctk.CTkLabel(master=titleFrame, text="Travelling Salesperson Problem Solver", font=("Bahnschrift", 30))
        label.pack(pady=5)

        label = ctk.CTkLabel(master=titleFrame, text="Uses an Ant Colony Optimisation Solver with Google's ORTools Solver for Comparison", font=("Bahnschrift", 15))
        label.pack(pady=5)

        titleFrame.pack(side=tk.TOP, fill=tk.X)
        
        self.coords = []
        self.loader = Loader()

        self.running = False

        self.createWidgets()

    def openFileBrowser(self):
        filepath = filedialog.askopenfilename(initialdir="./",title="Select a File", filetypes=(("TSP files", "*.tsp"), ("All files", "*.*")))
        if(filepath):
            file = self.loader.loadFile(filepath=filepath)
            self.coords = file[0]
            self.edges = file[1]
            self.tour = file[2]
            if(self.coords):
                self.tsp = TSP(coords=self.coords)
                self.graph.initGraph(self.coords)
                self.graph.drawGraph()
                self.solverGraph.initGraph(self.coords)
                self.solverGraph.drawGraph()
                self.solutionGraph.initGraph(self.coords)
                self.solutionGraph.drawGraph()
            elif(self.edges):
                self.tsp = TSP(matrix=self.edges)
            if(self.tour):
                self.tour.append(self.tour[0])
                self.solutionGraph.updateGraph(self.tour,self.coords)
                self.solutionGraph.drawGraph()
                cost = self.tsp.getCost(self.tour)
                self.solutionCost.configure(text="File Solution Cost: "+str(math.floor(cost)))

    def menuBar(self,root):
        menuBar = tk.Menu(root)
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Open", command=self.openFileBrowser)
        menuBar.add_cascade(label="File", menu=fileMenu)
        return menuBar

    def createWidgets(self):

        widgetFrame = ctk.CTkFrame(master=self)

        menuFrame = ctk.CTkFrame(master=widgetFrame)

        load = ctk.CTkButton(master=menuFrame,text="Load Problem",command=self.openFileBrowser, font=("Bahnschrift", 15))
        load.pack(pady=10, padx=10)

        # Add file info

        count = FrameObject(master=menuFrame,type="entry",text="Ant Count",val="30")
        count.pack(pady=10, padx=10)

        # Possibly bring back iterations as a toggle
        iterations = FrameObject(master=menuFrame,type="entry",text="How many iterations: ",val="30")
        # iterations.pack()

        alpha = FrameObject(master=menuFrame,type="scale",text="Pheromone impact",val=1,size=(0,2),steps=20)
        alpha.pack(pady=10, padx=10)

        beta = FrameObject(master=menuFrame,type="scale",text="Proximity impact",val=2,size=(0,4),steps=40)
        beta.pack(pady=10, padx=10)

        evap = FrameObject(master=menuFrame,type="scale",text="Evaporation",val=0.1,size=(0,1))
        evap.pack(pady=10, padx=10)

        acoFrame =  ctk.CTkFrame(master=menuFrame)

        self.startButton = ctk.CTkButton(
            master=acoFrame,
            text="Start ACO", 
            width=25, 
            command=lambda:self.runThread(alpha.get(),beta.get(),evap.get(),1,int(count.get()),int(iterations.get())),
            font=("Bahnschrift", 15)
        )
        self.startButton.pack()

        self.stopButton = ctk.CTkButton(
            master=acoFrame,
            text="Stop", 
            width=25, 
            command=self.stopRunning,
            font=("Bahnschrift", 15)
        )

        acoFrame.pack(pady=10, padx=10)

        solverButton = ctk.CTkButton(
            master=menuFrame,
            text="Run Solver", 
            width=25, 
            command=self.runSolver,
            font=("Bahnschrift", 15)
        )
        solverButton.pack(pady=10, padx=10)
        
        menuFrame.pack(side=tk.LEFT, pady=10, padx=10)

        displayFrame = ctk.CTkFrame(master=widgetFrame)

        graphView = ctk.CTkTabview(master=displayFrame)
        graphView.add("ACO Graph")
        graphView.add("Solver Graph")
        graphView.add("Solution Graph")
        graphView._segmented_button.configure(font=("Bahnschrift", 15))

        self.graph = GraphObject(master=graphView.tab("ACO Graph"),colour="#CC6600")
        self.graph.redrawGraph()

        self.solverGraph = GraphObject(master=graphView.tab("Solver Graph"),colour="#0099CC")
        self.solverGraph.drawGraph()

        self.solutionGraph = GraphObject(master=graphView.tab("Solution Graph"),colour="#66FF33")
        self.solutionGraph.drawGraph()

        graphView.pack(side=tk.TOP, pady=10, padx=10)

        statsFrame = ctk.CTkFrame(master=displayFrame, width=1000)

        self.cost = ctk.CTkLabel(master=statsFrame, text="ACO Cost: 0", font=("Bahnschrift", 15))
        self.cost.pack(pady=10)

        self.solverCost = ctk.CTkLabel(master=statsFrame, text="Solver Cost: 0", font=("Bahnschrift", 15))
        self.solverCost.pack(pady=10)

        self.solutionCost = ctk.CTkLabel(master=statsFrame, text="File Solution Cost: 0", font=("Bahnschrift", 15))
        self.solutionCost.pack(pady=10)

        # self.cost = FrameObject(master=displayFrame,type="label",text="ACO Cost: 0")
        # self.cost.pack()

        # self.solverCost = FrameObject(master=displayFrame,type="label",text="Solver Cost: 0")
        # self.solverCost.pack()

        # self.solutionCost = FrameObject(master=displayFrame,type="label",text="File Solution Cost: 0")
        # self.solutionCost.pack()

        statsFrame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)

        displayFrame.pack(side=tk.RIGHT)

        widgetFrame.pack(fill=tk.BOTH)

    def stopRunning(self):
        self.running = False
        self.startButton.pack()
        self.stopButton.pack_forget()

    def runThread(self,alpha,beta,evap,q,count,iterations):
        self.thread = threading.Thread(target=lambda:self.runTSP(alpha,beta,evap,q,count,iterations))
        self.thread.start()

    def runTSP(self,α,β,evaporationCoeff,q,antCount,iterations) -> None:
        self.stopButton.pack()
        self.startButton.pack_forget()
        if(self.coords == []):
            return
        self.running = True
        while(self.running):
            bestRoute,bestCost = self.tsp.iterate(α,β,evaporationCoeff,q,antCount)
            bestCost = self.tsp.getCost(bestRoute)
            self.graph.updateGraph(bestRoute,self.coords)
            self.cost.configure(text="ACO Cost: "+str(math.floor(bestCost)))
        self.graph.updateGraph(bestRoute,self.coords)

    def runSolver(self) -> None:
        bestRoute,bestCost = self.tsp.useSolver()
        bestCost = self.tsp.getCost(bestRoute)
        self.solverGraph.updateGraph(bestRoute,self.coords)
        self.solverGraph.drawGraph()
        self.solverCost.configure(text="Solver Cost: "+str(math.floor(bestCost)))

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
        self.progressLabel.configure(text=string+"Training Progress: "+("█"*(percentOver4))+("▒"*(25-percentOver4)))#+str(percent)+"% "

class SimFrame(ctk.CTkFrame):
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        label = ctk.CTkLabel(self, text="Virtual Simulation using ACO")
        label.pack(side="top", fill="x", pady=10)

        self.foodTau = None
        self.nestTau = None
        self.ants = []

        self.createWidgets()

    def menuBar(self,root):
        menuBar = tk.Menu(root)
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Open", command=self.openFileBrowser)
        menuBar.add_cascade(label="File", menu=fileMenu)
        return menuBar
    
    def openFileBrowser(self):
        filepath = filedialog.askopenfilename(initialdir="./",title="Select a File", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
        if(filepath):
            self.loadSim(filename=filepath)

    def createWidgets(self) -> None:

        self.WIDTH, self.HEIGHT = 320, 320
        
        self.SIMWIDTH = 64
        
        self.canvas = ctk.CTkCanvas(self, width=self.WIDTH, height=self.HEIGHT, bg="#000000")
        self.canvas.pack()

        alphaFrame = ctk.CTkFrame(master=self)

        alphaLabel = ctk.CTkLabel(master=alphaFrame, text="Value of pheromone impact: ", width=40)
        alphaLabel.pack(side=tk.LEFT)

        alphaScale = tk.Scale(master=alphaFrame, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, tickinterval=1, width=20)
        alphaScale.set(1)
        alphaScale.pack(side=tk.RIGHT)

        alphaFrame.pack()

        betaFrame = ctk.CTkFrame(master=self)

        betaLabel = ctk.CTkLabel(master=betaFrame, text="Value of proximity impact: ", width=40)
        betaLabel.pack(side=tk.LEFT)

        betaScale = tk.Scale(master=betaFrame, from_=0, to=4, resolution=0.1, orient=tk.HORIZONTAL, tickinterval=1, width=20)
        betaScale.set(2)
        betaScale.pack(side=tk.RIGHT)

        betaFrame.pack()

        evapFrame = ctk.CTkFrame(master=self)

        evapLabel = ctk.CTkLabel(master=evapFrame, text="Evaporation Coefficient: ", width=40)
        evapLabel.pack(side=tk.LEFT)

        evapScale = tk.Scale(master=evapFrame, from_=0, to=0.5, resolution=0.01, orient=tk.HORIZONTAL, width=20)
        evapScale.set(0.1)
        evapScale.pack(side=tk.RIGHT)

        evapFrame.pack()

        startButton = ctk.CTkButton(
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