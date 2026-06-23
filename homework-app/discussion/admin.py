from django.contrib import admin

from .models import Teacher, Student, Subject, Reply, Post
from django.contrib.admin import ModelAdmin
import logging

logger = logging.getLogger(__name__)


class BaseAdmin(ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change:
            logger.info(f"Admin: {request.user.username} updated {obj.__class__.__name__}: {obj}")
        else:
            logger.info(f"Admin: {request.user.username} created {obj.__class__.__name__}: {obj}")
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        logger.warning(f"Admin: {request.user.username} deleted {obj.__class__.__name__}: {obj}")
        super().delete_model(request, obj)

    def log_addition(self, request, obj, message):
        logger.info(f"Admin addition: {request.user.username} - {obj}")
        super().log_addition(request, obj, message)

    def log_change(self, request, obj, message):
        logger.info(f"Admin change: {request.user.username} - {obj}")
        super().log_change(request, obj, message)

    def log_deletion(self, request, obj, object_repr):
        logger.warning(f"Admin deletion: {request.user.username} - {object_repr}")
        super().log_deletion(request, obj, object_repr)


@admin.register(Student)
class StudentAdmin(BaseAdmin):
    list_display = ['name', 'grade', 'school_name', 'user', 'uuid']
    search_fields = ['name', 'grade']


@admin.register(Teacher)
class TeacherAdmin(BaseAdmin):
    list_display = ['name', 'qualification', 'years_of_exp', 'user', 'uuid']
    search_fields = ['name', 'qualification']


@admin.register(Subject)
class SubjectAdmin(BaseAdmin):
    list_display = ['name', 'uuid']
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(BaseAdmin):
    list_display = ['content', 'student', 'subject', 'created_at', 'uuid']
    search_fields = ['content']


@admin.register(Reply)
class ReplyAdmin(BaseAdmin):
    list_display = ['reply', 'post', 'teacher', 'created_at', 'uuid']
    search_fields = ['reply']