import random
import numpy as np

class Ant:

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

def main() -> None:
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
            ants.append(Ant(start,end,adjMat))
        for ant in ants:
            ant.move(tau,alpha,beta)
            if(ant.cost < bestCost):
                bestCost = ant.cost
                bestRoute = ant.route
            for r in range(len(ant.route)-1):
                tauChange[ant.route[r]][ant.route[r+1]] += q / ant.cost
        tau *= (1-evaporationCoeff)
        tau += tauChange / antCount
    print("Best Route: "+str(bestRoute))
    print("Cost of: "+str(bestCost))

if __name__ == "__main__":
    main()