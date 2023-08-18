import random

from distance_matrix import Mat

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
    remaining: list
    cost: int
    route: list
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
    
    def probabilityIJ(self,i,j,τ,η) -> float:
        if(η[i][j] == 0):
            return 0
        pheromoneProx = τ[i][j]**self.alpha * η[i][j]**-self.beta
        # sumAllowed = 0
        # for m in range(len(η[i])):
        #     if(η[i][m] == 0):
        #         continue
        #     sumAllowed += τ[i][m]**self.alpha * η[i][m]**-self.beta
        # probIJ = pheromoneProx/sumAllowed
        return pheromoneProx#probIJ

    def nextNode(self,τ,η) -> int:
        i = self.node
        probs = []
        # Calculate denominator outside of ij probability as it stays the same regardless of j
        sumAllowed = 0
        for m in range(len(η[i])):
            if(η[i][m] == 0):
                continue
            sumAllowed += τ[i][m]**self.alpha * η[i][m]**-self.beta
        for n in self.remaining:
            prob = self.probabilityIJ(i,n,τ,η) / sumAllowed
            probs.append(prob)
        return random.choices(self.remaining,weights=probs,k=1)[0]
    
    def move(self,τ,η) -> None:
        originalNode = self.node
        while(self.remaining):
            newNode = self.nextNode(τ,η)
            self.remaining.remove(newNode)
            self.route.append(newNode)
            self.cost += η[self.node][newNode]
            self.node = newNode
        self.route.append(originalNode)
        self.cost += η[self.node][originalNode]
        self.node = originalNode

    def printAnt(self) -> None:
        print("Current Node: "+str(self.node))
        print("Goal Node: "+str(self.end))
        print("Current Cost: "+str(self.cost))
        print("Route so Far: "+str(self.route))