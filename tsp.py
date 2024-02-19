import numpy as np

from python_tsp.heuristics import solve_tsp_simulated_annealing


from ant import Ant,AntSim
from distance_matrix import Mat
from pheromone_matrix import PMat

class TSP:

    def __init__(self, coords):
        self.coords = coords
        self.distMat = Mat(len(self.coords))
        self.distMat.formDistMat(self.coords,"haversine")
        self.tau = np.ones(self.distMat.shape)
        # Python version of infinitely high cost
        self.bestCost = float("inf")
        self.bestRoute = []

    def iterate(self,alpha,beta,evaporationCoeff,q,antCount):
        ants = []
        tauChange = np.zeros(self.distMat.shape)
        for a in range(antCount):
            ants.append(Ant(nodes=list(range(self.distMat.size)),alpha=alpha,beta=beta))
        for a, ant in enumerate(ants):
            ant.move(self.tau,self.distMat)
            if(ant.cost < self.bestCost):
                self.bestCost = ant.cost
                self.bestRoute = ant.route
            for r in range(len(ant.route)-1):
                tauChange[ant.route[r]][ant.route[r+1]] += q / ant.cost
            self.tau += tauChange / antCount
            tauChange = np.zeros(self.distMat.shape)
        self.tau *= (1-evaporationCoeff)
        return self.bestRoute

    def useSolver(self):
        route,distance = solve_tsp_simulated_annealing(np.array(self.distMat.all()))
        route.append(route[0])
        return route,distance