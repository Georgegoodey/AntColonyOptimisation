from math import pi,sin,cos,atan2,sqrt
# import numpy as np

class Mat:

    content: list[list[float]]
    proximity: list[list[float]]
    size: int
    '''size: the height and length of the content in the matrix'''
    shape: list[int]
    beta: float

    def __init__(self, size:int, content:list[list[float]]=None) -> None:
        if(content):
            self.content = content
        else:
            self.content = [[0] * size for i in range(size)]
        # self.content = np.array((size,size))
        self.size = size
        self.shape = [size,size]
        # self.beta = beta
        # self.proximity = [[0] * size for i in range(size)]

    def set(self,i:int,j:int,distance:float) -> None:
        '''
            Replaces the value at position i,j with the distance parameter
        '''
        self.content[i][j] = distance

    def get(self,i:int,j:int) -> float:
        '''
            Returns the value held at position i,j
        '''
        return self.content[i][j]
    
    def all(self) -> list[list[float]]:
        '''
            Returns entire distance matrix
        '''
        return self.content

    def getProx(self,i:int,j:int) ->  float:
        '''
            Returns the proximity of the value at i,j rather than the distance
        '''
        return self.proximity[i][j]
    
    def row(self,i:int) -> list[float]:
        '''
            Returns the row of held at position i
        '''
        return self.content[i]
    
    def formDistMat(self,vertexCoords:list[list[float]],distance:str) -> None:
        '''
            Forms a distance matrix between all the given vertex coordinates
            vertexCoords: a list of coordinates for each data point vertex
            distance: the distance function to be used in the distance matrix calculations
        '''
        if(distance == "haversine"):
            distFunc = self.haversineDistance
        else:
            distFunc = self.pythagoreanDistance
        for i,n in enumerate(vertexCoords):
            for j,m in enumerate(vertexCoords):
                if(n==m):
                    continue
                self.content[i][j] = distFunc(n,m)

    def haversineDistance(self,i:list[float],j:list[float]) -> float:
        '''
            Use haversine forumla for finding distances between longitude and latitude coords
            i: first position
            j: second position
        '''
        R = 6371e3
        phiI = i[0] * pi / 180
        phiJ = j[0] * pi / 180
        deltaPhi = (j[0]-i[0]) * pi / 180
        deltaLambda = (j[1]-i[1]) * pi / 180

        a = (sin(deltaPhi/2) * sin(deltaPhi/2)) + (cos(phiI) * cos(phiJ) * sin(deltaLambda/2) * sin(deltaLambda/2))
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        return distance

    def pythagoreanDistance(self,a:float,b:float) -> float:
        '''
            Use pythagoras formula to calculate distance between two points
        '''
        xDist = abs(a[0]-b[0])
        yDist = abs(a[1]-b[1])
        distance = sqrt((xDist**2) + (yDist**2))

        return distance