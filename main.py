import numpy as np
import tkinter as tk
import customtkinter as ctk
import threading

from ant import Ant,AntSim
from pheromone_matrix import PMat
from frames import InfoFrame,TSPFrame,SimFrame

class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.geometry("1920x1080")
        self.title("Ant Colony Optimisation")

        self.fs = False
        self.bind("<F11>", self.toggleFullscreen)
        self.bind("<Escape>", self.endFullscreen)

        mainView = ctk.CTkTabview(master=self)
        mainView.add("Info")
        mainView.add("Graphs")
        mainView.add("Simulation")

        infoFrame = InfoFrame(master=mainView.tab("Info"))
        infoFrame.pack()

        graphFrame = TSPFrame(master=mainView.tab("Graphs"))
        graphFrame.pack()

        simFrame = SimFrame(master=mainView.tab("Simulation"))
        simFrame.pack()

        mainView.pack()

    def showFrame(self, page_name):
        '''
            Show a frame for the given page name
        '''
        frame = self.frames[page_name]
        frame.tkraise()

        # menuBar = frame.menuBar(self)
        # self.configure(menu=menuBar)

    def toggleFullscreen(self,even=None):
        self.fs = not self.fs
        self.attributes("-fullscreen", self.fs)

    def endFullscreen(self,event=None):
        self.fs = False
        self.attributes("-fullscreen", False)

if __name__ == "__main__":
    app = App()
    app.mainloop()
    # print("App finished")
