from django.urls import path
from .views import *

urlpatterns = [
    path("generate_registration_otp/", GenerateRegistrationOtpAPIView.as_view(), name = "generate_registration_otp"),
    path("registration/", RegistrationAPIView.as_view(), name = "registration"),
    path("login/", LoginAPIView.as_view(), name = "login"),
    path("generate_reset_password_otp/", GenerateResetPasswordAPIView.as_view(), name = "generate_reset_password_otp"),
    path("reset_password/", ResetPasswordAPIView.as_view(), name = "reset_password"),
    path("logout/", LogoutAPIView.as_view(), name = "logout"),

    path("upload_file/", FileUploadAPIView.as_view(), name = "upload_file"),
    path("download_file/", FileDownloadAPIView.as_view(), name = "download_file"),
    path("delete_file/", FileDeleteAPIView.as_view(), name = "delete_file"),
    path("list_files/", FileListAPIView.as_view(), name = "list_files"),

    path("create_thread/", CreateThreadAPIView.as_view(), name = "create_thread"),
    path("post_reply/", PostReplyAPIView.as_view(), name = "post_reply"),
    path("list_threads/", ListThreadsAPIView.as_view(), name = "list_threads"),
    path("list_replies/", ListRepliesAPIView.as_view(), name = "list_replies"),
    path("delete_thread/", DeleteThreadAPIView.as_view(), name = "delete_thread"),

    path("add_course/", AddCourseAPIView.as_view(), name = "add_course"),
    path("list_courses/", ListCoursesAPIView.as_view(), name = "list_courses"),
    path("add_student/", AddStudentAPIView.as_view(), name = "add_student"),
    path("list_students/", ListStudentsAPIView.as_view(), name = "list_students"),
    path("mark_attendance/", MarkAttendanceAPIView.as_view(), name = "mark_attendance"),
    path("list_attendance/", ListAttendanceAPIView.as_view(), name = "list_attendance"),
]