"""
Views (API endpoints) for the Discussion App.

This module defines all API views using Django REST Framework's ViewSets
and APIViews. It includes:

- ViewSets for CRUD operations on all models with custom permissions
- Custom views for registration, login, and logout
- JWT authentication for protected endpoints
- Comprehensive logging for all actions
- Automatic field assignment (student, teacher, user) from authenticated user
- Optimized queries using select_related() and prefetch_related()

All views include proper authentication, permission checks, and error handling.
"""

from rest_framework.viewsets import ModelViewSet
from .models import Teacher, Student, Subject, Post, Reply
from .serializers import (
    LoginSerializer,
    PostSerializer,
    SubjectSerializer,
    TeacherSerializer,
    StudentSerializer,
    ReplySerializer,
    RegisterSerializer,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .permissions import IsStudent, IsTeacher, IsOwner
from rest_framework.views import APIView
from rest_framework import status
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser

# Initialize logger for view actions
logger = logging.getLogger(__name__)


class SubjectViewSet(ModelViewSet):
    """
    ViewSet for Subject model operations.

    Permissions:
    - Anyone logged in can view subjects (list/retrieve)
    - Only admin users can create, update, or delete subjects

    Authentication: JWT required for all actions.
    """

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny()]

    def get_permissions(self):
        """
        Apply different permissions based on the action.

        - List and retrieve: Only authentication required
        - Create, update, delete: Admin privileges required
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]


class PostViewSet(ModelViewSet):
    """
    ViewSet for Post (doubt) model operations.

    Permissions:
    - Create: Only authenticated students
    - Update/Delete: Only the owner (student who created the post)
    - List/Retrieve: Any authenticated user

    Authentication: JWT required for all actions.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    def get_queryset(self):
        """
        Optimize queries by fetching related data in a single query.

        Uses select_related to fetch:
        - student: The student who created the post
        - student__user: The user account of that student
        - subject: The subject this post belongs to

        Returns:
            QuerySet: Optimized queryset with related data prefetched
        """
        return Post.objects.select_related(
            'student__user',  # Post → Student → User (for owner info)
            'subject'          # Post → Subject
        ).all()

    def get_permissions(self):
        """
        Apply different permissions based on the action.

        - Create: Student role required
        - Update/Delete: Ownership required
        - List/Retrieve: Authentication only
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]
        if self.action == 'create':
            return [IsAuthenticated(), IsStudent()]
        return []

    def perform_create(self, serializer):
        """
        Auto-set the student field from the logged-in user.

        Overrides the default create to automatically assign the student
        profile of the authenticated user.

        Args:
            serializer: The serializer instance with validated data
        """
        student = self.request.user.student
        logger.info(f"User {self.request.user.username} creating a new post")
        serializer.save(student=student)
        logger.info(f"Post created by {self.request.user.username}")

    def perform_update(self, serializer):
        """
        Log when a post is updated.

        Args:
            serializer: The serializer instance with validated data
        """
        logger.info(
            f"User {self.request.user.username} "
            f"updating post {serializer.instance.uuid}"
        )
        serializer.save()
        logger.info(
            f"Post {serializer.instance.uuid} "
            f"updated by {self.request.user.username}"
        )

    def perform_destroy(self, instance):
        """
        Log when a post is deleted.

        Args:
            instance: The post instance being deleted
        """
        logger.info(
            f"User {self.request.user.username} "
            f"deleting post {instance.uuid}"
        )
        instance.delete()
        logger.info(
            f"Post {instance.uuid} "
            f"deleted by {self.request.user.username}"
        )

    def handle_exception(self, exc):
        """
        Log any exceptions raised in the viewset.

        Args:
            exc: The exception that was raised

        Returns:
            Response: The error response from DRF
        """
        logger.error(f"Exception in PostViewSet: {exc}")
        return super().handle_exception(exc)


class ReplyViewSet(ModelViewSet):
    """
    ViewSet for Reply model operations.

    Permissions:
    - Create: Only authenticated teachers
    - Update/Delete: Only the owner (teacher who created the reply)
    - List/Retrieve: Any authenticated user

    Authentication: JWT required for all actions.
    """

    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated(), IsTeacher()]

    def get_queryset(self):
        """
        Optimize queries by fetching related data in a single query.

        Uses select_related to fetch:
        - post: The post this reply belongs to
        - post__student: The student who created the post
        - post__student__user: The user account of that student
        - teacher: The teacher who created this reply
        - teacher__user: The user account of that teacher

        Returns:
            QuerySet: Optimized queryset with related data prefetched
        """
        return Reply.objects.select_related(
            'post__student__user',  # Reply → Post → Student → User
            'teacher__user'          # Reply → Teacher → User
        ).all()

    def get_permissions(self):
        """
        Apply different permissions based on the action.

        - Create: Teacher role required
        - Update/Delete: Ownership required
        - List/Retrieve: Authentication only
        """
        if self.action in ['update', 'destroy', 'partial_update']:
            return [IsAuthenticated(), IsOwner()]
        if self.action == 'create':
            return [IsAuthenticated(), IsTeacher()]
        return []

    def perform_create(self, serializer):
        """
        Auto-set the teacher field from the logged-in user.

        Overrides the default create to automatically assign the teacher
        profile of the authenticated user.

        Args:
            serializer: The serializer instance with validated data
        """
        teacher = self.request.user.teacher
        logger.info(f"Teacher {self.request.user.username}"
                    f"creating a new reply")
        serializer.save(teacher=teacher)
        logger.info(f"Reply created by teacher {self.request.user.username}")

    def perform_update(self, serializer):
        """
        Log when a reply is updated.

        Args:
            serializer: The serializer instance with validated data
        """
        logger.info(
            f"Teacher {self.request.user.username} "
            f"updating reply {serializer.instance.uuid}"
        )
        serializer.save()
        logger.info(
            f"Reply {serializer.instance.uuid} "
            f"updated by {self.request.user.username}"
        )

    def perform_destroy(self, instance):
        """
        Log when a reply is deleted.

        Args:
            instance: The reply instance being deleted
        """
        logger.info(
            f"Teacher {self.request.user.username} "
            f"deleting reply {instance.uuid}"
        )
        instance.delete()
        logger.info(
            f"Reply {instance.uuid} "
            f"deleted by {self.request.user.username}"
        )

    def handle_exception(self, exc):
        """
        Log any exceptions raised in the viewset.

        Args:
            exc: The exception that was raised

        Returns:
            Response: The error response from DRF
        """
        logger.error(f"Exception in ReplyViewSet: {exc}")
        return super().handle_exception(exc)


class TeacherViewSet(ModelViewSet):
    """
    ViewSet for Teacher profile operations.

    Permissions:
    - Create: Any authenticated user (to create their own teacher profile)
    - Update/Delete: Only the owner of the profile
    - List/Retrieve: Any authenticated user

    Authentication: JWT required for all actions.
    HTTP Methods: GET, PUT, PATCH, POST, DELETE
    """

    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated(), IsTeacher()]

    # Allowed HTTP methods for this viewset
    http_method_names = ['get', 'put', 'patch', 'post', 'delete']

    def get_queryset(self):
        """
        Optimize queries by fetching related data efficiently.

        Uses:
        - select_related for the user relationship (OneToOne)
        - prefetch_related for the subjects relationship (ManyToMany)

        Returns:
            QuerySet: Optimized queryset with related data prefetched
        """
        return Teacher.objects.select_related(
            'user'  # Teacher → User
        ).prefetch_related(
            'subject'  # Teacher → Subjects (ManyToMany)
        ).all()

    def perform_create(self, serializer):
        """
        Auto-set the user field from the logged-in user.

        Overrides the default create to automatically assign the
        authenticated user to the teacher profile.

        Args:
            serializer: The serializer instance with validated data
        """
        logger.info(f"User {self.request.user.username}"
                    f" creating a teacher profile")
        serializer.save(user=self.request.user)
        logger.info(f"Teacher profile created for"
                    f" {self.request.user.username}")

    def get_permissions(self):
        """
        Apply different permissions based on the action.

        - Create: Authentication only
        - Update/Delete: Ownership required
        - List/Retrieve: Teacher role required
        """
        if self.action in ['update', 'destroy', 'partial_update']:
            return [IsAuthenticated(), IsOwner()]
        if self.action == 'create':
            return [IsAuthenticated()]
        return []

    def handle_exception(self, exc):
        """
        Log any exceptions raised in the viewset.

        Args:
            exc: The exception that was raised

        Returns:
            Response: The error response from DRF
        """
        logger.error(f"Exception in TeacherViewSet: {exc}")
        return super().handle_exception(exc)


class StudentViewSet(ModelViewSet):
    """
    ViewSet for Student profile operations.

    Permissions:
    - Create: Any authenticated user (to create their own student profile)
    - Update/Delete: Only the owner of the profile
    - List/Retrieve: Any authenticated user

    Authentication: JWT required for all actions.
    HTTP Methods: GET, PUT, PATCH, POST, DELETE
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated(), IsStudent()]

    # Allowed HTTP methods for this viewset
    http_method_names = ['get', 'put', 'patch', 'post', 'delete']

    def get_queryset(self):
        """
        Optimize queries by fetching related data efficiently.

        Uses:
        - select_related for the user relationship (OneToOne)
        - prefetch_related for the subjects relationship (ManyToMany)

        Returns:
            QuerySet: Optimized queryset with related data prefetched
        """
        return Student.objects.select_related(
            'user'  # Student → User
        ).prefetch_related(
            'subject'  # Student → Subjects (ManyToMany)
        ).all()

    def perform_create(self, serializer):
        """
        Auto-set the user field from the logged-in user.

        Overrides the default create to automatically assign the
        authenticated user to the student profile.

        Args:
            serializer: The serializer instance with validated data
        """
        logger.info(f"User {self.request.user.username}"
                    f" creating a student profile")
        serializer.save(user=self.request.user)
        logger.info(f"Student profile created for"
                    f"{self.request.user.username}")

    def get_permissions(self):
        """
        Apply different permissions based on the action.

        - Create: Authentication only
        - Update/Delete: Ownership required
        - List/Retrieve: Student role required
        """
        if self.action in ['update', 'destroy', 'partial_update']:
            return [IsAuthenticated(), IsOwner()]
        if self.action == 'create':
            return [IsAuthenticated()]
        return []

    def handle_exception(self, exc):
        """
        Log any exceptions raised in the viewset.

        Args:
            exc: The exception that was raised

        Returns:
            Response: The error response from DRF
        """
        logger.error(f"Exception in StudentViewSet: {exc}")
        return super().handle_exception(exc)


class RegisterView(APIView):
    """
    View for user registration.

    Accepts POST requests with username, email, and password.
    Creates a new user account and returns an authentication token.

    Authentication: Public (no authentication required)
    Permissions: Public (no permissions required)
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """
        Handle user registration.

        Args:
            request: The HTTP request containing user registration data

        Returns:
            Response: 201 Created with user data and token, or 400 Bad Request
        """
        username = request.data.get('username')
        logger.info(f"Registration attempt for username: {username}")

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"User {username} registered successfully")
            return Response(
                serializer.validated_data,
                status=status.HTTP_201_CREATED
            )

        logger.warning(f"Registration failed for {username}"
                       f": {serializer.errors}")
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def handle_exception(self, exc):
        """
        Log any exceptions raised in the view.

        Args:
            exc: The exception that was raised

        Returns:
            Response: The error response from DRF
        """
        logger.error(f"Exception in RegisterView: {exc}")
        return super().handle_exception(exc)


class LoginView(APIView):
    """
    View for user login.

    Accepts POST requests with username and password.
    Authenticates the user and returns JWT tokens (access and refresh).

    Authentication: Public (no authentication required)
    Permissions: Public (no permissions required)
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """
        Handle user login.

        Args:
            request: The HTTP request containing login credentials

        Returns:
            Response: 200 OK with JWT tokens, or 400 Bad Request
        """
        username = request.data.get('username')
        logger.info(f"Login attempt for username: {username}")

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            logger.info(f"User {username} logged in successfully")
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK
            )

        logger.warning(f"Login failed for {username}")
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def handle_exception(self, exc):
        """
        Log any exceptions raised in the view.

        Args:
            exc: The exception that was raised

        Returns:
            Response: The error response from DRF
        """
        logger.error(f"Exception in LoginView: {exc}")
        return super().handle_exception(exc)


class LogoutView(APIView):
    """
    View for user logout.

    Accepts POST requests with the refresh token.
    Blacklists the refresh token to prevent further access token generation.

    Authentication: JWT required (user must be logged in)
    Permissions: User must be authenticated
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle user logout by blacklisting the refresh token.

        Args:
            request: The HTTP request containing the refresh token

        Returns:
            Response: 200 OK on success, or 400 Bad Request on failure
        """
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()

            logger.info(f"User {request.user.username} logged out")
            return Response(
                {"message": "Logged out successfully"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"Logout failed: {e}")
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )
