from rest_framework import serializers
from .models import Subject
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields=['id','sub_name']    
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