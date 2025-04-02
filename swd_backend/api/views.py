from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status
from .serializers import *
import os
from django.conf import settings
from django.http import HttpResponse
import uuid

import random as rd
from .email_sender import Email
from .database import Database
from .hash_password import PasswordHasher

def get_client_ip(request):
    # Check if the request is behind a proxy
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # If there are multiple IPs in the header, take the first one
        ip = x_forwarded_for.split(',')[0]
    else:
        # Fallback to the remote address
        ip = request.META.get('REMOTE_ADDR')
    return ip

class GenerateRegistrationOtpAPIView(APIView):

    def post(self, request):
        
        database = Database()
        database.create_tables()
        serializer = GenerateRegistrationOtpSerializer(data = request.data)

        if(serializer.is_valid()):
            
            try:
                email = Email()


                if(database.email_exists(request.data["email"])):

                    database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                    database.close()
                    return Response({"message": "Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
                
                database.free_otps_if_required(100000, 999999)

                while(True):
                    otp = rd.randint(100000, 999999)
                    if(not database.registration_otp_exists(str(otp))):
                        break
                                      
                database.remember_otp(str(otp))

                database.save_registration_otp(request.data["email"], PasswordHasher.hash_password_bcrypt(str(otp)))
                email.send_email(
                    subject = "Registration OTP",
                    body = "Your Registration OTP is " + str(otp),
                    to_email = request.data["email"]
                )

                email.close()

                database.save_log("anonymous", request.path, status.HTTP_201_CREATED, get_client_ip(request), "null")
                database.close()
                return Response({"message": "OTP sent successfully!"}, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                print(f"Exception -> {e}")
                database.save_log("anonymous", request.path, status.HTTP_500_INTERNAL_SERVER_ERROR, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Failed to generate OTP."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
        database.close()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationAPIView(APIView):

    def post(self, request):

        database = Database()
        database.create_tables()
        serializer = RegistrationSerializer(data = request.data)

        if(serializer.is_valid()):


            if(database.user_exists(request.data["username"])):
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "User already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            
            if(database.email_exists(request.data["email"])):
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            
            if(not database.valid_registration_otp(request.data["email"], str(request.data["otp"]))):
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Incorrect OTP!"}, status=status.HTTP_400_BAD_REQUEST)

            hashed_password = PasswordHasher.hash_password_bcrypt(request.data["password"])

            database.clear_otp(request.data["email"], "registration")
            database.register(request.data["username"], hashed_password, request.data["email"], request.data["is_student"])
            
            database.save_log(request.data["username"], request.path, status.HTTP_201_CREATED, get_client_ip(request), "null")
            database.close()
            return Response({"message": "Registered successfully!"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(APIView):
    def post(self, request):
        
        database = Database()
        database.create_tables()
        serializer = LoginSerializer(data = request.data)

        if(serializer.is_valid()):

            
            if(database.authenticate(request.data["username"], request.data["password"])):
                is_student = database.is_student(request.data["username"])
                session_id = str(uuid.uuid4())
                database.save_session_id(request.data["username"], session_id)
                
                database.save_log(request.data["username"], request.path, status.HTTP_200_OK, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Logged in successfully!", 
                                 "username" : request.data["username"], 
                                 "is_student" : is_student,
                                 "session_id" : session_id}, 
                                 status=status.HTTP_200_OK)
            else:
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenerateResetPasswordAPIView(APIView):

    def post(self, request):
        
        database = Database()
        database.create_tables()
        serializers = GenerateResetPasswordOtpSerializer(data = request.data)

        if(serializers.is_valid()):
            email = Email()


            if(database.user_email_combination_exists(request.data["username"], request.data["email"])):

                database.free_otps_if_required(100000, 999999)

                while(True):
                    otp = rd.randint(100000, 999999)
                    if(not database.registration_otp_exists(str(otp))):
                        break
                                      
                database.remember_otp(str(otp))

                database.save_reset_password_otp(request.data["email"], PasswordHasher.hash_password_bcrypt(str(otp)))
                email.send_email(
                    subject = "Reset Password OTP",
                    body = "Your Reset Password OTP is " + str(otp),
                    to_email = request.data["email"]
                )

                
                database.close()
            
            else:
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid Details"}, status=status.HTTP_400_BAD_REQUEST)

            database.save_log("anonymous", request.path, status.HTTP_201_CREATED, get_client_ip(request), "null")
            database.close()
            return Response({"message": "OTP sent successfully!"}, status=status.HTTP_201_CREATED)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordAPIView(APIView):

    def post(self, request):
        
        database = Database()
        database.create_tables()
        serializers = ResetPasswordSerializer(data = request.data)

        if(serializers.is_valid()):

            if(not database.valid_reset_password_otp(request.data["email"], str(request.data["otp"]))):
                
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Incorrect OTP!"}, status=status.HTTP_400_BAD_REQUEST)
            
            elif(not database.user_email_combination_exists(request.data["username"], request.data["email"])):
                
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid Details!"}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                database.clear_otp(request.data["email"], "reset_password")
                database.reset_password(request.data["username"], PasswordHasher.hash_password_bcrypt(request.data["new_password"]))
                database.save_log(request.data["username"], request.path, status.HTTP_200_OK, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Password reset successfully!"}, status=status.HTTP_200_OK)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):

    def post(self, request):
        
        database = Database()
        database.create_tables()
        serializers = LogoutSerializer(data = request.data)

        if(serializers.is_valid()):
            
            if(database.valid_session_id(request.data["username"], request.data["session_id"])):
                database.clear_session_id(request.data["username"])
                
                database.save_log(request.data["username"], request.path, status.HTTP_200_OK, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Logged out successfully!"}, status=status.HTTP_200_OK)
            else:
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid session id!"}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class FileUploadAPIView(APIView):

    def post(self, request):

        database = Database()
        database.create_tables()
        serializers = FileUploadSerializer(data = request.data)

        if(serializers.is_valid()):

            if(database.valid_session_id(request.data["username"], request.data["session_id"]) == False):
                
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid session id!"}, status=status.HTTP_400_BAD_REQUEST)
            
            uploaded_file = request.FILES["file"]

            save_path = os.path.join(settings.UPLOADED_DOCS, request.data["username"], uploaded_file.name)
            os.makedirs(os.path.dirname(save_path), exist_ok = True)

            if(os.path.exists(save_path)):
                database.save_log(request.data["username"], request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "File already exists!"}, status=status.HTTP_400_BAD_REQUEST)

            with open(save_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            database.save_log(request.data["username"], request.path, status.HTTP_201_CREATED, get_client_ip(request), "null")
            database.close()
            return Response({"message": "File uploaded successfully!", "file_name": uploaded_file.name}, status = status.HTTP_201_CREATED)

        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response({"message": str(serializers.errors["file"][0])}, status=status.HTTP_400_BAD_REQUEST)
        
class FileDownloadAPIView(APIView):

    def post(self, request):

        database = Database()
        database.create_tables()
        serializers = FileDownloadSerializer(data = request.data)

        if(serializers.is_valid()):

            if(database.valid_session_id(request.data["username"], request.data["session_id"]) == False):
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid session id!"}, status=status.HTTP_400_BAD_REQUEST)
        
            file_path = os.path.join(settings.UPLOADED_DOCS, request.data["username"], request.data["file_name"])

            if(os.path.exists(file_path)):
                with open(file_path, "rb") as file:
                    file_data = file.read() # Read file data

                database.save_log(request.data["username"], request.path, status.HTTP_200_OK, get_client_ip(request), "null")
                database.close()
                return HttpResponse(file_data, status = status.HTTP_200_OK) 
                   
            else:
                database.save_log(request.data["username"], request.path, status.HTTP_404_NOT_FOUND, get_client_ip(request), "null")
                database.close()
                return Response({"message": "File not found!"}, status = status.HTTP_404_NOT_FOUND)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
class FileDeleteAPIView(APIView):

    def post(self, request):
      
        database = Database()
        database.create_tables()
        serializers = FileDownloadSerializer(data = request.data)

        if(serializers.is_valid()):

            if(database.valid_session_id(request.data["username"], request.data["session_id"]) == False):
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid session id!"}, status=status.HTTP_400_BAD_REQUEST)
            
            file_path = os.path.join(settings.UPLOADED_DOCS, request.data["username"], request.data["file_name"])

            if(os.path.exists(file_path)):
                os.remove(file_path)
                database.save_log(request.data["username"], request.path, status.HTTP_200_OK, get_client_ip(request), "null")
                database.close()
                return Response({"message": "File deleted successfully!"}, status = status.HTTP_200_OK)
                   
            else:
                database.save_log(request.data["username"], request.path, status.HTTP_404_NOT_FOUND, get_client_ip(request), "null")
                database.close()
                return Response({"message": "File not found!"}, status = status.HTTP_404_NOT_FOUND)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
class FileListAPIView(APIView):

    def post(self, request):

        database = Database()
        database.create_tables()
        serializers = FileListSerializer(data = request.data)

        if(serializers.is_valid()):

            if(database.valid_session_id(request.data["username"], request.data["session_id"]) == False):
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid session id!"}, status=status.HTTP_400_BAD_REQUEST)
        
            user_dir = os.path.join(settings.UPLOADED_DOCS, request.data["username"])

            if(os.path.exists(user_dir)):
                files = os.listdir(user_dir)
                database.save_log(request.data["username"], request.path, status.HTTP_200_OK, get_client_ip(request), "null")
                database.close()
                return Response({"files": files}, status = status.HTTP_200_OK)
                   
            else:
                database.save_log(request.data["username"], request.path, status.HTTP_200_OK, get_client_ip(request), "null")
                database.close()
                return Response({"files": []}, status = status.HTTP_200_OK)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateThreadAPIView(APIView):

    def post(self, request):

        database = Database()
        database.create_tables()
        serializers = CreateThreadSerializer(data = request.data)

        if(serializers.is_valid()):

            if(database.valid_session_id(request.data["username"], request.data["session_id"]) == False):
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid session id!"}, status=status.HTTP_400_BAD_REQUEST)

            if(database.if_thread_exists(request.data["thread_name"])):
                database.save_log(request.data["username"], request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Thread already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            
            database.create_thread(request.data["username"], request.data["thread_name"])
            
            database.save_log(request.data["username"], request.path, status.HTTP_201_CREATED, get_client_ip(request), "null")
            database.close()
            return Response({"message": "Thread created successfully!"}, status = status.HTTP_201_CREATED)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PostReplyAPIView(APIView):

    def post(self, request):

        database = Database()
        database.create_tables()
        serializers = PostReplySerializer(data = request.data)

        if(serializers.is_valid()):

            if(database.valid_session_id(request.data["username"], request.data["session_id"]) == False):
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid session id!"}, status=status.HTTP_400_BAD_REQUEST)
            
            database.post_reply(request.data["thread_name"], request.data["username"], request.data["reply"])
            
            database.save_log(request.data["username"], request.path, status.HTTP_201_CREATED, get_client_ip(request), "null")
            database.close()
            return Response({"message": "Reply posted successfully!"}, status = status.HTTP_201_CREATED)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ListThreadsAPIView(APIView):

    def post(self, request):

        database = Database()
        database.create_tables()
        serializers = ListThreadsSerializer(data = request.data)

        if(serializers.is_valid()):

            if(database.valid_session_id(request.data["username"], request.data["session_id"]) == False):
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid session id!"}, status=status.HTTP_400_BAD_REQUEST)
            
            threads = database.list_threads()

            database.save_log(request.data["username"], request.path, status.HTTP_200_OK, get_client_ip(request), "null")
            database.close()
            return Response({"threads": threads}, status = status.HTTP_200_OK)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ListRepliesAPIView(APIView):

    def post(self, request):

        database = Database()
        database.create_tables()
        serializers = ListRepliesSerializer(data = request.data)

        if(serializers.is_valid()):

            if(database.valid_session_id(request.data["username"], request.data["session_id"]) == False):
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid session id!"}, status=status.HTTP_400_BAD_REQUEST)
            
            replies = database.list_replies(request.data["thread_name"])
            
            database.save_log(request.data["username"], request.path, status.HTTP_200_OK, get_client_ip(request), "null")
            database.close()
            return Response({"replies": replies}, status = status.HTTP_200_OK)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteThreadAPIView(APIView):

    def post(self, request):

        database = Database()
        database.create_tables()
        serializers = DeleteThreadSerializer(data = request.data)

        if(serializers.is_valid()):

            if(database.valid_session_id(request.data["username"], request.data["session_id"]) == False):
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid session id!"}, status=status.HTTP_400_BAD_REQUEST)
            
            database.delete_thread(request.data["thread_name"])

            database.save_log(request.data["username"], request.path, status.HTTP_200_OK, get_client_ip(request), "null")
            database.close()

            return Response({"message": "Thread deleted successfully!"}, status = status.HTTP_200_OK)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AddCourseAPIView(APIView):

    def post(self, request):

        database = Database()
        database.create_tables()
        serializers = AddCourseSerializer(data = request.data)

        if(serializers.is_valid()):

            if(database.valid_session_id(request.data["username"], request.data["session_id"]) == False):
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid session id!"}, status=status.HTTP_400_BAD_REQUEST)
            
            if(database.course_exists(request.data["username"], request.data["course_code"], request.data["course_name"], request.data["batch"])):
                database.save_log(request.data["username"], request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Course already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            
            database.add_course(request.data["username"], request.data["course_code"], request.data["course_name"], request.data["batch"])
            
            database.save_log(request.data["username"], request.path, status.HTTP_201_CREATED, get_client_ip(request), "null")
            database.close()
            return Response({"message": "Course added successfully!"}, status = status.HTTP_201_CREATED)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ListCoursesAPIView(APIView):

    def post(self, request):

        database = Database()
        database.create_tables()
        serializers = ListCoursesSerializer(data = request.data)

        if(serializers.is_valid()):

            if(database.valid_session_id(request.data["username"], request.data["session_id"]) == False):
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid session id!"}, status=status.HTTP_400_BAD_REQUEST)
            
            courses = database.list_courses(request.data["username"])
            
            database.save_log(request.data["username"], request.path, status.HTTP_200_OK, get_client_ip(request), "null")
            database.close()
            return Response({"courses": courses}, status = status.HTTP_200_OK)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AddStudentAPIView(APIView):

    def post(self, request):


        database = Database()
        database.create_tables()
        serializers = AddStudentSerializer(data = request.data)

        if(serializers.is_valid()):

            if(database.valid_session_id(request.data["username"], request.data["session_id"]) == False):
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid session id!"}, status=status.HTTP_400_BAD_REQUEST)
            
            if(database.user_exists(request.data["student_username"]) == False):
                database.save_log(request["username"], request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Student does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
            
            if(database.student_exists(request.data["student_username"], request.data["course_code"], request.data["batch"])):
                database.save_log(request["username"], request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Student already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            
            database.add_student(request.data["course_code"], request.data["batch"], request.data["student_username"], request.data["mac_address"])
            
            database.save_log(request.data["username"], request.path, status.HTTP_201_CREATED, get_client_ip(request), "null")
            database.close()
            return Response({"message": "Student added successfully!"}, status = status.HTTP_201_CREATED)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ListStudentsAPIView(APIView):

    def post(self, request):

        database = Database()
        database.create_tables()
        serializers = ListStudentsSerializer(data = request.data)

        if(serializers.is_valid()):

            if(database.valid_session_id(request.data["username"], request.data["session_id"]) == False):
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid session id!"}, status=status.HTTP_400_BAD_REQUEST)
            
            students = database.list_students(request.data["course_code"], request.data["batch"])
            
            database.save_log(request.data["username"], request.path, status.HTTP_200_OK, get_client_ip(request), "null")
            database.close()
            return Response({"students": students}, status = status.HTTP_200_OK)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class MarkAttendanceAPIView(APIView):

    def post(self, request):

        serializers = MarkAttendanceSerializer(data = request.data)
        database = Database()
        database.create_tables()

        if(serializers.is_valid()):

            if(database.valid_session_id(request.data["username"], request.data["session_id"]) == False):

                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid session id!"}, status=status.HTTP_400_BAD_REQUEST)
            
            database.mark_attendance(request.data["course_code"], request.data["batch"], request.data["students"])
            
            database.save_log(request.data["username"], request.path, status.HTTP_201_CREATED, get_client_ip(request), "null")
            database.close()
            return Response({"message": "Attendance marked successfully!"}, status = status.HTTP_201_CREATED)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ListAttendanceAPIView(APIView):

    def post(self, request):

        database = Database()
        database.create_tables()
        serializers = ListAttendanceSerializer(data = request.data)

        if(serializers.is_valid()):

            if(database.valid_session_id(request.data["username"], request.data["session_id"]) == False):
                database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
                database.close()
                return Response({"message": "Invalid session id!"}, status=status.HTTP_400_BAD_REQUEST)
            
            attendance = database.list_attendance(request.data["username"])
            
            database.save_log(request.data["username"], request.path, status.HTTP_200_OK, get_client_ip(request), "null")
            database.close()
            return Response({"attendance": attendance}, status = status.HTTP_200_OK)
        
        else:
            database.save_log("anonymous", request.path, status.HTTP_400_BAD_REQUEST, get_client_ip(request), "null")
            database.close()
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)