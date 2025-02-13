from tkinter import Frame, Label, Button, messagebox
from BusinessLogicLayer.user_business_logic import UserBusinessLogic
from tkinter.ttk import Combobox
from ttkbootstrap import Button, PRIMARY, SUCCESS, Label
from CommonLayer.Decorators.Performance_logger import performance_logger_decorator


class RoleFrame(Frame):
    def __init__(self, window, main_view):
        super().__init__(window)
        self.current_user = None
        self.user_business_logic = UserBusinessLogic()
        self.main_view = main_view
        self.update_role_id=None
        role_list = self.user_business_logic.get_role_management_list()
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.header = Label(self, text="Change Role Page",bootstyle=PRIMARY)
        self.header.grid(row=0, column=1,padx=10, pady=10,columnspan=2, sticky="w")
        self.label=Label(self,text="Select role",bootstyle=PRIMARY)
        self.label.grid(row=1, column=0,padx=10, pady=10, sticky="w")

        self.role_combobox=Combobox(self,values=role_list,state="readonly",bootstyle=PRIMARY)
        self.role_combobox.grid(row=2, column=0,padx=10, pady=10, sticky="w")
        self.save_button=Button(self,text="save",command=self.save,bootstyle=SUCCESS)
        self.save_button.grid(row=3, column=0, pady=10,padx=10, sticky="w")

    @performance_logger_decorator("RoleFrame")
    def initialize(self,update_role_id=None):
        self.update_role_id=update_role_id

    @performance_logger_decorator("RoleFrame")
    def save(self):
        title=self.role_combobox.get()
        if not title:
            messagebox.showerror(title="Error",message="Please select a role.")
            return

        if not self.update_role_id:
            messagebox.showerror(title="Error",message="No role id provided.")
            return

        self.user_business_logic.change_role(title,self.update_role_id)
        self.main_view.switch_frame("home")




