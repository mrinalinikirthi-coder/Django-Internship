from rest_framework.viewsets import ModelViewSet
from .models import Teacher, Student, Subject, Post, Reply
from .serializers import LoginSerializer, PostSerializer, SubjectSerializer
from .serializers import TeacherSerializer, StudentSerializer
from .serializers import ReplySerializer, RegisterSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .permissions import IsStudent, IsTeacher, IsOwner
from rest_framework.views import APIView
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    authentication_classes = [IsAuthenticated]
    permission_classes = []


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = []

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]
        elif self.action == 'create':
            return [IsAuthenticated(), IsStudent()]
        else:
            return []

    def perform_create(self, serializer):
        student = self.request.user.student
        logger.info(f"User {self.request.user.username} creating a new post")
        serializer.save(student=student)
        logger.info(f"Post created by {self.request.user.username}")

    def perform_update(self, serializer):
        logger.info(f"User {self.request.user.username} updating post {serializer.instance.uuid}")
        serializer.save()
        logger.info(f"Post {serializer.instance.uuid} updated by {self.request.user.username}")

    def perform_destroy(self, instance):
        logger.info(f"User {self.request.user.username} deleting post {instance.uuid}")
        instance.delete()
        logger.info(f"Post {instance.uuid} deleted by {self.request.user.username}")


class ReplyViewSet(ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated(), IsTeacher()]

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            return [IsAuthenticated(), IsOwner()]
        elif self.action == 'create':
            return [IsAuthenticated(), IsTeacher()]
        else:
            return []

    def perform_create(self, serializer):
        teacher = self.request.user.teacher
        logger.info(f"Teacher {self.request.user.username} creating a new reply")
        serializer.save(teacher=teacher)
        logger.info(f"Reply created by teacher {self.request.user.username}")

    def perform_update(self, serializer):
        logger.info(f"Teacher {self.request.user.username} updating reply {serializer.instance.uuid}")
        serializer.save()
        logger.info(f"Reply {serializer.instance.uuid} updated by {self.request.user.username}")

    def perform_destroy(self, instance):
        logger.info(f"Teacher {self.request.user.username} deleting reply {instance.uuid}")
        instance.delete()
        logger.info(f"Reply {instance.uuid} deleted by {self.request.user.username}")


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated(), IsTeacher()]

    def perform_create(self, serializer):
        logger.info(f"User {self.request.user.username} creating a teacher profile")
        serializer.save(user=self.request.user)
        logger.info(f"Teacher profile created for {self.request.user.username}")

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            return [IsAuthenticated(), IsOwner()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        else:
            return []
    http_method_names = ['get', 'put', 'patch', 'post', 'delete']


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated(), IsStudent()]

    def perform_create(self, serializer):
        logger.info(f"User {self.request.user.username} creating a student profile")
        serializer.save(user=self.request.user)
        logger.info(f"Student profile created for {self.request.user.username}")

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            return [IsAuthenticated(), IsOwner()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        else:
            return []
    http_method_names = ['get', 'put', 'patch', 'post', 'delete']


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        logger.info(f"Registration attempt for username: {username}")
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User {username} registered successfully")
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        logger.warning(f"Registration failed for {username}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        logger.info(f"Login attempt for username: {username}")
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            logger.info(f"User {username} logged in successfully")
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        logger.warning(f"Login failed for {username}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)