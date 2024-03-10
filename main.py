import numpy as np
import tkinter as tk
import customtkinter as ctk
import threading

from ant import Ant,AntSim
from pheromone_matrix import PMat
from frames import StartFrame,TSPFrame,SimFrame

class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.geometry("1920x1080")

        # self.attributes('-fullscreen', True)
        # self.state('zoomed') 

        self.fs = False
        self.bind("<F11>", self.toggleFullscreen)
        self.bind("<Escape>", self.endFullscreen)

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartFrame,TSPFrame,SimFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("StartFrame")

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
    print("App finished")
