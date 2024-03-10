import csv
import os

class Loader:

    coords: list[tuple[float,float]]

    def __init__(self) -> None:
        self.coords = []

    def loadFile(self, filepath:str) -> None:
        filetype = os.path.splitext(filepath)[1][1:]
        if(filetype == "csv"):
            self.coords = loadCSV(filename=filepath)
        elif(filetype == "tsp"):
            self.coords = loadTSP(filename=filepath)
        elif(filetype == "txt"):
            self.coords = loadTXT(filename=filepath)

        return self.coords

def loadCSV(filename:str) -> list[list[float]]:
    '''
        Forms a list of vertex coordinates from the csv contents of a file
        filename: a string representing the name of the data
        index1: a int representing the csv index of the first datum, can represent latitude, x etc.
        index2: a int representing the csv index of the second datum, can represent longitude, y etc.
        header: a boolean of whether or not the file has a header row
        limit: an int that will limit the number of rows loaded from the csv, higher than the length of file will be ignored
    '''
    # Empty list of vertex coordinates
    coords = []
    # CSV file reference
    csvFile = open(filename)
    # CSV reader object
    csvReader = csv.reader(csvFile)
    
    # indices default to 0 and 1, will be overwritten if possible(adding later)
    index1, index2 = 0,1

    # Iterate while there is a next row in the file with row as the reference
    for row in csvReader:
        # If the current line of the csv reader is higher than the limit then stop loading file and return
        # if(csvReader.line_num>limit):
        #     break
        # If there is no header row or the current line of the csv reader is not 1
        if((csvReader.line_num != 1)):
            # Add the indexed items from the current row to the list of coordinates
            coords.append([float(row[index1]),float(row[index2])])
        else:
            for i,item in enumerate(row):
                if item == "lat":
                    index1 = i
                elif item == "lng":
                    index2 = i

    return coords

def loadTXT(filename:str) -> list[list[float]]:
    # Empty list of vertex coordinates
    coords = []
    # TSP file reference
    txtFile = open(filename)
    
    for row in txtFile:
        nums = row.split()
        coords.append([int(nums[0]),int(nums[1])])

    txtFile.close()

    return coords

def loadTSP(filename:str):
    with open(filename, 'r') as tspFile:
        lines = tspFile.readlines()
    
    dimension = int([line.split(":")[1] for line in lines if line.startswith("DIMENSION")][0])

    coords = None

    if("NODE_COORD_SECTION\n" in lines):
        coord_section_index = lines.index("NODE_COORD_SECTION\n") + 1

        coords = []
        for line in lines[coord_section_index:coord_section_index + dimension]:
            parts = line.split()
            city_number = int(parts[0])
            x, y = map(float, parts[1:])
            coords.append((x, y))

    edges = None

    if("EDGE_WEIGHT_SECTION\n" in lines):
        edge_section_index = lines.index("EDGE_WEIGHT_SECTION\n") + 1

        edges = []
        for line in lines[edge_section_index:edge_section_index + dimension]:
            parts = line.split()
            # city_number = int(parts[0])
            edge_row = map(float, parts[1:])
            edges.append(edge_row)

    tour = None

    if("TOUR_SECTION\n" in lines):
        tour_index = lines.index("TOUR_SECTION\n") + 1
        
        tour = []
        for line in lines[tour_index:tour_index + dimension]:
            city_number = int(line)-1
            tour.append(city_number)

    return (coords,edges,tour)