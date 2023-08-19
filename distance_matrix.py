class Mat:

    content: list[list[float]]
    size: int
    '''size: the height and length of the content in the matrix'''
    shape: list[int]

    def __init__(self, size:int) -> None:
        self.content = [[0] * size for i in range(size)]
        self.size = size
        self.shape = [size,size]

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
    
    def row(self,i:int) -> list[float]:
        '''
            Returns the row of held at position i
        '''
        return self.content[i]