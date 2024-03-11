import numpy as np

from python_tsp.heuristics import solve_tsp_simulated_annealing
from python_tsp.exact import solve_tsp_dynamic_programming
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from ant import Ant,AntSim
from distance_matrix import Mat
from pheromone_matrix import PMat

class TSP:

    def __init__(self, coords=None,matrix=None):
        if(coords):
            self.distMat = Mat(size=len(coords))
            self.distMat.formDistMat(coords,"pythagoras")
        elif(matrix):
            self.distMat = Mat(size=len(matrix),content=matrix)
        self.tau = np.ones(self.distMat.shape)
        # Python version of infinitely high cost
        self.bestCost = float("inf")
        self.bestRoute = []

    def iterate(self,alpha,beta,evaporationCoeff,q,antCount,pRange):
        ants = []
        self.tauChange = np.zeros(self.distMat.shape)
        for a in range(antCount):
            ants.append(Ant(nodes=list(range(self.distMat.size)),alpha=alpha,beta=beta))
        roundBestRoute = []
        roundBestCost = float('inf')
        for ant in ants:
            ant.move(self.tau,self.distMat)
            if(ant.cost < self.bestCost):
                self.bestCost = ant.cost
                self.bestRoute = ant.route
            if(ant.cost < roundBestCost):
                roundBestCost = ant.cost
                roundBestRoute = ant.route
        for r in range(len(self.bestRoute)-1):
            self.tauChange[self.bestRoute[r]][self.bestRoute[r+1]] += q
        for r in range(len(roundBestRoute)-1):
            self.tauChange[roundBestRoute[r]][roundBestRoute[r+1]] += q * (roundBestCost/self.bestCost)
        self.tau += self.tauChange / 2
        # tauChange = np.zeros(self.distMat.shape)
        self.tau *= (1-evaporationCoeff)
        self.tau = np.where(self.tau > pRange[0], self.tau, pRange[0])
        self.tau = np.where(self.tau < pRange[1], self.tau, pRange[1])
        return self.bestRoute,self.bestCost

    def getCost(self,route):
        cost = 0
        for r in range(len(route)-1):
            cost += self.distMat.get(route[r],route[r+1])
        return cost

    def useSolver(self):
        solution,cost = self.useORSolver()
        if(solution):
            # print("Used OR")
            return solution,cost
        else:
            # print("Used Py")
            solution,cost = self.usePySolver()
            return solution,cost

    def usePySolver(self):
        route,distance = solve_tsp_simulated_annealing(np.array(self.distMat.all()))
        route.append(route[0])
        return route,distance
    
    def useORSolver(self):
        distance_matrix_np = np.array(self.distMat.all())*100
        self.distance_matrix = np.floor(distance_matrix_np).astype(int).tolist()

        self.manager = pywrapcp.RoutingIndexManager(self.distMat.size,1,0)

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(self.manager)

        transit_callback_index = routing.RegisterTransitCallback(self.distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        
        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            index = routing.Start(0)
            route = [self.manager.IndexToNode(index)]
            while not routing.IsEnd(index):
                index = solution.Value(routing.NextVar(index))
                route.append(self.manager.IndexToNode(index))

            return route,solution.ObjectiveValue()
        return None

    def distance_callback(self,from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = self.manager.IndexToNode(from_index)
        to_node = self.manager.IndexToNode(to_index)
        return self.distance_matrix[from_node][to_node]

