import random
import numpy as np
from tkinter import *
import time

class AntTraverse:

    node: int
    end: int
    cost: int
    route: list

    def __init__(self, startNode, endNode, adjMat) -> None:
        self.node = startNode
        self.end = endNode
        self.cost = 0
        self.route = [startNode]
        self.mat = adjMat
    
    def probabilityIJ(self,i,j,tau,eta,alpha,beta) -> float:
        if(eta[i][j] == 0):
            return 0
        pheromoneProx = tau[i][j]**alpha * eta[i][j]**-beta
        sumAllowed = 0
        for m in range(len(eta[i])):
            if(eta[i][m] == 0):
                continue
            sumAllowed += tau[i][m]**alpha * eta[i][m]**-beta
        probIJ = pheromoneProx/sumAllowed
        return probIJ

    def nextNode(self,tau,alpha,beta) -> int:
        i = self.node
        probs = []
        nodes = self.mat[i]
        for n in range(len(nodes)):
            prob = self.probabilityIJ(i,n,tau,self.mat,alpha,beta)
            probs.append(prob)
        return random.choices(range(len(probs)),weights=probs,k=1)[0]
    
    def move(self,tau,alpha,beta) -> None:
        while(self.node != self.end):
            newNode = self.nextNode(tau,alpha,beta)
            self.route.append(newNode)
            self.cost += self.mat[self.node][newNode]
            self.node = newNode

    def printAnt(self) -> None:
        print("Current Node: "+str(self.node))
        print("Goal Node: "+str(self.end))
        print("Current Cost: "+str(self.cost))
        print("Route so Far: "+str(self.route))

class Ant:

    node: int
    remaining: list
    cost: int
    route: list
    alpha: float
    beta: float

    def __init__(self, nodes, alpha, beta) -> None:
        self.remaining = nodes
        self.node = random.choice(nodes)
        self.remaining.remove(self.node)
        self.cost = 0
        self.route = [self.node]
        self.alpha = alpha
        self.beta = beta
    
    def probabilityIJ(self,i,j,tau,eta) -> float:
        if(eta[i][j] == 0):
            return 0
        pheromoneProx = tau[i][j]**self.alpha * eta[i][j]**-self.beta
        sumAllowed = 0
        for m in range(len(eta[i])):
            if(eta[i][m] == 0):
                continue
            sumAllowed += tau[i][m]**self.alpha * eta[i][m]**-self.beta
        probIJ = pheromoneProx/sumAllowed
        return probIJ

    def nextNode(self,tau,eta) -> int:
        i = self.node
        probs = []
        for n in self.remaining:
            prob = self.probabilityIJ(i,n,tau,eta)
            probs.append(prob)
        return random.choices(self.remaining,weights=probs,k=1)[0]
    
    def move(self,tau,eta) -> None:
        originalNode = self.node
        while(self.remaining):
            newNode = self.nextNode(tau,eta)
            self.remaining.remove(newNode)
            self.route.append(newNode)
            self.cost += eta[self.node][newNode]
            self.node = newNode
        self.route.append(originalNode)
        self.cost += eta[self.node][originalNode]
        self.node = originalNode

    def printAnt(self) -> None:
        print("Current Node: "+str(self.node))
        print("Goal Node: "+str(self.end))
        print("Current Cost: "+str(self.cost))
        print("Route so Far: "+str(self.route))

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

def main():
    adjMat = [ # For travelling salesman
        # 0   1   2   3   4   5   6
        [0,  1,  4,  1,  2,  4,  5],  # Vertex 0
        [1,  0,  2,  2,  1,  3,  4],  # Vertex 1
        [4,  2,  0,  3,  1,  2,  1],  # Vertex 2
        [1,  2,  3,  0,  1,  2,  4],  # Vertex 3
        [2,  1,  1,  1,  0,  1,  2],  # Vertex 4
        [4,  3,  2,  2,  1,  0,  1],  # Vertex 5
        [5,  4,  1,  4,  2,  1,  0]   # Vertex 6
    ]
    tau  = np.ones(np.shape(adjMat))
    alpha = 1
    beta = 2
    evaporationCoeff = 0.1
    q = 1
    antCount = int(input("How many ants do you want to simulate: "))
    iterations = int(input("How many iterations do you want to simulate: "))
    bestCost = float("inf")
    bestRoute = []
    ants = []
    for i in range(iterations):
        ants = []
        tauChange = np.zeros(np.shape(adjMat))
        for a in range(antCount):
            ants.append(Ant(nodes=list(range(len(adjMat))),alpha=alpha,beta=beta))
        for n, ant in enumerate(ants):
            ant.move(tau,adjMat)
            if(ant.cost < bestCost):
                bestCost = ant.cost
                bestRoute = ant.route
            for r in range(len(ant.route)-1):
                tauChange[ant.route[r]][ant.route[r+1]] += q / ant.cost
            progressBar((i/iterations)+((n/(len(ants))/iterations)),("Best Route: "+str(bestRoute)+"\n"+"Cost of: "+str(bestCost)+"\n"))
            time.sleep(0.01)
        tau *= (1-evaporationCoeff)
        tau += tauChange / antCount
    # print("Best Route: "+str(bestRoute))
    # print("Cost of: "+str(bestCost))

def progressBar(data,string):
    '''
        data: float between 0-1
    '''
    # Gets position of index in list over list length as a floored percentage
    percent = int(np.floor(data*100))
    # Calculates half the percentage, this provides only 50 characters and a less excessive progress bar
    percentOver2 = int(percent/2)
    # Prints out the progress bar, ending in an escape character "\r" so that it keeps printing on the same line everytime
    print(string+"Training Progress: "+str(percent)+"% "+("#"*(percentOver2))+("."*(50-percentOver2)), end="\r")

if __name__ == "__main__":
    main()