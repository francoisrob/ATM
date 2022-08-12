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
import pyglet
from PIL import Image, ImageTk

pyglet.font.add_file('OpenSans.ttf')

class ATM_Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._frame = None
        self.geometry('1000x600')
        self.title('National Bank')
        self.iconbitmap('favicon.ico')

        # Theme
        style = ttk.Style()
        style.configure('Header.TLabel')

        # background image (Do not delete)
        width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.image = Image.open('background_image01.png')
        self.image = self.image.resize((width, height))
        self.bg_image = ImageTk.PhotoImage(self.image)
        ttk.Label(self, image=self.bg_image).place(relx=.5,
                                                   rely=.5,
                                                   anchor='center')

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
        self.update_size()

    def set_theme(self):
        if self.tk.call("ttk::style", "theme", "use") == "azure-dark":
            # Set Light theme
            self.tk.call("set_theme", "light")
        else:
            self.tk.call("set_theme", "dark")
        self.update_size()

    def update_size(self):
        self._frame.update()
        width = self._frame.winfo_reqwidth() + 40
        height = self._frame.winfo_height() + 40
        print(str(height))
        self.minsize(width=width, height=height)

class MainMenu(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # Gui Creation
        # Center Widget
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(anchor='center', expand=True, fill='both')
        self.main_frame.columnconfigure(1, weight=3)

        self.left_panel = ttk.Frame(self.main_frame, style="Card.TFrame")
        self.left_panel.grid(row=0,
                             column=0)

        self.right_panel = ttk.Frame(self.main_frame)
        self.right_panel.grid(row=0,
                              column=1,
                              sticky='news')

        self.header_label = ttk.Label(self.left_panel,
                                      text='Welcome',
                                      font=('Open Sans', 30))
        self.header_label.grid(row=0,
                               column=0,
                               pady=20,
                               sticky='n')

        self.accounts_button = ttk.Button(self.left_panel,
                                          text='Accounts',
                                          width=30,
                                          style="Panel.TButton")
        self.accounts_button.grid(row=1,
                                  column=0,
                                  pady=(20, 0),
                                  padx=1)
        self.cards_button = ttk.Button(self.left_panel,
                                       text='Cards',
                                       width=30,
                                       style="Panel.TButton")
        self.cards_button.grid(row=2,
                               column=0)
        self.payments_button = ttk.Button(self.left_panel,
                                          text='Payments',
                                          command=lambda: master.switch_frame(LoginPage),
                                          width=30,
                                          style="Panel.TButton")
        self.payments_button.grid(row=3,
                                  column=0)

        # theme button
        theme_button = ttk.Button(self.left_panel,
                                  command=master.set_theme,
                                  text='Theme',
                                  width=30,
                                  style="Panel.TButton")
        theme_button.grid(row=4,
                          column=0,
                          pady=(150, 0))

        self.logout_button = ttk.Button(self.left_panel,
                                        text='Log Out',
                                        command=lambda: master.switch_frame(LoginPage),
                                        width=10)
        self.logout_button.grid(row=5,
                                column=0,
                                pady=10)
        # Right Panels
        self.accounts_panel = ttk.Frame(self.right_panel)
        self.cards_panel = ttk.Frame(self.right_panel)
        self.payments_panel = ttk.Frame(self.right_panel)
        self.show_panel(self.accounts_panel)
        for f in (self.accounts_panel, self.cards_panel, self.payments_panel):
            f.pack(expand=False, fill='none', side='right')

        # accounts panel
        ttk.Label(self.accounts_panel, text="Your balance").grid(column=0,
                                                                 row=0,
                                                                 sticky='w',
                                                                 pady=(20, 0),
                                                                 padx=20)
        self.balance_label = ttk.Label(self.accounts_panel,
                                       text='$ 1 568,95',
                                       font=20)
        self.balance_label.grid(column=0,
                                row=1,
                                sticky='w',
                                padx=25,
                                columnspan=1,
                                pady=(0, 20))
        self.payments_view = ttk.Treeview(self.accounts_panel, height=14)
        self.payments_view.grid(column=0,
                                row=3,
                                columnspan=3,
                                sticky='n',
                                pady=0,
                                padx=20)

    @staticmethod
    def show_panel(frame):
        frame.tkraise()


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
                                      text='Login to Your Account', font=('Open Sans', 20))
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
                            sticky='e')
        entry_username = ttk.Entry(login_frame,
                                   textvariable=username,
                                   justify='center',
                                   width=20,
                                   style='Custom.TEntry')
        entry_username.grid(row=1,
                            column=1,
                            pady=10,
                            padx=10,
                            sticky='w')

        password_label = ttk.Label(login_frame,
                                   text='Password')
        password_label.grid(row=2,
                            column=0,
                            sticky='e')
        entry_password = ttk.Entry(login_frame,
                                   textvariable=password,
                                   justify='center',
                                   width=20,
                                   show='*')
        entry_password.grid(row=2,
                            column=1,
                            pady=10,
                            padx=10,
                            sticky='w')

        # Login in button, currently only show the next frame, no verification function yet
        button_login = ttk.Button(login_frame,
                                  text='SIGN IN',
                                  width=35,
                                  style='Accent.TButton',
                                  command=lambda: master.switch_frame(MainMenu))
        button_login.grid(row=3,
                          column=0,
                          pady=(50, 20),
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
