import logging

from rest_framework import serializers

from .models import Subject, Student, Teacher, Post, Reply

from django.contrib.auth.models import User

from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ['uuid', 'name']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['uuid', 'name', 'grade', 'school_name', 'gender', 'nationality', 'subject', 'user', 'created_at', 'updated_at', 'deleted_at']
        read_only_fields = ['user', 'created_at', 'updated_at', 'deleted_at']


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ['uuid', 'name', 'qualification', 'years_of_exp', 'gender',
                  'nationality', 'subject', 'user',
                  'created_at', 'updated_at', 'deleted_at']
        read_only_fields = ['user', 'created_at', 'updated_at', 'deleted_at']


class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['uuid', 'student', 'subject', 'content', 'created_at',
                  'updated_at', 'deleted_at']
        read_only_fields = ['student', 'created_at', 'updated_at', 'deleted_at']


class ReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        fields = ['uuid', 'post', 'teacher', 'reply', 'created_at',
                  'updated_at', 'deleted_at']
        read_only_fields = ['teacher', 'created_at', 'updated_at', 'deleted_at']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def create(self, validated_data):
        logger.info(f"Creating user: {validated_data['username']}")
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        token = Token.objects.create(user=user)
        logger.info(f"User {validated_data['username']} created with token")
        return {"user": user, "token": token}


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs['username']
        logger.info(f"Validating login for: {username}")
        user = authenticate(username=username, password=attrs['password'])
        if not user:
            logger.warning(f"Login failed for: {username}")
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            logger.warning(f"Inactive user attempted login: {username}")
            raise serializers.ValidationError("Invalid credentials")
        
        refresh = RefreshToken.for_user(user)
        logger.info(f"Login successful for: {username}")
        return {
            "user": user.username,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }