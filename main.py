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
from PIL import Image, ImageTk


class ATM_Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._frame = None

        # Theme
        style = ttk.Style()
        style.configure('Header.TLabel')
        style.configure('Custom.TButton', border=0)

        self.geometry('1000x600')

        # background image (Do not delete)
        width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.image = Image.open('background_image01.png')
        self.image = self.image.resize((width, height))
        self.bg_image = ImageTk.PhotoImage(self.image)
        ttk.Label(self, image=self.bg_image).place(relx=.5,
                                                   rely=.5,
                                                   anchor='center')

        # theme button
        theme_button = ttk.Button(self,
                                  command=self.set_theme,
                                  text='Theme')
        theme_button.place(relx=0.5,
                           rely=0,
                           anchor='n')

        self.switch_frame(LoginPage)

    def switch_frame(self, page_name):
        # This function displays new frames and deletes old ones
        new_frame = page_name(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(relx=.5,
                          rely=.5,
                          anchor='center')

    def set_theme(self):
        if self.tk.call("ttk::style", "theme", "use") == "azure-dark":
            # Set Light theme
            self.tk.call("set_theme", "light")
        else:
            self.tk.call("set_theme", "dark")

class MainMenu(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # Gui Creation
        # Center Widget
        self.main_frame = ttk.Frame(self, style='Parent.TFrame')
        self.main_frame.pack(anchor='center', expand=True, fill='both')
        self.header_label = ttk.Label(self.main_frame,
                                      text='Welcome _User', font=20)
        self.header_label.grid(row=0,
                               column=0,
                               padx=20,
                               pady=(20, 40),
                               columnspan=4)

        self.deposit_button = ttk.Button(self.main_frame,
                                         text='Deposit',
                                         command=lambda: print('deposit'))
        self.deposit_button.grid(row=1,
                                 column=1,
                                 padx=20,
                                 pady=(20, 40))

        self.back_button = ttk.Button(self.main_frame,
                                      text='Back',
                                      command=lambda: master.switch_frame(LoginPage))
        self.back_button.grid(row=1,
                              column=0,
                              padx=20,
                              pady=(20, 40))


class LoginPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # Variables
        username = tk.StringVar()
        password = tk.StringVar()

        # GUI creation
        # Center Widget
        login_frame = ttk.Frame(self)
        login_frame.pack(fill='none', expand=True, anchor='center')

        # Header Text
        self.header_label = ttk.Label(login_frame,
                                      text='Login to Your Account', font=('Bold', 20))
        self.header_label.grid(row=0,
                               column=0,
                               padx=20,
                               pady=20,
                               columnspan=2)

        # Input
        username_label = ttk.Label(login_frame,
                                   text='Username')
        username_label.grid(row=1,
                            column=0,
                            padx=(20, 0),
                            sticky='e')
        entry_username = ttk.Entry(login_frame,
                                   textvariable=username,
                                   justify='center',
                                   width=20,
                                   style='Custom.TEntry')
        entry_username.grid(row=1,
                            column=1,
                            pady=10,
                            padx=(10, 20),
                            sticky='e')

        password_label = ttk.Label(login_frame,
                                   text='Password')
        password_label.grid(row=2,
                            column=0,
                            padx=(20, 0),
                            sticky='e')
        entry_password = ttk.Entry(login_frame,
                                   textvariable=password,
                                   justify='center',
                                   width=20,
                                   show='*')
        entry_password.grid(row=2,
                            column=1,
                            pady=10,
                            padx=(10, 20),
                            sticky='e')

        # Login in button, currently only show the next frame, no verification function yet
        button_login = ttk.Button(login_frame,
                                  text='SIGN IN',
                                  width=20,
                                  style='Accent.TButton',
                                  command=lambda: master.switch_frame(MainMenu))
        button_login.grid(row=3,
                          column=0,
                          pady=20,
                          columnspan=2)


if __name__ == "__main__":
    root = ATM_Application()
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "light")
    root.mainloop()
"""
==Most basic code to create a new frame

class PageName(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        
        # When creating a new form please parent all widgets inside of a parent frame, 
        # this will make organising the widgets easier in future. Take LoginPage as example
"""