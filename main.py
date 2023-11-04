import numpy as np
import tkinter as tk
import networkx as nx
import time
import threading
import math
import csv

from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 

from ant import Ant,AntTraverse,AntSim
from distance_matrix import Mat
from pheromone_matrix import PMat

def mainTraversal() -> None:
    # adjMat  =  [[0,1,2,0],[1,0,0,1],[2,0,0,2],[0,1,2,0]]
    adjMat = [
        # 0   1   2   3   4   5   6   7   8   9
        [0,  3,  5,  0,  0,  0,  0,  0,  0,  0],  # Vertex 0
        [0,  0,  2,  7,  0,  0,  0,  0,  0,  4],  # Vertex 1
        [0,  0,  0,  0,  4,  0,  0,  2,  2,  0],  # Vertex 2
        [0,  0,  0,  0,  6,  0,  8,  0,  0,  8],  # Vertex 3
        [8,  3,  0,  0,  0,  1,  9,  0,  6,  0],  # Vertex 4
        [0,  2,  0,  0,  1,  0,  2,  0,  0,  0],  # Vertex 5
        [0,  0,  3,  0,  0,  5,  0,  0,  1,  5],  # Vertex 6
        [4,  0,  1,  0,  2,  0,  0,  0,  3,  0],  # Vertex 7
        [0,  2,  0,  5,  0,  7,  0,  4,  0,  4],  # Vertex 8
        [1,  0,  0,  1,  5,  0,  3,  0,  2,  0],  # Vertex 9
    ]
    tau  = np.ones(np.shape(adjMat))
    print(tau)
    alpha = 1
    beta = 2
    evaporationCoeff = 0.1
    q = 1
    antCount = int(input("How many ants do you want to simulate: "))
    iterations = int(input("How many iterations do you want to simulate: "))
    start = int(input("Enter start node: "))
    end = int(input("Enter goal node: "))
    bestCost = float("inf")
    bestRoute = []
    ants = []
    for i in range(iterations):
        ants = []
        tauChange = np.zeros(np.shape(adjMat))
        for a in range(antCount):
            ants.append(AntTraverse(start,end,adjMat))
        for ant in ants:
            ant.move(tau,alpha,beta)
            if(ant.cost < bestCost):
                bestCost = ant.cost
                bestRoute = ant.route
            for r in range(len(ant.route)-1):
                tauChange[ant.route[r]][ant.route[r+1]] += q / ant.cost
        tau *= (1-evaporationCoeff)
        tau += tauChange / antCount
    print("Done")
    print("Best Route: "+str(bestRoute))
    print("Cost of: "+str(bestCost))

def mainSim() -> None:
    tau = PMat(size=6)
    for i in range(6):
        for j in range(6):
            if(i == 0 or i == 5 or j == 0 or j == 5):
                tau.set(i,j,-1)
            else:
                tau.set(i,j,1)
    tau.set(1,2,10)
    tau.set(2,3,3)
    tau.set(3,3,3)
    ant = AntSim([4,3],1,2)
    tau.evaporate(0.05)
    print(ant.x,ant.y)
    ant.move(tau)
    print(ant.x,ant.y)
    ant.move(tau)
    print(ant.x,ant.y)
    ant.move(tau)
    print(ant.x,ant.y)

def main() -> None:
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
  
    # plotting the graph 
    # plot1.plot()

    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
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
    # canvas.draw()
    plot1 = fig.add_subplot(111)
    # Create a NetworkX graph

    # pos = nx.spring_layout(G)
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
    distMat = formDistMat(coords, haversineDistance, β)
    tau  = np.ones(distMat.shape)
    # antCount = int(input("How many ants do you want to simulate: "))
    # iterations = int(input("How many iterations do you want to simulate: "))
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
            progressBar((i/iterations)+((a/(len(ants))/iterations)))
            progressBarLabel((i/iterations)+((a/(len(ants))/iterations)))
        tau *= (1-evaporationCoeff)
        tau += tauChange / antCount
    endTime = time.time()
    totalTime = endTime - startTime
    print("Best Route: "+str(bestRoute))
    print("Cost of: "+str(bestCost))
    print("Time taken: "+str(totalTime))
    print("Time per ant: "+str(totalTime/(iterations*antCount)))
    updateGraph(bestRoute,coords=coords)

def formDistMat(vertexCoords:list[list[float]],distance,beta:float) -> Mat:
    '''
        Forms a distance matrix between all the given vertex coordinates
        vertexCoords: a list of coordinates for each data point vertex
        distance: the distance function to be used in the distance matrix calculations
    '''
    distMat = Mat(size=len(vertexCoords),beta=beta)
    for n,i in enumerate(vertexCoords):
        for m,j in enumerate(vertexCoords):
            if(n==m):
                continue
            distMat.set(n,m,distance(i,j))
    distMat.init_prox()
    return distMat

def haversineDistance(i:list[float],j:list[float]) -> float:
    '''
        Use haversine forumla for finding distances between longitude and latitude coords
        i: first position
        j: second position
    '''
    R = 6371e3
    phiI = i[0] * math.pi / 180
    phiJ = j[0] * math.pi / 180
    deltaPhi = (j[0]-i[0]) * math.pi / 180
    deltaLambda = (j[1]-i[1]) * math.pi / 180

    a = (math.sin(deltaPhi/2) * math.sin(deltaPhi/2)) + (math.cos(phiI) * math.cos(phiJ) * math.sin(deltaLambda/2) * math.sin(deltaLambda/2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance

def pythagoreanDistance(a:float,b:float) -> float:
    '''
        Use pythagoras formula to calculate distance between two points
    '''
    xDist = abs(a[0]-b[0])
    yDist = abs(a[1]-b[1])
    distance = math.sqrt((xDist**2) + (yDist**2))

    return distance

def loadCSV(filename:str,index1:int,index2:int,header:bool,limit:int) -> list[list[float]]:
    '''
        Forms a list of vertex coordinates from the csv contents of a file
        filename: a string representing the name of the data
        index1: a int representing the csv index of the first datum, can represent latitude, x etc.
        index2: a int representing the csv index of the second datum, can represent longitude, y etc.
        header: a boolean of whether or not the file has a header row
        limit: an int that will limit the number of rows loaded from the csv, higher than the length of file will be ignored
    '''
    # Empty list of vertex coordinates
    coords = []
    # CSV file reference
    csvFile = open(filename)
    # CSV reader object
    csvReader = csv.reader(csvFile)
    
    # Iterate while there is a next row in the file with row as the reference
    for row in csvReader:
        # If the current line of the csv reader is higher than the limit then stop loading file and return
        if(csvReader.line_num>limit):
            break
        # If there is no header row or the current line of the csv reader is not 1
        if((not header) or (csvReader.line_num != 1)):
            # Add the indexed items from the current row to the list of coordinates
            coords.append([float(row[index1]),float(row[index2])])
    
    return coords

def loadTSP(filename:str,limit:int) -> list[list[float]]:
    # Empty list of vertex coordinates
    coords = []
    # TSP file reference
    tspFile = open(filename)
    
    for row in tspFile:
        nums = row.split()
        coords.append([int(nums[0]),int(nums[1])])

    tspFile.close()

    return coords

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

if __name__ == "__main__":
    mainSim()