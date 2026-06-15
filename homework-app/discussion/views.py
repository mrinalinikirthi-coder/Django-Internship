from rest_framework.viewsets import ModelViewSet
from .models import Teacher,Student,Subject,Post,Reply
from .serializers import SubjectSerializer,UserSerializer,StudentSerializer,TeacherSerializer,
PostSerializer,ReplySerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
class SubjectViewSet(ModelViewSet):
    queryset=Subject.objects.all()
    serializer_class=SubjectSerializer
    authentication_classes=[]
    permission_classes=[]
class PostViewSet(ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
class ReplyViewSet(ModelViewSet):
    queryset=Reply.objects.all()
    serializer_class=ReplySerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
class TeacherViewSet(ModelViewSet):
    queryset=Teacher.objects.all()
    serializer_class=TeacherSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
class StudentViewSet(ModelViewSet):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]