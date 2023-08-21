class Mat:

    content: list[list[float]]
    proximity: list[list[float]]
    size: int
    '''size: the height and length of the content in the matrix'''
    shape: list[int]
    beta: float

    def __init__(self, size:int, beta:float) -> None:
        self.content = [[0] * size for i in range(size)]
        self.size = size
        self.shape = [size,size]
        self.beta = beta
        self.proximity = [[0] * size for i in range(size)]

    def init_prox(self):
        for i,row in enumerate(self.content):
            for j,item in enumerate(row):
                if(item == 0):
                    continue
                self.proximity[i][j] = item**-self.beta

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