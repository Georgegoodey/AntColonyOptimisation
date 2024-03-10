import tkinter as tk
import customtkinter as ctk

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