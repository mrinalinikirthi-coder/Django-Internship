import logging
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Teacher, Student, Subject, Post, Reply, BaseModel

logger = logging.getLogger(__name__)


def log_model_change(sender, instance, created, action, **kwargs):
    """Helper function to log model changes"""
    model_name = sender.__name__
    obj_id = getattr(instance, 'uuid', getattr(instance, 'id', 'Unknown'))
    user = getattr(instance, 'user', None)
    username = user.username if user and hasattr(user, 'username') else 'System'
    
    if action == 'created':
        logger.info(f"{model_name} created: {obj_id} by {username}")
    elif action == 'updated':
        logger.info(f"{model_name} updated: {obj_id} by {username}")
    elif action == 'deleted':
        logger.info(f"{model_name} deleted: {obj_id} by {username}")
    elif action == 'restored':
        logger.info(f"{model_name} restored: {obj_id}")


# User Signals
@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"User created: {instance.username} (ID: {instance.id})")
    else:
        logger.info(f"User updated: {instance.username} (ID: {instance.id})")


@receiver(pre_delete, sender=User)
def log_user_delete(sender, instance, **kwargs):
    logger.warning(f"User deleted: {instance.username} (ID: {instance.id})")


# Teacher Signals
@receiver(post_save, sender=Teacher)
def log_teacher_save(sender, instance, created, **kwargs):
    username = instance.user.username if instance.user else 'Unknown'
    action = 'created' if created else 'updated'
    logger.info(f"Teacher {action}: {instance.name} (UUID: {instance.uuid}) by {username}")


@receiver(pre_delete, sender=Teacher)
def log_teacher_delete(sender, instance, **kwargs):
    username = instance.user.username if instance.user else 'Unknown'
    logger.warning(f"Teacher deleted: {instance.name} (UUID: {instance.uuid}) by {username}")


# Student Signals
@receiver(post_save, sender=Student)
def log_student_save(sender, instance, created, **kwargs):
    username = instance.user.username if instance.user else 'Unknown'
    action = 'created' if created else 'updated'
    logger.info(f"Student {action}: {instance.name} (UUID: {instance.uuid}) by {username}")


@receiver(pre_delete, sender=Student)
def log_student_delete(sender, instance, **kwargs):
    username = instance.user.username if instance.user else 'Unknown'
    logger.warning(f"Student deleted: {instance.name} (UUID: {instance.uuid}) by {username}")


# Subject Signals
@receiver(post_save, sender=Subject)
def log_subject_save(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    logger.info(f"Subject {action}: {instance.name} (UUID: {instance.uuid})")


@receiver(pre_delete, sender=Subject)
def log_subject_delete(sender, instance, **kwargs):
    logger.warning(f"Subject deleted: {instance.name} (UUID: {instance.uuid})")


# Post Signals
@receiver(post_save, sender=Post)
def log_post_save(sender, instance, created, **kwargs):
    student_name = instance.student.name if instance.student else 'Unknown'
    action = 'created' if created else 'updated'
    logger.info(f"Post {action}: '{instance.content[:50]}...' by {student_name} (UUID: {instance.uuid})")


@receiver(pre_delete, sender=Post)
def log_post_delete(sender, instance, **kwargs):
    student_name = instance.student.name if instance.student else 'Unknown'
    logger.warning(f"Post deleted: '{instance.content[:50]}...' by {student_name} (UUID: {instance.uuid})")


# Reply Signals
@receiver(post_save, sender=Reply)
def log_reply_save(sender, instance, created, **kwargs):
    teacher_name = instance.teacher.name if instance.teacher else 'Unknown'
    action = 'created' if created else 'updated'
    logger.info(f"Reply {action}: '{instance.reply[:50]}...' by {teacher_name} (UUID: {instance.uuid})")


@receiver(pre_delete, sender=Reply)
def log_reply_delete(sender, instance, **kwargs):
    teacher_name = instance.teacher.name if instance.teacher else 'Unknown'
    logger.warning(f"Reply deleted: '{instance.reply[:50]}...' by {teacher_name} (UUID: {instance.uuid})")