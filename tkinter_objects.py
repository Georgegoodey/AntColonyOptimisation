import tkinter as tk
import customtkinter as ctk
import networkx as nx

from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg) 

class FrameObject(ctk.CTkFrame):

    # frame: ctk.CTkFrame
    label: ctk.CTkLabel

    def __init__(self, master, type, text="", val=0, size=None, steps=None):
        ctk.CTkFrame.__init__(self, master=master)

        label_width = 400
        if(type == "label"):
            label_width = 600
        
        self.label = ctk.CTkLabel(master=self, text=text, width=label_width)
        self.label.pack(side=tk.LEFT)

        if(type == "entry"):
            self.val = ctk.CTkEntry(master=self, width=200)
            self.val.insert(0,val)
            self.val.pack(side=tk.RIGHT)
        elif(type == "scale"):
            # self.val = tk.Scale(master=self.frame, from_=size[0], to=size[1], resolution=resolution, orient=tk.HORIZONTAL, tickinterval=1, width=20)
            self.val = ctk.CTkSlider(master=self, from_=size[0], to=size[1], width=200, number_of_steps=steps)
            self.val.set(val)
            self.val.pack(side=tk.RIGHT)

    def get(self):
        return float(self.val.get())

    def setText(self, text=""):
        self.label.configure(text=text)

class GraphObject(Figure):

    def __init__(self, master:ctk.CTkFrame, colour, figsize=(15,10), dpi=100) -> None:
        Figure.__init__(self,figsize=figsize, dpi=dpi)

        self.master = master

        self.colour = colour

        self.canvas = FigureCanvasTkAgg(self,master=master)
        self.canvas.draw() 

        self.canvas.get_tk_widget().pack()

        self.graph = nx.Graph()

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