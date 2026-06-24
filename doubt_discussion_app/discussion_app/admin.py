"""
Admin configuration for the Discussion App.

This module registers all models with the Django admin interface and provides
custom admin functionality including:
- Extended logging for all admin actions (create, update, delete)
- Custom list displays and search fields for each model
- Consistent admin interface across all models
"""

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Teacher, Student, Subject, Reply, Post
import logging

# Initialize logger for admin actions
logger = logging.getLogger(__name__)


class BaseAdmin(ModelAdmin):
    """
    Base admin class that all model admins inherit from.

    Provides extended logging functionality for all admin actions:
    - Logs when a model is created, updated, or deleted
    - Logs additions, changes, and deletions with user context
    - Uses INFO level for normal operations and WARNING for deletions
    """
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model to log admin creation/update actions.

        Args:
            request: The HTTP request object
            obj: The model instance being saved
            form: The form used for saving
            change: Boolean indicating if this is an update (True) or creation (False)
        """
        if change:
            logger.info(
                f"Admin: {request.user.username} updated "
                f"{obj.__class__.__name__}: {obj}"
            )
        else:
            logger.info(
                f"Admin: {request.user.username} created "
                f"{obj.__class__.__name__}: {obj}"
            )
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """
        Override delete_model to log admin deletion actions.

        Args:
            request: The HTTP request object
            obj: The model instance being deleted
        """
        logger.warning(
            f"Admin: {request.user.username} deleted "
            f"{obj.__class__.__name__}: {obj}"
        )
        super().delete_model(request, obj)

    def log_addition(self, request, obj, message):
        """
        Log when a new object is added via admin.

        Args:
            request: The HTTP request object
            obj: The newly created model instance
            message: Additional log message
        """
        logger.info(f"Admin addition: {request.user.username} - {obj}")
        super().log_addition(request, obj, message)

    def log_change(self, request, obj, message):
        """
        Log when an existing object is changed via admin.

        Args:
            request: The HTTP request object
            obj: The modified model instance
            message: Additional log message
        """
        logger.info(f"Admin change: {request.user.username} - {obj}")
        super().log_change(request, obj, message)

    def log_deletion(self, request, obj, object_repr):
        """
        Log when an object is deleted via admin.

        Args:
            request: The HTTP request object
            obj: The deleted model instance
            object_repr: String representation of the deleted object
        """
        logger.warning(
            f"Admin deletion: {request.user.username} - {object_repr}"
        )
        super().log_deletion(request, obj, object_repr)


@admin.register(Student)
class StudentAdmin(BaseAdmin):
    """
    Admin configuration for the Student model.

    Displays key student information in the list view and enables
    searching by name and grade for quick lookup.
    """
    # Fields to display in the admin list view
    list_display = [
        'name',
        'grade',
        'school_name',
        'user',
        'uuid'
    ]
    # Fields that can be searched in the admin interface
    search_fields = ['name', 'grade']


@admin.register(Teacher)
class TeacherAdmin(BaseAdmin):
    """
    Admin configuration for the Teacher model.

    Displays key teacher information including qualifications and
    years of experience in the list view.
    """
    list_display = [
        'name',
        'qualification',
        'years_of_exp',
        'user',
        'uuid'
    ]
    search_fields = ['name', 'qualification']


@admin.register(Subject)
class SubjectAdmin(BaseAdmin):
    """
    Admin configuration for the Subject model.

    Simple list display with subject name and UUID.
    """
    list_display = ['name', 'uuid']
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(BaseAdmin):
    """
    Admin configuration for the Post (doubt) model.

    Displays post content, student, subject, and creation timestamp.
    Enables searching by content for quick lookup.
    """
    list_display = [
        'content',
        'student',
        'subject',
        'created_at',
        'uuid'
    ]
    search_fields = ['content']


@admin.register(Reply)
class ReplyAdmin(BaseAdmin):
    """
    Admin configuration for the Reply model.

    Displays reply content, associated post, teacher, and creation timestamp.
    Enables searching by reply content for quick lookup.
    """
    list_display = [
        'reply',
        'post',
        'teacher',
        'created_at',
        'uuid'
    ]
    search_fields = ['reply']