class PMat:

    content: list[list[float]]
    size: int
    '''size: the height and length of the content in the matrix'''
    shape: list[int]

    def __init__(self, size:int) -> None:
        self.content = [[0] * size for i in range(size)]
        self.size = size
        self.shape = [size,size]

    def set(self,i:int,j:int,value:float) -> None:
        '''
            Replaces the value at position i,j with the value parameter
        '''
        self.content[i][j] = value

    def add(self,i:int,j:int,value:float) -> None:
        '''
            Increases the value stored at position i,j by the value parameter
        '''
        self.content[i][j] += value

    def get(self,i:int,j:int) -> list[float]:
        '''
            Returns the neighbours of position i,j
        '''
        corners = [self.content[i-1][j-1],self.content[i-1][j+1],self.content[i+1][j-1],self.content[i+1][j+1]]
        sides = [self.content[i-1][j],self.content[i][j-1],self.content[i][j+1],self.content[i+1][j]]
        c = self.content
        neighbours = [c[i-1][j],c[i-1][j+1],c[i][j+1],c[i+1][j+1],c[i+1][j],c[i+1][j-1],c[i][j-1],c[i-1][j-1]]
        return neighbours

    def evaporate(self,val:float) -> None:
        '''
            Evaporates the values in the matrix
            Reduces the values to be (1-val) of the original value
            val: float representing how much evaporation should occur
        '''
        for row in self.content:
            for num in row:
                num *= (1-val)