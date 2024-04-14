import csv
import matplotlib.pyplot as plt
import numpy as np
import customtkinter as ctk
import tkinter as tk
import math as maths

from tkinter import filedialog,StringVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure 

class CompareFrame(ctk.CTkFrame):
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        titleFrame = ctk.CTkFrame(master=self, width=1000)

        label = ctk.CTkLabel(master=titleFrame, text="Parameter Data", font=("Bahnschrift", 30))
        label.pack(pady=5)

        titleFrame.pack(side=tk.TOP, fill=tk.X)

        self.loadData()
        self.createWidgets()

    def loadData(self):

        inFile = open("testsScore.csv")
        inReader = csv.reader(inFile)

        self.fileDict = {}
        self.timeDict = {}

        iterations = 500
        self.iterator = list(range(0,iterations))
        self.tests = 5

        for row in inReader:
            key = row[0]
            if(key in self.fileDict):
                iteration = float(row[1])
                score = float(row[2])
                time = float(row[3])
                if(iteration in self.iterator):
                    self.fileDict[key][self.iterator.index(iteration)] += score
                    self.timeDict[key][self.iterator.index(iteration)] += time
            else:
                self.fileDict[key] = np.zeros(len(self.iterator))
                self.timeDict[key] = np.zeros(len(self.iterator))
                iteration = float(row[1])
                score = float(row[2])
                time = float(row[3])
                if(iteration in self.iterator):
                    self.fileDict[key][self.iterator.index(iteration)] += score
                    self.timeDict[key][self.iterator.index(iteration)] += time

        inFile.close()

        inFile = open("testsOR.csv")
        inReader = csv.reader(inFile)

        for row in inReader:
            key = row[0]+",OR Tools"
            if(key in self.fileDict):
                score = float(row[1])
                time = float(row[2])
                self.fileDict[key] += score
                self.timeDict[key] += time
            else:
                self.fileDict[key] = np.zeros(len(self.iterator))
                self.timeDict[key] = np.zeros(len(self.iterator))
                score = float(row[1])
                time = float(row[2])
                self.fileDict[key] += score
                self.timeDict[key] += time

        inFile.close()

    def createWidgets(self):
        widgetFrame = ctk.CTkFrame(master=self)

        files = ['dj38.tsp','att48.tsp','berlin52.tsp','pr76.tsp','kroB100.tsp']
        filesOR = ['dj38.tsp,OR Tools','att48.tsp,OR Tools','berlin52.tsp,OR Tools','pr76.tsp,OR Tools','kroB100.tsp,OR Tools']

        plot = Plot(widgetFrame,files=files+filesOR,fileDict=self.fileDict,tests=self.tests,iterator=self.iterator)
        plot.pack(pady=10,padx=10,fill=tk.BOTH,side=tk.LEFT)

        plot = Table(widgetFrame,files=files,orfiles=filesOR,fileDict=self.fileDict,timeDict=self.timeDict,tests=self.tests,iterator=self.iterator)
        plot.pack(pady=10,padx=10,fill=tk.BOTH,side=tk.RIGHT)

        widgetFrame.pack(pady=10, padx=10, fill=tk.BOTH)

    def drawPlots(self):

        self.data = self.data/self.tests

        self.ax = self.fig.add_subplot()

        self.ax.set_title('Score per alpha, beta parameter (no processing)')

        self.ax.set_xlabel('Alpha')
        self.ax.set_ylabel('Beta')

        self.ax.invert_yaxis()

    def savePlot(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                  filetypes=[("PNG files", "*.png"),
                                                             ("JPEG files", "*.jpg"),
                                                             ("All files", "*.*")])
        if file_path:
            self.fig.savefig(file_path)
            print(f"Plot saved as {file_path}")

class Table(ctk.CTkFrame):
    def __init__(self, master, files, orfiles, fileDict, timeDict, tests, iterator):
        ctk.CTkFrame.__init__(self, master)

        self.fileDict = fileDict
        self.timeDict = timeDict
        self.tests = tests
        self.iterator = iterator
        self.colours = ['b','g','c','m','y','k','tab:orange','tab:purple','tab:blue','tab:brown']
        self.files = files

        self.save = ctk.CTkButton(self, text="Save Plot", command=self.savePlot)
        self.save.pack(side=tk.BOTTOM,pady=10,padx=10)

        self.fig = Figure(figsize=(10,2))

        data = [['', 'ACO Solution', 'OR Tools Solution', 'ACO Time', 'OR Tools Time', 'ACO Beats OR Score Time']]
        for f1,f2 in zip(files,orfiles):
            acoData = fileDict[f1]/tests
            acoTimes = timeDict[f1]/tests
            acoBest = np.min(acoData)
            orBest = np.min(fileDict[f2]/tests)
            orTime = timeDict[f2]/tests
            timeIndex = np.argmax(acoData <= acoBest)
            acoTime = np.sum(acoTimes[:timeIndex])
            timeIndexOR = np.argmax(acoData <= orBest)
            beatTime = np.sum(acoTimes[:timeIndexOR])
            data.append([f1,acoBest,orBest,acoTime,orTime[0],beatTime])

        self.ax = self.fig.add_subplot()
        self.ax.axis('off')
        self.table = self.ax.table(cellText=data, loc='center', cellLoc='center')
        self.table.scale(1.5, 1)
        self.table.auto_set_font_size(False)
        self.table.set_fontsize(10)
        # self.ax.plot(self.iterator, data, color='r', label=files[0])
        self.ax.set_title('Score data for each dataset')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=10,padx=10,side=tk.TOP, fill=tk.BOTH, expand=1)

    def savePlot(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                  filetypes=[("PNG files", "*.png"),
                                                             ("JPEG files", "*.jpg"),
                                                             ("All files", "*.*")])
        if file_path:
            self.fig.savefig(file_path, bbox_inches='tight')
            print(f"Plot saved as {file_path}")

class ParamFrame(ctk.CTkFrame):

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        titleFrame = ctk.CTkFrame(master=self, width=1000)

        label = ctk.CTkLabel(master=titleFrame, text="Parameter Data", font=("Bahnschrift", 30))
        label.pack(pady=5)

        titleFrame.pack(side=tk.TOP, fill=tk.X)

        self.loadData()
        self.createWidgets()

    def loadData(self):

        inFile = open("testsParameters.csv")
        inReader = csv.reader(inFile)

        fileDict = {}

        self.alphas = list(np.arange(0, 5.5, 0.5))
        self.betas = list(np.arange(0, 5.5, 0.5))
        for row in inReader:
            key = row[0]
            if(key in fileDict):
                alpha = float(row[1])
                beta = float(row[2])
                if(alpha in self.alphas and beta in self.betas):
                    fileDict[key][self.betas.index(beta)][self.alphas.index(alpha)] += float(row[-1])
            else:
                fileDict[key] = np.zeros((len(self.betas),len(self.alphas)))
                alpha = float(row[1])
                beta = float(row[2])
                if(alpha in self.alphas and beta in self.betas):
                    fileDict[key][self.betas.index(beta)][self.alphas.index(alpha)] += float(row[-1])

        inFile.close()

        self.data = fileDict['oliver30.tsp']

    def createWidgets(self):
        self.fig = Figure(figsize=(8,6))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=10,padx=10,side=tk.TOP, fill=tk.BOTH, expand=1)

        self.save = ctk.CTkButton(self, text="Save Plot", command=self.savePlot)
        self.save.pack(side=tk.BOTTOM,pady=10,padx=10)

        self.drawPlots()

    def drawPlots(self):

        # self.data = self.data-np.min(self.data)
        self.data = self.data/10
        # self.data = np.log2(self.data, out=np.zeros_like(self.data), where=(self.data!=0))

        self.ax = self.fig.add_subplot()

        self.heatmap = self.ax.imshow(self.data, cmap='seismic',extent=[self.alphas[0], self.alphas[-1]+0.5, self.betas[-1]+0.5, self.betas[0]])

        self.fig.colorbar(self.heatmap)

        self.ax.set_title('Score per alpha, beta parameter (no processing)')

        self.ax.set_xlabel('Alpha')
        self.ax.set_ylabel('Beta')

        self.ax.invert_yaxis()

    def savePlot(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                  filetypes=[("PNG files", "*.png"),
                                                             ("JPEG files", "*.jpg"),
                                                             ("All files", "*.*")])
        if file_path:
            self.fig.savefig(file_path)
            print(f"Plot saved as {file_path}")

class IterFrame(ctk.CTkFrame):

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        titleFrame = ctk.CTkFrame(master=self, width=1000)

        label = ctk.CTkLabel(master=titleFrame, text="Iteration-Score Data", font=("Bahnschrift", 30))
        label.pack(pady=5)

        titleFrame.pack(side=tk.TOP, fill=tk.X)

        self.loadData()
        self.createWidgets()

    def loadData(self):
        inFile = open("testsScore.csv")
        inReader = csv.reader(inFile)

        self.fileDict = {}

        iterations = 500
        self.iterator = list(range(0,iterations))
        self.tests = 5

        for row in inReader:
            key = row[0]
            if(key in self.fileDict):
                iteration = float(row[1])
                score = float(row[2])
                if(iteration in self.iterator):
                    self.fileDict[key][self.iterator.index(iteration)] += score
            else:
                self.fileDict[key] = np.zeros(len(self.iterator))
                iteration = float(row[1])
                score = float(row[2])
                if(iteration in self.iterator):
                    self.fileDict[key][self.iterator.index(iteration)] += score

        inFile.close()

    def createWidgets(self):

        widgetFrame = ctk.CTkFrame(master=self)

        files1 = ['oliver30.tsp','dj38.tsp','att48.tsp','berlin52.tsp','pr76.tsp','kroB100.tsp']
        # files1= ['att48.tsp','berlin52.tsp']
        files2 = ['4x16.tsp','5x25.tsp','6x36.tsp','7x49.tsp','8x64.tsp','9x81.tsp','10x100.tsp']

        # self.drawPlots(files1,widgetFrame,side=tk.LEFT)
        plot = Plot(widgetFrame,files=files1,fileDict=self.fileDict,tests=self.tests,iterator=self.iterator)
        plot.pack(pady=10,padx=10,fill=tk.BOTH,side=tk.LEFT)

        # self.drawPlots(files2,widgetFrame,side=tk.RIGHT)
        plot = Plot(widgetFrame,files=files2,fileDict=self.fileDict,tests=self.tests,iterator=self.iterator)
        plot.pack(pady=10,padx=10,fill=tk.BOTH,side=tk.RIGHT)

        widgetFrame.pack(pady=10, padx=10, fill=tk.BOTH)

    def drawPlots(self,files,frame,side):
        plot = Plot(frame,files=files,fileDict=self.fileDict,tests=self.tests,iterator=self.iterator)
        plot.pack(pady=10,padx=10,fill=tk.BOTH,side=side)

class Plot(ctk.CTkFrame):
    def __init__(self, master, files, fileDict, tests, iterator):
        ctk.CTkFrame.__init__(self, master)

        self.fig = None

        self.fileDict = fileDict
        self.tests = tests
        self.iterator = iterator
        self.colours = ['b','g','c','m','y','k','tab:orange','tab:purple','tab:blue','tab:brown']
        self.files = files

        sliderFrame = ctk.CTkFrame(master=self)

        self.var = tk.DoubleVar(value=2.7)

        slider = ctk.CTkSlider(sliderFrame, from_=0.5, to=2.7, command=self.updatePlot,variable=self.var)
        slider.pack(pady=10,padx=10)

        self.save = ctk.CTkButton(sliderFrame, text="Save Plot", command=self.savePlot)
        self.save.pack(side=tk.BOTTOM,pady=10,padx=10)

        # self.slider_val = ctk.CTkLabel(self, textvariable=var)

        sliderFrame.pack(side=tk.BOTTOM,pady=10,padx=10)

        checkFrame = ctk.CTkFrame(master=self)

        self.checks = {}

        for i in self.files:
            # file = StringVar(i)
            fileCheck = ctk.CTkCheckBox(master=checkFrame, text=i, command=self.updateFiles, onvalue=i, offvalue="")
            fileCheck.select()
            self.checks[i] = fileCheck
            fileCheck.pack(pady=10,padx=10)

        checkFrame.pack(pady=10,padx=10,side=tk.LEFT)

        self.fig = Figure(figsize=(10,6))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=10,padx=10,side=tk.TOP, fill=tk.BOTH, expand=1)

        self.drawPlots(files=files)

    def updateFiles(self):
        wantedFiles = []
        for i in self.files:
            if(self.checks[i].get() == i):
                wantedFiles.append(i)
        if(len(wantedFiles)>0):
            self.drawPlots(files=wantedFiles)

    def drawPlots(self,files):

        data = self.fileDict[files[0]]
        data = data/self.tests

        self.fig.clf()
            
        self.ax = self.fig.add_subplot()
        self.ax.plot(self.iterator, data, color='r', label=files[0])
        self.ax.tick_params(axis='y', labelcolor='r')
        low = np.min(data)
        high = np.max(data)
        offset = (high-low)*0.05
        low-=offset
        high+=offset
        self.ax.set_ylim(low,high)
        self.ax.set_title('Model distance per iteration')

        self.ax.set_xlabel('Iterations')
        self.ax.set_ylabel('Distance')

        for i,f in enumerate(files[1:]):
            self.plot(f,i)

        self.fig.legend()

        self.updatePlot(self.var.get())

    def updatePlot(self, value):
        newLimit = int(maths.floor(10**float(value)))
        self.ax.set_xlim(0, newLimit)
        self.canvas.draw()

    def plot(self,name,colourIndex):
        data = self.fileDict[name]
        data = data/self.tests

        ax = self.ax.twinx()

        nameComps = name.split(',')
        if(len(nameComps)==1):
            colour = self.colours[colourIndex]
        
            ax.plot(self.iterator, data, color=colour, label=name)
            ax.tick_params(axis='y', labelcolor=colour)
            low = np.min(data)
            high = np.max(data)
            offset = (high-low)*0.05
            low-=offset
            high+=offset
            ax.set_ylim(low,high)
            ax.spines['right'].set_position(('outward', colourIndex*60))
        else:
            colour = self.colours[colourIndex]
        
            ax.plot(self.iterator, data, color=colour, label=name)
            compData = self.fileDict[nameComps[0]]/self.tests
            low = np.min(compData)
            high = np.max(compData)
            offset = (high-low)*0.05
            low-=offset
            high+=offset
            ax.set_ylim(low,high)
            ax.set_yticks([])
        return ax
    
    def savePlot(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                  filetypes=[("PNG files", "*.png"),
                                                             ("JPEG files", "*.jpg"),
                                                             ("All files", "*.*")])
        if file_path:
            self.fig.savefig(file_path, bbox_inches='tight')
            print(f"Plot saved as {file_path}")

class App(ctk.CTk):
    def __init__(self) -> None:
        ctk.set_appearance_mode("light")
        super().__init__()

        self.geometry("1920x1080")
        self.title("Ant Colony Optimisation Test Suite")

        mainView = ctk.CTkTabview(master=self)
        mainView.add("Parameters")
        mainView.add("Iterations")
        mainView.add("OR Comparison")
        mainView._segmented_button.configure(font=("Tw Cen MT", 15))

        self.iterFrame = IterFrame(master=mainView.tab("Iterations"))
        self.iterFrame.pack()

        self.paramFrame = ParamFrame(master=mainView.tab("Parameters"))
        self.paramFrame.pack()

        self.compareFrame = CompareFrame(master=mainView.tab("OR Comparison"))
        self.compareFrame.pack()

        mainView.pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()

# print(data)