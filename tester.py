import csv
import matplotlib.pyplot as plt
import numpy as np

inFile = open("tests.csv")
inReader = csv.reader(inFile)

fileDict = {}

alphas = list(np.arange(0, 5.5, 0.5))
betas = list(np.arange(0, 5.5, 0.5))
evaps = [0.5]
# alphas = [0, 0.5, 1, 2, 5]
# betas = [0, 1, 2, 5]  
# evaps = [0.3, 0.5, 0.7, 0.9, 0.999]
def initFile(fileName):
    fileDict[fileName] = np.empty((len(betas),len(alphas)))
    # fileDict[fileName] = {}
    # fileDict[fileName]['alpha'] = {}
    # fileDict[fileName]['beta'] = {}
    # fileDict[fileName]['evap'] = {}
    # for a in alphas:
    #     fileDict[fileName]['alpha'][str(a)] = []
    # for b in betas:
    #     fileDict[fileName]['beta'][str(b)] = []
    # for e in evaps:
    #     fileDict[fileName]['evap'][str(e)] = []

for row in inReader:
    key = row[0]
    if(key in fileDict):
        alpha = float(row[1])
        beta = float(row[2])
        if(alpha in alphas and beta in betas):
            # print(alpha,beta)
            fileDict[key][betas.index(beta)][alphas.index(alpha)] += float(row[-1])
        # fileDict[key]['alpha'][row[1]].append(row[2:])
        # fileDict[key]['beta'][row[2]].append([row[1]]+row[3:])
        # fileDict[key]['evap'][row[3]].append((row[1:3]+row[4:]))
    else:
        initFile(key)

inFile.close()

data = fileDict['oliver30.tsp']

def plot(type):

    x = []
    y = []

    for key in data[type]:

        x.append(key)

        total = 0
        for v in data[type][key]:
            total += float(v[-1])
        
        y.append(total/len(data[type][key]))

    plt.plot(x, y)

# plot('alpha')
# plot('beta')
# plot('evap')

data = np.min(data)/data

plt.imshow(data, cmap='viridis',extent=[alphas[0], alphas[-1]+0.5, betas[-1]+0.5, betas[0]])

plt.colorbar()

plt.xlabel('Alpha')
plt.ylabel('Beta')

plt.gca().invert_yaxis()

plt.show()

# print(data)