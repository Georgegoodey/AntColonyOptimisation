import random
import math

from collections import deque

from distance_matrix import Mat
from pheromone_matrix import PMat

class AntTraverse:

    node: int
    end: int
    cost: int
    route: list
    mat: Mat

    def __init__(self, startNode, endNode, distMat:Mat) -> None:
        self.node = startNode
        self.end = endNode
        self.cost = 0
        self.route = [startNode]
        self.mat = distMat
    
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
        nodes = self.mat.row(i)
        for n in range(len(nodes)):
            prob = self.probabilityIJ(i,n,tau,self.mat.content,alpha,beta)
            probs.append(prob)
        return random.choices(range(len(probs)),weights=probs,k=1)[0]
    
    def move(self,tau,alpha,beta) -> None:
        while(self.node != self.end):
            newNode = self.nextNode(tau,alpha,beta)
            self.route.append(newNode)
            self.cost += self.mat.content[self.node][newNode]
            self.node = newNode

    def printAnt(self) -> None:
        print("Current Node: "+str(self.node))
        print("Goal Node: "+str(self.end))
        print("Current Cost: "+str(self.cost))
        print("Route so Far: "+str(self.route))

class Ant:

    node: int
    remaining: list[int]
    cost: float
    route: list[int]
    alpha: float
    beta: float

    def __init__(self, nodes:list[int], alpha:float, beta:float) -> None:
        self.remaining = nodes
        self.node = random.choice(nodes)
        self.remaining.remove(self.node)
        self.cost = 10000
        self.route = [self.node]
        self.alpha = alpha
        self.beta = beta
    
    def probabilityIJ(self,i:int,j:int,τ:list[list[float]],η:Mat) -> float:
        if(η.get(i,j) == 0):
            return 0
        pheromoneProx = τ[i][j]**self.alpha * η.get(i,j)**-self.beta
        # sumAllowed should be calculated here if following equation
        return pheromoneProx

    def nextNode(self,τ,η:Mat) -> int:
        i = self.node
        probs = []
        # Calculate denominator while calculating ij probability as it stays the same regardless of j and only needs to be calced once
        sumAllowed = 0
        for n in self.remaining:
            prob = self.probabilityIJ(i,n,τ,η)
            sumAllowed += prob
            probs.append(prob)
        for n,i in enumerate(probs):
            probs[n] = i / sumAllowed 
        return random.choices(self.remaining,weights=probs,k=1)[0]
    
    def move(self,τ:list[list[float]],η:Mat) -> None:
        originalNode = self.node
        while(self.remaining):
            newNode = self.nextNode(τ,η)
            self.remaining.remove(newNode)
            self.route.append(newNode)
            self.cost += η.get(self.node,newNode)
            self.node = newNode
        self.route.append(originalNode)
        self.cost += η.get(self.node,originalNode)
        self.node = originalNode

class AntSim:

    x: int
    y: int
    cost:  float
    alpha: float
    beta: float
    lastMove: int
    foundFood: bool
    mapSize: int

    def __init__(self, pos:list[int], alpha:float, beta:float, mapSize:int) -> None:
        self.x = pos[0]
        self.y = pos[1]
        self.cost = 2*mapSize
        self.alpha = alpha
        self.beta = beta
        self.lastMove = 3
        self.foundFood = False
        self.mapSize = 2*mapSize
    
    def probabilityIJ(self,tau,eta) -> float:
        if(tau <= 0):
            return 0
        pheromoneProx = tau**self.alpha * eta**-self.beta
        return pheromoneProx

    def nextNode(self,tau,eta) -> int:
        probs = []
        # Calculate denominator while calculating ij probability as it stays the same regardless of j and only needs to be calced once
        sumAllowed = 0
        for n in range(len(tau)):
            prob = self.probabilityIJ(tau[n],eta[n])
            sumAllowed += prob
            probs.append(prob)
        for n,i in enumerate(probs):
            probs[n] = i / sumAllowed
        return random.choices(range(len(tau)),weights=probs,k=1)[0]
    
    def calcNewPos(self,x,y,index):
        positions = [[x-1,y],[x-1,y+1],[x,y+1],[x+1,y+1],[x+1,y],[x+1,y-1],[x,y-1],[x-1,y-1]]
        return positions[index]

    def move(self,foodTau:PMat,nestTau:PMat) -> None:
        if(self.foundFood):
            tau = nestTau.getNeighbours(self.x,self.y)
        else:
            tau = foodTau.getNeighbours(self.x,self.y)
        r2 = math.sqrt(2)
        eta = deque([1,r2,2,2*r2,4,2*r2,2,r2])
        # eta = deque([1,1.3,1.6,2,2.5,2,1.6,1.3])
        eta.rotate(self.lastMove)
        # eta = list(eta)
        for e in range(len(eta)):
            if(e%2 != 0):
                eta[e] = eta[e] * r2
        # eta = [eta[e]*r2 for e in range(len(eta)) if e%2 == 0]
        newPosIndex = self.nextNode(tau,eta)
        cost = eta[newPosIndex]
        if(self.cost - cost > 0):
            self.cost -= cost
        else:
            self.cost = 0
        self.lastMove = newPosIndex
        newPos = self.calcNewPos(self.x,self.y,newPosIndex)
        self.x,self.y = newPos
        if(nestTau.tiles[self.x][self.y] == 2 and self.foundFood):
            self.foundFood = False
            self.cost = self.mapSize
            return True
        if(foodTau.tiles[self.x][self.y] == 2 and not self.foundFood):
            self.foundFood = True
            self.cost = self.mapSize
            return True
        return False