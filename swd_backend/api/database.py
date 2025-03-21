import mysql.connector as mc
from .hash_password import PasswordHasher

import os
from dotenv import load_dotenv
load_dotenv()

HOSTED_DB = False

class Database:

    def __init__(self, host="localhost", port=3306,  user="root", password="root", database="swd_project", autocommit=True, auth_plugin = "mysql_native_password"):
        
        if(HOSTED_DB):
            host = os.getenv("DB_HOST")
            port = os.getenv("DB_PORT")
            user = os.getenv("DB_USER")
            password = os.getenv("DB_PASSWORD")
            database = os.getenv("DB_NAME")

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.autocommit = autocommit
        self.auth_plugin = auth_plugin
        self.hdl = mc.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                              database=self.database, autocommit=self.autocommit, auth_plugin = self.auth_plugin)
        self.crs = self.hdl.cursor()

    def create_tables(self):
        self.crs.execute("""
        create table if not exists registration_otp(
                        email varchar(256) primary key,
                        otp int
                        );
        """)

        self.crs.execute("""
        create table if not exists reset_password_otp(
                        email varchar(256) primary key,
                        otp int
                        );
        """)

        self.crs.execute("""
        create table if not exists user_credentials(
                        username varchar(256) primary key,
                        password varchar(64),
                        email varchar(256),
                        is_student boolean,
                        session_id varchar(36)
                        );
        """)


    def save_registration_otp(self, email, otp):

        self.crs.execute("""
        select * from registration_otp where email = %s;
        """, (email,))

        result = self.crs.fetchone()

        if(result):
            self.crs.execute("""
            update registration_otp set otp = %s where email = %s; 
            """, (otp, email))
        else:
            self.crs.execute("""
            insert into registration_otp values (%s, %s);
            """, (email, otp))

    def user_exists(self, username):
        
        self.crs.execute("""
            select * from user_credentials where username = %s;
            """, (username,))
        
        result = self.crs.fetchone()

        if(result):
            return True
        else:
            return False

    def email_exists(self, email):

        self.crs.execute("""
            select * from user_credentials where email = %s;
            """, (email,))
        
        result = self.crs.fetchone()

        if(result):
            return True 
        else:
            return False
        

    def valid_registration_otp(self, email, otp):

        self.crs.execute("""
        select otp from registration_otp where email = %s;
        """, (email,))

        result = self.crs.fetchone()

        if(result and result[0] == otp):
            return True
        else:
            return False

    def register(self, username, password, email, is_student):

        if(is_student):
            is_student = 1
        else:
            is_student = 0

        self.crs.execute("""
        insert into user_credentials values (%s, %s, %s, %s, NULL);
        """, (username, password, email, is_student))
    
    def authenticate(self, username, password):
        
        self.crs.execute("""
        select password from user_credentials where username = %s;
        """, (username,))

        result = self.crs.fetchone()

        if(result and PasswordHasher.check_password_bcrypt(password, result[0])):
            return True
        else:
            return False
        
    def user_email_combination_exists(self, username, email):
        
        self.crs.execute("""
        select * from user_credentials where username = %s and email = %s;
        """, (username, email))

        result = self.crs.fetchone()

        if(result):
            return True
        else:
            return False
        
    def save_reset_password_otp(self, email, otp):

        self.crs.execute("""
        select * from reset_password_otp where email = %s;
        """, (email,))

        result = self.crs.fetchone()

        if(result):
            self.crs.execute("""
            update reset_password_otp set otp = %s where email = %s;
            """, (otp, email))
        else:
            self.crs.execute("""
            insert into reset_password_otp values (%s, %s);
            """, (email, otp))
    
    def reset_password(self, username, new_password):
        
        self.crs.execute("""
        update user_credentials set password = %s where username = %s;
        """, (new_password, username))    

    def valid_reset_password_otp(self, email, otp):
        
        self.crs.execute("""
        select otp from reset_password_otp where email = %s;
        """, (email,))

        result = self.crs.fetchone()

        if(result and result[0] == otp):
            return True
        else:
            return False
        
    def is_student(self, username):
        
        self.crs.execute("""
        select is_student from user_credentials where username = %s;
        """, (username,))

        result = self.crs.fetchone()

        if(result and result[0]):
            return True
        else:
            return False
        
    def clear_otp(self, email, otp_type):
        
        if (otp_type == "registration"):
            self.crs.execute("""
            delete from registration_otp where email = %s;
            """, (email,))
        
        elif (otp_type == "reset_password"):
            self.crs.execute("""
            delete from reset_password_otp where email = %s;
            """, (email,))

    def user_email_combination_exists(self, username, email):
        
        self.crs.execute("""
        select * from user_credentials where username = %s and email = %s;
        """, (username, email))

        result = self.crs.fetchone()

        if(result):
            return True
        else:
            return False
        
    def save_session_id(self, username, session_id):
        
        self.crs.execute("""
        update user_credentials set session_id = %s where username = %s;
        """, (session_id, username))

    def valid_session_id(self, username, session_id):
        
        self.crs.execute("""
        select session_id from user_credentials where username = %s;
        """, (username,))

        result = self.crs.fetchone()

        print(result)

        if(result and result[0] == session_id):
            return True
        else:
            return False
        
    def clear_session_id(self, username):
        
        self.crs.execute("""
        update user_credentials set session_id = NULL where username = %s;
        """, (username,))

    def valid_session_id(self, username, session_id):
        
        self.crs.execute("""
        select session_id from user_credentials where username = %s;
        """, (username,))

        result = self.crs.fetchone()

        if(result and result[0] == session_id):
            return True
        else:
            return False
        
    def close(self):
        self.hdl.close()

    def delete_tables(self):
        self.crs.execute("drop table registration_otp;")
        self.crs.execute("drop table reset_password_otp;")
        self.crs.execute("drop table user_credentials;")

def main():
    database = Database()
    database.delete_tables()
    database.close()

if (__name__ == "__main__"):
    main()