"""
                                        ============================
                                        |  Python ATM Application  |
                                        ============================


Objectives:
    * This program should have a gui with different frames/pages to access different parts of the program.
    * There must be a login page for the user to log in with a Username and password.
    * There must be a withdraw option. (How does one go about withdrawing cash from an online bank?)
    * There must be a transfer option (Funds from the same user's account to another)
    * There must be a pay outstanding credit button
    * There must be a pay beneficiaries buttons (One user's account to another user's account)
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
from tkinter import messagebox

import pyglet
from PIL import Image, ImageTk

import mysql.connector
from mysql.connector import errorcode

import re

Version = 'v2-0813'
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
        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "light")

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
        self.entry_username = ttk.Entry(login_frame,
                                        textvariable=username,
                                        justify='center',
                                        width=20,
                                        style='Custom.TEntry')
        self.entry_username.grid(row=1,
                                 column=1,
                                 pady=10,
                                 padx=10,
                                 sticky='w')

        password_label = ttk.Label(login_frame,
                                   text='Password')
        password_label.grid(row=2,
                            column=0,
                            sticky='e')
        self.entry_password = ttk.Entry(login_frame,
                                        textvariable=password,
                                        justify='center',
                                        width=20,
                                        show='*')
        self.entry_password.grid(row=2,
                                 column=1,
                                 pady=10,
                                 padx=10,
                                 sticky='w')

        # Login in button, currently only show the next frame, no verification function yet
        button_login = ttk.Button(login_frame,
                                  text='SIGN IN',
                                  width=35,
                                  style='Accent.TButton',
                                  command=lambda: self.check_login_details(self.entry_username.get(),
                                                                           self.entry_password.get()))
        button_login.grid(row=3,
                          column=0,
                          pady=(50, 20),
                          columnspan=2)

        """DB check for username and password"""

    @staticmethod
    def check_login_details(username, password):

        # No username and password entered
        if not username:
            messagebox.showerror("Invalid entry", "Username cannot be left blank.\nPlease enter a Username.")
        elif not password:
            messagebox.showerror("Invalid entry", "Password cannot be left blank.\nPlease enter a Password.")

        # Username and password entered
        else:
            db = db_connect()
            db_cursor = db.cursor()
            db_cursor.execute("SELECT username, password FROM db_atm.tbl_users")
            users = db_cursor.fetchall()
            user_input = password
            user_password = ""

            for user in users:
                if user[0] == username:
                    user_input = password  # Fetches the typed password
                    user_password = user[1]  # Fetches the correct password
                    # Reason for this is because I do not want an error message running on each unmatched entry

            if user_password == "":
                # Warning message displayed for unmatched entry form db
                messagebox.showerror("Invalid entry", "Username or password is incorrect")
            elif user_input == user_password:
                ATM_Application().switch_frame(MainMenu)
                """<--------------- BIG ERROR HERE"""
            else:
                # Password is incorrect and does not match username
                messagebox.showerror("Invalid entry", "Username or password is incorrect")

            # You can be specific and tell the user what is wrong with their inputs.
            # The reason I want to leave it ambiguous is, because anybody can guess a username and in the instance
            # where they guess correctly they can attempt to crack the password.
            # (Discuss which approach to follow)



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

        self.header_label = ttk.Label(self.left_panel,
                                      text='Welcome',
                                      font=('Open Sans', 30))
        self.header_label.pack(side='top',
                               padx=(20, 30),
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
        theme_button = ttk.Button(self.left_panel,
                                  command=master.set_theme,
                                  text='Theme',
                                  style="Panel.TButton")
        theme_button.pack(side='bottom', fill='x')

    def show_panel(self, panel):
        # This function displays new panels on the right
        new_panel = panel(self.right_panel)
        if self._panel is not None:
            self._panel.destroy()
        self._panel = new_panel
        self._panel.grid()


class AccountsPanel(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # Gui Creation
        self.accounts_panel = ttk.Frame(self, width=500, height=500, style="Card.TFrame")
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
        self.cards_panel = ttk.Frame(self, width=500, height=500, style="Card.TFrame")
        self.cards_panel.grid()
        self.cards_panel.grid_propagate(False)

        ttk.Label(self.cards_panel, text="Cards").grid(column=0,
                                                       row=0,
                                                       padx=30,
                                                       pady=(30, 0),
                                                       sticky='w')


class PaymentsPanel(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # Gui Creation
        self.payments_panel = ttk.Frame(self, width=500, height=500, style="Card.TFrame")
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


# This can be used later on
"""Validation for username and password
    def error_check_username(self, username):
        # Checks if the received username matches the required conditions.

        # Usernames can't be shorter than 1 character
        if len(username) < 1:
            messagebox.showerror("Invalid username", "Username must be longer than 1 character")
            return False
        # Usernames can only use letters, numbers, dots, underscores and hyphens
        if not re.match('^[a-z0-9._-]*$', username):
            messagebox.showerror("Invalid username", "u")
            return False
        # Usernames can't begin with a non-alphanumeric character
        if not username[0].isalpha():
            messagebox.showerror("Invalid username", "Username must begin with a letter")
            return False
        return True
"""

if __name__ == "__main__":
    root = ATM_Application()
    root.mainloop()
