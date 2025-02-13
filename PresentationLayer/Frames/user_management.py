from tkinter import Frame, Label, Entry, Button, messagebox
from BusinessLogicLayer.user_business_logic import UserBusinessLogic
from tkinter.ttk import Treeview
from ttkbootstrap import Button, SUCCESS,  DANGER, INFO, Label,PRIMARY
from CommonLayer.Decorators.Performance_logger import performance_logger_decorator

class UserManagementFrame(Frame):
    def __init__(self, window, main_view):
        super().__init__(window)
        self.user_business_logic = UserBusinessLogic()
        self.main_view = main_view
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.header = Label(self, text="User Management Page",bootstyle=INFO)
        self.header.grid(row=0, column=0, columnspan=4, pady=10)


        self.search_entry = Entry(self)
        self.search_entry.grid(row=1, column=0, columnspan=3, pady=(0, 10), padx=10, sticky="ew")


        self.search_button = Button(self, text="Search",command=self.search,bootstyle=INFO)
        self.search_button.grid(row=1, column=3, pady=(0, 10), padx=(0, 10))

        self.active_button = Button(self, text="Active", command=self.active_user,bootstyle=SUCCESS)
        self.active_button.grid(row=2, column=0, pady=(0, 10), padx=10)

        self.deactive_button = Button(self, text="Deative",command=self.deactive_user,bootstyle=DANGER)
        self.deactive_button.grid(row=2, column=1, pady=(0, 10), padx=10)

        self.pending_button = Button(self, text="Pending",command=self.pending_user,bootstyle=PRIMARY)
        self.pending_button.grid(row=2, column=2, pady=(0, 10), padx=10)

        self.change_role_button = Button(self, text="Change Role",command=self.change_role,bootstyle=INFO)
        self.change_role_button.grid(row=2, column=3, pady=(0, 10), padx=10)

        self.user_treeview = Treeview(self, columns=("firstname", "lastname", "username", "status", "role"),bootstyle=PRIMARY)

        self.back_button = Button(self, text="Back", command=self.go_to_home,bootstyle=INFO)
        self.back_button.grid(row=5, column=0,pady=(0, 10),padx=10, sticky="w")

        self.pagination_frame = Frame(self)


        self.previous_button = Button(self.pagination_frame, text="Previous",command= self.previous_page,bootstyle=INFO)

        self.current_page=1
        self.rows_per_page=10
        self.total_pages = self.user_business_logic.count_total_pages()

        self.page_label = Label(self.pagination_frame, text=f"Page {self.current_page} of {self.total_pages}",bootstyle=INFO)

        self.next_button = Button(self.pagination_frame, text="Next", command=self.next_page,bootstyle=INFO)

        self.row_list = []
        self.current_user=None
        self.change_role_button.config(state="disabled")
        self.user_treeview.bind("<<TreeviewSelect>>", self.manage_buttons)

    @performance_logger_decorator("UserManagementFrame")
    def display(self,offset):
        self.user_treeview.grid(row=3, column=0, columnspan=4, pady=(0, 10), padx=10, sticky="nsew")
        self.user_treeview.heading("#0", text="NO")
        self.user_treeview.heading("firstname", text="First Name")
        self.user_treeview.heading("lastname", text="Last Name")
        self.user_treeview.heading("username", text="Username")
        self.user_treeview.heading("status", text="Status")
        self.user_treeview.heading("role", text="Role")
        self.user_treeview.column("#0", width=70)
        self.next_button.grid(row=0, column=2, padx=10)
        self.page_label.grid(row=0, column=1, padx=10)
        self.previous_button.grid(row=0, column=0, padx=10)
        self.pagination_frame.grid(row=4, column=0, columnspan=4, pady=(0, 10), sticky="ew")

    @performance_logger_decorator("UserManagementFrame")
    def set_current_user(self, user):
        self.current_user=user
        response = self.user_business_logic.get_user_management_list(user,int(self.current_page),int(self.rows_per_page))
        if response.success:
            user_list = response.data
            self.load_data_treeview(user_list)
        else:
            messagebox.showerror(title="Error", message=response.message)
            self.main_view.switch_frame("login")

    @performance_logger_decorator("UserManagementFrame")
    def load_data_treeview(self, user_list):
        for row in self.row_list:
            self.user_treeview.delete(row)
        self.row_list.clear()

        row_number = 1 + (self.current_page - 1) * self.rows_per_page
        for user in user_list:
            row = self.user_treeview.insert("", "end", iid=user.id, text=str(row_number), values=(user.first_name,
                                                                                                  user.last_name,
                                                                                                  user.username,
                                                                                                  user.get_status(),
                                                                                                  user.get_role()))
            self.row_list.append(row)
            row_number += 1

        self.display(0)
        self.page_label.config(text=f"Page {self.current_page} of {self.total_pages}",bootstyle=INFO)
        self.previous_button.config(state="normal" if self.current_page > 1 else "disabled")
        self.next_button.config(state="normal" if self.current_page < self.total_pages else "disabled")

    @performance_logger_decorator("UserManagementFrame")
    def previous_page(self):
        response = self.user_business_logic.get_user_management_list(self.current_user,int(self.current_page),int(self.rows_per_page))
        if response.success and self.current_page > 1 :
            self.current_page -= 1
            '''user_list = response.data
            self.load_data_treeview(user_list)'''
            self.update_table()
        else:
            messagebox.showerror(title="Error", message=response.message)
            self.main_view.switch_frame("login")

    @performance_logger_decorator("UserManagementFrame")
    def next_page(self):
        response = self.user_business_logic.get_user_management_list(self.current_user,int(self.current_page),int(self.rows_per_page))
        if response.success and self.current_page < self.total_pages:
            self.current_page += 1
            '''user_list = response.data
            self.load_data_treeview(user_list)'''
            self.update_table()
        else:
            messagebox.showerror(title="Error", message=response.message)
            self.main_view.switch_frame("login")

    @performance_logger_decorator("UserManagementFrame")
    def update_table(self):
        response = self.user_business_logic.get_user_management_list(self.current_user,int(self.current_page),int(self.rows_per_page))
        if response.success:
            user_list = response.data
            self.load_data_treeview(user_list)
        else:
            messagebox.showerror(title="Error", message=response.message)

    @performance_logger_decorator("UserManagementFrame")
    def active_user(self):
        id_list = self.user_treeview.selection()
        self.user_business_logic.active_user(id_list)

        response = self.user_business_logic.get_user_management_list(self.current_user,int(self.current_page),int(self.rows_per_page))
        if response.success:
            user_list = response.data
            self.load_data_treeview(user_list)
        else:
            messagebox.showerror(title="Error", message=response.message)
            self.main_view.switch_frame("login")

    @performance_logger_decorator("UserManagementFrame")
    def pending_user(self):
        id_list = self.user_treeview.selection()
        self.user_business_logic.pending_user(id_list)

        response = self.user_business_logic.get_user_management_list(self.current_user,int(self.current_page),int(self.rows_per_page))
        if response.success:
            user_list = response.data
            self.load_data_treeview(user_list)
        else:
            messagebox.showerror(title="Error", message=response.message)
            self.main_view.switch_frame("login")

    @performance_logger_decorator("UserManagementFrame")
    def deactive_user(self):
        id_list =self.user_treeview.selection()
        self.user_business_logic.deactive_user(id_list)

        response = self.user_business_logic.get_user_management_list(self.current_user,int(self.current_page),int(self.rows_per_page))
        if response.success:
            user_list = response.data
            self.load_data_treeview(user_list)
        else:
            messagebox.showerror(title="Error", message=response.message)
            self.main_view.switch_frame("login")

    @performance_logger_decorator("UserManagementFrame")
    def change_role(self):
        selection=self.user_treeview.selection()
        if not selection:
            messagebox.showerror(title="Error",message="No user selected")
            return
        update_role_id = int(selection[0])
        self.main_view.switch_frame("change_role",update_role_id=update_role_id)
        response = self.user_business_logic.get_user_management_list(self.current_user,int(self.current_page),int(self.rows_per_page))
        if response.success:
            user_list = response.data
            self.load_data_treeview(user_list)
        else:
            messagebox.showerror(title="Error", message=response.message)
            self.main_view.switch_frame("login")

    @performance_logger_decorator("UserManagementFrame")
    def search(self):
        searched_text = self.search_entry.get()
        response = self.user_business_logic.search(searched_text)
        if response.success:
            user_searched_list = response.data
            self.load_data_treeview(user_searched_list)
        self.search_entry.delete(0, "end")

    @performance_logger_decorator("UserManagementFrame")
    def go_to_home(self):
        self.main_view.switch_frame("home")

    @performance_logger_decorator("UserManagementFrame")
    def manage_buttons(self,event):
        select_count = len(self.user_treeview.selection())
        if select_count == 1:
            self.change_role_button.config(state="normal")
        else:
            self.change_role_button.config(state="disabled")



