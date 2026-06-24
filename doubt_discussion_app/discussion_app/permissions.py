"""
Custom permission classes for the Discussion App.

This module defines role-based and object-level permissions:
- IsStudent: Restricts access to users with a Student profile
- IsTeacher: Restricts access to users with a Teacher profile
- IsOwner: Restricts access to the owner of a specific object

All permissions include detailed logging for audit and debugging purposes.
"""

from rest_framework import permissions
import logging

# Initialize logger for permission checks
logger = logging.getLogger(__name__)


class IsStudent(permissions.BasePermission):
    """
    Custom permission class to check if the logged-in user is a student.

    This permission checks if the user has a Student profile linked to them.
    Used to restrict student-only endpoints like creating posts.

    Returns:
        bool: True if user is a student, False otherwise
    """

    def has_permission(self, request, view):
        """
        Check if the request user has a Student profile.

        Args:
            request: The HTTP request object
            view: The view being accessed

        Returns:
            bool: True if user has a student attribute, False otherwise
        """
        logger.info(f"Student permission check for user: {request.user}")

        if hasattr(request.user, 'student'):
            logger.info(f"User {request.user} is a student")
            return True

        logger.warning(f"User {request.user} is NOT a student")
        return False


class IsTeacher(permissions.BasePermission):
    """
    Custom permission class to check if the logged-in user is a teacher.

    This permission checks if the user has a Teacher profile linked to them.
    Used to restrict teacher-only endpoints like creating replies.

    Returns:
        bool: True if user is a teacher, False otherwise
    """

    def has_permission(self, request, view):
        """
        Check if the request user has a Teacher profile.

        Args:
            request: The HTTP request object
            view: The view being accessed

        Returns:
            bool: True if user has a teacher attribute, False otherwise
        """
        logger.info(f"Teacher permission check for user: {request.user}")

        if hasattr(request.user, 'teacher'):
            logger.info(f"User {request.user} is a teacher")
            return True

        logger.warning(f"User {request.user} is NOT a teacher")
        return False


class IsOwner(permissions.BasePermission):
    """
    Custom permission class to check if the user owns the requested object.

    This permission is used for object-level permission checks on:
    - Post objects: User is the student who created the post
    - Reply objects: User is the teacher who created the reply
    - Student/Teacher objects: User is linked to the profile

    Returns:
        bool: True if the user owns the object, False otherwise
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the request user owns the specific object.

        The check varies based on the object type:
        - Post: Compares obj.student.user with request.user
        - Reply: Compares obj.teacher.user with request.user
        - Student/Teacher: Compares obj.user with request.user

        Args:
            request: The HTTP request object
            view: The view being accessed
            obj: The specific object being accessed

        Returns:
            bool: True if the user owns the object, False otherwise
        """
        # Unauthenticated users cannot own anything
        if not request.user.is_authenticated:
            logger.warning("Unauthenticated user tried to check ownership")
            return False

        logger.info(
            f"Owner permission check for user: {request.user} on object: {obj}"
        )

        # Check ownership for Post objects (belongs to a Student)
        if hasattr(obj, 'student'):
            is_owner = obj.student.user == request.user
            logger.info(f"Post owner check: {is_owner}")
            return is_owner

        # Check ownership for Reply objects (belongs to a Teacher)
        if hasattr(obj, 'teacher'):
            is_owner = obj.teacher.user == request.user
            logger.info(f"Reply owner check: {is_owner}")
            return is_owner

        # Check ownership for Student/Teacher objects (have direct user link)
        if hasattr(obj, 'user'):
            is_owner = obj.user == request.user
            logger.info(f"Student/Teacher owner check: {is_owner}")
            return is_owner

        # If the object doesn't have any recognizable ownership field
        logger.warning(f"Object {obj} has no user/student/teacher attribute")
        return False