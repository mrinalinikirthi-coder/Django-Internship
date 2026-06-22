from rest_framework import permissions  
from .models import Post, Reply

class IsStudent(permissions.BasePermission):

    def has_permission(self, request,view):
        print("Current user:",request.user)
        print("Has student:",hasattr(request.user,'student'))

        if hasattr(request.user, 'student'):
            print("Student Exists")
            return True
        print("Student does not exist")
        return False
    

class IsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):        
        if hasattr(request.user, 'teacher'):
            return True
        else:
            return False
        

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # For Post objects
        if hasattr(obj, 'student'):
            return obj.student.user == request.user
        
        # For Reply objects
        if hasattr(obj, 'teacher'):
            return obj.teacher.user == request.user
        
        # For Student/Teacher objects
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False