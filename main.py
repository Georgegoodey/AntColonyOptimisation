import random

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
        pheromoneProx = tau[i][j]**alpha * (1/eta[i][j])**beta
        sumAllowed = 0
        for m in range(len(eta[i])):
            if(eta[i][m] == 0):
                continue
            sumAllowed += tau[i][m]**alpha * (1/eta[i][m])**beta
        probIJ = pheromoneProx/sumAllowed
        return probIJ

    def nextNode(self,tau,alpha,beta) -> int:
        i = self.node
        probs = []
        nodes = self.mat[i]
        # validNodes = list(filter(lambda x: x != 0, nodes))
        # eta = list(map(lambda x: 1/x, validNodes))
        # print(eta)
        for n in range(len(nodes)):
            prob = self.probabilityIJ(i,n,tau,self.mat,alpha,beta)
            probs.append(prob)
        return random.choices(range(len(probs)),weights=probs,k=1)[0]
    
    def move(self,tau,alpha,beta):
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
    adjMat  =  [[0,1,2,0],[1,0,0,1],[2,0,0,2],[0,1,2,0]]
    tau  = [[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
    alpha = 1
    beta = 2
    antCount = int(input("How many ants do you want to simulate: "))
    iterations = int(input("How many iterations do you want to simulate: "))
    start = int(input("Enter start node: "))
    end = int(input("Enter goal node: "))
    bestCost = float("inf")
    for i in range(iterations):
        ants = []
        for a in range(antCount):
            ants.append(Ant(start,end,adjMat))
        for ant in ants:
            ant.move(tau,alpha,beta)
            # if(ant.cost < bestCost):

            

if __name__ == "__main__":
    main()