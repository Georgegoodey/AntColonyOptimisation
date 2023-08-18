class Mat:

    content: list[list[float]]
    size: int
    shape: list[int]

    def __init__(self, size) -> None:
        self.content = [[0] * size for i in range(size)]
        self.size = size
        self.shape = [size,size]

    def set(self,i,j,item):
        self.content[i][j] = item

    def get(self,i,j):
        return self.content[i,j]
    
    def row(self,i):
        return self.content[i]