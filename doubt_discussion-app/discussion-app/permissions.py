from rest_framework import permissions
import logging

logger = logging.getLogger(__name__)


class IsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        logger.info(f"Student permission check for user: {request.user}")
        if hasattr(request.user, 'student'):
            logger.info(f"User {request.user} is a student")
            return True
        logger.warning(f"User {request.user} is NOT a student")
        return False


class IsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        logger.info(f"Teacher permission check for user: {request.user}")
        if hasattr(request.user, 'teacher'):
            logger.info(f"User {request.user} is a teacher")
            return True
        logger.warning(f"User {request.user} is NOT a teacher")
        return False


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            logger.warning("Unauthenticated user tried to check ownership")
            return False

        logger.info(f"Owner permission check for user: "
                    f"{request.user} on object: {obj}")

        # For Post objects
        if hasattr(obj, 'student'):
            is_owner = obj.student.user == request.user
            logger.info(f"Post owner check: {is_owner}")
            return is_owner

        # For Reply objects
        if hasattr(obj, 'teacher'):
            is_owner = obj.teacher.user == request.user
            logger.info(f"Reply owner check: {is_owner}")
            return is_owner

        # For Student/Teacher objects
        if hasattr(obj, 'user'):
            is_owner = obj.user == request.user
            logger.info(f"Student/Teacher owner check: {is_owner}")
            return is_owner

        logger.warning(f"Object {obj} has no user/student/teacher attribute")
        return False
