from rest_framework import serializers
import os

class RegistrationSerializer(serializers.Serializer):
    
    username = serializers.CharField(max_length = 256)
    password = serializers.CharField(max_length = 64)
    email = serializers.CharField(max_length = 256)
    is_student = serializers.BooleanField()
    otp = serializers.IntegerField(min_value=100000, max_value=999999)

class GenerateRegistrationOtpSerializer(serializers.Serializer):

    email = serializers.CharField(max_length = 256)

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length = 256)
    password = serializers.CharField(max_length = 64)

class GenerateResetPasswordOtpSerializer(serializers.Serializer):

    username = serializers.CharField(max_length = 256)
    email = serializers.CharField(max_length = 256)

class ResetPasswordSerializer(serializers.Serializer):

    username = serializers.CharField(max_length = 256)
    email = serializers.CharField(max_length = 256)
    otp = serializers.IntegerField(min_value=100000, max_value=999999)
    new_password = serializers.CharField(max_length = 64)

class LogoutSerializer(serializers.Serializer):
    
    username = serializers.CharField(max_length = 256)
    session_id = serializers.CharField()

class FileUploadSerializer(serializers.Serializer):

    username =  serializers.CharField(max_length = 256)
    file = serializers.FileField()
    session_id = serializers.CharField()

    def validate_file(self, value):
        """ Custom validation for file size and type """
        max_size = 10 * 1024 * 1024  # 10MB limit
        allowed_extensions = [".pdf", ".txt", ".docx", ".pptx"]
        ext = os.path.splitext(value.name)[1].lower()  # Extract file extension

        if (value.size > max_size):
            raise serializers.ValidationError("File size exceeds 10MB limit.")
        
        if (ext not in allowed_extensions):
            raise serializers.ValidationError("Only .pdf, .txt, .docx and .pptx are allowed.")

        return value
    
class FileDownloadSerializer(serializers.Serializer):
    
    username = serializers.CharField(max_length = 256)
    file_name = serializers.CharField(max_length = 256)
    session_id = serializers.CharField()

class FileDeleteSerializer(serializers.Serializer):
    
    username = serializers.CharField(max_length = 256)
    file_name = serializers.CharField(max_length = 256)
    session_id = serializers.CharField()

class FileListSerializer(serializers.Serializer):
    
    username = serializers.CharField(max_length = 256)
    session_id = serializers.CharField()

class CreateThreadSerializer(serializers.Serializer):

    username = serializers.CharField(max_length = 256)
    thread_name = serializers.CharField(max_length = 256)
    session_id = serializers.CharField()

class PostReplySerializer(serializers.Serializer):

    username = serializers.CharField(max_length = 256)
    thread_name = serializers.CharField(max_length = 256)
    reply = serializers.CharField(max_length = 8192)
    session_id = serializers.CharField()

class ListThreadsSerializer(serializers.Serializer):

    username = serializers.CharField(max_length = 256)
    session_id = serializers.CharField()

class ListRepliesSerializer(serializers.Serializer):

    thread_name = serializers.CharField(max_length = 256)
    username = serializers.CharField(max_length = 256)
    session_id = serializers.CharField()

class DeleteThreadSerializer(serializers.Serializer):

    username = serializers.CharField(max_length = 256)
    thread_name = serializers.CharField(max_length = 256)
    session_id = serializers.CharField()

class AddCourseSerializer(serializers.Serializer):

    username = serializers.CharField(max_length = 256)  # Faculty username
    course_code = serializers.CharField(max_length = 256)
    course_name = serializers.CharField(max_length = 256)
    batch = serializers.CharField(max_length = 256)
    session_id = serializers.CharField()

class ListCoursesSerializer(serializers.Serializer):

    username = serializers.CharField(max_length = 256)  # Faculty username
    session_id = serializers.CharField()

class AddStudentSerializer(serializers.Serializer):

    username = serializers.CharField(max_length = 256)  # Faculty username
    course_code = serializers.CharField(max_length = 256)
    batch = serializers.CharField(max_length = 256)
    student_username = serializers.CharField(max_length = 256)
    mac_address = serializers.CharField(max_length = 32)
    session_id = serializers.CharField()

class ListStudentsSerializer(serializers.Serializer):

    username = serializers.CharField(max_length = 256)  # Faculty username
    course_code = serializers.CharField(max_length = 256)
    batch = serializers.CharField(max_length = 256)
    session_id = serializers.CharField()

class MarkAttendanceSerializer(serializers.Serializer):

    username = serializers.CharField(max_length = 256)  # Faculty username
    course_code = serializers.CharField(max_length = 256)
    batch = serializers.CharField(max_length = 256)
    students = serializers.DictField()
    session_id = serializers.CharField()

class ListAttendanceSerializer(serializers.Serializer):

    username = serializers.CharField(max_length = 256)  
    session_id = serializers.CharField()

class GetAttendanceReportSerializer(serializers.Serializer):
    
        username = serializers.CharField(max_length = 256)  # Faculty username
        course_code = serializers.CharField(max_length = 256)
        batch = serializers.CharField(max_length = 256)
        session_id = serializers.CharField()