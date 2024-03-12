import tkinter as tk
from typing import Tuple
import customtkinter as ctk
import networkx as nx
import numpy as np

from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg) 
from PIL import Image

class FrameObject(ctk.CTkFrame):

    # frame: ctk.CTkFrame
    label: ctk.CTkLabel

    def __init__(self, master, type, text="", val=0, val2=0, size=None, steps=None, fontType="tsp"):
        ctk.CTkFrame.__init__(self, master=master)

        fontStyle = ("Bahnschrift", 15)
        if(fontType=="sim"):
            fontStyle = ("Small Fonts", 15)

        labelWidth = 400
        if(type == "label"):
            labelWidth = 600
        
        self.label = ctk.CTkLabel(master=self, text=text, width=labelWidth,font=fontStyle)
        self.label.pack(side=tk.LEFT)

        if(type == "entry"):
            self.val = ctk.CTkEntry(master=self, width=200,font=fontStyle)
            self.val.insert(0,val)
            self.val.pack(side=tk.RIGHT)
        elif(type == "scale"):
            # self.val = tk.Scale(master=self.frame, from_=size[0], to=size[1], resolution=resolution, orient=tk.HORIZONTAL, tickinterval=1, width=20)
            self.val = ctk.CTkSlider(master=self, from_=size[0], to=size[1], width=200, number_of_steps=steps)
            self.val.set(val)
            self.val.pack(side=tk.RIGHT)
        elif(type == "dualEntry"):
            self.vFrame = ctk.CTkFrame(master=self, width=200)
            self.val = ctk.CTkEntry(master=self.vFrame, width=100,font=fontStyle)
            self.val.insert(0,val)
            self.val.pack(side=tk.LEFT)
            self.val2 = ctk.CTkEntry(master=self.vFrame, width=100,font=fontStyle)
            self.val2.insert(0,val2)
            self.val2.pack(side=tk.RIGHT)
            self.vFrame.pack(side=tk.RIGHT)

    def get(self,vals=1):
        if(vals == 1):
            return float(self.val.get())
        else:
            return (float(self.val.get()),float(self.val2.get()))

    def setText(self, text=""):
        self.label.configure(text=text)

class GraphObject(Figure):

    def __init__(self, master:ctk.CTkFrame, colour, figsize=(12,5), dpi=100) -> None:
        Figure.__init__(self,figsize=figsize, dpi=dpi)

        self.master = master

        self.colour = colour

        self.canvas = FigureCanvasTkAgg(self,master=master)
        self.canvas.draw() 

        self.canvas.get_tk_widget().pack()

        self.graph = nx.Graph()

    def initGraph(self,coords):
        self.graph.clear()
        for node in coords:
            self.graph.add_node(node,pos=(node[1], node[0]))

    def updateGraph(self,route,coords):
        self.graph.clear()
        for r in range(len(route)-1):
            node = route[r]
            self.graph.add_node(node,pos=(coords[node][1], coords[node][0]))
            self.graph.add_edge(node, route[r+1])

    def redrawGraph(self): 
        self.clf()
        plot1 = self.add_subplot(111)

        pos = {node: coords for node, coords in nx.get_node_attributes(self.graph, "pos").items()}
        nx.draw(self.graph, pos, with_labels=False, node_size=50, node_color=self.colour, ax=plot1)
        self.canvas.draw()
        self.master.after(100,self.redrawGraph)

    def drawGraph(self):
        self.clf()
        plot1 = self.add_subplot(111)

        pos = {node: coords for node, coords in nx.get_node_attributes(self.graph, "pos").items()}
        nx.draw(self.graph, pos, with_labels=False, node_size=50, node_color=self.colour, ax=plot1)
        self.canvas.draw()

class ImageObject(ctk.CTkImage):

    viewSize: Tuple[int,int]
    
    def __init__(self, size: Tuple[int, int] = (100,100)):
        blankImage = np.zeros((size[0], size[1], 3), dtype=np.uint8)
        blankImage = Image.fromarray(blankImage)
        blankImage = blankImage.resize(size, resample=Image.NEAREST)
        super().__init__(light_image=None, dark_image=blankImage, size=size)
        self.viewSize = size

    def reRender(self,image):
        self.configure(dark_image=image)

class FileObject(ctk.CTkFrame):

    def __init__(self, master, fontType="tsp"):
        super().__init__(master=master)

        fontStyle = ("Bahnschrift", 15)
        if(fontType=="sim"):
            fontStyle = ("Small Fonts", 15)

        labelWidth = 350

        self.nameLabel = ctk.CTkLabel(master=self, text="File Name:  N/A", width=labelWidth,font=fontStyle)
        self.nameLabel.pack()

        self.commentTitle = ctk.CTkLabel(master=self, text="File Comment:", width=labelWidth,font=fontStyle)
        self.commentTitle.pack()
        
        self.commentLabel = ctk.CTkLabel(master=self, text="N/A", width=labelWidth,font=fontStyle)
        self.commentLabel.pack()

        self.nodeLabel = ctk.CTkLabel(master=self, text="Nodes: N/A", width=labelWidth,font=fontStyle)
        self.nodeLabel.pack()

        self.solLabel = ctk.CTkLabel(master=self, text="Contains Solution: N/A", width=labelWidth,font=fontStyle)
        self.solLabel.pack()

    def editVars(self,fileName:str="N/A",fileComment:str="N/A",nodes:int=0,sol:bool=False):
        self.nameLabel.configure(text=("File Name:  "+str(fileName)))

        self.commentLabel.configure(text=(str(fileComment)))

        self.nodeLabel.configure(text=("Nodes: "+str(nodes)))

        if(sol):
            self.solLabel.configure(text=("Contains Solution: Yes"))
        else:
            self.solLabel.configure(text=("Contains Solution: No"))