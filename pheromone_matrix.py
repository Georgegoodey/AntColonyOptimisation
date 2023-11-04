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
        self.content[i][j] += value

    def get(self,i:int,j:int) -> list[float]:
        '''
            Returns the neighbours of position i,j
        '''
        corners = [self.content[i-1][j-1],self.content[i-1][j+1],self.content[i+1][j-1],self.content[i+1][j+1]]
        sides = [self.content[i-1][j],self.content[i][j-1],self.content[i][j+1],self.content[i+1][j]]
        return corners,sides