"""
                                        ============================
                                        |  Python ATM Application  |
                                        ============================
"""
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import pyglet
import requests
# import http.client as httplib
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import errorcode
import re
import datetime
from datetime import date
import luhn_validator
from threading import Thread

Version = 'v1.0822'
exchange_data = ['', '', '', '', '', '', '', '', '', '', '', '']
UserID = ''
UserData = []
TransactionData = []
AccountsData = []
CardType = []
pyglet.font.add_file('theme/OpenSans.ttf')
Reg_details = ["", "", "", ""]
Reg_id = ""
Reg_address = ["", "", "WC", ""]  # Leave WC as the default value || Used to populate a listbox
Reg_auth = ["", ""]
BankLogo = ImageTk.PhotoImage
latestTime = datetime


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._frame = None
        self.geometry('1100x700')
        self.title('National Bank')
        self.iconbitmap('theme/favicon.ico')

        # Theme
        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "light")
        self.style = ttk.Style(self)

        # background image
        width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.image = Image.open('theme/background.jpg')
        self.image = self.image.resize((width, height))
        self.bg_image = ImageTk.PhotoImage(self.image)
        ttk.Label(self, image=self.bg_image).place(relx=.5,
                                                   rely=.5,
                                                   anchor='center')
        # Thread
        background = backgroundTime()
        background.start()
        monitor_time(self, background)
        api = liveAPI()
        api.start()
        monitor_exchange(self, api)

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


def monitor_time(self, thread):
    if thread.is_alive():
        self.after(10, lambda: monitor_time(self, thread))
    else:
        self.after(10, lambda: monitor_time(self, thread))
        # if not thread.run():
        #     if (not str(self._frame) == '.!loginpage'):
        #         print(self._frame)
        #         self.switch_frame(LoginPage)
        #         messagebox.showerror('Connection Lost', 'Please try logging in again')

def monitor_exchange(self, thread):
    if thread.is_alive():
        self.after(3000, lambda: monitor_exchange(self, thread))
    else:
        if not exchange_data == ['', '', '', '', '', '', '', '', '', '', '', '']:
            self.after(600000, lambda: monitor_exchange(self, thread))
            thread.run()
        else:
            self.after(1000, lambda: monitor_exchange(self, thread))
            thread.run()


class backgroundTime(Thread):
    def __init__(self):
        super().__init__()
        # self.count = 9

    def run(self):
        # self.count += 1
        global latestTime
        # connected = True
        latestTime = datetime.datetime.now().strftime("%H:%M:%S")
        # if self.count == 200:
        #     self.count = 0
        #     con = httplib.HTTPSConnection('8.8.8.8', timeout=1)
        #     try:
        #         con.request('HEAD', '/')
        #     except Exception as e:
        #         print(e)
        #         connected = False
        #     finally:
        #         con.close()
        # return connected


class LoginPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        global BankLogo
        # GUI creation
        # Center Widget
        login_frame = ttk.Frame(self)
        self.image = Image.open('theme/bank_logo.png')
        self.image = self.image.resize((100, 50))
        BankLogo = ImageTk.PhotoImage(self.image)
        ttk.Label(login_frame, image=BankLogo).grid(row=0,
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
                                  command=lambda: login_check(master, entry_username.get(), entry_password.get()))
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
        login_frame.grid()


def login_check(master, username, password):
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
            if not exchange_data == ['', '', '', '', '', '', '', '', '', '', '', '']:
                fetchUser()
                fetchAccounts()
                fetchTransactions()
                master.switch_frame(MainMenu)
            else:
                messagebox.showerror('No Connection', 'Make sure you have a stable internet connection then try again')
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
        ttk.Label(register_frame, image=BankLogo).grid(row=0,
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
                               text='* ZA Identification number-\n\t(18 years or older)')
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
                        pady=(0, 20),
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
        register_frame.grid()


# Register page for name, email, cell   [Remember to remove redundant self.'s][Was testing something ;)]
class RegisterPageDetails(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        global Reg_details

        # GUI creation
        # Center Widget
        register_frame = ttk.Frame(self)
        ttk.Label(register_frame, image=BankLogo).grid(row=0,
                                                       column=0,
                                                       pady=(20, 10),
                                                       padx=20,
                                                       sticky='n')

        # Header Text
        header_label = ttk.Label(register_frame,
                                 text='Input your details', font=('Open Sans', 24))
        header_label.grid(row=1,
                          column=0,
                          padx=20,
                          pady=(0, 15),
                          sticky='w',
                          columnspan=2)

        step_label = ttk.Label(register_frame,
                               text='Step 1 of 4', font=('Open Sans', 24))
        step_label.grid(row=1,
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
        entry_fname.focus_set()
        entry_fname.insert(0, Reg_details[0])

        # Surname
        sname_label = ttk.Label(register_frame,
                                text='Last name',
                                )
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

        entry_sname.insert(0, Reg_details[1])

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
        entry_email.insert(0, Reg_details[2])

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

        entry_cellnum.insert(0, Reg_details[3])

        # Register button
        button_register = ttk.Button(register_frame,
                                     text='Confirm details',
                                     width=20,
                                     style='Accent.TButton',
                                     command=lambda: details_error_check(master, entry_fname.get(),
                                                                         entry_sname.get(),
                                                                         entry_email.get(),
                                                                         entry_cellnum.get()))
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
                                            command=lambda: cancel_register(master))
        button_cancel_register.grid(row=6,
                                    padx=20,
                                    column=1,
                                    pady=(20, 20),
                                    )
        register_frame.grid()


# Register page for id num
class RegisterPageID(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        global Reg_id
        # GUI creation
        # Center Widget
        register_frame = ttk.Frame(self)
        # register_frame.grid()
        ttk.Label(register_frame, image=BankLogo).grid(row=0,
                                                       column=0,
                                                       pady=(20, 10),
                                                       padx=20,
                                                       sticky='n')

        # Header Text
        header_label = ttk.Label(register_frame,
                                 text='Identification number', font=('Open Sans', 24))
        header_label.grid(row=1,
                          column=0,
                          padx=20,
                          pady=(0, 15),
                          sticky='w',
                          columnspan=2)

        step_label = ttk.Label(register_frame,
                               text='Step 2 of 4', font=('Open Sans', 24))
        step_label.grid(row=1,
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

        entry_id.insert(0, Reg_id)
        entry_id.focus_set()
        # Register button
        button_register = ttk.Button(register_frame,
                                     text='Confirm ID Number',
                                     width=20,
                                     style='Accent.TButton',
                                     command=lambda: id_error_check(master, entry_id.get()))
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
                                            command=lambda: cancel_register(master))
        button_cancel_register.grid(row=6,
                                    padx=20,
                                    column=1,
                                    pady=(20, 20),
                                    )
        register_frame.grid()


# Register page for billing address
class RegisterPageAddress(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # GUI creation
        # Center Widget
        register_frame = ttk.Frame(self)
        # register_frame.grid()
        ttk.Label(register_frame, image=BankLogo).grid(row=0,
                                                       column=0,
                                                       pady=(20, 10),
                                                       padx=20,
                                                       sticky='n')

        # Header Text
        header_label = ttk.Label(register_frame,
                                 text='Billing Address', font=('Open Sans', 24))
        header_label.grid(row=1,
                          column=0,
                          padx=20,
                          pady=(0, 15),
                          sticky='w',
                          columnspan=2)

        step_label = ttk.Label(register_frame,
                               text='Step 3 of 4', font=('Open Sans', 24))
        step_label.grid(row=1,
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
        entry_street.insert(0, Reg_address[0])
        entry_street.focus_set()
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
        entry_city.insert(0, Reg_address[1])

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
        entry_post.insert(0, Reg_address[3])

        # State
        state_label = ttk.Label(register_frame,
                                text='Province')
        state_label.grid(row=4,
                         column=0,
                         sticky='w',
                         padx=20)

        default_state = tk.StringVar()
        default_state.set("Select an option")
        provinces_list = ["WC", "EC", "FS", "GP", "KZN", "NC", "NW", "LP", "MP"]
        ddl_state = tk.OptionMenu(register_frame, default_state, *provinces_list)
        ddl_state.grid(row=5,
                       column=0,
                       sticky='w',
                       padx=20)

        # Register button
        button_register = ttk.Button(register_frame,
                                     text='Confirm Billing Address',
                                     width=20,
                                     style='Accent.TButton',
                                     command=lambda: address_error_check(master, entry_street.get(),
                                                                         entry_city.get(), default_state.get(),
                                                                         entry_post.get()))
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
                                            command=lambda: cancel_register(master))
        button_cancel_register.grid(row=8,
                                    padx=20,
                                    column=1,
                                    pady=(20, 20),
                                    )
        register_frame.grid()


# Register page for username and password
class RegisterPageAuth(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # GUI creation
        # Center Widget
        register_frame = ttk.Frame(self)
        # register_frame.grid()
        ttk.Label(register_frame, image=BankLogo).grid(row=0,
                                                       column=0,
                                                       pady=(20, 10),
                                                       padx=20,
                                                       sticky='n')

        # Header Text
        header_label = ttk.Label(register_frame,
                                 text='Authentication details', font=('Open Sans', 24))
        header_label.grid(row=1,
                          column=0,
                          padx=20,
                          pady=(0, 15),
                          sticky='w',
                          columnspan=2)

        step_label = ttk.Label(register_frame,
                               text='Step 4 of 4', font=('Open Sans', 24))
        step_label.grid(row=1,
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

        entry_username.focus_set()
        entry_username.insert(0, Reg_auth[0])

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

        entry_password.insert(0, Reg_auth[1])
        # Register button
        button_register = ttk.Button(register_frame,
                                     text='Confirm Authentication details',
                                     width=30,
                                     style='Accent.TButton',
                                     command=lambda: auth_error_check(master, entry_username.get(),
                                                                      entry_password.get()))

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
                                            command=lambda: cancel_register(master))
        button_cancel_register.grid(row=4,
                                    padx=20,
                                    column=1,
                                    pady=(20, 20),
                                    )
        register_frame.grid()


# Registration successful page
class RegisterPageFinal(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        register_insert()
        # GUI creation
        # Center Widget
        register_frame = ttk.Frame(self)
        # register_frame.grid()
        ttk.Label(register_frame, image=BankLogo).grid(row=0,
                                                       column=0,
                                                       pady=(20, 10),
                                                       padx=20,
                                                       sticky='n')
        # Header Text
        header_label = ttk.Label(register_frame,
                                 text='Your Registration was successful.\n \nPlease use your Username\nand '
                                      'Password to login.', font=('Open Sans', 18))

        header_label.grid(row=1,
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
                                     command=lambda: cancel_register(master))
        button_register.grid(row=6,
                             column=0,
                             padx=20,
                             pady=(20, 20), )
        register_frame.grid()


"Error handling for registration input values"


def details_error_check(master, fname, sname, email, cell):
    global Reg_details
    Reg_details = []
    check = [False, False, False, False]
    if fname and sname and email and cell:
        # Fname check
        if not len(fname) > 45:
            # Allows all letters, spaces and hyphens
            if re.match('^[A-zÀ-ÿ- ]*$', fname):
                Reg_details.append(fname.capitalize())
                check[0] = True
            else:
                messagebox.showerror("Invalid First name entry",
                                     "No numbers or special characters allowed in First name field.")
        else:
            messagebox.showerror("Invalid First name entry",
                                 "First name must be less than 45 characters.")
        # Sname check
        if not len(sname) > 45:
            # Allows all letters, spaces and hyphens
            if re.match('^[A-zÀ-ÿ- ]*$', sname):
                Reg_details.append(sname.capitalize())
                check[1] = True
            else:
                messagebox.showerror("Invalid Last name entry",
                                     "No numbers or special characters allowed in Last name field.")
        else:
            messagebox.showerror("Invalid Last name entry",
                                 "Last name must be less than 45 characters.")
        # Email check
        if not len(fname) > 45:
            # Regex for email allows one @ and one dot (.co.za will not work)
            # elif re.match('^[a-z0-9] + [\._] ? [a-z0-9] + [@]\w + [.] \w{2,3}$', email):
            if re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
                Reg_details.append(email)
                check[2] = True
            else:
                messagebox.showerror("Invalid Email entry",
                                     "Try using a valid email address.\n[Example: name_surname@mail.com]")
        else:
            messagebox.showerror("Invalid Email name entry",
                                 "Email must be less than 45 characters.")
        # Cellphone number check
        if cell.isdigit():
            if len(cell) == 10:
                Reg_details.append(cell)
                check[3] = True
            else:
                messagebox.showerror("Invalid Contact number entry",
                                     "Contact number must be 10 digits.")
        else:
            messagebox.showerror("Invalid Contact number entry",
                                 "Contact number can only contain digits.")

        master.switch_frame(RegisterPageID)
    else:
        messagebox.showerror("Missing field(s)",
                             "Please ensure that no field(s) is/are left blank.")

    if check[0] and check[1] and check[2] and check[3]:
        master.switch_frame(RegisterPageID)


def id_error_check(master, inputid):
    global Reg_id
    Reg_id = ""

    # Check if id is blank
    if inputid:

        # checks if the id is made up of digits only
        if not inputid.isdigit():
            messagebox.showerror("Invalid ID entry",
                                 "ID field can only contain digits.\n "
                                 "[Example: 9202204645082]")
        # Check if the size of the id is valid
        elif len(inputid) != 13:
            messagebox.showerror("Invalid ID entry",
                                 "Please ensure that the ID field is 13 digits.\n "
                                 "[Example: 9202204645082]")
        # Check if the date is valid
        elif not id_date_check(inputid):
            messagebox.showerror("Invalid ID entry",
                                 "Please ensure that the first 6 digits of the ID is a valid birth date.\n "
                                 "Remember, you must be 18 years or older to register.\n"
                                 "[Example: 9202204645082]")
        # Check if the 11th digit is valid
        elif inputid[10] != "1" and inputid[10] != "0":
            messagebox.showerror("Invalid ID entry",
                                 "The 11th digit can only be 0 or 1.\n"
                                 "0: SA citizen.\n"
                                 "1: Permanent resident\n"
                                 "[Example: 9202204645082]")

        # Checksum digit check just to ensure that the ID is valid
        elif luhn_validator.validate(inputid):
            Reg_id = inputid
        else:
            messagebox.showerror("Invalid ID entry",
                                 "Please ensure that the ID field was correctly entered\n"
                                 "[Example: 9202204645082]")

    if Reg_id:
        master.switch_frame(RegisterPageAddress)


def id_date_check(inputid):
    str_date = ""
    for x in range(len(inputid) - 7):  # Populates list with the first six digits of the ID
        str_date = str_date + inputid[x]

    year = int(str_date[0] + str_date[1])
    month = int(str_date[2] + str_date[3])
    day = int(str_date[4] + str_date[5])

    if year >= 23:
        year += 1900  # Places the year value into 1900 range.
        # Anyone older than 99 from this year 2022 will be classified as well.
        # Someone older than 99 in the year 2022 cannot be registered. :(
    else:
        year += 2000  # Places the year value into the 2000 range
    if int(date.today().year) - 18 <= year:  # If the year value is in the range of 18 years from the current year,
        # it becomes invalid
        return False
    try:
        datetime.date(year, month, day)  # Checks if the date is a valid date
        return True
    except ValueError:
        return False


def address_error_check(master, street, city, state, post):
    global Reg_address
    Reg_address = []
    check = [False, False, False, False]
    if street and city and state and post:

        # Street check
        if len(street) > 45:
            messagebox.showerror("Invalid Street entry",
                                 "Street must be less than 45 characters.")
            # Allows letter and spaces and numbers in street field
        elif not re.match('^[a-zA-z0-9 ]*$', street):
            messagebox.showerror("Invalid Street entry",
                                 "No special characters allowed in Street field.")
        else:
            Reg_address.append(street)
            check[0] = True

        # City check
        if len(city) > 45:
            messagebox.showerror("Invalid city entry",
                                 "City must be less than 45 characters.")

            # Allows letter and spaces in city field
        elif not re.match('^[a-zA-Z ]*$', city):
            messagebox.showerror("Invalid City entry",
                                 "No special characters or numbers allowed in City field.")
        else:
            Reg_address.append(city.capitalize())
            check[1] = True

        # Checks if the user changed the default state of the option menu
        if not state == "Select an option":
            Reg_address.append(state)
            check[2] = True
        else:
            messagebox.showerror("No State selected",
                                 "Click on the drop down list to select your state.")

        # Postal number check
        if not post.isdigit():
            messagebox.showerror("Invalid Postal code entry",
                                 "Postal code may only consist of digits.")
        elif len(post) != 4:
            messagebox.showerror("Invalid Postal code entry",
                                 "Postal code may only consist of 4 digits.")
        else:
            Reg_address.append(post)
            check[3] = True

    else:
        messagebox.showerror("Missing field(s)",
                             "Please ensure that no field(s) is/are left blank.")

    if check[0] and check[1] and check[2] and check[3]:
        master.switch_frame(RegisterPageAuth)


def auth_error_check(master, username, password):
    global Reg_auth
    Reg_auth = []
    check = [False, False]
    if username and password:

        if not len(username) > 45:
            # Allows letters, numbers and underscore in username. No special characters or spaces
            if re.match('^[A-z0-9_ ]*$', username):
                db = db_connect()
                db_cur = db.cursor()
                sql = "SELECT username FROM db_atm.tbl_users WHERE username = %s"
                val = (username,)
                db_cur.execute(sql, val)
                db_username = db_cur.fetchone()
                if not db_username:
                    Reg_auth.append(username)
                    check[0] = True
                else:
                    messagebox.showerror("Invalid Username entry",
                                         "Username already in use\n Please try a different username."
                                         "\n[Example: tony_stark7])")
            else:
                messagebox.showerror("Invalid Username entry",
                                     "No special characters or spaces allowed in Username entry."
                                     "\n[Example: tony_stark7])")

        else:
            messagebox.showerror("Invalid Username entry",
                                 "Username must be less than 45 characters.")

        if len(password) > 45:
            messagebox.showerror("Invalid Password entry",
                                 "Password must be less than 45 characters.")

        # Password must be 8 or more characters
        elif len(password) < 8:
            messagebox.showerror("Invalid Password entry",
                                 "Password must be 8 or more characters long")

        elif not re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password):
            messagebox.showerror("Invalid Password entry",
                                 "Password must contain:\n"
                                 "* an uppercase letter\n"
                                 "* a lowercase letter\n"
                                 "* a numeric character\n"
                                 "* a special character")
        else:
            Reg_auth.append(password)
            check[1] = True

    else:
        messagebox.showerror("Missing field(s)",
                             "Please ensure that no field(s) is/are left blank.")

    if check[0] and check[1]:
        master.switch_frame(RegisterPageFinal)


def register_insert():
    db = db_connect()
    db_cursor = db.cursor()
    sql = "INSERT INTO db_atm.tbl_users " \
          "(fname, sname, street , city, state, post, cell_num, email, id_num, username, password )" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    val = (Reg_details[0], Reg_details[1], Reg_address[0], Reg_address[1], Reg_address[2], Reg_address[3],
           Reg_details[3], Reg_details[2], Reg_id, Reg_auth[0], Reg_auth[1])
    db_cursor.execute(sql, val)
    acc_id = db_cursor.lastrowid
    sql = "INSERT INTO db_atm.tbl_accounts " \
          "(acc_balance, date_created, acc_type, tbl_users_user_id, credit_due)" \
          "VALUES (%s, %s, %s, %s, %s);"
    val = (float(0), datetime.date.today(), 'd', acc_id, float(0))
    db_cursor.execute(sql, val)
    db.commit()
    db.close()


def cancel_register(master):
    """
    :type master: Misc | None
    """
    # Variables made empty with the intention of clearing the values from the registration page entries
    global Reg_details, Reg_id, Reg_address, Reg_auth
    Reg_details = ["", "", "", ""]
    Reg_id = ""
    Reg_address = ["", "", "WC", ""]
    Reg_auth = ["", ""]
    master.switch_frame(LoginPage)


class ForgotPage(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # GUI creation
        # Center Widget
        forgot_page = ttk.Frame(self)
        ttk.Label(forgot_page, image=BankLogo).grid(row=0,
                                                    column=0,
                                                    pady=20,
                                                    padx=20)
        # Header Text
        self.header_label = ttk.Label(forgot_page,
                                      text='Forgot Password',
                                      font=('Open Sans', 20))
        self.header_label.grid(row=1,
                               column=0,
                               padx=20,
                               pady=10,
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
        email_label = ttk.Label(forgot_page,
                                text='Email')
        email_label.grid(row=4,
                         column=0,
                         sticky='w',
                         padx=20)
        entry_email = ttk.Entry(forgot_page,
                                justify='center',
                                width=30,
                                style='Custom.TEntry')
        entry_email.grid(row=5,
                         column=0,
                         padx=20,
                         pady=(0, 10),
                         sticky='w')
        password_label = ttk.Label(forgot_page,
                                   text='New Password')
        password_label.grid(row=2,
                            column=1,
                            sticky='w',
                            padx=20,
                            pady=(10, 0))
        entry_password = ttk.Entry(forgot_page,
                                   justify='center',
                                   width=30,
                                   show='*')
        entry_password.grid(row=3,
                            column=1,
                            padx=20,
                            sticky='w')
        vpassword_label = ttk.Label(forgot_page,
                                    text='Re-enter Password')
        vpassword_label.grid(row=4,
                             column=1,
                             sticky='w',
                             padx=20,
                             pady=(10, 0))
        vpassword_entry = ttk.Entry(forgot_page,
                                    justify='center',
                                    width=30,
                                    show='*')
        vpassword_entry.grid(row=5,
                             column=1,
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
                                                            vpassword_entry.get(),
                                                            entry_email.get()))
        button_save.grid(row=6,
                         column=1,
                         padx=20,
                         pady=10)
        button_back = ttk.Button(forgot_page,
                                 text='Back',
                                 width=29,
                                 command=lambda: master.switch_frame(LoginPage))
        button_back.grid(row=6,
                         column=0,
                         padx=20,
                         pady=10)
        forgot_page.pack()


def ForgotPass(master, username, password, vpassword, email):
    if not username:
        messagebox.showerror("Invalid entry", "Username cannot be left blank.\nPlease enter a Username.")
    elif not (password == vpassword):
        messagebox.showerror("Invalid entry", "Passwords do not match.\nPlease enter a Password.")
    elif not password:
        messagebox.showerror('Invalid Entry', 'Password cannot be left blank\nPlease enter a password')
    elif not email:
        messagebox.showerror('Invalid Entry', 'Email cannot be left blank.\nPlease enter an email')
    else:
        db = db_connect()
        db_cursor = db.cursor()
        sql = "SELECT username, password, user_id, email FROM db_atm.tbl_users WHERE username = %s"
        val = (username,)
        db_cursor.execute(sql, val)
        user = db_cursor.fetchone()
        if not user:
            messagebox.showerror('Invalid Entry', 'The input does not appear to be associated with an account')
        else:
            if (user[0] == username) and (user[3] == email):
                sql = 'UPDATE db_atm.tbl_users SET password = %s WHERE user_id = %s'
                val = (password, user[2])
                db_cursor.execute(sql, val)
                db.commit()
                messagebox.showinfo('Successful', 'Password updated successfully!')
                master.switch_frame(LoginPage)
            else:
                messagebox.showerror('Invalid Entry', 'The input does not appear to be associated with an account')


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
        # Right Panel
        self.right_panel = ttk.Frame(self.main_frame)
        self.right_panel.pack(side='right')
        self._panel = None
        self.header_panel = ttk.Panedwindow(self.left_panel,
                                            height=160)
        self.header_panel.pack(side='top', fill='x')
        self.header_panel.pack_propagate(False)
        ttk.Label(self.header_panel, image=BankLogo).pack(side='top',
                                                          padx=20,
                                                          pady=10)
        self.header_label = ttk.Label(self.header_panel, text='Welcome back', font=('Open Sans', 18))
        self.header_label.pack(side='top')
        self.header_name = ttk.Label(self.header_panel, text=UserData[1], font=('Open Sans', 18))
        self.header_name.pack(side='top')
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
                                       text='Dark Mode',
                                       style="Switch.TCheckbutton")
        theme_button.pack(side='bottom', fill='x', padx=60)
        if self.tk.call("ttk::style", "theme", "use") == "azure-dark":
            theme_button.state(['selected'])

        self.left_panel.pack(side='left', fill='y')
        self.show_panel(AccountsPanel)

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
        self.accounts_panel = ttk.Frame(self,
                                        style="Card.TFrame")
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
                                       text="R {:,.2f}".format(total).replace(',', ' '),
                                       font=('Open Sans', 20))
        self.balance_label.grid(column=0,
                                row=1,
                                sticky='w',
                                padx=35,
                                columnspan=1,
                                pady=(0, 10))

        # Foreign exchange frame
        self.right_panel = ttk.Frame(self.accounts_panel,
                                     width=298,
                                     height=598)
        self.right_panel.grid_propagate(False)
        self.right_panel.grid(column=2,
                              row=0,
                              padx=1,
                              pady=1,
                              sticky='e')
        self.time_lbl = ttk.Label(self.right_panel, text='00:00:00', font=('Open Sans', 12))
        self.time_lbl.grid(row=0, sticky='e', padx=25, pady=10)

        self.exchange_frame = ttk.Frame(self.right_panel, style='Card.TFrame')
        self.exchange_frame.grid(row=1,
                                 padx=25,
                                 pady=1,
                                 column=0)
        ttk.Label(self.exchange_frame,
                  text='Foreign Exchange',
                  font=('Open Sans', 14),
                  justify='center').grid(column=0,
                                         columnspan=2,
                                         row=0,
                                         padx=40,
                                         pady=30)
        self.list = tk.Listbox(self.exchange_frame,
                               font=('Open Sans', 10),
                               borderwidth=0,
                               width=15, justify='right')
        self.list.grid(column=0,
                       row=1,
                       sticky='n',
                       padx=(1, 10))
        self.list.insert(1, f'China')
        self.list.insert(2, f'Japan')
        self.list.insert(3, f'Switzerland')
        self.list.insert(4, f'Russia')
        self.list.insert(5, f'India')
        self.list.insert(6, f'Taiwan')
        self.list.insert(7, f'Hong Kong')
        self.list.insert(8, f'Saudi Arabia')
        self.list.insert(9, f'United States')
        self.list.insert(10, f'United Kingdom')
        self.exchange_list = tk.Listbox(self.exchange_frame,
                                        font=('Open Sans', 10),
                                        borderwidth=0,
                                        width=6)
        self.exchange_list.grid(column=1,
                                row=1,
                                sticky='w',
                                pady=(0, 30),
                                padx=1)
        self.monitor(backgroundTime)
        self.monitor_exchange()
        self.exchange_list.bindtags(('', 'all'))
        self.list.bindtags(('', 'all'))

        # Recent transactions
        ttk.Label(self.left_panel,
                  text='Recent Transactions',
                  font=('Open Sans Bold', 14)).grid(row=2,
                                                    padx=150,
                                                    columnspan=2)
        self.tag_panel = ttk.Frame(self.left_panel, style="Card.TFrame")
        self.tag_panel.grid(row=3, padx=25, pady=(0, 20))
        self.recent_transactions()
        self.accounts_panel.grid()

    def update_rates(self):
        if len(exchange_data) > 0:
            self.exchange_list.insert(1, exchange_data[2])
            self.exchange_list.insert(2, exchange_data[3])
            self.exchange_list.insert(3, exchange_data[4])
            self.exchange_list.insert(4, exchange_data[5])
            self.exchange_list.insert(5, exchange_data[6])
            self.exchange_list.insert(6, exchange_data[7])
            self.exchange_list.insert(7, exchange_data[8])
            self.exchange_list.insert(8, exchange_data[9])
            self.exchange_list.insert(9, exchange_data[10])
            self.exchange_list.insert(10, exchange_data[11])
        else:
            raise SystemExit

    def recent_transactions(self):
        tags = len(TransactionData)
        if tags > 10:
            tags = 10
        for a in range(0, tags):
            frame = ttk.Frame(self.tag_panel,
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
            dates = TransactionData[a][3].strftime('%Y-%m-%d %H:%M')
            lbldate = ttk.Label(frame,
                                text=dates,
                                width=20,
                                font=('Open Sans Light', 10))
            lbldate.grid(row=0,
                         column=1,
                         sticky='e',
                         padx=4,
                         pady=10)
            value = ttk.Label(frame,
                              text="R {:,.2f}".format((TransactionData[a][2])),
                              width=10,
                              font=('Open Sans', 10))
            value.grid(row=0,
                       column=2,
                       sticky='e',
                       padx=(10, 13),
                       pady=10)

    def monitor(self, thread):
        self.after(1000, lambda: self.monitor(thread))
        self.time_lbl['text'] = latestTime

    def monitor_exchange(self):
        self.after(600000, lambda: self.monitor_exchange())
        self.update_rates()


class CardsPanel(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # Gui Creation
        self.bottom_panel = ttk.Frame(self, style='Card.TFrame')
        self.card_panel = ttk.Frame(self.bottom_panel, style='Card.TFrame')
        self.main_panel = ttk.Frame(self.card_panel,
                                    width=600,
                                    height=600)
        self.main_panel.pack_propagate(False)
        self.right_panel = ttk.Frame(self.card_panel,
                                     width=198,
                                     height=598)
        self.right_panel.pack_propagate(False)
        self.right_panel.pack(side='right',
                              pady=1,
                              padx=1)

        self.card_panel.grid()
        self.bottom_panel.grid()

        # Credit panel
        self.credit_panel = ttk.Frame(self.main_panel,
                                      style='Card.TFrame'
                                      )
        self.credit_panel.pack(side='top', fill='x')

        # Debit panel
        self.debit_panel = ttk.Frame(self.main_panel,
                                     height=200,
                                     width=600,
                                     style='Card.TFrame'
                                     )
        self.debit_panel.pack_propagate(False)
        self.debit_panel.pack(side='top', fill='x')

        # Savings panel
        self.savings_panel = ttk.Frame(self.main_panel,
                                       height=200,
                                       width=600,
                                       style='Card.TFrame'
                                       )
        self.savings_panel.pack_propagate(False)
        self.savings_panel.pack(side='top', fill='x')

        self.image = Image.open('theme/credit_card.png')
        self.image = self.image.resize((204, 120))
        self.c_img = ImageTk.PhotoImage(self.image)
        self.credit_img = ttk.Label(self.credit_panel, image=self.c_img)
        self.credit_img.grid(column=0, row=0, padx=(50, 20), pady=38)

        self.image = Image.open('theme/debit_card.png')
        self.image = self.image.resize((204, 120))
        self.d_img = ImageTk.PhotoImage(self.image)
        self.debit_img = ttk.Label(self.debit_panel, image=self.d_img)
        self.debit_img.grid(column=0, row=0, padx=(50, 20), pady=38)

        self.image = Image.open('theme/savings_card.png')
        self.image = self.image.resize((204, 120))
        self.s_img = ImageTk.PhotoImage(self.image)
        self.saving_img = ttk.Label(self.savings_panel, image=self.s_img)
        self.saving_img.grid(column=0, row=0, padx=(50, 20), pady=38)
        self.populate()
        self.main_panel.pack(side='left')

    def populate(self):
        ccard, dcard, scard = False, False, False
        count = 0
        for x in CardType[1]:
            if x == 'Credit':
                ccard = True
                c_panel = ttk.Frame(self.credit_panel)
                c_panel.grid(column=1, row=0, pady=40, sticky='n')
                ttk.Label(c_panel, text='Credit Account', font=('Open Sans Bold', 14)).grid(row=0)
                # data
                ttk.Label(c_panel,
                          text=f'{AccountsData[count][0]}',
                          font=('Open Sans Light', 12)).grid(row=1, sticky='nw')
                ttk.Label(c_panel,
                          text="R {:,.2f}".format(AccountsData[count][1]).replace(',', ' '),
                          font=('Open Sans', 14)).grid(row=2, sticky='sw', pady=(10, 0))
                ttk.Label(c_panel,
                          text='Balance',
                          font=('Open Sans Light', 10)).grid(row=3, sticky='nw')
            elif x == 'Debit':
                dcard = True
                d_panel = ttk.Frame(self.debit_panel)
                d_panel.grid(column=1, row=0, pady=40, sticky='n')
                ttk.Label(d_panel, text='Debit Account', font=('Open Sans Bold', 14)).grid(row=0)
                # data
                ttk.Label(d_panel,
                          text=f'{AccountsData[count][0]}',
                          font=('Open Sans Light', 12)).grid(row=1, sticky='nw')
                ttk.Label(d_panel,
                          text="R {:,.2f}".format(AccountsData[count][1]).replace(',', ' '),
                          font=('Open Sans', 14)).grid(row=2, sticky='sw', pady=(10, 0))
                ttk.Label(d_panel,
                          text='Balance',
                          font=('Open Sans Light', 10)).grid(row=3, sticky='nw')

            elif x == 'Savings':
                scard = True
                s_panel = ttk.Frame(self.savings_panel)
                s_panel.grid(column=1, row=0, pady=40, sticky='n')
                ttk.Label(s_panel, text='Savings Account', font=('Open Sans Bold', 14)).grid(row=0)
                # data
                ttk.Label(s_panel,
                          text=f'{AccountsData[count][0]}',
                          font=('Open Sans Light', 12)).grid(row=1, sticky='nw')
                ttk.Label(s_panel,
                          text="R {:,.2f}".format(AccountsData[count][1]).replace(',', ' '),
                          font=('Open Sans', 14)).grid(row=2, sticky='sw', pady=(10, 0))
                ttk.Label(s_panel,
                          text='Balance',
                          font=('Open Sans Light', 10)).grid(row=3, sticky='nw')
            count += 1
        if not ccard:
            ttk.Label(self.credit_panel,
                      text='You don''t have a Credit Account',
                      font=('Open Sans Bold', 14)).grid(column=1,
                                                        sticky='news',
                                                        padx=152,
                                                        pady=(60, 20),
                                                        row=0)
            ttk.Button(self.credit_panel,
                       style='Accent.TButton',
                       text='Apply Now').grid(column=1,
                                              pady=(0, 54),
                                              row=1)
            self.credit_img.grid_remove()
        if not dcard:
            ttk.Label(self.debit_panel,
                      text='You don''t have a Debit Account',
                      font=('Open Sans Bold', 14)).grid(column=1,
                                                        sticky='news',
                                                        padx=152,
                                                        pady=(60, 20),
                                                        row=0)
            ttk.Button(self.debit_panel,
                       style='Accent.TButton',
                       text='Apply Now').grid(column=1,
                                              pady=(0, 54),
                                              row=1)
            self.debit_img.grid_remove()
        if not scard:
            ttk.Label(self.savings_panel,
                      text='You don''t have a Savings Account',
                      font=('Open Sans Bold', 14)).grid(column=1,
                                                        sticky='news',
                                                        padx=152,
                                                        pady=(60, 20),
                                                        row=0)
            ttk.Button(self.savings_panel,
                       style='Accent.TButton',
                       text='Apply Now').grid(column=1,
                                              pady=(0, 54),
                                              row=1)
            self.saving_img.grid_remove()


class PaymentsPanel(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self._payments = None
        # Gui Creation
        self.bottom_panel = ttk.Frame(self, style='Card.TFrame')
        self.transfer_panel = ttk.Frame(self.bottom_panel)
        self.pay_panel = ttk.Frame(self.bottom_panel)
        self.payments_panel = ttk.Frame(self.bottom_panel, style='Card.TFrame')
        self.canvas = tk.Canvas(self.payments_panel,
                                width=500,
                                height=590,
                                borderwidth=0)
        self.frame = ttk.Frame(self.canvas)
        self.scrollboard = ttk.Scrollbar(self.payments_panel,
                                         orient='vertical',
                                         command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollboard.set)
        self.right_panel = ttk.Frame(self.payments_panel,
                                     style='Card.TFrame',
                                     width=284,
                                     height=600)
        self.right_panel.pack(side='right')
        self.right_panel.pack_propagate(False)

        self.time_lbl = ttk.Label(self.right_panel, text='00:00:00', font=('Open Sans', 12))
        self.time_lbl.pack(side='top', anchor='e', padx=32, pady=11)
        self.monitor(monitor_time)

        self.scrollboard.pack(side='right',
                              fill='y',
                              pady=2)
        self.canvas.pack(side='left',
                         fill='both',
                         expand=True,
                         padx=1,
                         pady=1)
        self.canvas.create_window((0, 0),
                                  window=self.frame,
                                  anchor='n',
                                  tags='self.frame')
        self.frame.bind('<Configure>',
                        self.onFrameConfigure)
        self.header = ttk.Frame(self.frame)
        self.header.pack(side='top')
        self.pay_button = ttk.Button(self.header,
                                     command=self.showpay,
                                     style='Accent.TButton',
                                     text='Pay')
        self.pay_button.grid(row=0,
                             column=0,
                             padx=10,
                             pady=40,
                             sticky='e')
        self.transfer_button = ttk.Button(self.header,
                                          command=self.show_transfer,
                                          style='Accent.TButton',
                                          text='Transfer')
        if len(CardType[0]) == 1:
            self.transfer_button['state'] = tk.DISABLED
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
                                                    padx=188,
                                                    pady=1)
        self.receipt_frame = ttk.Frame(self.frame,
                                       style='Card.TFrame')
        self.receipt_frame.pack(side='top')
        self.payments_panel.pack()
        self.populate()
        self.bottom_panel.grid()

    def populate(self):
        fetchTransactions()
        tags = len(TransactionData)
        if tags > 30:
            tags = 30
        for a in range(0, tags):
            receipt = ttk.Frame(self.receipt_frame)
            receipt.pack(side='top',
                         fill='x',
                         padx=1,
                         pady=5,
                         expand=True)
            title = ttk.Label(receipt,
                              text=TransactionData[a][1],
                              font=('Open Sans', 12),
                              width=20)
            title.grid(row=0,
                       column=0,
                       sticky='n',
                       padx=10)
            if TransactionData[a][4] == CardType[0][0]:
                text = 'Debit'
            elif TransactionData[a][4] == CardType[0][1]:
                text = 'Credit'
            else:
                text = 'Savings'
            card = ttk.Label(receipt,
                             text=text,
                             font=('Open Sans Light', 8),
                             width=30)
            card.grid(row=1,
                      column=0,
                      sticky='n',
                      pady=(0, 5),
                      padx=10)
            dates = TransactionData[a][3].strftime('%Y-%m-%d %H:%M')
            lbldate = ttk.Label(receipt,
                                text=dates,
                                font=('Open Sans Light', 10),
                                width=20)
            lbldate.grid(row=0,
                         column=1,
                         sticky='e',
                         padx=10)
            value = ttk.Label(receipt,
                              text="R {:,.2f}".format(TransactionData[a][2]),
                              width=10,
                              font=('Open Sans', 10))
            value.grid(row=0,
                       column=2,
                       sticky='e',
                       padx=10)

    def update_values(self):
        for x in self.receipt_frame.winfo_children():
            x.destroy()
        self.populate()

    def onFrameConfigure(self, x):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        return x

    def showpay(self):
        self.payments_panel.pack_forget()
        self.pay_panel.configure(style='Card.TFrame')
        rightpanel = ttk.Frame(self.pay_panel,
                               style='Card.TFrame',
                               width=300,
                               height=600)
        rightpanel.grid(row=0,
                        column=3,
                        rowspan=12)
        rightpanel.grid_propagate(False)
        ttk.Label(self.pay_panel,
                  text='Pay beneficiary',
                  font=('Open Sans', 20)).grid(row=0,
                                               column=0,
                                               padx=152,
                                               pady=(30, 50),
                                               columnspan=2)
        ttk.Label(self.pay_panel,
                  text='From:').grid(row=1,
                                     column=0,
                                     pady=(0, 5),
                                     sticky='e')
        value = tk.StringVar()
        # From Combobox
        cbb_from = ttk.Combobox(self.pay_panel,
                                textvariable=value,
                                width=20)
        cbb_from.grid(row=1,
                      column=1,
                      padx=10,
                      pady=(0, 5),
                      sticky='w')
        cbb_from['state'] = 'readonly'
        cbb_from['values'] = CardType[1]

        ttk.Label(self.pay_panel,
                  text='Recipient Account ID:').grid(row=2,
                                                     column=0,
                                                     sticky='e')
        # recipient Entry
        entry_to = ttk.Entry(self.pay_panel,
                             width=15)
        entry_to.grid(row=2,
                      column=1,
                      padx=10,
                      sticky='w')
        # Own Reference
        ttk.Label(self.pay_panel,
                  text='Own Reference').grid(row=3,
                                             column=0,
                                             pady=(60, 5),
                                             sticky='e')
        entry_own_ref = ttk.Entry(self.pay_panel,
                                  width=20)
        entry_own_ref.grid(row=3,
                           column=1,
                           padx=10,
                           pady=(60, 5),
                           sticky='w')
        # Recipient reference
        ttk.Label(self.pay_panel,
                  text='Recipient Reference').grid(row=4,
                                                   column=0,
                                                   sticky='e')
        entry_recipient_ref = ttk.Entry(self.pay_panel,
                                        width=20)
        entry_recipient_ref.grid(row=4,
                                 column=1,
                                 padx=10,
                                 sticky='w')
        # Value Entry
        ttk.Label(self.pay_panel,
                  text='Enter Amount:').grid(row=5,
                                             column=0,
                                             pady=(80, 0),
                                             sticky='e')
        value_entry = ttk.Entry(self.pay_panel,
                                width=15)
        value_entry.grid(row=5,
                         column=1,
                         padx=10,
                         pady=(80, 0),
                         sticky='w')
        back_button = ttk.Button(self.pay_panel,
                                 width=25,
                                 text='Back',
                                 command=lambda: self.showpayment(1))
        back_button.grid(row=6,
                         column=0,
                         pady=(60, 0),
                         padx=(20, 0),
                         sticky='e')
        pay_button = ttk.Button(self.pay_panel,
                                width=25,
                                text='Pay',
                                style='Accent.TButton',
                                command=lambda: self.pay_money(cbb_from.get(),
                                                               entry_to.get(),
                                                               entry_own_ref.get(),
                                                               entry_recipient_ref.get(),
                                                               value_entry.get()))
        pay_button.grid(row=6,
                        padx=20,
                        pady=(60, 0),
                        sticky='w',
                        column=1)
        self.pay_panel.pack_propagate(False)
        self.pay_panel.pack()

    def show_transfer(self):
        self.payments_panel.pack_forget()
        self.transfer_panel.configure(style='Card.TFrame')
        rightpanel = ttk.Frame(self.transfer_panel,
                               style='Card.TFrame',
                               width=299,
                               height=600)
        rightpanel.grid(row=0,
                        column=3,
                        rowspan=12)
        rightpanel.grid_propagate(False)
        ttk.Label(self.transfer_panel,
                  text='Transfers',
                  font=('Open Sans', 20)).grid(row=0,
                                               column=0,
                                               padx=189,
                                               pady=(30, 50))
        ttk.Label(self.transfer_panel,
                  text='From:').grid(row=1, sticky='s')

        acc_from = tk.StringVar()
        # From Combobox
        cbb_from = ttk.Combobox(self.transfer_panel,
                                textvariable=acc_from,
                                width=20)
        cbb_from.grid(row=2, sticky='n')
        cbb_from['state'] = 'readonly'
        cbb_from['values'] = CardType[1]

        ttk.Label(self.transfer_panel,
                  text='To:').grid(row=3, sticky='s')

        acc_to = tk.StringVar()
        # to Combobox
        cbb_to = ttk.Combobox(self.transfer_panel,
                              textvariable=acc_to,
                              width=20)
        cbb_to.grid(row=4,
                    pady=(0, 80),
                    sticky='n')
        cbb_to['state'] = 'readonly'
        cbb_to['values'] = CardType[1]

        # Value Entry
        ttk.Label(self.transfer_panel,
                  text='Enter Amount:').grid(row=7, sticky='s')
        value_entry = ttk.Entry(self.transfer_panel,
                                width=15)
        value_entry.grid(row=8,
                         pady=(0, 70),
                         sticky='n')

        back_button = ttk.Button(self.transfer_panel,
                                 width=25,
                                 text='Back',
                                 command=lambda: self.showpayment(2))
        back_button.grid(row=9,
                         column=0,
                         sticky='w',
                         pady=20,
                         padx=(30, 0))
        transfer_button = ttk.Button(self.transfer_panel,
                                     width=25,
                                     text='Pay',
                                     command=lambda: self.transfer_money(cbb_from.get(),
                                                                         cbb_to.get(),
                                                                         value_entry.get()),
                                     style='Accent.TButton')
        transfer_button.grid(row=9,
                             padx=(0, 30),
                             sticky='e',
                             pady=20)
        self.transfer_panel.pack_propagate(False)
        self.transfer_panel.pack()

    def showpayment(self, x):
        self.update_values()
        if x == 1:
            self.pay_panel.pack_forget()
            for y in self.pay_panel.winfo_children():
                y.destroy()
        else:
            self.transfer_panel.pack_forget()
            for y in self.transfer_panel.winfo_children():
                y.destroy()
        self.payments_panel.pack()

    def pay_money(self, account, userid, own_reference, recipient_reference, amount):
        if pay(account, userid, own_reference, recipient_reference, amount):
            self.showpayment(1)

    def transfer_money(self, acc_from, acc_to, amount):
        if transfer(acc_from, acc_to, amount):
            self.showpayment(2)

    def monitor(self, thread):
        self.after(1000, lambda: self.monitor(thread))
        self.time_lbl['text'] = latestTime


class TransferPanel(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # Gui Creation
        self.cards_panel = ttk.Frame(self, width=800, height=600, style="Card.TFrame")
        self.cards_panel.grid()
        self.cards_panel.grid_propagate(False)


def db_connect():
    # Connecting to the database is set as a method since we need to open and close it for different transactions
    # Error handling code:
    # https://docs.oracle.com/cd/E17952_01/connector-python-en/connector-python-example-connecting.html
    # Start of borrowed code
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password='12345678',
            # password="toor",
            # password='Kgalela@07',
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


class liveAPI(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        url = 'https://api.exchangerate.host/latest&v=' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            r = requests.get(url=url, timeout=3)
            data = r.json()
            exchange_data[0] = ("{:.3f}".format((data['rates']['CNY'] / data['rates']['ZAR'])))
            exchange_data[1] = ("{:.3f}".format((data['rates']['JPY'] / data['rates']['ZAR'])))
            exchange_data[2] = ("{:.3f}".format((data['rates']['CHF'] / data['rates']['ZAR'])))
            exchange_data[3] = ("{:.3f}".format((data['rates']['RUB'] / data['rates']['ZAR'])))
            exchange_data[4] = ("{:.3f}".format((data['rates']['INR'] / data['rates']['ZAR'])))
            exchange_data[5] = ("{:.3f}".format((data['rates']['TWD'] / data['rates']['ZAR'])))
            exchange_data[6] = ("{:.3f}".format((data['rates']['HKD'] / data['rates']['ZAR'])))
            exchange_data[7] = ("{:.3f}".format((data['rates']['SAR'] / data['rates']['ZAR'])))
            exchange_data[8] = ("{:.3f}".format((data['rates']['KRW'] / data['rates']['ZAR'])))
            exchange_data[9] = ("{:.3f}".format((data['rates']['SGD'] / data['rates']['ZAR'])))
            exchange_data[10] = ("{:.3f}".format((data['rates']['USD'] / data['rates']['ZAR'])))
            exchange_data[11] = ("{:.3f}".format((data['rates']['GBP'] / data['rates']['ZAR'])))
            return True
        except requests.exceptions.ReadTimeout:
            url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/zar.json'
            r = requests.get(url=url, timeout=3)
            data = r.json()['zar']
            exchange_data[0] = ("{:.3f}".format(data['cny']))
            exchange_data[1] = ("{:.3f}".format(data['jpy']))
            exchange_data[2] = ("{:.3f}".format(data['chf']))
            exchange_data[3] = ("{:.3f}".format(data['rub']))
            exchange_data[4] = ("{:.3f}".format(data['inr']))
            exchange_data[5] = ("{:.3f}".format(data['twd']))
            exchange_data[6] = ("{:.3f}".format(data['hkd']))
            exchange_data[7] = ("{:.3f}".format(data['sar']))
            exchange_data[8] = ("{:.3f}".format(data['krw']))
            exchange_data[9] = ("{:.3f}".format(data['sgd']))
            exchange_data[10] = ("{:.3f}".format(data['usd']))
            exchange_data[11] = ("{:.3f}".format(data['gbp']))
            return True
        except requests.exceptions.ConnectionError:
            return False

def fetchUser():
    global UserData
    db = db_connect()
    db_cursor = db.cursor()
    sql = "SELECT * FROM db_atm.tbl_users WHERE user_id = %s"
    adr = (UserID,)
    db_cursor.execute(sql, adr)
    UserData = db_cursor.fetchone()


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
    AccountsData = sorted(db_cursor.fetchall(), key=lambda x: x[3])
    length = len(AccountsData)
    card_type = []
    card_num = []
    for a in range(0, length):
        card_num.append(AccountsData[a][0])
        if AccountsData[a][3] == 'c':
            card_type.append('Credit')
        elif AccountsData[a][3] == 'd':
            card_type.append('Debit')
        elif AccountsData[a][3] == 's':
            card_type.append('Savings')
    CardType.insert(0, card_num)
    CardType.insert(1, card_type)


def pay(account, userid, own_reference, recipient_reference, amount):
    valid = False
    exists = False
    user = None
    userdata = None
    # Data verification
    if not account:
        messagebox.showerror('Invalid Account', 'Please choose an account to use.')
    elif not userid:
        messagebox.showerror('Invalid Recipient ID', 'Please type a recipient ID.')
    elif not own_reference:
        messagebox.showerror('Invalid Reference', 'Please add an own reference.')
    elif not recipient_reference:
        messagebox.showerror('Invalid Reference', 'Please add a recipient reference.')

    elif len(own_reference) > 20:
        messagebox.showerror('Invalid Reference', 'Own reference length exceeds the maximum\n (20 characters)')
    elif len(recipient_reference) > 20:
        messagebox.showerror('Invalid Reference', 'Recipient reference length exceeds the maximum\n (20 characters)')

    elif not amount:
        messagebox.showerror('Invalid Amount', 'Please add an amount.')
    else:
        try:
            amount = float(amount)
            valid = True
        except ValueError:
            messagebox.showerror('Invalid Amount', 'Amount can only be numbers\nPeriod as decimal seperator')
        else:
            try:
                userid = int(userid)
            except ValueError:
                valid = False
                messagebox.showerror('Invalid Input', 'Recipient ID can only be numbers')
    if valid:
        if account == 'Debit':
            account = CardType[0][0]
        elif account == 'Credit':
            account = CardType[0][1]
        else:
            account = CardType[0][2]
        for x in AccountsData:
            if x[0] == account:
                userdata = x
                if amount > x[1]:
                    valid = False
                    messagebox.showerror('Insufficient Funds',
                                         'The required funds are not available in the selected account')
    if valid:
        try:
            db = db_connect()
            db_cursor = db.cursor()
            check_id = 'SELECT * FROM db_atm.tbl_accounts WHERE acc_ID = %s'
            val = (userid,)
            db_cursor.execute(check_id, val)
            user = db_cursor.fetchone()
            if not user:
                messagebox.showerror('Invalid Recipient ID', 'The ID does not exist')
            else:
                exists = True
                for x in CardType[0]:
                    if x == user[0]:
                        messagebox.showerror('Invalid Recipient ID', 'You cannot pay your own account')
                        exists = False
        except Exception as e:
            messagebox.showerror('Error', 'An unknown error occurred')
            print(e)
    if exists:
        # Finalizing Payment
        own_amount = float(userdata[1]) - amount
        recipient_amount = float(user[1]) + amount
        try:
            # Update Account balances
            update_amount = 'UPDATE db_atm.tbl_accounts SET acc_balance = %s WHERE acc_ID = %s'
            val = (own_amount, userdata[0])
            db = db_connect()
            db_cursor = db.cursor()
            db_cursor.execute(update_amount, val)
            val = (recipient_amount, user[0])
            db_cursor.execute(update_amount, val)
            # Add transactions
            add_transaction = '''INSERT INTO db_atm.tbl_transactions 
            (description, amount, date, tbl_accounts_acc_ID, tbl_accounts_tbl_users_user_id) 
            VALUES (%s, %s, %s, %s, %s) '''
            transaction_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            own_amount = amount * -1
            val = (own_reference, own_amount, transaction_date, userdata[0], userdata[4])
            db_cursor.execute(add_transaction, val)
            val = (recipient_reference, amount, transaction_date, user[0], user[4])
            db_cursor.execute(add_transaction, val)
            db.commit()
            fetchAccounts()
            fetchTransactions()
            messagebox.showinfo('Successful', 'Payment done successfully!')
            return True
        except Exception as e:
            print(e)
            raise e


def transfer(acc_from, acc_to, amount):
    valid = False
    # Data verification
    if not acc_from:
        messagebox.showerror('Invalid Account', 'Please choose an account to use.')
    elif not acc_to:
        messagebox.showerror('Invalid Account', 'Please choose an account to transfer to.')
    elif acc_to == acc_from:
        messagebox.showerror('Invalid Account', 'Please choose a different account to transfer to')
    elif not amount:
        messagebox.showerror('Invalid Amount', 'Please add an amount.')
    else:
        try:
            amount = float(amount)
            valid = True
        except ValueError:
            messagebox.showerror('Invalid Amount', 'Amount can only be numbers\nPeriod as decimal seperator')
            valid = False
    if valid:
        if acc_from == 'Credit':
            acc_from = CardType[0][0]
        elif acc_from == 'Debit':
            acc_from = CardType[0][1]
        else:
            acc_from = CardType[0][2]
        if acc_to == 'Credit':
            acc_to = CardType[0][0]
        elif acc_to == 'Debit':
            acc_to = CardType[0][1]
        else:
            acc_to = CardType[0][2]
        for x in AccountsData:
            if x[0] == acc_from:
                acc_from = x
                if amount > x[1]:
                    valid = False
                    messagebox.showerror('Insufficient Funds',
                                         'The required funds are not available in the selected account')
            elif x[0] == acc_to:
                acc_to = x

    if valid:
        # Finalize transfer
        from_amount = float(acc_from[1]) - amount
        to_amount = float(acc_to[1]) + amount
        try:
            # Update account balances
            update_amount = 'UPDATE db_atm.tbl_accounts SET acc_balance = %s WHERE acc_ID = %s'
            val = (from_amount, acc_from[0])
            db = db_connect()
            db_cursor = db.cursor()
            db_cursor.execute(update_amount, val)
            val = (to_amount, acc_to[0])
            db_cursor.execute(update_amount, val)
            db.commit()
            fetchAccounts()
            fetchTransactions()
            messagebox.showinfo('Successful', 'Transfer made successfully!')
            return True
        except Exception as e:
            print(e)


if __name__ == "__main__":
    root = Application()
    root.mainloop()
