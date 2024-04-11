import tkinter as tk
import customtkinter as ctk
import cv2
import threading
import numpy as np
import math
import time
import warnings
import csv

from tkinter import filedialog
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg) 
from PIL import Image, ImageTk

from tkinter_objects import FrameObject,GraphObject,FileObject
from file_loader import Loader
from tsp import TSP
from pheromone_matrix import PMat
from ant import AntSim

# For getting rid of complaints about using unofficial image, as the official one causes flickering
warnings.filterwarnings("ignore", category=Warning)

class InfoFrame(ctk.CTkFrame):

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        scrollFrame = ctk.CTkScrollableFrame(self, width=1400, height=700)

        label = ctk.CTkLabel(scrollFrame, text="Ant Colony Optimisation", font=("Tw Cen MT", 50))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="This is a project using the Ant Colony Optimisation algorithm to solve travelling salesperson problems and simulate an ant colony", font=("Tw Cen MT", 20))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="It is intended to show how parameters affect the algorithm and hopefully give an understanding of how it works", font=("Tw Cen MT", 20))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="Travelling Salesperson Problem Solver", font=("Bahnschrift", 30))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="This problem is about finding the shortest route around every point in a graph", font=("Bahnschrift", 16))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="This can be done using ACO to simulate ants travelling and just like real ants will eventually settle into a shortest route", font=("Bahnschrift", 16))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="There are a few parameters that can be changed and they'll be explained here to keep the UI clean so switch to the other screen when you're ready", font=("Bahnschrift", 16))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="Ant Count", font=("Bahnschrift", 18))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="This is the number of virtual ants running around the simulation, more ants mean more paths may be explored each pass but will increase the runtime as well", font=("Bahnschrift", 14))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="Pheromone Impact", font=("Bahnschrift", 18))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="How much the ants are affected by the pheromones they've laid, can encourage exploration when higher but will reinforce known paths too", font=("Bahnschrift", 14))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="Proximity Impact", font=("Bahnschrift", 18))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="How much the ants are affected by the distance to the next node when choosing a route, higher values give greedier solutions", font=("Bahnschrift", 14))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="Evaporation", font=("Bahnschrift", 18))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="This is how quickly the pheromones will evaporate, default is 10% per pass, increasing this forgets known routes faster but encourages exploration", font=("Bahnschrift", 14))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="Ant Colony Simulation", font=("Small Fonts", 30))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="This can simulate a nest and food sources and is done using ACO to simulate ants navigating and just like real ants will eventually form paths to food sources from their nest", font=("Small Fonts", 16))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="There are a few parameters that work differently to above and they'll be explained below, the rest work the same as in the other sim", font=("Small Fonts", 16))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="Ant Count", font=("Small Fonts", 18))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        label = ctk.CTkLabel(scrollFrame, text="This is the number of virtual ants running around the simulation, these are all spawned when the map is created so can't change during runtime", font=("Small Fonts", 14))
        label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        scrollFrame.pack()

    def menuBar(self,root):
        menuBar = tk.Menu(root)
        return menuBar

class TSPFrame(ctk.CTkFrame):

    coords: list
    loader: Loader
    lastFile: str
    running: bool

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

        self.lastFile = None

        self.running = False

        self.createWidgets()

    def openFileBrowser(self):
        filepath = filedialog.askopenfilename(initialdir="./",title="Select a File", filetypes=(("TSP files", "*.tsp"), ("All files", "*.*")))
        self.loadFile(filepath)

    def loadFile(self,filepath=None):
        if(filepath):
            self.lastFile = filepath
        elif(self.lastFile):
            filepath = self.lastFile
        self.loadProblem(filepath)

    def loadProblem(self,filepath):
        file = self.loader.loadFile(filepath=filepath,fileInfo=self.fileInfo)
        self.coords = file[0]
        self.tour = file[2]
        if(self.coords):
            self.tsp = TSP(coords=self.coords)
            self.createGraphs(self.coords)
        if(self.tour):
            self.tour.append(self.tour[0])
            self.solutionGraph.updateGraph(self.tour,self.coords)
            self.solutionGraph.drawGraph()
            cost = self.tsp.getCost(self.tour)
            self.solutionCost.configure(text="File Solution Cost: "+str(math.floor(cost)))
        else:
            self.solutionCost.configure(text="File Solution Cost: N/A")
        self.cost.configure(text="ACO Cost: 0")
        self.solverCost.configure(text="Solver Cost: 0")

    def createGraphs(self,coords):
        self.graph.initGraph(self.coords)
        self.graph.drawGraph()
        self.solverGraph.initGraph(self.coords)
        self.solverGraph.drawGraph()
        self.solutionGraph.initGraph(self.coords)
        self.solutionGraph.drawGraph()

    def createWidgets(self):

        widgetFrame = ctk.CTkFrame(master=self)

        menuFrame = ctk.CTkFrame(master=widgetFrame)

        fileFrame = ctk.CTkFrame(master=menuFrame)

        label = ctk.CTkLabel(master=fileFrame,text="File Info",font=("Bahnschrift", 15))
        label.pack(side=tk.TOP, pady=10, padx=10)

        buttonFrame = ctk.CTkFrame(master=fileFrame)

        load = ctk.CTkButton(master=buttonFrame,text="Load Problem",command=self.openFileBrowser, font=("Bahnschrift", 15), width=100)
        load.pack(side=tk.LEFT, pady=10, padx=10)

        reLoad = ctk.CTkButton(master=buttonFrame,text="Reload",command=self.loadFile, font=("Bahnschrift", 15), width=100)
        reLoad.pack(side=tk.RIGHT, pady=10, padx=10)

        buttonFrame.pack(padx=10)

        self.fileInfo = FileObject(master=fileFrame)
        self.fileInfo.pack(side=tk.BOTTOM, pady=10, padx=10)

        fileFrame.pack(pady=10, padx=10)

        count = FrameObject(master=menuFrame,type="entry",text="Ant Count",val="30")
        count.pack(pady=10, padx=10)

        # Possibly bring back iterations as a toggle
        iterations = FrameObject(master=menuFrame,type="entry",text="How many iterations: ",val="30")
        # iterations.pack()

        alpha = FrameObject(master=menuFrame,type="scale",text="Pheromone impact",val=1,size=(0,5),steps=50)
        alpha.pack(pady=10, padx=10)

        beta = FrameObject(master=menuFrame,type="scale",text="Proximity impact",val=2,size=(0,5),steps=50)
        beta.pack(pady=10, padx=10)

        evap = FrameObject(master=menuFrame,type="scale",text="Evaporation",val=0.1,size=(0,1),steps=100)
        evap.pack(pady=10, padx=10)

        pheromoneRange = FrameObject(master=menuFrame,type="dualEntry",text="Pheromone range", val=0.0001, val2=1)
        pheromoneRange.pack(pady=10, padx=10)

        acoFrame =  ctk.CTkFrame(master=menuFrame)

        self.startButton = ctk.CTkButton(
            master=acoFrame,
            text="Start ACO", 
            width=200, 
            command=lambda:self.runThread(alpha.get(),beta.get(),evap.get(),0.5,int(count.get()),int(iterations.get()),pheromoneRange.get(vals=2)),
            font=("Bahnschrift", 15)
        )
        self.startButton.pack()

        self.stopButton = ctk.CTkButton(
            master=acoFrame,
            text="Stop", 
            width=200, 
            command=self.stopRunning,
            font=("Bahnschrift", 15)
        )

        acoFrame.pack(pady=10, padx=10)

        solverButton = ctk.CTkButton(
            master=menuFrame,
            text="Run Solver", 
            width=200, 
            command=self.runSolver,
            font=("Bahnschrift", 15)
        )
        solverButton.pack(pady=10, padx=10)

        testButton = ctk.CTkButton(
            master=menuFrame,
            text="Run Tests", 
            width=200, 
            command=self.runTests,
            font=("Bahnschrift", 15)
        )
        testButton.pack(pady=10, padx=10)
        
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

        graphView.pack(side=tk.TOP, pady=5, padx=10)

        statsFrame = ctk.CTkFrame(master=displayFrame, width=1000)

        self.cost = ctk.CTkLabel(master=statsFrame, text="ACO Cost: 0", font=("Bahnschrift", 15))
        self.cost.pack(pady=3)

        self.solverCost = ctk.CTkLabel(master=statsFrame, text="Solver Cost: 0", font=("Bahnschrift", 15))
        self.solverCost.pack(pady=3)

        self.solutionCost = ctk.CTkLabel(master=statsFrame, text="File Solution Cost: 0", font=("Bahnschrift", 15))
        self.solutionCost.pack(pady=3)

        self.pheromone = ctk.CTkLabel(master=statsFrame, text="Pheromone Range: [1,1]", font=("Bahnschrift", 15))
        self.pheromone.pack(pady=3)

        statsFrame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)

        displayFrame.pack(pady=10, padx=10, side=tk.RIGHT)

        widgetFrame.pack(pady=10, padx=10, fill=tk.BOTH)

    def stopRunning(self):
        self.running = False
        self.startButton.pack()
        self.stopButton.pack_forget()

    def runThread(self,alpha,beta,evap,q,count,iterations,pRange):
        self.thread = threading.Thread(target=lambda:self.runTSP(alpha,beta,evap,q,count,iterations,pRange))
        self.thread.start()

    def runTests(self):
        file = self.loader.loadFile(filepath=self.lastFile,fileInfo=self.fileInfo)
        self.coords = file[0]
        outFile = open('tests.csv', 'a', newline='')
        outWriter = csv.writer(outFile)
        alphas = np.arange(0, 5.5, 0.5)
        betas = np.arange(0, 5.5, 0.5)
        # evaps = np.arange(0.05, 1.05, 0.05)
        # alphas = [0, 0.5, 1, 2, 5]
        # betas = [0, 1, 2, 5]  
        # evaps = [0.3, 0.5, 0.7, 0.9, 0.999]
        evaps = [0.5]*10
        iterations = 100
        iterator = range(iterations)
        fileName = self.lastFile.split("/")[-1]
        for a in alphas:
            for b in betas:
                for e in evaps:
                    self.tsp = TSP(coords=self.coords)
                    for i in iterator:
                        bestRoute,bestCost = self.tsp.iterate(a,b,e,0.5,50,[0.01,5])
                        bestCost = self.tsp.getCost(bestRoute)
                    # print("Alpha: "+str(a)+" Beta: "+str(b)+" Evap: "+str(e)+" Cost "+str(bestCost))
                    outWriter.writerow([fileName,str(a),str(b),str(e),str(iterations),str(bestCost)])
        outFile.close()

    def runTSP(self,α,β,evaporationCoeff,q,antCount,iterations,pRange) -> None:
        self.stopButton.pack()
        self.startButton.pack_forget()
        if(self.coords == []):
            return
        self.running = True
        while(self.running):
            bestRoute,bestCost = self.tsp.iterate(α,β,evaporationCoeff,q,antCount,pRange)
            bestCost = self.tsp.getCost(bestRoute)
            self.graph.updateGraph(bestRoute,self.coords)
            self.cost.configure(text="ACO Cost: "+str(math.floor(bestCost)))
            self.pheromone.configure(text="Pheromone Range: ["+str(math.floor(self.tsp.tau.min()*1000)/1000)+","+str(math.floor(self.tsp.tau.max()*1000)/1000)+"]")
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

    ants:list[AntSim]
    foodTau:PMat
    nestTau:PMat
    lastFile:str
    running:bool

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        titleFrame = ctk.CTkFrame(master=self, width=1000)

        label = ctk.CTkLabel(master=titleFrame, text="Ant Colony Simulation", font=("Small Fonts", 30))
        label.pack(pady=5)

        label = ctk.CTkLabel(master=titleFrame, text="Uses an Ant Colony Optimisation Path Finding Algorithm", font=("Small Fonts", 15))
        label.pack(pady=5)

        titleFrame.pack(side=tk.TOP, fill=tk.X)

        self.foodTau = None
        self.nestTau = None
        self.ants = []

        self.lastFile = None

        self.running = False

        self.createWidgets()

    def menuBar(self,root):
        menuBar = tk.Menu(root)
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Open", command=self.openFileBrowser)
        menuBar.add_cascade(label="File", menu=fileMenu)
        return menuBar
    
    def openFileBrowser(self):
        filepath = filedialog.askopenfilename(initialdir="./",title="Select a File", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
        self.loadFile(filepath=filepath)
    
    def loadFile(self,filepath=None):
        if(filepath):
            self.lastFile = filepath
        elif(self.lastFile):
            filepath = self.lastFile
        self.loadSim(filename=filepath)

    def createWidgets(self) -> None:

        self.WIDTH = 768
        
        self.SIMWIDTH = 64

        self.RATIO = self.WIDTH / self.SIMWIDTH
        
        blankImage = np.zeros((self.WIDTH, self.WIDTH, 3), dtype=np.uint8)
        blankImage = Image.fromarray(blankImage)
        blankImage = blankImage.resize((self.WIDTH, self.WIDTH), resample=Image.NEAREST)        

        self.image = ImageTk.PhotoImage(image=blankImage)
        self.imageLabel = ctk.CTkLabel(self,image=self.image,text="")
        self.imageLabel.pack(side=tk.RIGHT, padx=10, pady=10)
        
        menuFrame = ctk.CTkFrame(master=self)

        mapFrame = ctk.CTkFrame(master=menuFrame)

        mapLabel = ctk.CTkLabel(master=mapFrame,text="Map Info", font=("Small Fonts", 20))
        mapLabel.pack(pady=10)

        antFrame = ctk.CTkFrame(master=mapFrame)
        
        antLabel = ctk.CTkLabel(master=antFrame,text="Ant Count", width=140, font=("Small Fonts", 15))
        antLabel.pack(side=tk.LEFT)

        self.antCount = ctk.CTkEntry(master=antFrame, width=100, font=("Small Fonts", 15))
        self.antCount.insert(0,"500")
        self.antCount.pack(side=tk.RIGHT)

        antFrame.pack(padx=10)

        loadButtonFrame = ctk.CTkFrame(master=mapFrame)

        load = ctk.CTkButton(master=loadButtonFrame,text="Load Map",command=self.openFileBrowser, width=100, font=("Small Fonts", 15))
        load.pack(side=tk.LEFT, pady=10, padx=10)

        reLoad = ctk.CTkButton(master=loadButtonFrame,text="Reload",command=self.loadFile, width=100, font=("Small Fonts", 15))
        reLoad.pack(side=tk.RIGHT, pady=10, padx=10)
        
        loadButtonFrame.pack(pady=10, padx=10)

        mapFrame.pack(pady=10, padx=10)

        self.iterations = FrameObject(master=menuFrame,type="entry",text="Iterations",val="200",fontType="sim")
        # self.iterations.pack(pady=10, padx=10)

        self.alpha = FrameObject(master=menuFrame,type="scale",text="Pheromone impact",val=1,size=(0,2),steps=20,fontType="sim")
        self.alpha.pack(pady=10, padx=10)

        self.beta = FrameObject(master=menuFrame,type="scale",text="Proximity impact",val=2,size=(0,4),steps=40,fontType="sim")
        self.beta.pack(pady=10, padx=10)

        self.evap = FrameObject(master=menuFrame,type="scale",text="Evaporation",val=0.1,size=(0,1),fontType="sim")
        self.evap.pack(pady=10, padx=10)

        self.pheromoneRange = FrameObject(master=menuFrame,type="dualEntry",text="Pheromone range", val=0.005, val2=5, fontType="sim")
        self.pheromoneRange.pack(pady=10, padx=10)

        self.foodPheromone = ctk.CTkLabel(master=menuFrame, text="Food Pheromone Range: [1,1]", font=("Small Fonts", 15))
        self.foodPheromone.pack(pady=5)

        self.nestPheromone = ctk.CTkLabel(master=menuFrame, text="Nest Pheromone Range: [1,1]", font=("Small Fonts", 15))
        self.nestPheromone.pack(pady=5)

        self.counts = ctk.CTkLabel(master=menuFrame, text="Ant Counts (Nest,Food): (0,0)", font=("Small Fonts", 15))
        self.counts.pack(pady=5)

        startFrame =  ctk.CTkFrame(master=menuFrame)

        self.startButton = ctk.CTkButton(
            master=startFrame,
            text="Run Sim", 
            width=200, 
            command=self.runSimThread,
            font=("Small Fonts", 15)
        )
        self.startButton.pack(pady=10, padx=10)

        self.stopButton = ctk.CTkButton(
            master=startFrame,
            text="Stop", 
            width=200, 
            command=self.stopRunning,
            font=("Small Fonts", 15)
        )

        startFrame.pack(pady=10, padx=10)

        menuFrame.pack(side=tk.LEFT, pady=10, padx=10)

    def loadSim(self, filename):

        self.img = tk.PhotoImage(width=self.WIDTH, height=self.WIDTH,file=filename)
        
        self.foodTau = PMat(size=self.SIMWIDTH)
        self.nestTau = PMat(size=self.SIMWIDTH)

        self.antMap = np.zeros((self.SIMWIDTH,self.SIMWIDTH))

        for i in range(self.SIMWIDTH):
            for j in range(self.SIMWIDTH):
                if(self.img.get(i,j)[1] == 255):
                    self.foodTau.tiles[i][j] = 2
                    self.nestTau.tiles[i][j] = 0
                elif(self.img.get(i,j)[2] == 255):
                    self.nestTau.tiles[i][j] = 2
                    self.foodTau.tiles[i][j] = 0
                elif(self.img.get(i,j)[0] == 0):
                    self.foodTau.tiles[i][j] = 0
                    self.nestTau.tiles[i][j] = 0
                else:
                    self.foodTau.tiles[i][j] = 1
                    self.nestTau.tiles[i][j] = 1

        antCount = int(self.antCount.get())

        self.ants = []
        spawns = np.where(self.nestTau.tiles == 2)
        spawn = (spawns[0][0],spawns[1][0])
        for i in range(antCount):
            ant = AntSim(spawn,1,2,self.SIMWIDTH)
            self.antMap[spawn[0]][spawn[1]] += 1
            self.ants.append(ant)
        
        self.nestCount = antCount
        self.foodCount = 0

        self.redrawPixels()

    def stopRunning(self):
        self.running = False
        self.startButton.pack()
        self.stopButton.pack_forget()

    def runSimThread(self):
        t = threading.Thread(target=self.runSim)
        t.start()

    def runSim(self):
        ants=self.ants
        alpha=self.alpha.get()
        beta=self.beta.get()
        evaporation=self.evap.get()
        iterations=int(self.iterations.get())
        pRange=self.pheromoneRange.get(vals=2)

        for ant in ants:
            ant.alpha = alpha
            ant.beta = beta
        
        if(self.foodTau == None):
            return
        
        population = len(ants)
        pheromone = 1
        startTime = time.time_ns()
        
        self.stopButton.pack()
        self.startButton.pack_forget()
        self.running = True
        while(self.running):
            self.counts.configure(text="Ant Counts (Nest,Food): ("+str(self.nestCount)+","+str(self.foodCount)+")")
            for ant in ants:
                self.antMap[ant.x][ant.y] -= 1
                if(ant.move(self.foodTau,self.nestTau)):
                    if(ant.foundFood):
                        self.nestCount -= 1
                        self.foodCount += 1
                    else:
                        self.nestCount += 1
                        self.foodCount -= 1

                if(ant.foundFood):
                    self.foodTau.add(ant.x,ant.y,(pheromone/population*50))
                else:
                    self.nestTau.add(ant.x,ant.y,(pheromone/population*50))

                self.antMap[ant.x][ant.y] += 1

            self.foodTau.evaporate(evaporation)
            self.foodTau.threshold(pRange)
            self.nestTau.evaporate(evaporation)
            self.nestTau.threshold(pRange)

            self.foodPheromone.configure(text="Food Pheromone Range: ["+str(math.floor(self.foodTau.content.min()*1000)/1000)+","+str(math.floor(self.foodTau.content.max()*1000)/1000)+"]")
            self.nestPheromone.configure(text="Nest Pheromone Range: ["+str(math.floor(self.nestTau.content.min()*1000)/1000)+","+str(math.floor(self.nestTau.content.max()*1000)/1000)+"]")

            self.redrawPixels()

            endTime = time.time_ns()
            if(False):
                print("Iteration Time:   " + str((endTime-startTime) / (10 ** 9)))
            startTime = time.time_ns()

    def redrawPixels(self):
        startTime = time.time_ns()
        colourMap = np.zeros((self.SIMWIDTH, self.SIMWIDTH, 3), dtype=np.uint8)

        foodMap = self.foodTau.content
        colourMap[:,:,0] = ((foodMap - foodMap.min()) / (foodMap.max() - foodMap.min())) * 255

        nestMap = self.nestTau.content
        colourMap[:,:,1] = ((nestMap - nestMap.min()) / (nestMap.max() - nestMap.min())) * 255
        
        antMap = self.antMap
        colourMap[:,:,2] = ((antMap - antMap.min()) / (antMap.max() - antMap.min())) * 255

        colourMap[self.foodTau.tiles == 1] = 30
        colourMap[self.foodTau.tiles == 2,0] = 255
        colourMap[self.nestTau.tiles == 2,1] = 255
        
        colourMap = np.flip(colourMap, axis=0)

        calcTime = time.time_ns()

        colourMap = cv2.resize(colourMap,(self.WIDTH,self.WIDTH),interpolation=cv2.INTER_NEAREST)
        colourMap = cv2.rotate(colourMap, cv2.ROTATE_90_CLOCKWISE)
        newImage = Image.fromarray(colourMap)
        
        # newImage2 = newImage.resize((self.WIDTH,self.WIDTH), resample=Image.NEAREST)
        # newImage3 = ImageTk.PhotoImage(image=newImage2)

        self.image.paste(newImage)
        # self.imageLabel.configure(image=self.image)
        self.update_idletasks()
        endTime = time.time_ns()
        if(False):
            print("Calculation Time: " + str((calcTime-startTime) / (10 ** 9)))
            print("Render Time:      " + str((endTime-calcTime) / (10 ** 9)))
            print("Total Time:       " + str((endTime-startTime) / (10 ** 9)))