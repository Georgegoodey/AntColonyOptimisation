import tkinter as tk
import networkx as nx
import threading
import numpy as np

from tkinter import filedialog
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg) 

from tkinterObjects import FrameObject
from file_loader import Loader
from tsp import TSP

class StartFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page")
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("TSPFrame"))
        # button2 = tk.Button(self, text="Go to Page Two",
        #                     command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        # button2.pack()

    def menuBar(self,root):
        menuBar = tk.Menu(root)
        return menuBar

class TSPFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        self.coords = []
        self.loader = Loader()

        self.createWidgets()

        self.after(0, self.redrawGraph)

    def open_file_browser(self):
        filepath = filedialog.askopenfilename(initialdir="./",title="Select a File")#, filetypes=(("all files", "*.*")))
        self.coords = self.loader.loadFile(filepath=filepath)
        if(self.coords):
            self.tsp = TSP(self.coords)

    def menuBar(self,root):
        menuBar = tk.Menu(root)
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Open", command=self.open_file_browser)
        menuBar.add_cascade(label="File", menu=fileMenu)
        return menuBar

    def createWidgets(self):

        limit = FrameObject(master=self,type="entry",text="How many nodes: ",val="20")

        count = FrameObject(master=self,type="entry",text="How many ants: ",val="30")

        iterations = FrameObject(master=self,type="entry",text="How many iterations: ",val="30")

        alpha = FrameObject(master=self,type="scale",text="Value of pheromone impact: ",val=1,size=(0,2),resolution=0.1)

        beta = FrameObject(master=self,type="scale",text="Value of proximity impact: ",val=2,size=(0,4),resolution=0.1)

        evap = FrameObject(master=self,type="scale",text="Evaporation Coefficient: ",val=0.1,size=(0,1),resolution=0.05)

        startButton = tk.Button(
            master=self,
            text="Run Sim", 
            width=25, 
            command=lambda:self.runThread(alpha.get(),beta.get(),evap.get(),1,int(count.get()),int(iterations.get()))
        )
        startButton.pack()

        solverButton = tk.Button(
            master=self,
            text="Run Solver", 
            width=25, 
            command=lambda:self.runSolver()
        )
        solverButton.pack()

        progressFrame = tk.Frame(master=self)

        self.progressLabel = tk.Label(master=progressFrame, text="", width=60)
        self.progressLabel.pack(side=tk.LEFT)

        progressFrame.pack()

        self.fig = Figure(figsize = (4, 4), dpi = 100) 

        self.canvas = FigureCanvasTkAgg(self.fig, 
                                master = self)   
        self.canvas.draw() 

        self.canvas.get_tk_widget().pack()

        self.graph = nx.Graph()

        self.solverGraph = nx.Graph()

    def runThread(self,alpha,beta,evap,q,count,iterations):
        t = threading.Thread(target=lambda:self.runTSP(alpha,beta,evap,q,count,iterations))
        t.start()

    def runTSP(self,α,β,evaporationCoeff,q,antCount,iterations) -> None:
        if(self.coords == []):
            return
        for i in range(iterations):
            bestRoute = self.tsp.iterate(α,β,evaporationCoeff,q,antCount)
            self.updateGraph(bestRoute,coords=self.coords)
            self.progressBarLabel((i/iterations))
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
        bestRoute = self.tsp.useORSolver()
        self.updateSolverGraph(bestRoute)

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
        self.progressLabel.config(text=string+"Training Progress: "+str(percent)+"% "+("█"*(percentOver4))+("▒"*(25-percentOver4)))