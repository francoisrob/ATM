#############################
#                           #
#   PYTHON ATM APPLICATION  #
#                           #
#############################

import tkinter as tk

class MainWindow:
    def __init__(self, master):
        self.root = master
        root.title('ATM')
        root.geometry('500x500')
        # self.hover = HoverInfo(self, 'Hello', self)

        print('Hello world')

    def ChangeColor(self):
        print('hello dude')


root = tk.Tk()
MainWindow(root)
root.mainloop()
