"""
                                        ============================
                                        |  Python ATM Application  |
                                        ============================


Objectives:
    * This program should have a gui with different frames/pages to access different parts of the program.
    * There must be a login page for the user to log in with a Username and password.
    * There must be a with-draw option.
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
import tkinter.messagebox as messagebox
import pyglet
import requests
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import errorcode

Version = 'v0.818'
exchange_data = []
UserID = ''
UserData = []
TransactionData = []
AccountsData = []
CardType = ['', '', '']
pyglet.font.add_file('OpenSans.ttf')


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._frame = None
        self.geometry('1100x700')
        self.title('National Bank')
        self.iconbitmap('favicon.ico')

        # Theme
        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "light")
        self.style = ttk.Style(self)

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

    def update_size(self):
        self._frame.update()
        width = self._frame.winfo_reqwidth() + 40
        height = self._frame.winfo_height() + 40
        self.minsize(width=width, height=height)


class LoginPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
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
                                   justify='center',
                                   width=30,
                                   show='*')
        entry_password.grid(row=5,
                            column=0,
                            padx=20,
                            sticky='w')
        forgot_label = ttk.Label(login_frame,
                                 text="Forgot your Password?",
                                 font=('Open Sans light', 8))
        forgot_label.grid(row=6,
                          column=0,
                          sticky='e',
                          pady=(0, 15),
                          padx=20)
        forgot_label.bind("<Button-1>",
                          lambda e: master.switch_frame(ForgotPage))

        # Login in
        button_login = ttk.Button(login_frame,
                                  text='SIGN IN',
                                  width=29,
                                  style='Accent.TButton',
                                  command=lambda: Login(master,
                                                        entry_username.get(),
                                                        entry_password.get()))
        button_login.grid(row=7,
                          column=0,
                          padx=20,
                          pady=10,
                          columnspan=2)

        button_register = ttk.Button(login_frame,
                                     text='Register',
                                     width=29,
                                     style='Panel.TButton',
                                     command=lambda: master.switch_frame(RegisterPageStart))
        button_register.grid(row=8,
                             padx=20,
                             pady=(0, 10),
                             columnspan=2)


def Login(master, username, password):
    username = 'js'
    password = '1234'
    global UserID
    # No username and password entered
    if not username:
        messagebox.showerror("Invalid entry", "Username cannot be left blank.\nPlease enter a Username.")
    elif not password:
        messagebox.showerror("Invalid entry", "Password cannot be left blank.\nPlease enter a Password.")

    # Username and password entered
    else:
        db = db_connect()
        db_cursor = db.cursor()
        db_cursor.execute("SELECT username, password, user_id FROM db_atm.tbl_users")
        users = db_cursor.fetchall()
        user_input = password
        user_password = ""

        for user in users:
            if user[0] == username:
                user_input = password  # Fetches the typed password
                user_password = user[1]  # Fetches the correct password
                UserID = user[2]
                # Reason for this is because I do not want an error message running on each unmatched entry

        if user_password == "":
            # Warning message displayed for unmatched entry form db
            messagebox.showerror("Invalid entry", "Username or password is incorrect")
        elif user_input == user_password:
            # Correct input which takes you to the MainMenu frame
            exchangeapi('zar')
            print("user:", username, "pass:", password, 'userID:', UserID)
            fetchUser()
            fetchAccounts()
            fetchTransactions()
            master.switch_frame(MainMenu)
        else:
            # Password is incorrect and does not match username
            messagebox.showerror("Invalid entry", "Username or password is incorrect")

        # You can be specific and tell the user what is wrong with their inputs.
        # The reason I want to leave it ambiguous is, because anybody can guess a username and in the instance
        # where they guess correctly they can attempt to crack the password.
        # (Discuss which approach to follow)


class RegisterPageStart(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # GUI creation
        # Center Widget
        register_frame = ttk.Frame(self)
        register_frame.grid()
        self.image = Image.open('bank_logo.png')
        self.image = self.image.resize((100, 50))
        self.bg_image = ImageTk.PhotoImage(self.image)
        ttk.Label(register_frame, image=self.bg_image).grid(row=0,
                                                            column=0,
                                                            pady=(20, 10),
                                                            padx=20,
                                                            sticky='n')

        # Header Text
        self.header_label = ttk.Label(register_frame,
                                      text='Requirements:', font=('Open Sans', 24))
        self.header_label.grid(row=1,
                               column=0,
                               padx=20,
                               pady=(0, 15),
                               sticky='w')

        # Requirements labels
        req1_label = ttk.Label(register_frame,
                               text='* First name and Last name')
        req1_label.grid(row=2,
                        column=0,
                        sticky='w',
                        padx=20)

        req2_label = ttk.Label(register_frame,
                               text='* Email and Cellphone number')
        req2_label.grid(row=3,
                        column=0,
                        sticky='w',
                        padx=20)

        req3_label = ttk.Label(register_frame,
                               text='* ZA Identification number')
        req3_label.grid(row=4,
                        column=0,
                        sticky='w',
                        padx=20)

        req4_label = ttk.Label(register_frame,
                               text='* Billing address')
        req4_label.grid(row=5,
                        column=0,
                        sticky='w',
                        padx=20)

        req5_label = ttk.Label(register_frame,
                               text='* Strong Username and Password')
        req5_label.grid(row=6,
                        column=0,
                        sticky='w',
                        padx=20)

        # Register button
        button_register = ttk.Button(register_frame,
                                     text='Ok, I Understand',
                                     width=29,
                                     style='Accent.TButton',
                                     command=lambda: master.switch_frame(RegisterPageDetails))
        button_register.grid(row=7,
                             column=0,
                             padx=20,
                             pady=10,
                             columnspan=1)
        # Return button
        button_return = ttk.Button(register_frame,
                                   text='Return to login',
                                   width=29,
                                   style='Panel.TButton',
                                   command=lambda: master.switch_frame(LoginPage))
        button_return.grid(row=8,
                           padx=20,
                           column=0,
                           pady=(0, 10),
                           columnspan=1)


# Register page for name, email, cell
class RegisterPageDetails(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # GUI creation
        # Center Widget
        register_frame = ttk.Frame(self)
        register_frame.grid()
        self.image = Image.open('bank_logo.png')
        self.image = self.image.resize((100, 50))
        self.bg_image = ImageTk.PhotoImage(self.image)
        ttk.Label(register_frame, image=self.bg_image).grid(row=0,
                                                            column=0,
                                                            pady=(20, 10),
                                                            padx=20,
                                                            sticky='n')

        # Header Text
        self.header_label = ttk.Label(register_frame,
                                      text='Input your details', font=('Open Sans', 24))
        self.header_label.grid(row=1,
                               column=0,
                               padx=20,
                               pady=(0, 15),
                               sticky='w',
                               columnspan=2)

        self.step_label = ttk.Label(register_frame,
                                    text='Step 1 of 4', font=('Open Sans', 24))
        self.step_label.grid(row=1,
                             column=2,
                             padx=20,
                             pady=(0, 15),
                             sticky='w', )

        # Input labels and entries
        # First name
        fname_label = ttk.Label(register_frame,
                                text='First name')
        fname_label.grid(row=2,
                         column=0,
                         sticky='w',
                         padx=20)
        entry_fname = ttk.Entry(register_frame,
                                justify='left',
                                width=22,
                                style='Custom.TEntry')
        entry_fname.grid(row=3,
                         column=0,
                         padx=20,
                         pady=(0, 10),
                         sticky='w')

        # Surname
        sname_label = ttk.Label(register_frame,
                                text='Last name')
        sname_label.grid(row=2,
                         column=1,
                         sticky='w',
                         padx=20)
        entry_sname = ttk.Entry(register_frame,
                                justify='left',
                                width=22,
                                style='Custom.TEntry')
        entry_sname.grid(row=3,
                         column=1,
                         padx=20,
                         pady=(0, 10),
                         sticky='w')

        # Email
        email_label = ttk.Label(register_frame,
                                text='E-mail')
        email_label.grid(row=4,
                         column=0,
                         sticky='w',
                         padx=20)
        entry_email = ttk.Entry(register_frame,
                                justify='left',
                                width=22)
        entry_email.grid(row=5,
                         column=0,
                         padx=20,
                         sticky='w',
                         pady=(0, 10))

        # Cell num
        cellnum_label = ttk.Label(register_frame,
                                  text='Contact Number')
        cellnum_label.grid(row=4,
                           column=1,
                           sticky='w',
                           padx=20)
        entry_cellnum = ttk.Entry(register_frame,
                                  justify='left',
                                  width=15)
        entry_cellnum.grid(row=5,
                           column=1,
                           padx=20,
                           sticky='w',
                           pady=(0, 10))

        # Register button
        button_register = ttk.Button(register_frame,
                                     text='Confirm details',
                                     width=20,
                                     style='Accent.TButton',
                                     command=lambda: master.switch_frame(RegisterPageID))
        button_register.grid(row=6,
                             column=2,
                             padx=20,
                             pady=(20, 20),
                             )
        # Return button
        button_return = ttk.Button(register_frame,
                                   text='Previous Page',
                                   width=17,
                                   style='Panel.TButton',
                                   command=lambda: master.switch_frame(RegisterPageStart))
        button_return.grid(row=6,
                           padx=20,
                           column=0,
                           pady=(20, 20),
                           )
        # Cancel button
        button_cancel_register = ttk.Button(register_frame,
                                            text='Cancel Registration',
                                            width=17,
                                            style='Panel.TButton',
                                            command=lambda: master.switch_frame(LoginPage))
        button_cancel_register.grid(row=6,
                                    padx=20,
                                    column=1,
                                    pady=(20, 20),
                                    )


# Register page for id num
class RegisterPageID(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # GUI creation
        # Center Widget
        register_frame = ttk.Frame(self)
        register_frame.grid()
        self.image = Image.open('bank_logo.png')
        self.image = self.image.resize((100, 50))
        self.bg_image = ImageTk.PhotoImage(self.image)
        ttk.Label(register_frame, image=self.bg_image).grid(row=0,
                                                            column=0,
                                                            pady=(20, 10),
                                                            padx=20,
                                                            sticky='n')

        # Header Text
        self.header_label = ttk.Label(register_frame,
                                      text='Identification number', font=('Open Sans', 24))
        self.header_label.grid(row=1,
                               column=0,
                               padx=20,
                               pady=(0, 15),
                               sticky='w',
                               columnspan=2)

        self.step_label = ttk.Label(register_frame,
                                    text='Step 2 of 4', font=('Open Sans', 24))
        self.step_label.grid(row=1,
                             column=2,
                             padx=20,
                             pady=(0, 15),
                             sticky='w', )

        # Input labels and entries
        # ID num
        id_label = ttk.Label(register_frame,
                             text='Identification number')
        id_label.grid(row=2,
                      column=0,
                      sticky='w',
                      padx=20)
        entry_id = ttk.Entry(register_frame,
                             justify='left',
                             width=22,
                             style='Custom.TEntry')
        entry_id.grid(row=3,
                      column=0,
                      padx=20,
                      pady=(0, 10),
                      sticky='w')

        # Register button
        button_register = ttk.Button(register_frame,
                                     text='Confirm ID Number',
                                     width=20,
                                     style='Accent.TButton',
                                     command=lambda: master.switch_frame(RegisterPageAddress))
        button_register.grid(row=6,
                             column=2,
                             padx=20,
                             pady=(20, 20),
                             )
        # Return button
        button_return = ttk.Button(register_frame,
                                   text='Previous Page',
                                   width=17,
                                   style='Panel.TButton',
                                   command=lambda: master.switch_frame(RegisterPageDetails))
        button_return.grid(row=6,
                           padx=20,
                           column=0,
                           pady=(20, 20),
                           )
        # Cancel button
        button_cancel_register = ttk.Button(register_frame,
                                            text='Cancel Registration',
                                            width=17,
                                            style='Panel.TButton',
                                            command=lambda: master.switch_frame(LoginPage))
        button_cancel_register.grid(row=6,
                                    padx=20,
                                    column=1,
                                    pady=(20, 20),
                                    )


# Register page for billing address
class RegisterPageAddress(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # GUI creation
        # Center Widget
        register_frame = ttk.Frame(self)
        register_frame.grid()
        self.image = Image.open('bank_logo.png')
        self.image = self.image.resize((100, 50))
        self.bg_image = ImageTk.PhotoImage(self.image)
        ttk.Label(register_frame, image=self.bg_image).grid(row=0,
                                                            column=0,
                                                            pady=(20, 10),
                                                            padx=20,
                                                            sticky='n')

        # Header Text
        self.header_label = ttk.Label(register_frame,
                                      text='Billing Address', font=('Open Sans', 24))
        self.header_label.grid(row=1,
                               column=0,
                               padx=20,
                               pady=(0, 15),
                               sticky='w',
                               columnspan=2)

        self.step_label = ttk.Label(register_frame,
                                    text='Step 3 of 4', font=('Open Sans', 24))
        self.step_label.grid(row=1,
                             column=2,
                             padx=20,
                             pady=(0, 15),
                             sticky='w', )

        # Input labels and entries
        # Street
        street_label = ttk.Label(register_frame,
                                 text='Address')
        street_label.grid(row=2,
                          column=0,
                          sticky='w',
                          padx=20)
        entry_street = ttk.Entry(register_frame,
                                 justify='left',
                                 width=25,
                                 style='Custom.TEntry')
        entry_street.grid(row=3,
                          column=0,
                          padx=20,
                          pady=(0, 10),
                          sticky='w')

        # City
        city_label = ttk.Label(register_frame,
                               text='City')
        city_label.grid(row=2,
                        column=1,
                        sticky='w',
                        padx=20)
        entry_city = ttk.Entry(register_frame,
                               justify='left',
                               width=15,
                               style='Custom.TEntry')
        entry_city.grid(row=3,
                        column=1,
                        padx=20,
                        pady=(0, 10),
                        sticky='w')

        # Post
        post_label = ttk.Label(register_frame,
                               text='Postal Code')
        post_label.grid(row=4,
                        column=1,
                        sticky='w',
                        padx=20)
        entry_post = ttk.Entry(register_frame,
                               justify='left',
                               width=22,
                               style='Custom.TEntry')
        entry_post.grid(row=5,
                        column=1,
                        padx=20,
                        pady=(0, 10),
                        sticky='w')

        # State
        state_label = ttk.Label(register_frame,
                                text='Province')
        state_label.grid(row=4,
                         column=0,
                         sticky='w',
                         padx=20)

        defualt_state = tk.StringVar()
        defualt_state.set("")
        ddl_state = ttk.OptionMenu(register_frame, defualt_state,
                                   "WC",
                                   "WC",
                                   "EC",
                                   "FS",
                                   "GP",
                                   "KZN",
                                   "NC",
                                   "NW",
                                   "LP",
                                   "MP")
        ddl_state.grid(row=5,
                       column=0,
                       sticky='w',
                       padx=20)

        # Register button
        button_register = ttk.Button(register_frame,
                                     text='Confirm Billing Address',
                                     width=20,
                                     style='Accent.TButton',
                                     command=lambda: master.switch_frame(RegisterPageAuth))
        button_register.grid(row=8,
                             column=2,
                             padx=20,
                             pady=(20, 20),
                             )
        # Return button
        button_return = ttk.Button(register_frame,
                                   text='Previous Page',
                                   width=17,
                                   style='Panel.TButton',
                                   command=lambda: master.switch_frame(RegisterPageID))
        button_return.grid(row=8,
                           padx=20,
                           column=0,
                           pady=(20, 20),
                           )
        # Cancel button
        button_cancel_register = ttk.Button(register_frame,
                                            text='Cancel Registration',
                                            width=17,
                                            style='Panel.TButton',
                                            command=lambda: master.switch_frame(LoginPage))
        button_cancel_register.grid(row=8,
                                    padx=20,
                                    column=1,
                                    pady=(20, 20),
                                    )


# Register page for username and password
class RegisterPageAuth(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # GUI creation
        # Center Widget
        register_frame = ttk.Frame(self)
        register_frame.grid()
        self.image = Image.open('bank_logo.png')
        self.image = self.image.resize((100, 50))
        self.bg_image = ImageTk.PhotoImage(self.image)
        ttk.Label(register_frame, image=self.bg_image).grid(row=0,
                                                            column=0,
                                                            pady=(20, 10),
                                                            padx=20,
                                                            sticky='n')

        # Header Text
        self.header_label = ttk.Label(register_frame,
                                      text='Authentication details', font=('Open Sans', 24))
        self.header_label.grid(row=1,
                               column=0,
                               padx=20,
                               pady=(0, 15),
                               sticky='w',
                               columnspan=2)

        self.step_label = ttk.Label(register_frame,
                                    text='Step 4 of 4', font=('Open Sans', 24))
        self.step_label.grid(row=1,
                             column=2,
                             padx=20,
                             pady=(0, 15),
                             sticky='w', )

        # Input labels and entries
        # Username
        uname_label = ttk.Label(register_frame,
                                text='Username')
        uname_label.grid(row=2,
                         column=0,
                         sticky='w',
                         padx=20)
        entry_username = ttk.Entry(register_frame,
                                   justify='left',
                                   width=22,
                                   style='Custom.TEntry')
        entry_username.grid(row=3,
                            column=0,
                            padx=20,
                            pady=(0, 10),
                            sticky='w')
        #  Password
        pass_label = ttk.Label(register_frame,
                               text='Password')
        pass_label.grid(row=2,
                        column=1,
                        sticky='w',
                        padx=20)
        entry_password = ttk.Entry(register_frame,
                                   justify='left',
                                   width=22,
                                   style='Custom.TEntry',
                                   show="*")
        entry_password.grid(row=3,
                            column=1,
                            padx=20,
                            pady=(0, 10),
                            sticky='w')
        # Register button
        button_register = ttk.Button(register_frame,
                                     text='Confirm Authentication details',
                                     width=30,
                                     style='Accent.TButton',
                                     command=lambda: master.switch_frame(RegisterPageFinal))
        button_register.grid(row=4,
                             column=2,
                             padx=20,
                             pady=(20, 20),
                             )
        # Return button
        button_return = ttk.Button(register_frame,
                                   text='Previous Page',
                                   width=17,
                                   style='Panel.TButton',
                                   command=lambda: master.switch_frame(RegisterPageAddress))
        button_return.grid(row=4,
                           padx=20,
                           column=0,
                           pady=(20, 20),
                           )
        # Cancel button
        button_cancel_register = ttk.Button(register_frame,
                                            text='Cancel Registration',
                                            width=17,
                                            style='Panel.TButton',
                                            command=lambda: master.switch_frame(LoginPage))
        button_cancel_register.grid(row=4,
                                    padx=20,
                                    column=1,
                                    pady=(20, 20),
                                    )


# Registration successful pag
class RegisterPageFinal(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # GUI creation
        # Center Widget
        register_frame = ttk.Frame(self)
        register_frame.grid()
        self.image = Image.open('bank_logo.png')
        self.image = self.image.resize((100, 50))
        self.bg_image = ImageTk.PhotoImage(self.image)
        ttk.Label(register_frame, image=self.bg_image).grid(row=0,
                                                            column=0,
                                                            pady=(20, 10),
                                                            padx=20,
                                                            sticky='n')

        # Header Text
        self.header_label = ttk.Label(register_frame,
                                      text='Your Registration was successful.\n \nPlease use your Username\nand '
                                           'Password to login', font=('Open Sans', 18))
        self.header_label.grid(row=1,
                               column=0,
                               padx=20,
                               pady=(0, 15),
                               sticky='w',
                               columnspan=2)

        # Register button
        button_register = ttk.Button(register_frame,
                                     text='Return to Login Page',
                                     width=40,
                                     style='Accent.TButton',
                                     command=lambda: master.switch_frame(LoginPage))
        button_register.grid(row=6,
                             column=0,
                             padx=20,
                             pady=(20, 20), )


def Register(master):
    print("register")

    """Error handling for registration input values"""


class ForgotPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # GUI creation
        # Center Widget
        forgot_page = ttk.Frame(self)
        forgot_page.grid()

        self.image = Image.open('bank_logo.png')
        self.image = self.image.resize((100, 50))
        self.bg_image = ImageTk.PhotoImage(self.image)
        ttk.Label(forgot_page, image=self.bg_image).grid(row=0,
                                                         column=0,
                                                         pady=(20, 10),
                                                         padx=20,
                                                         sticky='n')

        # Header Text
        self.header_label = ttk.Label(forgot_page,
                                      text='Forgot Password', font=('Open Sans', 20))
        self.header_label.grid(row=1,
                               column=0,
                               padx=20,
                               pady=(0, 15),
                               sticky='w')

        # Input
        username_label = ttk.Label(forgot_page,
                                   text='Username')
        username_label.grid(row=2,
                            column=0,
                            sticky='w',
                            padx=20)
        entry_username = ttk.Entry(forgot_page,
                                   justify='center',
                                   width=30,
                                   style='Custom.TEntry')
        entry_username.grid(row=3,
                            column=0,
                            padx=20,
                            pady=(0, 10),
                            sticky='w')
        password_label = ttk.Label(forgot_page,
                                   text='Password')
        password_label.grid(row=4,
                            column=0,
                            sticky='w',
                            padx=20,
                            pady=(10, 0))
        entry_password = ttk.Entry(forgot_page,
                                   justify='center',
                                   width=30,
                                   show='*')
        entry_password.grid(row=5,
                            column=0,
                            padx=20,
                            sticky='w')
        vpassword_label = ttk.Label(forgot_page,
                                    text='Re-enter Password')
        vpassword_label.grid(row=6,
                             column=0,
                             sticky='w',
                             padx=20,
                             pady=(10, 0))
        vpassword_entry = ttk.Entry(forgot_page,
                                    justify='center',
                                    width=30,
                                    show='*')
        vpassword_entry.grid(row=7,
                             column=0,
                             padx=20,
                             pady=(0, 10),
                             sticky='w')

        # Save Pass
        button_save = ttk.Button(forgot_page,
                                 text='Save Password',
                                 width=29,
                                 style='Accent.TButton',
                                 command=lambda: ForgotPass(master,
                                                            entry_username.get(),
                                                            entry_password.get(),
                                                            vpassword_entry.get()))
        button_save.grid(row=8,
                         column=0,
                         padx=20,
                         pady=10,
                         columnspan=2)
        button_back = ttk.Button(forgot_page,
                                 text='Back',
                                 width=29,
                                 style='Panel.TButton',
                                 command=lambda: master.switch_frame(LoginPage))
        button_back.grid(row=9,
                         column=0,
                         padx=20,
                         pady=(0, 10),
                         columnspan=2)


def ForgotPass(master, username, password, vpassword):
    if not username:
        messagebox.showerror("Invalid entry", "Username cannot be left blank.\nPlease enter a Username.")
    elif not (password == vpassword):
        messagebox.showerror("Invalid entry", "Passwords do not match.\nPlease enter a Password.")
    else:
        db = db_connect()
        db_cursor = db.cursor()
        sql = "SELECT username, password, user_id FROM db_atm.tbl_users WHERE username = %s"
        val = (username,)
        db_cursor.execute(sql, val)
        user = db_cursor.fetchall()
        print(user)
        if not user:
            messagebox.showerror('', '')
        # for user in users:
        #     if user[0] == username:
        #         user_input = password  # Fetches the typed password
        #         user_password = user[1]  # Fetches the correct password
        # if user_password == "":
        #     # Warning message displayed for unmatched entry form db
        #     messagebox.showerror("Invalid entry", "Username or password is incorrect")
        # elif user_input == user_password:
        #     # Correct input which takes you to the MainMenu frame
        #     exchangeapi('zar')
        #     print("user:", username, "pass:", password, 'userID:', UserID)
        #     fetchUser()
        #     fetchAccounts()
        #     fetchTransactions()
        #     master.switch_frame(MainMenu)
        # else:
        #     # Password is incorrect and does not match username
        #     messagebox.showerror("Invalid entry", "Username or password is incorrect")


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

        self.header_panel = ttk.Panedwindow(self.left_panel,
                                            height=150)
        self.header_panel.pack(side='top', fill='x')
        self.header_panel.pack_propagate(False)
        self.image = Image.open('bank_logo.png')
        self.image = self.image.resize((100, 50))
        self.bg_image = ImageTk.PhotoImage(self.image)
        ttk.Label(self.header_panel, image=self.bg_image).pack(side='top',
                                                               padx=20,
                                                               pady=(10, 0))
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
        # MainMenu.update(self)
        # print(self.winfo_reqwidth(), self.winfo_reqheight())


class AccountsPanel(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # Gui Creation
        self.accounts_panel = ttk.Frame(self,
                                        width=800,
                                        height=600,
                                        style="Card.TFrame")
        self.accounts_panel.grid()
        self.accounts_panel.grid_propagate(False)
        self.left_panel = ttk.Frame(self.accounts_panel,
                                    style='Card.TFrame',
                                    width=500,
                                    height=600)
        self.left_panel.grid(row=0, column=0)
        self.left_panel.grid_propagate(False)
        ttk.Label(self.left_panel, text="Your balance").grid(column=0,
                                                             row=0,
                                                             padx=30,
                                                             pady=(30, 0),
                                                             sticky='w')

        # Total account balance
        total = 0
        for a in AccountsData:
            total += a[1]
        self.balance_label = ttk.Label(self.left_panel,
                                       text="R {:,.2f}".format(total),
                                       font=('Open Sans', 20))
        self.balance_label.grid(column=0,
                                row=1,
                                sticky='w',
                                padx=35,
                                columnspan=1,
                                pady=(0, 10))

        # Foregin exchange frame
        self.exchange_frame = ttk.Frame(self.accounts_panel,
                                        width=300,
                                        height=600, )
        self.exchange_frame.grid(column=2,
                                 row=0,
                                 sticky='e')
        self.exchange_frame.grid_propagate(False)
        ttk.Label(self.exchange_frame,
                  text='Foreign Exchange',
                  font=('Open Sans', 14),
                  justify='center').grid(column=0,
                                         columnspan=2,
                                         row=0,
                                         padx=(70, 0),
                                         pady=(20, 10),
                                         sticky='news')
        self.list = tk.Listbox(self.exchange_frame,
                               font=('Open Sans', 10),
                               borderwidth=0,
                               width=15, justify='right')
        self.list.grid(column=0,
                       row=1,
                       sticky='n',
                       padx=(50, 10))
        self.list.insert(1, f'China')
        self.list.insert(2, f'Japan')
        self.list.insert(3, f'Switzerland')
        self.list.insert(4, f'Russia')
        self.list.insert(5, f'India')
        self.list.insert(6, f'Taiwan')
        self.list.insert(7, f'Hong Kong')
        self.list.insert(8, f'Saudi Arabia')
        self.list.insert(9, f'South Korea')
        self.list.insert(10, f'Singapore')
        self.exchange_list = tk.Listbox(self.exchange_frame,
                                        font=('Open Sans', 10),
                                        borderwidth=0,
                                        width=10)
        self.exchange_list.grid(column=1,
                                row=1,
                                sticky='n',
                                ipadx=5)
        if len(exchange_data) > 0:
            self.exchange_list.insert(1, exchange_data[0])
            self.exchange_list.insert(2, exchange_data[1])
            self.exchange_list.insert(3, exchange_data[2])
            self.exchange_list.insert(4, exchange_data[3])
            self.exchange_list.insert(5, exchange_data[4])
            self.exchange_list.insert(6, exchange_data[5])
            self.exchange_list.insert(7, exchange_data[6])
            self.exchange_list.insert(8, exchange_data[7])
            self.exchange_list.insert(9, exchange_data[8])
            self.exchange_list.insert(10, exchange_data[9])
        else:
            raise SystemExit
        self.exchange_list.bindtags(('', 'all'))
        self.list.bindtags(('', 'all'))

        # Recent transactions
        ttk.Label(self.left_panel,
                  text='Recent Transactions',
                  font=('Open Sans', 14)).grid(row=2,
                                               columnspan=2)
        self.tag_panel = ttk.Frame(self.left_panel, style="Card.TFrame")
        self.tag_panel.grid(row=3, column=0, padx=30, pady=(0, 20))
        tags = len(TransactionData)
        if tags > 10:
            tags = 10
        for a in range(0, tags):
            frame = ttk.Frame(self.tag_panel,
                              # style='Card.TFrame',
                              width=700,
                              height=30)
            frame.pack(side='top',
                       fill='x',
                       padx=1,
                       pady=1)
            frame.pack_propagate(False)
            title = ttk.Label(frame, text=TransactionData[a][1], font=('Open Sans', 10), width=25)
            title.grid(row=0,
                       column=0,
                       sticky='news',
                       padx=10,
                       pady=10)
            date = ttk.Label(frame,
                             text=TransactionData[a][3],
                             width=20,
                             font=('Open Sans Light', 8))
            date.grid(row=0,
                      column=1,
                      sticky='e',
                      padx=10,
                      pady=10)
            value = ttk.Label(frame,
                              text="R {:,.2f}".format((TransactionData[a][2])),
                              width=10,
                              font=('Open Sans', 10))
            value.grid(row=0,
                       column=2,
                       sticky='e',
                       padx=10,
                       pady=10)


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
        self.payments_panel = ttk.Frame(self,
                                        style='Card.TFrame')
        self.payments_panel.grid()
        self.canvas = tk.Canvas(self.payments_panel,
                                width=500,
                                height=590,
                                borderwidth=0)
        self.frame = ttk.Frame(self.canvas)
        self.scrollbard = ttk.Scrollbar(self.payments_panel,
                                        orient='vertical',
                                        command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbard.set)
        self.right_panel = ttk.Frame(self.payments_panel,
                                     style='Card.TFrame',
                                     width=284,
                                     height=600)
        self.right_panel.pack(side='right')
        self.scrollbard.pack(side='right',
                             fill='y',
                             pady=2)
        self.canvas.pack(side='left',
                         fill='both',
                         expand=True,
                         pady=1,
                         padx=1)
        self.canvas.create_window((1, 1),
                                  window=self.frame,
                                  anchor='nw',
                                  tags='self.frame')
        self.frame.bind('<Configure>',
                        self.onFrameConfigure)
        self.header = ttk.Frame(self.frame)
        self.header.pack(side='top')
        self.pay_button = ttk.Button(self.header,
                                     text='Pay')
        self.pay_button.grid(row=0,
                             column=0,
                             padx=10,
                             pady=40,
                             sticky='e')
        self.transfer_button = ttk.Button(self.header,
                                          text='Transfer')
        self.transfer_button.grid(row=0,
                                  column=1,
                                  padx=10,
                                  pady=40,
                                  sticky='w')
        ttk.Label(self.header,
                  text='Transactions',
                  font=('Open Sans Bold', 14)).grid(row=1,
                                                    column=0,
                                                    columnspan=2,
                                                    padx=188)
        self.populate()

    def populate(self):
        tags = len(TransactionData)
        if tags > 30:
            tags = 30
        for a in range(0, tags):
            receipt = ttk.Frame(self.frame, width=100, height=20)
            receipt.pack(side='top',
                         fill='x',
                         expand=True,
                         padx=20,
                         pady=10)
            title = ttk.Label(receipt,
                              text=TransactionData[a][1],
                              font=('Open Sans', 10),
                              width=25)
            title.grid(row=0,
                       column=0,
                       sticky='w',
                       padx=10,
                       pady=10)
            date = ttk.Label(receipt,
                             text=TransactionData[a][3],
                             width=20,
                             font=('Open Sans Light', 8))
            date.grid(row=0,
                      column=1,
                      sticky='e',
                      padx=20,
                      pady=10)
            value = ttk.Label(receipt,
                              text="R {:,.2f}".format(TransactionData[a][2]),
                              width=10,
                              font=('Open Sans', 10))
            value.grid(row=0,
                       column=2,
                       sticky='e',
                       padx=20,
                       pady=10)

    def onFrameConfigure(self, x):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))


def db_connect():
    # Connecting to the database is set as a method since we need to open and close it for different transactions
    # Error handling code:
    # https://docs.oracle.com/cd/E17952_01/connector-python-en/connector-python-example-connecting.html
    # Start of borrowed code
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            # password='12345678',
            password="toor",
            port="3306"
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


def exchangeapi(currency):
    url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/' + currency + '.json'
    try:
        r = requests.get(url=url, timeout=1)
        data = r.json()[currency]
        exchange_data.append("{:.3f}".format(data['cny']))
        exchange_data.append("{:.3f}".format(data['jpy']))
        exchange_data.append("{:.3f}".format(data['chf']))
        exchange_data.append("{:.3f}".format(data['rub']))
        exchange_data.append("{:.3f}".format(data['inr']))
        exchange_data.append("{:.3f}".format(data['twd']))
        exchange_data.append("{:.3f}".format(data['hkd']))
        exchange_data.append("{:.3f}".format(data['sar']))
        exchange_data.append("{:.3f}".format(data['krw']))
        exchange_data.append("{:.3f}".format(data['sgd']))
        exchange_data.append("{:.3f}".format(data['usd']))
        exchange_data.append("{:.3f}".format(data['gbp']))
    except requests.exceptions.ConnectionError:
        messagebox.showerror('No Connection', 'Make sure you have a stable internet connection then try again')
    except requests.exceptions.ReadTimeout:
        messagebox.showerror('Connection Timeout', 'Connection timed out\nPlease try again later.')


def fetchUser():
    global UserData
    db = db_connect()
    db_cursor = db.cursor()
    sql = "SELECT * FROM db_atm.tbl_users WHERE user_id = %s"
    adr = (UserID,)
    db_cursor.execute(sql, adr)
    UserData = db_cursor.fetchall()


def fetchTransactions():
    global TransactionData
    db = db_connect()
    db_cursor = db.cursor()
    sql = "SELECT * FROM db_atm.tbl_transactions WHERE tbl_accounts_tbl_users_user_id = %s"
    adr = (UserID,)
    db_cursor.execute(sql, adr)
    TransactionData = sorted(db_cursor.fetchall(), key=lambda x: x[3], reverse=True)


def fetchAccounts():
    global AccountsData
    db = db_connect()
    db_cursor = db.cursor()
    sql = "SELECT * FROM db_atm.tbl_accounts WHERE tbl_users_user_id = %s"
    adr = (UserID,)
    db_cursor.execute(sql, adr)
    AccountsData = db_cursor.fetchall()
    x = len(AccountsData)
    # dcs
    # 012
    for y in range(0, x):
        if AccountsData[y][3] == 'd':
            CardType[0] = AccountsData[y][0]
        elif AccountsData[y][3] == 'c':
            CardType[1] = AccountsData[y][0]
        else:
            CardType[2] = AccountsData[y][0]


if __name__ == "__main__":
    root = Application()
    root.mainloop()
