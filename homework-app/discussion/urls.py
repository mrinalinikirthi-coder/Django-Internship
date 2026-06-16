from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet,PostViewSet,ReplyViewSet,TeacherViewSet,StudentViewSet
router=DefaultRouter()
router.register('posts',PostViewSet)
router.register('replies',ReplyViewSet)
router.register('students',StudentViewSet)
router.register('teachers',TeacherViewSet)
router.register('subjects',SubjectViewSet)
urlpatterns=[
    path('api/',include(router.urls))
]