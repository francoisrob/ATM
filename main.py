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
import mysql.connector
from mysql.connector import errorcode

Version = 'v0.813'
pyglet.font.add_file('OpenSans.ttf')


class ATM_Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._frame = None
        self.geometry('1000x700')
        self.title('National Bank')
        self.iconbitmap('favicon.ico')

        # Theme
        style = ttk.Style()
        style.configure('Header.TLabel')
        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "light")

        # background image
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
        self.minsize(width=width, height=height)


class LoginPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # Variables
        username = tk.StringVar()
        password = tk.StringVar()

        # GUI creation
        # Center Widget
        login_frame = ttk.Frame(self)
        login_frame.grid()

        self.image = Image.open('bank_logo.png')
        self.image = self.image.resize((100, 50))
        self.bg_image = ImageTk.PhotoImage(self.image)
        ttk.Label(login_frame, image=self.bg_image).grid(row=0,
                                                         column=0,
                                                         pady=(20, 10),
                                                         padx=20,
                                                         sticky='n')

        # Header Text
        self.header_label = ttk.Label(login_frame,
                                      text='Log In', font=('Open Sans', 24))
        self.header_label.grid(row=1,
                               column=0,
                               padx=20,
                               pady=(0, 15),
                               sticky='w')

        # Input
        username_label = ttk.Label(login_frame,
                                   text='Username')
        username_label.grid(row=2,
                            column=0,
                            sticky='w',
                            padx=20)
        entry_username = ttk.Entry(login_frame,
                                   textvariable=username,
                                   justify='center',
                                   width=30,
                                   style='Custom.TEntry')
        entry_username.grid(row=3,
                            column=0,
                            padx=20,
                            pady=(0, 10),
                            sticky='w')

        password_label = ttk.Label(login_frame,
                                   text='Password')
        password_label.grid(row=4,
                            column=0,
                            sticky='w',
                            padx=20)
        entry_password = ttk.Entry(login_frame,
                                   textvariable=password,
                                   justify='center',
                                   width=30,
                                   show='*')
        entry_password.grid(row=5,
                            column=0,
                            padx=20,
                            pady=(0, 20),
                            sticky='w')

        # Login in button, currently only show the next frame, no verification function yet
        button_login = ttk.Button(login_frame,
                                  text='SIGN IN',
                                  width=29,
                                  style='Accent.TButton',
                                  command=lambda: master.switch_frame(MainMenu))
        button_login.grid(row=6,
                          column=0,
                          padx=20,
                          pady=10,
                          columnspan=2)

        button_register = ttk.Button(login_frame,
                                     text='Register',
                                     width=29,
                                     style='Panel.TButton',
                                     command=lambda: master.switch_frame(MainMenu))
        button_register.grid(row=7,
                             padx=20,
                             pady=(0, 10),
                             columnspan=2)


class MainMenu(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # Gui Creation
        # Center Widget
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack()
        self.main_frame.columnconfigure(1, weight=3)
        # Left Panel
        self.left_panel = ttk.Frame(self.main_frame)
        self.left_panel.pack(side='left', fill='y')
        # Right Panel
        self.right_panel = ttk.Frame(self.main_frame)
        self.right_panel.pack(side='right')
        self._panel = None
        self.show_panel(AccountsPanel)

        self.header_panel = ttk.Panedwindow(self.left_panel, style='Card.TFrame')
        self.header_panel.pack(side='top', fill='x')
        self.header_label = ttk.Label(self.header_panel, text='Welcome', font=('Open Sans', 20))
        self.header_label.pack(side='top',
                               pady=(10, 20))
        self.accounts_button = ttk.Button(self.left_panel,
                                          text='Accounts',
                                          style="Panel.TButton",
                                          command=lambda: self.show_panel(AccountsPanel))
        self.accounts_button.pack(side='top', fill='x')
        self.cards_button = ttk.Button(self.left_panel,
                                       text='Cards',
                                       style="Panel.TButton",
                                       command=lambda: self.show_panel(CardsPanel))
        self.cards_button.pack(side='top', fill='x')
        self.payments_button = ttk.Button(self.left_panel,
                                          text='Payments',
                                          command=lambda: self.show_panel(PaymentsPanel),
                                          style="Panel.TButton")
        self.payments_button.pack(side='top', fill='x')

        self.version_label = ttk.Label(self.left_panel, font=('Open Sans light', 5))
        self.version_label.pack(side='bottom', fill='x')
        self.version_label.configure(text=Version)
        self.logout_button = ttk.Button(self.left_panel,
                                        text='Log Out',
                                        command=lambda: master.switch_frame(LoginPage),
                                        style="Panel.TButton")
        self.logout_button.pack(side='bottom', fill='x')

        # theme button
        theme_button = ttk.Checkbutton(self.left_panel,
                                       command=master.set_theme,
                                       text='Theme',
                                       style="Switch.TCheckbutton")
        theme_button.pack(side='bottom', fill='x', padx=60)
        if self.tk.call("ttk::style", "theme", "use") == "azure-dark":
            theme_button.state(['selected'])

    def show_panel(self, panel):
        # This function displays new panels on the right
        new_panel = panel(self.right_panel)
        if self._panel is not None:
            self._panel.destroy()
        self._panel = new_panel
        self._panel.pack()


class AccountsPanel(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # Gui Creation
        self.accounts_panel = ttk.Frame(self, width=600, height=600, style="Card.TFrame")
        self.accounts_panel.grid()
        self.accounts_panel.grid_propagate(False)

        ttk.Label(self.accounts_panel, text="Your balance").grid(column=0,
                                                                 row=0,
                                                                 padx=30,
                                                                 pady=(30, 0),
                                                                 sticky='w')
        self.balance_label = ttk.Label(self.accounts_panel,
                                       text='$ 1 568,95',
                                       font=('Open Sans', 20))
        self.balance_label.grid(column=0,
                                row=1,
                                sticky='e',
                                padx=30,
                                columnspan=2,
                                pady=(0, 20))


class CardsPanel(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # Gui Creation
        self.cards_panel = ttk.Frame(self, width=600, height=600, style="Card.TFrame")
        self.cards_panel.grid()
        self.cards_panel.grid_propagate(False)

        # ttk.Label(self.cards_panel, text="Cards").grid(column=0,
        #                                                row=0,
        #                                                padx=30,
        #                                                pady=(30, 0),
        #                                                sticky='w')
        self.credit_panel = ttk.Frame(self.cards_panel,
                                      width=600,
                                      height=200,
                                      style='Card.TFrame')
        self.credit_panel.grid(row=0, column=0, padx=1)
        self.debit_panel = ttk.Frame(self.cards_panel,
                                     width=600,
                                     height=200,
                                     style='Card.TFrame')
        self.debit_panel.grid(row=1, column=0, padx=1)
        self.savings_panel = ttk.Frame(self.cards_panel,
                                       width=600,
                                       height=200,
                                       style='Card.TFrame')
        self.savings_panel.grid(row=2, column=0, padx=1)


class PaymentsPanel(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # Gui Creation
        self.payments_panel = ttk.Frame(self, width=600, height=600, style="Card.TFrame")
        self.payments_panel.grid()
        self.payments_panel.grid_propagate(False)

        ttk.Label(self.payments_panel, text="Payments").grid(column=0,
                                                             row=0,
                                                             padx=30,
                                                             pady=(30, 0),
                                                             sticky='w')


"""
Code to create a database with relational tables.
Populates the tables with values.
"""


def db_connect():
    # Connecting to the database is set as a method since we need to open and close it for different transactions
    # Error handling code:
    # https://docs.oracle.com/cd/E17952_01/connector-python-en/connector-python-example-connecting.html
    # Start of borrowed code
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            port="3306",
        )
        return db
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            exit()
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            exit()
        else:
            print(e)
            exit()
    # End of borrowed code


if __name__ == "__main__":
    root = ATM_Application()
    root.mainloop()
