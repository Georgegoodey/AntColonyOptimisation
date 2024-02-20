import numpy as np
import tkinter as tk
import threading

from ant import Ant,AntSim
from pheromone_matrix import PMat
from frames import StartFrame,TSPFrame,SimFrame

class App(tk.Tk):
    def __init__(self,screenName:str|None=None,baseName:str|None=None,className:str="Tk",useTk:bool=True,sync:bool=False,use:str|None=None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        # self.attributes('-fullscreen', True)
        # self.state('zoomed') 

        self.fs = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartFrame,TSPFrame,SimFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartFrame")

    def show_frame(self, page_name):
        '''
            Show a frame for the given page name
        '''
        frame = self.frames[page_name]
        frame.tkraise()

        menuBar = frame.menuBar(self)
        self.configure(menu=menuBar)

    def toggle_fullscreen(self,even=None):
        self.fs = not self.fs
        self.attributes("-fullscreen", self.fs)

    def end_fullscreen(self,event=None):
        self.fs = False
        self.attributes("-fullscreen", False)

if __name__ == "__main__":
    app = App()
    app.mainloop()

def progressBar(data:float,string:str="") -> None:
    '''
        data: float between 0-1
        string: a string to be displayed after the progress bar
    '''
    # Gets position of index in list over list length as a floored percentage
    percent = int(np.floor(data*100))
    # Calculates half the percentage, this provides only 50 characters and a less excessive progress bar
    percentOver4 = int(percent/4)
    # Prints out the progress bar, ending in an escape character "\r" so that it keeps printing on the same line everytime
    print(string+"Training Progress: "+str(percent)+"% "+("█"*(percentOver4))+("▒"*(25-percentOver4)), end="\r")
