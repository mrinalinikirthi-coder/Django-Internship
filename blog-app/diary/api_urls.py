from django.urls import path
from . import api_views

urlpatterns = [
    # Authentication
    path('register/', api_views.register_view, name='api_register'),
    path('login/', api_views.login_view, name='api_login'),
    path('logout/', api_views.logout_view, name='api_logout'),
    
    # Users
    path('users/', api_views.user_list, name='api_user_list'),
    path('users/<int:id>/', api_views.user_detail, name='api_user_detail'),
    
    # Posts
    path('posts/', api_views.post_list, name='api_post_list'),
    path('posts/<int:id>/', api_views.post_detail, name='api_post_detail'),
    path('posts/create/', api_views.post_create, name='api_post_create'),
    path('posts/update/<int:id>/', api_views.post_update, name='api_post_update'),
    path('posts/delete/<int:id>/', api_views.post_delete, name='api_post_delete'),
    
    # Comments
    path('comments/', api_views.comment_list, name='api_comment_list'),
    path('comments/post/<int:post_id>/', api_views.comment_list_by_post, name='api_comment_by_post'),
    path('comments/create/', api_views.comment_create, name='api_comment_create'),
    path('comments/delete/<int:id>/', api_views.comment_delete, name='api_comment_delete'),
    
    # Edit History
    path('history/', api_views.edit_history_list, name='api_history_list'),
    path('history/post/<int:post_id>/', api_views.edit_history_by_post, name='api_history_by_post'),
]