from rest_framework.viewsets import ModelViewSet
from .models import Teacher,Student,Subject,Post,Reply
from .serializers import SubjectSerializer,UserSerializer,StudentSerializer,TeacherSerializer,
PostSerializer,ReplySerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
class SubjectViewSet(viewsets.ModelViewSet):
    queryset=Subject.object.all()
    serializer_class=SubjectSerializer
    authentication_classes=[]
    permission_classes=[]
    