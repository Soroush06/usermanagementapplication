from tkinter import Frame, Label, Entry, Button, messagebox
from BusinessLogicLayer.user_business_logic import UserBusinessLogic
from ttkbootstrap import Button, Label, INFO, SUCCESS, PRIMARY
from CommonLayer.Decorators.Performance_logger import performance_logger_decorator

class RegisterFrame(Frame):
    def __init__(self, window, main_view):
        super().__init__(window)

        self.grid_columnconfigure(1, weight=1)

        self.main_view = main_view
        self.user_business_logic = UserBusinessLogic()

        self.header = Label(self, text="Register Page",bootstyle=INFO)
        self.header.grid(row=0, column=1, pady=10, sticky="w")

        self.firstname_label = Label(self, text="First Name",bootstyle=INFO)
        self.firstname_label.grid(row=1, column=0, pady=(0, 10), padx=10, sticky="e")

        self.firstname_entry = Entry(self)
        self.firstname_entry.grid(row=1, column=1, pady=(0, 10), padx=(0, 20), sticky="ew")

        self.lastname_label = Label(self, text="Last Name",bootstyle=INFO)
        self.lastname_label.grid(row=2, column=0, pady=(0, 10), padx=10, sticky="e")

        self.lastname_entry = Entry(self)
        self.lastname_entry.grid(row=2, column=1, pady=(0, 10), padx=(0, 20), sticky="ew")

        self.username_label = Label(self, text="Username",bootstyle=INFO)
        self.username_label.grid(row=3, column=0, pady=(0, 10), padx=10, sticky="e")

        self.username_entry = Entry(self)
        self.username_entry.grid(row=3, column=1, pady=(0, 10), padx=(0, 20), sticky="ew")

        self.password_label = Label(self, text="Password",bootstyle=INFO)
        self.password_label.grid(row=4, column=0, pady=(0, 10), padx=10, sticky="e")

        self.password_entry = Entry(self, show="*")
        self.password_entry.grid(row=4, column=1, pady=(0, 10), padx=(0, 20), sticky="ew")

        self.register_button = Button(self, text="Register", command=self.register,bootstyle=SUCCESS)
        self.register_button.grid(row=5, column=1, pady=(0, 10), padx=(0, 20), sticky="w")

        self.back_button = Button(self, text="Back", command=self.go_to_login,bootstyle=PRIMARY)
        self.back_button.grid(row=6, column=1, pady=(0, 10), padx=(0, 20), sticky="w")

    @performance_logger_decorator("RegisterFrame")
    def register(self):
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        response = self.user_business_logic.register(firstname, lastname, username, password)

        if response.success:
            messagebox.showinfo(title="Info", message=response.message)
        else:
            messagebox.showerror(title="Error", message=response.message)

    @performance_logger_decorator("RegisterFrame")
    def go_to_login(self):
        self.main_view.switch_frame("login")
