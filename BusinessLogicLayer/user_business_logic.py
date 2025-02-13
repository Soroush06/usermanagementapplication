from math import ceil
from CommonLayer.Model.response import Response
from DataAccessLayer.user_data_access import UserDataAccess
import hashlib
import sqlite3
from CommonLayer.Decorators.Performance_logger import performance_logger_decorator
import CommonLayer.State.user_state


class UserBusinessLogic:
    def __init__(self):
        self.user_data_access = UserDataAccess()

    @performance_logger_decorator("UserBusinessLogic")
    def login(self, username, password):
        # Invalid
        if len(username) < 3 or len(password) < 6:
            return Response(False, None, "Invalid username or password.")

        # Hash password
        password_hash = hashlib.md5(password.encode()).hexdigest()
        # Data access
        user = self.user_data_access.get_user(username, password_hash)

        if user:
            match user.status:
                case 0:
                    return Response(False, None, "Your account is deactived.")
                case 1:
                    CommonLayer.State.user_state.current_user_id=user.id
                    return Response(True, user, None)
                case 2:
                    return Response(False, None, "Pending.")
        else:
            return Response(False, None, "Invalid username or password(NotFound).")

    @performance_logger_decorator("UserBusinessLogic")
    def register(self, firstname, lastname, username, password):
        if len(firstname) < 3:
            return Response(False, None, "Invalid First Name.")

        if len(lastname) < 3:
            return Response(False, None, "Invalid Last Name.")

        if len(username) < 3:
            return Response(False, None, "Invalid username.")

        if len(password) < 6:
            return Response(False, None, "Invalid password.")

        # Hash password
        password_hash = hashlib.md5(password.encode()).hexdigest()

        # Save to database
        try:
            self.user_data_access.insert_user(firstname, lastname, username, password_hash, 2, 2)
        except sqlite3.IntegrityError as error:
            # if "username" in error.args[0]:
            return Response(False, None, "Username exist.")
        else:
            return Response(True, None, "Register successfully.")

    @performance_logger_decorator("UserBusinessLogic")
    def get_user_management_list(self, current_user,page,rows_per_page=10):
        #offset=(page-1)*rows_per_page
        if current_user.role_id == 1:
            user_list = self.user_data_access.get_user_list(page,rows_per_page)
            return Response(True, user_list, None)
        else:
            return Response(False, None, "Access denied.")

    @performance_logger_decorator("UserBusinessLogic")
    def count_total_pages(self):
        no_rec=self.user_data_access.get_number_of_records()
        total_pages=ceil(no_rec/10)
        return total_pages

    @performance_logger_decorator("UserBusinessLogic")
    def get_role_management_list(self):
        role_list = self.user_data_access.get_role_list()
        return role_list

    @performance_logger_decorator("UserBusinessLogic")
    def active_user(self, id_list):
        for id in id_list:
            self.user_data_access.update_status(id, 1)

    @performance_logger_decorator("UserBusinessLogic")
    def pending_user(self, id_list):
        for id in id_list:
            self.user_data_access.update_status(id, 2)

    @performance_logger_decorator("UserBusinessLogic")
    def deactive_user(self, id_list):
        for id in id_list:
            self.user_data_access.update_status(id, 0)

    @performance_logger_decorator("UserBusinessLogic")
    def search(self,searched_text):
        user_searched_list = self.user_data_access.search(searched_text)
        return Response(True, user_searched_list, None)

    @performance_logger_decorator("UserBusinessLogic")
    def change_role(self,title,id):
        if title=="Admin":
            self.user_data_access.change_role(id, 1)
        else:
            self.user_data_access.change_role(id, 2)




