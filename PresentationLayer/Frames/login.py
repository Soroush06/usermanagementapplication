from tkinter import Frame, Label, Entry, Button, messagebox, BooleanVar
from tkinter.ttk import Checkbutton
from BusinessLogicLayer.user_business_logic import UserBusinessLogic
from ttkbootstrap import Button,Label,INFO,SUCCESS
from CommonLayer.Decorators.Performance_logger import performance_logger_decorator


class LoginFrame(Frame):
    def __init__(self, window, main_view):
        super().__init__(window)

        self.main_view = main_view
        self.user_business_logic = UserBusinessLogic()

        self.grid_columnconfigure(1, weight=1)

        self.header = Label(self, text="Login Page",bootstyle=INFO)
        self.header.grid(row=0, column=1, pady=10, sticky="w")

        self.username_label = Label(self, text="Username",bootstyle=INFO)
        self.username_label.grid(row=1, column=0, pady=(0, 10), padx=10, sticky="e")

        self.username_entry = Entry(self)
        self.username_entry.grid(row=1, column=1, pady=(0, 10), padx=(0, 20), sticky="ew")

        username = self.read_user_data()
        if username:
            self.username_entry.insert(0, username)

        self.password_label = Label(self, text="Password",bootstyle=INFO)
        self.password_label.grid(row=2, column=0, pady=(0, 10), padx=10, sticky="e")

        self.password_entry = Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, pady=(0, 10), padx=(0, 20), sticky="ew")

        self.remember_me_variable = BooleanVar(value=False)
        self.remember_me_checkbutton = Checkbutton(self, text="remember me?", variable=self.remember_me_variable,bootstyle=INFO)
        self.remember_me_checkbutton.grid(row=3, column=1, pady=(0, 10), padx=(0, 20), sticky="w")

        self.login_button = Button(self, text="Login", command=self.login,bootstyle=INFO)
        self.login_button.grid(row=4, column=1, pady=(0, 10), padx=(0, 20), sticky="w")

        self.register_button = Button(self, text="Register", command=self.go_to_register,bootstyle=SUCCESS)
        self.register_button.grid(row=5, column=1, pady=(0, 10), padx=(0, 20), sticky="w")

    @performance_logger_decorator("LoginFrame")
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        response = self.user_business_logic.login(username, password)

        if response.success:
            home_frame = self.main_view.switch_frame("home")
            home_frame.set_current_user(response.data)

            if self.remember_me_variable.get():
                self.write_user_data(username)

            # self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
        else:
            messagebox.showerror(title="Error", message=response.message)

    @performance_logger_decorator("LoginFrame")
    def write_user_data(self, username):
        with open("user_data.txt", mode="w") as file:
            file.write(username)

    @performance_logger_decorator("LoginFrame")
    def read_user_data(self):
        with open("user_data.txt") as file:
            username = file.read()
            return username

    @performance_logger_decorator("LoginFrame")
    def go_to_register(self):
        self.main_view.switch_frame("register")