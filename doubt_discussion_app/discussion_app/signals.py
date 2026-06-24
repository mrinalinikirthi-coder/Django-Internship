"""
Signal handlers for the Discussion App.

This module defines Django signal receivers that automatically log
all model lifecycle events including creation, update, and deletion.

Signals are registered for:
- User (Django's built-in model)
- Teacher, Student, Subject, Post, Reply (custom models)

All signals include detailed logging with user context and object identification
for audit and debugging purposes.
"""

import logging
from django.db.models.signals import pre_save, post_save
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Teacher, Student, Subject, Post, Reply, BaseModel

# Initialize logger for signal events
logger = logging.getLogger(__name__)


def log_model_change(sender, instance, created, action, **kwargs):
    """
    Helper function to log model changes in a consistent format.

    This function is used by individual signal handlers to maintain
    consistent logging across all models.

    Args:
        sender: The model class that triggered the signal
        instance: The model instance being modified
        created: Boolean indicating if the record was newly created
        action: String describing the action ('created', 'updated', etc.)
        **kwargs: Additional signal arguments
    """
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


# ======================== User Signals ========================

@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
    """
    Log when a User is created or updated.

    This signal fires after a User is saved, logging whether
    the user was newly created or updated.

    Args:
        sender: The User model class
        instance: The User instance being saved
        created: True if this is a new user, False if existing
        **kwargs: Additional signal arguments
    """
    if created:
        logger.info(f"User created: {instance.username} (ID: {instance.id})")
    else:
        logger.info(f"User updated: {instance.username} (ID: {instance.id})")


@receiver(pre_delete, sender=User)
def log_user_delete(sender, instance, **kwargs):
    """
    Log when a User is deleted.

    This signal fires before a User is deleted from the database.

    Args:
        sender: The User model class
        instance: The User instance being deleted
        **kwargs: Additional signal arguments
    """
    logger.warning(f"User deleted: {instance.username} (ID: {instance.id})")


# ======================== Teacher Signals ========================

@receiver(post_save, sender=Teacher)
def log_teacher_save(sender, instance, created, **kwargs):
    """
    Log when a Teacher profile is created or updated.

    Args:
        sender: The Teacher model class
        instance: The Teacher instance being saved
        created: True if this is a new teacher, False if existing
        **kwargs: Additional signal arguments
    """
    username = instance.user.username if instance.user else 'Unknown'
    action = 'created' if created else 'updated'
    logger.info(
        f"Teacher {action}: {instance.name} "
        f"(UUID: {instance.uuid}) by {username}"
    )


@receiver(pre_delete, sender=Teacher)
def log_teacher_delete(sender, instance, **kwargs):
    """
    Log when a Teacher profile is deleted.

    Args:
        sender: The Teacher model class
        instance: The Teacher instance being deleted
        **kwargs: Additional signal arguments
    """
    username = instance.user.username if instance.user else 'Unknown'
    logger.warning(
        f"Teacher deleted: {instance.name} "
        f"(UUID: {instance.uuid}) by {username}"
    )


# ======================== Student Signals ========================

@receiver(post_save, sender=Student)
def log_student_save(sender, instance, created, **kwargs):
    """
    Log when a Student profile is created or updated.

    Args:
        sender: The Student model class
        instance: The Student instance being saved
        created: True if this is a new student, False if existing
        **kwargs: Additional signal arguments
    """
    username = instance.user.username if instance.user else 'Unknown'
    action = 'created' if created else 'updated'
    logger.info(
        f"Student {action}: {instance.name} "
        f"(UUID: {instance.uuid}) by {username}"
    )


@receiver(pre_delete, sender=Student)
def log_student_delete(sender, instance, **kwargs):
    """
    Log when a Student profile is deleted.

    Args:
        sender: The Student model class
        instance: The Student instance being deleted
        **kwargs: Additional signal arguments
    """
    username = instance.user.username if instance.user else 'Unknown'
    logger.warning(
        f"Student deleted: {instance.name} "
        f"(UUID: {instance.uuid}) by {username}"
    )


# ======================== Subject Signals ========================

@receiver(post_save, sender=Subject)
def log_subject_save(sender, instance, created, **kwargs):
    """
    Log when a Subject is created or updated.

    Args:
        sender: The Subject model class
        instance: The Subject instance being saved
        created: True if this is a new subject, False if existing
        **kwargs: Additional signal arguments
    """
    action = 'created' if created else 'updated'
    logger.info(f"Subject {action}: {instance.name} (UUID: {instance.uuid})")


@receiver(pre_delete, sender=Subject)
def log_subject_delete(sender, instance, **kwargs):
    """
    Log when a Subject is deleted.

    Args:
        sender: The Subject model class
        instance: The Subject instance being deleted
        **kwargs: Additional signal arguments
    """
    logger.warning(f"Subject deleted: {instance.name} (UUID: {instance.uuid})")


# ======================== Post (Doubt) Signals ========================

@receiver(post_save, sender=Post)
def log_post_save(sender, instance, created, **kwargs):
    """
    Log when a Post (doubt) is created or updated.

    Logs the first 50 characters of the post content for readability.

    Args:
        sender: The Post model class
        instance: The Post instance being saved
        created: True if this is a new post, False if existing
        **kwargs: Additional signal arguments
    """
    student_name = instance.student.name if instance.student else 'Unknown'
    action = 'created' if created else 'updated'
    logger.info(
        f"Post {action}: '{instance.content[:50]}...' by "
        f"{student_name} (UUID: {instance.uuid})"
    )


@receiver(pre_delete, sender=Post)
def log_post_delete(sender, instance, **kwargs):
    """
    Log when a Post (doubt) is deleted.

    Args:
        sender: The Post model class
        instance: The Post instance being deleted
        **kwargs: Additional signal arguments
    """
    student_name = instance.student.name if instance.student else 'Unknown'
    logger.warning(
        f"Post deleted: '{instance.content[:50]}...' by "
        f"{student_name} (UUID: {instance.uuid})"
    )


# ======================== Reply Signals ========================

@receiver(post_save, sender=Reply)
def log_reply_save(sender, instance, created, **kwargs):
    """
    Log when a Reply is created or updated.

    Logs the first 50 characters of the reply content for readability.

    Args:
        sender: The Reply model class
        instance: The Reply instance being saved
        created: True if this is a new reply, False if existing
        **kwargs: Additional signal arguments
    """
    teacher_name = instance.teacher.name if instance.teacher else 'Unknown'
    action = 'created' if created else 'updated'
    logger.info(
        f"Reply {action}: '{instance.reply[:50]}...' by "
        f"{teacher_name} (UUID: {instance.uuid})"
    )


@receiver(pre_delete, sender=Reply)
def log_reply_delete(sender, instance, **kwargs):
    """
    Log when a Reply is deleted.

    Args:
        sender: The Reply model class
        instance: The Reply instance being deleted
        **kwargs: Additional signal arguments
    """
    teacher_name = instance.teacher.name if instance.teacher else 'Unknown'
    logger.warning(
        f"Reply deleted: '{instance.reply[:50]}...' by "
        f"{teacher_name} (UUID: {instance.uuid})"
    )