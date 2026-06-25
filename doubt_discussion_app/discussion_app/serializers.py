"""
Serializers for the Discussion App.

This module defines serializers for all models and custom serializers for:
- User registration and login (with JWT token generation)
- Model serializers with explicit field lists (no __all__)
- Read-only fields for auto-generated or sensitive fields
- Comprehensive logging for audit and debugging

All serializers follow the principle of explicit field declarations
to improve maintainability and security.
"""

import logging
from rest_framework import serializers
from .models import Subject, Student, Teacher, Post, Reply
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

# Initialize logger for serializer actions
logger = logging.getLogger(__name__)


class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subject model.

    Only exposes the UUID (public identifier) and name fields.
    Created_at, updated_at, and deleted_at are inherited but not exposed.
    """

    class Meta:
        model = Subject
        fields = ['uuid', 'name']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Django's built-in User model.

    Used for user registration and profile display.
    The password field is write-only for security.
    """

    # Password is write-only — never returned in responses
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Student model.

    Explicitly lists all fields for maintainability.
    User, created_at, updated_at, and deleted_at are read-only
    as they are auto-generated or set by the system.
    """

    class Meta:
        model = Student
        fields = [
            'uuid', 'name', 'grade', 'school_name', 'gender',
            'nationality', 'subject', 'user',
            'created_at', 'updated_at', 'deleted_at'
        ]
        # These fields are auto-generated and should not be sent by the client
        read_only_fields = ['user', 'created_at', 'updated_at', 'deleted_at']


class TeacherSerializer(serializers.ModelSerializer):
    """
    Serializer for the Teacher model.

    Explicitly lists all fields for maintainability.
    User, created_at, updated_at, and deleted_at are read-only
    as they are auto-generated or set by the system.
    """

    class Meta:
        model = Teacher
        fields = [
            'uuid', 'name', 'qualification', 'years_of_exp', 'gender',
            'nationality', 'subject', 'user',
            'created_at', 'updated_at', 'deleted_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at', 'deleted_at']


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post (doubt) model.

    Student field is read-only as it's auto-set in perform_create().
    Timestamp fields are read-only as they're auto-generated.
    """

    class Meta:
        model = Post
        fields = [
            'uuid', 'student', 'subject', 'content',
            'created_at', 'updated_at', 'deleted_at'
        ]
        # Student is set by the view from the logged-in user
        read_only_fields = ['student', 'created_at',
                            'updated_at', 'deleted_at']


class ReplySerializer(serializers.ModelSerializer):
    """
    Serializer for the Reply model.

    Teacher field is read-only as it's auto-set in perform_create().
    Timestamp fields are read-only as they're auto-generated.
    """

    class Meta:
        model = Reply
        fields = [
            'uuid', 'post', 'teacher', 'reply',
            'created_at', 'updated_at', 'deleted_at'
        ]
        # Teacher is set by the view from the logged-in user
        read_only_fields = ['teacher', 'created_at',
                            'updated_at', 'deleted_at']


class RegisterSerializer(serializers.Serializer):
    """
    Custom serializer for user registration.

    Handles user creation with hashed password and automatic token generation.
    The password field is write-only for security.

    Returns:
        dict: Contains the created user object and an authentication token
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def create(self, validated_data):
        """
        Create a new user and generate an authentication token.

        The user is created with a hashed password using Django's
        create_user() method, which handles password hashing automatically.

        Args:
            validated_data: Dictionary containing validated user data

        Returns:
            dict: User object and authentication token
        """
        logger.info(f"Creating user: {validated_data['username']}")

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Generate a token for the newly created user
        token = Token.objects.create(user=user)

        logger.info(f"User {validated_data['username']} created with token")
        return {"user": user, "token": token}


class LoginSerializer(serializers.Serializer):
    """
    Custom serializer for user login.

    Authenticates user credentials and returns JWT tokens.
    The password field is write-only for security.

    Returns:
        dict: User username, refresh token, and access token
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Validate user credentials and generate JWT tokens.

        The authentication process:
        1. Authenticate the user using Django's authenticate()
        2. Check if the user exists and is active
        3. Generate refresh and access tokens using JWT

        Args:
            attrs: Dictionary containing username and password

        Returns:
            dict: Username, refresh token, and access token

        Raises:
            ValidationError: If credentials are invalid or user is inactive
        """
        username = attrs['username']
        logger.info(f"Validating login for: {username}")

        # Authenticate using Django's built-in authentication
        user = authenticate(username=username, password=attrs['password'])

        # Check if authentication failed
        if not user:
            logger.warning(f"Login failed for: {username}")
            raise serializers.ValidationError("Invalid credentials")

        # Check if the user account is active
        if not user.is_active:
            logger.warning(f"Inactive user attempted login: {username}")
            raise serializers.ValidationError("Invalid credentials")

        # Generate JWT tokens using Simple JWT
        refresh = RefreshToken.for_user(user)

        logger.info(f"Login successful for: {username}")
        return {
            "user": user.username,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
