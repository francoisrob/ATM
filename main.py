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

Version = 'v1'
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

        # Right Panels
        self.right_panel = ttk.Frame(self.main_frame)
        self.right_panel.pack(side='right')
        self.accounts_panel = ttk.Frame(self.right_panel, width=500, height=500, style="Card.TFrame")
        self.cards_panel = ttk.Frame(self.right_panel, width=500, height=500)
        self.payments_panel = ttk.Frame(self.right_panel, width=500, height=500)
        for f in (self.accounts_panel, self.cards_panel, self.payments_panel):
            f.grid(row=0, column=0)
            f.grid_propagate(False)
        self.show_panel(self.accounts_panel)

        self.header_label = ttk.Label(self.left_panel,
                                      text='Welcome',
                                      font=('Open Sans', 30))
        self.header_label.pack(side='top',
                               padx=(20, 30),
                               pady=(10, 20))

        self.accounts_button = ttk.Button(self.left_panel,
                                          text='Accounts',
                                          style="Panel.TButton",
                                          command=self.show_panel(self.accounts_panel))
        self.accounts_button.pack(side='top', fill='x')
        self.cards_button = ttk.Button(self.left_panel,
                                       text='Cards',
                                       style="Panel.TButton")
        self.cards_button.pack(side='top', fill='x')
        self.payments_button = ttk.Button(self.left_panel,
                                          text='Payments',
                                          command=lambda: master.switch_frame(LoginPage),
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

        # accounts panel
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

        self.payments_scroll = ttk.Scrollbar(self.accounts_panel,
                                             orient='vertical')
        self.payments_scroll.grid(column=2, row=3, sticky='w', padx=(0, 20))

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


def db_create():
    db = db_connect()  # Method RETURNS the connection we made to the db
    db_cursor = db.cursor()

    # CREATES DATABASE db_ATM
    db_cursor.execute("SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;")
    db_cursor.execute("SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;")
    db_cursor.execute("SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,"
                      "NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';")

    db_cursor.execute("CREATE SCHEMA IF NOT EXISTS `db_ATM` DEFAULT CHARACTER SET utf8 ;")
    db_cursor.execute("USE `db_ATM` ;")
    db.commit()

    # CREATE TABLE tbl_users
    db_cursor.execute("DROP TABLE IF EXISTS `db_ATM`.`tbl_users` ;")
    sql = "CREATE TABLE IF NOT EXISTS `db_ATM`.`tbl_users` (" \
          "`user_id` INT NOT NULL AUTO_INCREMENT," \
          "`fname` VARCHAR(45) NOT NULL," \
          "`sname` VARCHAR(45) NOT NULL," \
          "`street` VARCHAR(45) NOT NULL," \
          "`city` VARCHAR(20) NOT NULL," \
          "`state` VARCHAR(3) NOT NULL," \
          "`cell_num` VARCHAR(10) NOT NULL," \
          "`email` VARCHAR(45) NOT NULL," \
          "`id_num` VARCHAR(13) NOT NULL," \
          "`username` VARCHAR(45) NOT NULL," \
          "`password` VARCHAR(45) NOT NULL," \
          "PRIMARY KEY (`user_id`))" \
          "ENGINE = InnoDB;"
    db_cursor.execute(sql)
    db.commit()

    # CREATE TABLE tbl_accounts
    db_cursor.execute("DROP TABLE IF EXISTS `db_ATM`.`tbl_accounts` ;")
    sql = "CREATE TABLE IF NOT EXISTS `db_ATM`.`tbl_accounts` (" \
          "`acc_ID` INT NOT NULL AUTO_INCREMENT," \
          "`acc_balance` DECIMAL(13,2) NOT NULL," \
          "`date_created` DATE NOT NULL," \
          "`acc_type` CHAR(1) NOT NULL," \
          "`tbl_users_user_id` INT NOT NULL," \
          "`credit_due` DECIMAL(13,2) NOT NULL," \
          "PRIMARY KEY (`acc_ID`, `tbl_users_user_id`)," \
          "CONSTRAINT `fk_tbl_accounts_tbl_users`" \
          " FOREIGN KEY (`tbl_users_user_id`)" \
          " REFERENCES `db_ATM`.`tbl_users` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION)" \
          "ENGINE = InnoDB;"
    db_cursor.execute(sql)
    db.commit()

    # CREATE TABLE tbl_accounts
    db_cursor.execute("DROP TABLE IF EXISTS `db_ATM`.`tbl_transactions` ;")
    sql = "CREATE TABLE IF NOT EXISTS `db_ATM`.`tbl_transactions` (" \
          "`trans_id` INT NOT NULL AUTO_INCREMENT," \
          "`trans_type` CHAR(1) NOT NULL," \
          "`description` VARCHAR(100) NOT NULL," \
          "`amount` DECIMAL(13,2) NOT NULL," \
          "`date` DATE NOT NULL," \
          "`tbl_accounts_acc_ID` INT NOT NULL," \
          "`tbl_accounts_tbl_users_user_id` INT NOT NULL," \
          "PRIMARY KEY (`trans_id`, `tbl_accounts_acc_ID`, `tbl_accounts_tbl_users_user_id`)," \
          "CONSTRAINT `fk_tbl_transactions_tbl_accounts1`" \
          " FOREIGN KEY (`tbl_accounts_acc_ID` , `tbl_accounts_tbl_users_user_id`)" \
          "REFERENCES `db_ATM`.`tbl_accounts` (`acc_ID` , `tbl_users_user_id`) ON DELETE NO ACTION ON UPDATE NO " \
          "ACTION)" \
          "ENGINE = InnoDB;"
    db_cursor.execute(sql)
    db.commit()

    db_cursor.execute("SET SQL_MODE=@OLD_SQL_MODE;")
    db_cursor.execute("SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;")
    db_cursor.execute("SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;")
    db.commit()

    # INSERT into tbl_users


if __name__ == "__main__":
    db_create()
    root = ATM_Application()
    root.mainloop()
"""
==Most basic code to create a new frame

class PageName(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        
        # When creating a new form please parent all widgets inside of a parent frame, 
        # this will make organising the widgets easier in future. Take LoginPage as example
"""
