from rest_framework import serializers
from .models import Subject,Student,Teacher,Post,Reply
from django.contrib.auth.models import User
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields=['id','name']    
class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','email','password']
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:   
        model=Teacher
        fields='__all__'
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields='__all__'
class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model=Reply
        fields='__all__'