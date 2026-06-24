from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import LogoutView, SubjectViewSet, PostViewSet, ReplyViewSet

from .views import TeacherViewSet, StudentViewSet, RegisterView, LoginView

router = DefaultRouter()

router.register('posts', PostViewSet)

router.register('replies', ReplyViewSet)

router.register('students', StudentViewSet)

router.register('teachers', TeacherViewSet)

router.register('subjects', SubjectViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]
urlpatterns += router.urls
