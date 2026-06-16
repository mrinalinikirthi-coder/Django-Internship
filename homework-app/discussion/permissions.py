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
    def has_object_permission(self,request,view,obj):
        if not(request.user.is_authenticated):
            return False
        if not(hasattr(obj,'user')):
            return False
        if obj.user==request.user:
            return True
        return False