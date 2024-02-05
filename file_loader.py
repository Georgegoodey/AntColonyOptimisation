import csv

def loadCSV(filename:str,index1:int,index2:int,header:bool,limit:int) -> list[list[float]]:
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
    
    # Iterate while there is a next row in the file with row as the reference
    for row in csvReader:
        # If the current line of the csv reader is higher than the limit then stop loading file and return
        if(csvReader.line_num>limit):
            break
        # If there is no header row or the current line of the csv reader is not 1
        if((not header) or (csvReader.line_num != 1)):
            # Add the indexed items from the current row to the list of coordinates
            coords.append([float(row[index1]),float(row[index2])])
    
    return coords

def loadTXT(filename:str,limit:int) -> list[list[float]]:
    # Empty list of vertex coordinates
    coords = []
    # TSP file reference
    tspFile = open(filename)
    
    for row in tspFile:
        nums = row.split()
        coords.append([int(nums[0]),int(nums[1])])

    tspFile.close()

    return coords