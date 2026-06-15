from rest_framework import permissions  
class IsStudent(permissions.BasePermission):
    def has_permission(self,request,view):        
        if hasattr(request.user,'student'):
            return True
        else:
            return False
class IsTeacher(permissions.BasePermission):
    def has_permission(self,request,view):        
        if hasattr(request.user,'teacher'):
            return True
        else:
            return False
class IsOwner(permissions.BasePermission):
    