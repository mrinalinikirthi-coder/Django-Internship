from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Posts
    path('', views.home_view, name='home'),  # Home page (list all posts)
    path('post/<int:post_id>/', views.single_post_view, name='single_post'),
    path('create/', views.create_post_view, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post_view, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post_view, name='delete_post'),
]