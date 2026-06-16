from rest_framework import serializers
from .models import Subject,Student,Teacher,Post,Reply
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
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
class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)
    email=serializers.EmailField()
    def create(self,validated_data):
        user=User.objects.create_user(username=validated_data['username'] , email = validated_data['email'],password = validated_data['password'])
        token=Token.objects.create(user=user)
        return {"user" : user , "token" : token}
