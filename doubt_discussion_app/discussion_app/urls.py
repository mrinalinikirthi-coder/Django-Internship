"""
URL configuration for the Discussion App.

This module defines all URL patterns for the application, including:
- Custom authentication endpoints (register, login, logout)
- REST API endpoints for all models via DRF's DefaultRouter

The router automatically generates standard CRUD endpoints for:
- posts: /api/posts/, /api/posts/{uuid}/
- replies: /api/replies/, /api/replies/{uuid}/
- students: /api/students/, /api/students/{uuid}/
- teachers: /api/teachers/, /api/teachers/{uuid}/
- subjects: /api/subjects/, /api/subjects/{uuid}/
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    LogoutView,
    SubjectViewSet,
    PostViewSet,
    ReplyViewSet,
    TeacherViewSet,
    StudentViewSet,
    RegisterView,
    LoginView,
)


# Initialize the default router for ViewSets
router = DefaultRouter()

# Register all ViewSets with the router for automatic CRUD endpoints
router.register('posts', PostViewSet)
router.register('replies', ReplyViewSet)
router.register('students', StudentViewSet)
router.register('teachers', TeacherViewSet)
router.register('subjects', SubjectViewSet)

# Custom URL patterns for authentication endpoints
# These are not part of the router because they are custom APIViews
urlpatterns = [
    # User registration endpoint
    path('register/', RegisterView.as_view(), name='register'),
    # User login endpoint (returns JWT tokens)
    path('login/', LoginView.as_view(), name='login'),
    # User logout endpoint (blacklists refresh token)
    path('logout/', LogoutView.as_view(), name='logout'),
]

# Add all router-generated URLs to the urlpatterns
urlpatterns += router.urls
