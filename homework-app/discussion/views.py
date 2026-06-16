from rest_framework.viewsets import ModelViewSet
from .models import Teacher,Student,Subject,Post,Reply
from .serializers import SubjectSerializer,UserSerializer,StudentSerializer,TeacherSerializer,PostSerializer,ReplySerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .permissions import IsStudent,IsTeacher,IsOwner
class SubjectViewSet(ModelViewSet):
    queryset=Subject.objects.all()
    serializer_class=SubjectSerializer
    authentication_classes=[]
    permission_classes=[]
class PostViewSet(ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated,IsStudent]
    def get_permissions(self):
        if self.action in ['update','destroy','partial_update']:
            return [IsOwner]
        else:
            return [IsAuthenticated,IsStudent]
class ReplyViewSet(ModelViewSet):
    queryset=Reply.objects.all()
    serializer_class=ReplySerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated,IsTeacher]
    def get_permissions(self):
        if self.action in ['update','destroy','partial_update']:
            return [IsOwner]
        else:
            return [IsAuthenticated,IsTeacher]
class TeacherViewSet(ModelViewSet):
    queryset=Teacher.objects.all()
    serializer_class=TeacherSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated,IsTeacher]
    def get_permissions(self):
        if self.action in ['update','destroy','partial_update']:
            return [IsOwner]
        else:
            return [IsAuthenticated,IsTeacher]
    http_method_names=['get','put','patch']
class StudentViewSet(ModelViewSet):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated,IsStudent]
    def get_permissions(self):
        if self.action in ['update','destroy','partial_update']:
            return [IsOwner]
        else:
            return [IsAuthenticated,IsStudent]