from rest_framework import permissions  
from .models import Post, Reply
class IsAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.method in ('GET', 'HEAD', 'OPTIONS')
        return False
class IsStudent(permissions.BasePermission):
    def has_permission(self,request,view):
        print("Current user:",request.user)
        print("Has student:",hasattr(request.user,'student'))

        if hasattr(request.user,'student'):
            print("Student Exists")
            return True
        print("Student does not exist")
        return False
class IsTeacher(permissions.BasePermission):
    def has_permission(self,request,view):        
        if hasattr(request.user,'teacher'):
            return True
        else:
            return False
class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        print("=== has_permission called ===")
        print("Current user:", request.user)
        return True

    def has_object_permission(self, request, view, obj):
        print("=== has_object_permission called ===")
        print("Object:", obj)

        if isinstance(obj, Post):
            print("Post owner:", obj.student.user)
            print("Current user:", request.user)
            return obj.student.user == request.user

        if isinstance(obj, Reply):
            print("Reply owner:", obj.teacher.user)
            print("Current user:", request.user)
            return obj.teacher.user == request.user

        return False