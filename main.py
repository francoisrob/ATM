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
import tkinter.ttk as ttk
# from PIL import Image, ImageTk

class ATM_Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # background image
        # width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        # self.image = Image.open('background_image01.png')
        # self.image = self.image.resize((width, height))
        # self.bg_image = ImageTk.PhotoImage(self.image)
        # ttk.Label(self, image=self.bg_image).place(relx=.5, rely=.5, anchor='center')

        # The container will be where we stack the frames on top of
        # The frames will be raised when called

        ttk.Style().configure('container.TFrame', background='blue')
        container = ttk.Frame(self)
        # container.pack(fill='both', expand=False, side='top')
        container.place(rely=.5, relx=.5, anchor='center')

        self.frames = {}
        for F in (MainMenu, LoginPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            # frame.pack(fill='both', expand=True, side='top')

        self.show_frame('LoginPage')

    def show_frame(self, page_name):
        # Displays frame with given name
        frame = self.frames[page_name]
        frame.tkraise()
        print('Raised ' + page_name)


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        print('f')
        # Center Widget
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(anchor='center', expand=True, fill='none')
        self.header_label = ttk.Label(self.main_frame,
                                      text='LOREEEyyyyyyyyyvFFFFFFFFFFvEM',
                                      style='Header.TLabel')
        self.header_label.grid(row=0,
                               column=0,
                               padx=20,
                               pady=(20, 40),
                               columnspan=2)

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        style = ttk.Style()

        # Variables
        username = tk.StringVar()
        password = tk.StringVar()

        # GUI creation
        style.configure('login.TFrame',
                        background='white')

        # Center Widget
        login_frame = ttk.Frame(self, style='login.TFrame',width=800)
        login_frame.pack(fill='none', expand=True, anchor='center')
        # Header Text
        style.configure('Header.TLabel',
                        background='white',
                        font='Ubuntu 24 bold')
        self.header_label = ttk.Label(login_frame,
                                      text='Login to Your Account',
                                      style='Header.TLabel')
        self.header_label.grid(row=0,
                               column=0,
                               padx=20,
                               pady=(20, 40),
                               columnspan=2)

        # Input
        style.configure('Subheader.TLabel',
                        background='white',
                        font='Ubuntu 14')
        username_label = ttk.Label(login_frame,
                                   text='Username',
                                   style='Subheader.TLabel')
        username_label.grid(row=1,
                            column=0,
                            padx=(20, 0))
        entry_username = ttk.Entry(login_frame,
                                   textvariable=username,
                                   justify='center',
                                   font='Ubuntu 14',
                                   foreground='black',
                                   width=20)
        entry_username.grid(row=1,
                            column=1,
                            pady=10,
                            padx=(10, 20),
                            sticky='e')

        password_label = ttk.Label(login_frame,
                                   text='Password',
                                   style='Subheader.TLabel')
        password_label.grid(row=2,
                            column=0,
                            padx=(20, 0))
        entry_password = ttk.Entry(login_frame,
                                   textvariable=password,
                                   justify='center',
                                   font='Ubuntu 14',
                                   foreground='black',
                                   width=20,
                                   show='*')
        entry_password.grid(row=2,
                            column=1,
                            pady=10,
                            padx=20,
                            sticky='e')

        button_login = tk.Button(login_frame,
                                 text='SIGN IN',
                                 font='Ubuntu 14',
                                 relief='groove',
                                 bg='white',
                                 command=lambda: controller.show_frame('MainMenu'))
        button_login.grid(row=3,
                          column=0,
                          pady=(20, 50),
                          columnspan=2)


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
