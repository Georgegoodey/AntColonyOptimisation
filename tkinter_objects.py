import tkinter as tk

class FrameObject():

    frame: tk.Frame
    label: tk.Label

    def __init__(self, master, type, text="", val=0, size=None, resolution=None):
        self.frame = tk.Frame(master=master)

        self.label = tk.Label(master=self.frame, text=text, width=40)
        self.label.pack(side=tk.LEFT)

        if(type == "entry"):
            self.val = tk.Entry(master=self.frame, width=20)
            self.val.insert(0,val)
            self.val.pack(side=tk.RIGHT)
        elif(type == "scale"):
            self.val = tk.Scale(master=self.frame, from_=size[0], to=size[1], resolution=resolution, orient=tk.HORIZONTAL, tickinterval=1, width=20)
            self.val.set(val)
            self.val.pack(side=tk.RIGHT)

        self.frame.pack()

    def get(self):
        return float(self.val.get())

    def setText(self, text=""):
        self.label.config(text=text)