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