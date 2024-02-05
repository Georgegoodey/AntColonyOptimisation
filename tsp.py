import numpy as np

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
                # self.app.updateGraph(bestRoute,coords=self.app.coords)
            for r in range(len(ant.route)-1):
                tauChange[ant.route[r]][ant.route[r+1]] += q / ant.cost
            self.tau += tauChange / antCount
            tauChange = np.zeros(self.distMat.shape)
            # progressBarLabel((i/iterations)+((a/(len(ants))/iterations)))
        self.tau *= (1-evaporationCoeff)
        return self.bestRoute