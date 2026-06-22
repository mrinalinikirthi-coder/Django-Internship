from rest_framework.viewsets import ModelViewSet

from .models import Teacher, Student, Subject, Post, Reply

from .serializers import PostSerializer, SubjectSerializer, UserSerializer, StudentSerializer, TeacherSerializer

from .serializers import PostSerializer, ReplySerializer, RegisterSerializer, LoginSerializer

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from .permissions import IsStudent, IsTeacher, IsOwner

from rest_framework.views import APIView

from rest_framework import status

class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    authentication_classes = []
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
        serializer.save(student = self.request.user.student)


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
        

class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated(), IsTeacher()]
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            return [IsAuthenticated(), IsOwner()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        else:
            return []
    http_method_names=['get', 'put', 'patch', 'post', 'delete']


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated(), IsStudent()]
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
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
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            return Response(serializer.validated_data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
