import numpy as np

from python_tsp.heuristics import solve_tsp_simulated_annealing
from python_tsp.exact import solve_tsp_dynamic_programming
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

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
        return self.bestRoute,self.bestCost

    def useSolver(self):
        if(solution := self.useORSolver()):
            return solution,0
        else:
            solution,cost = self.usePySolver()
            return solution,cost

    def usePySolver(self):
        route,distance = solve_tsp_simulated_annealing(np.array(self.distMat.all()))
        route.append(route[0])
        return route,distance
    
    def useORSolver(self):
        distance_matrix_np = np.array(self.distMat.all())
        self.distance_matrix = np.floor(distance_matrix_np*10000).astype(int).tolist()

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

            return route
        return None

    def distance_callback(self,from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = self.manager.IndexToNode(from_index)
        to_node = self.manager.IndexToNode(to_index)
        return self.distance_matrix[from_node][to_node]

