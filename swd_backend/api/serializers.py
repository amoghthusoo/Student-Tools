from rest_framework import serializers

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