import mysql.connector as mc
from .hash_password import PasswordHasher

import os
from dotenv import load_dotenv
from datetime import datetime
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
                        otp varchar(64)
                        );
        """)

        self.crs.execute("""
        create table if not exists reset_password_otp(
                        email varchar(256) primary key,
                        otp varchar(64)
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

        self.crs.execute("""
        create table if not exists used_otps(
                        otp varchar(64) primary key
                        );
        """)

        self.crs.execute("""
        create table if not exists threads(
                        thread_id int auto_increment primary key,
                        username varchar(256),
                        thread_name varchar(256)
                        );
        """)

        self.crs.execute("""
        create table if not exists thread_replies(
                        reply_id int auto_increment primary key,
                        thread_name varchar(256),
                        username varchar(256),
                        reply varchar(8192)
                        );
        """)

        self.crs.execute("""
        create table if not exists courses(
                        tuple_id int auto_increment primary key,
                        faculty_username varchar(256),
                        course_code varchar(256),
                        course_name varchar(256),
                        batch varchar(256)
                        );
        """)

        self.crs.execute("""
        create table if not exists students(
                        student_username varchar(256) primary key,
                        mac_address varchar(32)
                        );
        """)

        self.crs.execute("""
        create table if not exists attendance(
                        tuple_id int auto_increment primary key,
                        course_code varchar(256),
                        batch varchar(256),
                        student_username varchar(256),
                        attendance int,
                        total_classes int
                        );
        """)

        self.crs.execute("""
        create table if not exists logs(
                        log_id int auto_increment primary key,
                        date date,
                        time time,
                        username varchar(256),
                        api_endpoint varchar(256),
                        status_code int,
                        ip_address varchar(32),
                        os varchar(32),
                        os_version varchar(32),
                        architecture varchar(32),
                        python_version varchar(32),
                        hostname varchar(256),
                        processor varchar(256),
                        description varchar(1024) default null
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

        if(result and PasswordHasher.check_password_bcrypt(otp, result[0])):
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

        if(result and PasswordHasher.check_password_bcrypt(otp, result[0])):
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
        
    def if_thread_exists(self, thread_name):
        
        self.crs.execute("""
        select * from threads where thread_name = %s;
        """, (thread_name,))

        result = self.crs.fetchone()

        if(result):
            return True
        else:
            return False
        
    def create_thread(self, username, thread_name):
        
        self.crs.execute("""
        insert into threads(username, thread_name) values (%s, %s);
        """, (username, thread_name))

    def post_reply(self, thread_name, username, reply):
        
        self.crs.execute("""
        insert into thread_replies(thread_name, username, reply) values (%s, %s, %s);
        """, (thread_name, username, reply))

    def list_threads(self):
        
        self.crs.execute("""
        select username, thread_name from threads;
        """)

        result = self.crs.fetchall()

        return result
    
    def delete_thread(self, thread_name):
            
        self.crs.execute("""
        delete from threads where thread_name = %s;
        """, (thread_name,))

        self.crs.execute("""
        delete from thread_replies where thread_name = %s;
        """, (thread_name,))
    
    def list_replies(self, thread_name):
        
        self.crs.execute("""
        select username, reply from thread_replies where thread_name = %s;
        """, (thread_name,))

        result = self.crs.fetchall()

        return result
    
    def course_exists(self, username, course_code, course_name, batch):

        self.crs.execute("""
        select * from courses where faculty_username = %s and course_code = %s and course_name = %s and batch = %s;
        """, (username, course_code, course_name, batch))

        result = self.crs.fetchone()

        if(result):
            return True
        else:
            return False
        
    def add_course(self, username, course_code, course_name, batch):
        
        self.crs.execute("""
        insert into courses(faculty_username, course_code, course_name, batch) values (%s, %s, %s, %s);
        """, (username, course_code, course_name, batch))

    def list_courses(self, username):
        
        self.crs.execute("""
        select course_name, course_code, batch from courses where faculty_username = %s;
        """, (username,))

        result = self.crs.fetchall()

        return result
    
    def student_exists(self, student_username, course_code, batch):

        self.crs.execute("""
        select * from attendance where student_username = %s and course_code = %s and batch = %s;
        """, (student_username, course_code, batch))

        result = self.crs.fetchone()

        if(result):
            return True
        else:
            return False
        
    def add_student(self, course_code, batch, student_username, mac_address):
        
        self.crs.execute("""
        select * from students where student_username = %s and mac_address = %s;
        """, (student_username, mac_address))

        if(not self.crs.fetchone()):
            self.crs.execute("""
            insert into students values (%s, %s);
            """, (student_username, mac_address))

        self.crs.execute("""
        insert into attendance(course_code, batch, student_username, attendance, total_classes) values (%s, %s, %s, 0, 0);
        """, (course_code, batch, student_username))

    def list_students(self, course_code, batch):
        
        self.crs.execute("""
        select student_username, mac_address from students natural join attendance where course_code = %s and batch = %s;
        """, (course_code, batch))

        result = self.crs.fetchall()

        return result

    def mark_attendance(self, course_code, batch, students):
        
        for student, attendance in students.items():
            if(attendance):
                self.crs.execute("""
                update attendance set attendance = attendance + 1 where course_code = %s and batch = %s and student_username = %s;
                """, (course_code, batch, student))

        self.crs.execute("""
        update attendance set total_classes = total_classes + 1 where course_code = %s and batch = %s;
        """, (course_code, batch))

    def list_attendance(self, username):
            
            self.crs.execute("""
            select c.course_name, a.course_code, a.batch, a.attendance, a.total_classes
                            from attendance a inner join courses c 
                            on a.course_code = c.course_code 
                            where student_username = %s;
            """, (username,))
    
            result = self.crs.fetchall()
            return result
    
    def free_otps_if_required(self, lower_bound, upper_bound):
        
        self.crs.execute("""
        select count(*) from used_otps;
        """)

        result = self.crs.fetchone()

        total_otps = upper_bound - lower_bound + 1
        used_otps = result[0]

        if(used_otps/total_otps > 0.75):
            print("reaching here...")
            self.crs.execute("""
            delete from used_otps;
            """)

    def registration_otp_exists(self, otp):
            
            self.crs.execute("""
            select * from used_otps;
            """,)

            for result in self.crs.fetchall():
                if(PasswordHasher.check_password_bcrypt(otp, result[0])):
                    return True

            return False
    
    def remember_otp(self, opt):
        self.crs.execute("""
        insert into used_otps values (%s);
        """, (PasswordHasher.hash_password_bcrypt(opt),))

    def save_log(self, username, api_endpoint, status_code, ip_address,  os, os_version, architecture, python_version, hostname, processor, description):

        current_datetime = datetime.now()
        current_date = current_datetime.date()
        current_time = current_datetime.time()

        self.crs.execute("""
        insert into logs(date, time, username, api_endpoint, status_code, ip_address, os, os_version, architecture, python_version, hostname, processor, description) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);  
        """, (current_date, current_time, username, api_endpoint, status_code, ip_address,  os, os_version, architecture, python_version, hostname, processor, description))

    def faculty_coursecode_batch_combination_exists(self, username, course_code, batch):
        
        self.crs.execute("""
        select * from courses where faculty_username = %s and course_code = %s and batch = %s;
        """, (username, course_code, batch))

        result = self.crs.fetchone()
        if(result):
            return True
        else:
            return False

    def get_attendance_report(self, course_code, batch):
        
        self.crs.execute("""
        select student_username, attendance, total_classes from attendance where course_code = %s and batch = %s;
        """, (course_code, batch))

        result = self.crs.fetchall()

        return result

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