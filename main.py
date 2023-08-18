import numpy as np
import time
import math
import csv

from ant import Ant,AntTraverse
from distance_matrix import Mat

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

def main() -> None:
    limit = int(input("Enter row limit for data: "))
    coords = loadCSV("gb.csv",1,2,True,limit=limit)
    distMat = formDistMat(coords, haversineDistance)
    tau  = np.ones(distMat.shape)
    α = 1
    β = 2
    evaporationCoeff = 0.1
    q = 1
    antCount = int(input("How many ants do you want to simulate: "))
    iterations = int(input("How many iterations do you want to simulate: "))
    # Python version of infinitely high cost
    bestCost = float("inf")
    bestRoute = []
    ants = []
    for i in range(iterations):
        ants = []
        tauChange = np.zeros(distMat.shape)
        for a in range(antCount):
            ants.append(Ant(nodes=list(range(distMat.size)),alpha=α,beta=β))
        for a, ant in enumerate(ants):
            ant.move(tau,distMat.content)
            if(ant.cost < bestCost):
                bestCost = ant.cost
                bestRoute = ant.route
            for r in range(len(ant.route)-1):
                tauChange[ant.route[r]][ant.route[r+1]] += q / ant.cost
            progressBar((i/iterations)+((a/(len(ants))/iterations)))#,("Best Route: "+str(bestRoute)+"\n"+"Cost of: "+str(bestCost)+"\n"))
            # time.sleep(0.01)
        tau *= (1-evaporationCoeff)
        tau += tauChange / antCount
    print("Best Route: "+str(bestRoute))
    print("Cost of: "+str(bestCost))

def formDistMat(vertexCoords:list[list[float]],distance) -> Mat:
    '''
        Forms a distance matrix between all the given vertex coordinates
        vertexCoords: a list of coordinates for each data point vertex
        distance: the distance function to be used in the distance matrix calculations
    '''
    distMat = Mat(size=len(vertexCoords))
    for n,i in enumerate(vertexCoords):
        for m,j in enumerate(vertexCoords):
            if(n==m):
                continue
            distMat.set(n,m,distance(i,j))
    return distMat

def haversineDistance(i:float,j:float) -> float:
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

def progressBar(data:float,string:str="") -> None:
    '''
        data: float between 0-1
        string: a string to be displayed after the progress bar
    '''
    # Gets position of index in list over list length as a floored percentage
    percent = int(np.floor(data*100))
    # Calculates half the percentage, this provides only 50 characters and a less excessive progress bar
    percentOver2 = int(percent/2)
    # Prints out the progress bar, ending in an escape character "\r" so that it keeps printing on the same line everytime
    print(string+"Training Progress: "+str(percent)+"% "+("#"*(percentOver2))+("."*(50-percentOver2)), end="\r")

if __name__ == "__main__":
    main()