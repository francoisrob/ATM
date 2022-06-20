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
import tkinter.font as tkfont
import tkinter.ttk as ttk


class ATM_Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Ubuntu', size=18)

        # The container will be where we stack the frames on top of
        # The frames will be raised when called
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)


        self.frames = {}
        for F in (MainMenu, LoginPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('LoginPage')

    def show_frame(self, page_name):
        # Displays frame with given name
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # GUI creation old tk :/
        login_frame = tk.Frame(controller, bg='white')
        login_frame.pack(expand=False, fill='y', side='top')
        header_label = tk.Label(login_frame, text='Login to Your Account', font='Ubuntu 24', bg='white')
        header_label.grid(row=0, column=0, padx=20, pady=(20, 40))
        entry_username = tk.Entry(login_frame, relief='solid', font=controller.title_font)
        entry_username.grid(row=1, column=0, pady=10)
        entry_password = tk.Entry(login_frame, relief='solid', show="*", font=controller.title_font)
        entry_password.grid(row=2, column=0, pady=10)
        button_login = tk.Button(login_frame,
                                 text='SIGN IN',
                                 font=controller.title_font,
                                 relief='groove',
                                 bg='white',
                                 command=controller.show_frame)
        button_login.grid(row=3, column=0, pady=(20,50))


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
