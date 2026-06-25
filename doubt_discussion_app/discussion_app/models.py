"""
Database models for the Discussion App.

This module defines all the core data models for the application including:
- BaseModel with common fields (UUID, timestamps, soft delete)
- User profile models (Student, Teacher)
- Subject, Post (doubt), and Reply models
- Soft delete functionality with custom manager
"""

from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    """
    Custom model manager that excludes soft-deleted records by default.

    This manager overrides the default `get_queryset()` method to filter out
    records where `deleted_at` is not None, effectively hiding soft-deleted
    records from normal queries.

    To include soft-deleted records, use `objects_all` instead.
    """

    def get_queryset(self):
        """
        Return only records that are not soft-deleted.

        Returns:
            QuerySet: A queryset filtered to exclude soft-deleted records
        """
        return super().get_queryset().filter(deleted_at__isnull=True)


class BaseModel(models.Model):
    """
    Abstract base model providing common fields and soft delete functionality.

    All models in the application inherit from this class to get:
    - UUID as primary key (instead of auto-incrementing integer)
    - Automatic timestamps for creation and updates
    - Soft delete support with custom managers

    Attributes:
        uuid (UUIDField): Primary key using UUID v4
        created_at (DateTimeField): Timestamp when the record was created
        updated_at (DateTimeField): Timestamp when the record was last updated
        deleted_at (DateTimeField): Timestamp when the record
                                    was soft-deleted (NULL if active)
    """

    # Primary key using UUID for improved security and uniqueness
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Automatic timestamps for tracking record lifecycle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Default manager that filters out soft-deleted records
    objects = SoftDeleteManager()

    # Soft delete timestamp (NULL means the record is active)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Alternate manager that includes all records (including soft-deleted)
    objects_all = models.Manager()

    def delete(self):
        """
        Perform a soft delete by setting the deleted_at timestamp.

        This method overrides the default delete to soft-delete the record
        instead of permanently removing it from the database.

        To permanently delete, use hard_delete().
        """
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """
        Restore a soft-deleted record by clearing the deleted_at timestamp.

        After calling this method, the record will reappear in normal queries.
        """
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        """
        Permanently delete the record from the database.

        This bypasses soft delete and removes the record permanently.
        Use with caution as this action cannot be undone.
        """
        super().delete()

    class Meta:
        # This is an abstract model — it won't create a database table
        abstract = True


class Teacher(BaseModel):
    """
    Teacher profile model extending BaseModel.

    Represents a teacher in the system with their professional details
    and subject associations.

    Attributes:
        name (CharField): Teacher's full name
        qualification (CharField): Educational qualification
        years_of_exp (SmallIntegerField): Years of teaching experience
        gender (CharField): Gender with predefined choices
        nationality (CharField): Teacher's nationality
        subject (ManyToManyField): Subjects the teacher teaches
        user (OneToOneField): Link to Django's User model for authentication
    """

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', "Other")
    ]

    name = models.CharField(max_length=75)
    qualification = models.CharField(max_length=30)
    years_of_exp = models.SmallIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=30)

    # Subjects this teacher teaches (many-to-many relationship)
    subject = models.ManyToManyField('Subject')

    # Link to Django's built-in User model for authentication
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Student(BaseModel):
    """
    Student profile model extending BaseModel.

    Represents a student in the system with their academic details
    and subject associations.

    Attributes:
        name (CharField): Student's full name
        grade (CharField): Grade level (I to XII) with predefined choices
        school_name (CharField): Student's school name
        gender (CharField): Gender with predefined choices
        nationality (CharField): Student's nationality
        subject (ManyToManyField): Subjects the student is enrolled in
        user (OneToOneField): Link to Django's User model for authentication
    """

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', "Other")
    ]

    GRADE_CHOICES = [
        ('I', '1st'),
        ('II', '2nd'),
        ('III', '3rd'),
        ('IV', '4th'),
        ('V', '5th'),
        ('VI', '6th'),
        ('VII', '7th'),
        ('VIII', '8th'),
        ('IX', '9th'),
        ('X', '10th'),
        ('XI', '11th'),
        ('XII', '12th')
    ]

    name = models.CharField(max_length=75)
    grade = models.CharField(max_length=8, choices=GRADE_CHOICES)
    school_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=30)

    # Subjects the student is enrolled in (many-to-many relationship)
    subject = models.ManyToManyField('Subject')

    # Link to Django's built-in User model for authentication
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Subject(BaseModel):
    """
    Subject model representing academic subjects.

    Attributes:
        name (CharField): The name of the subject
    """

    name = models.CharField(max_length=50)


class Post(BaseModel):
    """
    Post model representing student doubts/questions.

    A post is created by a student and belongs to a specific subject.

    Attributes:
        student (ForeignKey): The student who posted the doubt
        subject (ForeignKey): The subject this doubt belongs to
        content (TextField): The actual question or doubt text
    """

    # The student who created this post
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    # The subject this post belongs to
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    # The actual content of the doubt
    content = models.TextField()


class Reply(BaseModel):
    """
    Reply model representing teacher responses to student doubts.

    A reply is created by a teacher in response to a specific post.

    Attributes:
        post (ForeignKey): The post this reply is responding to
        teacher (ForeignKey): The teacher who created this reply
        reply (TextField): The actual response text
    """

    # The post this reply belongs to
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # The teacher who created this reply
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    # The actual reply content
    reply = models.TextField()
