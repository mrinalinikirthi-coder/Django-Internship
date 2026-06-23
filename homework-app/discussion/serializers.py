from rest_framework import serializers

from .models import Subject, Student, Teacher, Post, Reply

from django.contrib.auth.models import User

from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token


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
        fields = '__all__'
        read_only_fields = ['user','created_at', 'updated_at','deleted_at']


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = '__all__'
        read_only_fields = ['user','created_at', 'updated_at','deleted_at']


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at','deleted_at','student']


class ReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at','deleted_at','teacher']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def create(self, validated_data):
        logger.info(f"Creating user: {validated_data['username']}")
        user = User.objects.create_user(...)
        token = Token.objects.create(user=user)
        logger.info(f"User {validated_data['username']} created with token")
        return {"user": user, "token": token}


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs['username']
        logger.info(f"Validating login for: {username}")
        user = authenticate(...)
        if not user:
            logger.warning(f"Login failed for: {username}")
            raise serializers.ValidationError("Invalid credentials")
        logger.info(f"Login successful for: {username}")
        return {"user": user.username, "token": token.key}
