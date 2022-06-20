"""
                                        ============================
                                        |  Python ATM Application  |
                                        ============================


Objectives:
    * This program should have a gui with different frames/pages to access different parts of the program.
    * There must be a login page for the user to log in with a Username and password.
    * There must be a withdraw option.
    * User should be able to view their funds.
    * Should be secure, the program should take extra measures in encryption preventing any
    unauthorized manipulation of data.

Ideas:
    * Fancy gui with animations, backgrounds, custom buttons etc.
    * Widgets to resize to window dimensions.
    *


Glossary:

*args allow us to pass a variable number of non-keyword arguments to a function, as a tuple
**kwargs allow us to pass variable number of keyword arguments to a function, type= Dictionary
source: https://tinyurl.com/yeyvstc3

The code to switch between different frames,
source: https://tinyurl.com/bdedjxcy

"""
import tkinter as tk

class ATM_Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # The container will be where we stack the frames on top of
        # The frames will be raised when called
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        Header_label = tk.Label(self, text='Hello')


if __name__ == "__main__":
    root = ATM_Application()
    root.mainloop()


"""
==Most basic code to create a new frame

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
"""
