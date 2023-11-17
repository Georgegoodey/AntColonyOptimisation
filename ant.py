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
        self.cost = 0
        self.route = [self.node]
        self.alpha = alpha
        self.beta = beta
    
    def probabilityIJ(self,i:int,j:int,τ:list[list[float]],η:Mat) -> float:
        if(η.get(i,j) == 0):
            return 0
        pheromoneProx = τ[i][j]**self.alpha * η.getProx(i,j)
        # sumAllowed should be calculated here if following equation
        return pheromoneProx

    def nextNode(self,τ,η:Mat) -> int:
        i = self.node
        probs = []
        # Calculate denominator while calculating ij probability as it stays the same regardless of j and only needs to be calced once
        sumAllowed = 0
        # for m in range(η.size):
        #     if(η.get(i,m) == 0):
        #         continue
        #     sumAllowed += τ[i][m]**self.alpha * η.getProx(i,m)
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

    def __init__(self, pos:list[int], alpha:float, beta:float) -> None:
        self.x = pos[0]
        self.y = pos[1]
        self.cost = 0
        self.alpha = alpha
        self.beta = beta
        self.lastMove = 3
    
    def probabilityIJ(self,tau,eta) -> float:
        if(tau < 0):
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
        if(index==0):
            return [x-1,y]
        elif(index==1):
            return [x-1,y+1]
        elif(index==2):
            return [x,y+1]
        elif(index==3):
            return [x+1,y+1]
        elif(index==4):
            return [x+1,y]
        elif(index==5):
            return [x+1,y-1]
        elif(index==6):
            return [x,y-1]
        elif(index==7):
            return [x-1,y-1]
        else:
            return []

    def move(self,τ:PMat) -> None:
        tau = τ.get(self.x, self.y)
        r2 = math.sqrt(2)
        eta = deque([1,r2,2,2*r2,4,2*r2,2,r2])
        eta.rotate(self.lastMove)
        newPosIndex = self.nextNode(tau,eta)
        self.cost = eta[newPosIndex]
        self.lastMove = newPosIndex
        newPos = self.calcNewPos(self.x,self.y,newPosIndex)
        self.x,self.y = newPos