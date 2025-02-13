import sqlite3
from CommonLayer.Decorators.Performance_logger import performance_logger_decorator
from . import sqlite_database_name
from CommonLayer.Entities.user import User
from CommonLayer.Entities.role import Role


class UserDataAccess:
    @performance_logger_decorator("UserDataAccess")
    def get_user(self, username, password):
        with sqlite3.connect(sqlite_database_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT id,
                   first_name,
                   last_name,
                   username,
                   status,
                   role_id
            FROM   User
            Where  username = '{username}'
            AND    password = '{password}'""")

            data = cursor.fetchone()

            if data:
                return User(data[0], data[1], data[2], data[3], None, data[4], data[5])

    @performance_logger_decorator("UserDataAccess")
    def insert_user(self, firstname, lastname, username, password, status, role_id):
        with sqlite3.connect(sqlite_database_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""
            INSERT INTO User (
                     first_name,
                     last_name,
                     username,
                     password,
                     status,
                     role_id
                 )
                 VALUES (
                     '{firstname}',
                     '{lastname}',
                     '{username}',
                     '{password}',
                     {status},
                     {role_id}
                 );""")
            connection.commit()

    @performance_logger_decorator("UserDataAccess")
    def get_role_list(self):
        role_list=[]
        with sqlite3.connect(sqlite_database_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT title
            FROM   Role;""")
            data_list = cursor.fetchall()

            for data in data_list:
                role = Role(data[0])
                role_list.append(role)

        return role_list

    @performance_logger_decorator("UserDataAccess")
    def get_user_list(self,page,limit):
        user_list = []
        offset=(page-1)*limit
        with sqlite3.connect(sqlite_database_name) as connection:
            cursor = connection.cursor()
            query="""
            SELECT id,
                   first_name,
                   last_name,
                   username,
                   status,
                   role_id
            FROM   User
            Where  role_id != 1
            LIMIT ? OFFSET ? 
            """
            cursor.execute(query,(limit,offset))
            data_list = cursor.fetchall()

            for data in data_list:
                user = User(data[0], data[1], data[2], data[3], None, data[4], data[5])
                user_list.append(user)


        return user_list

    @performance_logger_decorator("UserDataAccess")
    def get_number_of_records(self):
        with sqlite3.connect(sqlite_database_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""
                        SELECT count(*) as no FROM User
                        Where  role_id != 1 """)
            data_row = cursor.fetchone()
            no_rec = data_row[0]
        return no_rec

    @performance_logger_decorator("UserDataAccess")
    def update_status(self, user_id, new_status):
        with sqlite3.connect(sqlite_database_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""
            UPDATE User
            SET status = {new_status}       
            WHERE id   = {user_id} """)

            connection.commit()

    @performance_logger_decorator("UserDataAccess")
    def change_role(self, user_id, new_role):
        with sqlite3.connect(sqlite_database_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""
            UPDATE User
            SET role_id = {new_role}       
            WHERE id   = {user_id} """)

            connection.commit()

    @performance_logger_decorator("UserDataAccess")
    def search(self,searched_text):
        user_searched_list=[]
        with sqlite3.connect(sqlite_database_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT id,
                   first_name,
                   last_name,
                   username,
                   status,
                   role_id
            FROM   User
            Where  role_id != 1       AND
                 (  username LIKE ?    OR
                   last_name LIKE ?   OR
                   first_name LIKE ? )
        """,(f"%{searched_text}%",f"%{searched_text}%",f"%{searched_text}%"))

            data_list = cursor.fetchall()
            for data in data_list:
                user = User(data[0], data[1], data[2], data[3], None, data[4], data[5])
                user_searched_list.append(user)
        return user_searched_list