import numpy as np
import tkinter as tk
import customtkinter as ctk
import threading

from ant import Ant,AntSim
from pheromone_matrix import PMat
from frames import InfoFrame,TSPFrame,SimFrame

class App(ctk.CTk):
    def __init__(self) -> None:
        ctk.set_appearance_mode("light")
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
        mainView._segmented_button.configure(font=("Tw Cen MT", 15))

        self.infoFrame = InfoFrame(master=mainView.tab("Info"))
        self.infoFrame.pack()

        self.graphFrame = TSPFrame(master=mainView.tab("Graphs"))
        self.graphFrame.pack()

        self.simFrame = SimFrame(master=mainView.tab("Simulation"))
        self.simFrame.pack()

        mainView.pack()

    def showFrame(self, page_name):
        '''
            Show a frame for the given page name
        '''
        frame = self.frames[page_name]
        frame.tkraise()

    def toggleFullscreen(self,even=None):
        self.fs = not self.fs
        self.attributes("-fullscreen", self.fs)

    def endFullscreen(self,event=None):
        self.fs = False
        self.attributes("-fullscreen", False)

if __name__ == "__main__":
    app = App()
    app.mainloop()
    app.graphFrame.running = False
    # print("App finished")
