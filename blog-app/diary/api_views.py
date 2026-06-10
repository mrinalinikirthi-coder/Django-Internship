from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import User, Post, Comment, EditHistory
from .serializers import (
    UserSerializer, PostSerializer, PostCreateUpdateSerializer,
    CommentSerializer, EditHistorySerializer, RegisterSerializer, LoginSerializer
)

# ==================== AUTHENTICATION VIEWS ====================

@api_view(['POST'])
def register_view(request):
    """Register a new user"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User created successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    """Login user and start session"""
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Django's authenticate uses username field by default, so we need to use email
    # You'll need to create a custom authentication backend or use username
    # For now, let's use a simpler approach:
    if user.check_password(password):
        login(request, user)
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_view(request):
    """Logout user"""
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


# ==================== USER VIEWS ====================

@api_view(['GET'])
def user_list(request):
    """Get all users"""
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def user_detail(request, id):
    """Get a specific user"""
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user)
    return Response(serializer.data)


# ==================== POST VIEWS ====================

@api_view(['GET'])
def post_list(request):
    """Get all posts (with comments and edit history)"""
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def post_detail(request, id):
    """Get a specific post (with comments and edit history)"""
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PostSerializer(post)
    return Response(serializer.data)


@api_view(['POST'])
def post_create(request):
    """Create a new post"""
    # For now, let's set user_id = 1 (you can change this to get from session)
    # Later you can use: user = request.user if authenticated
    data = request.data.copy()
    
    # Temporary: use first user or require user_id in request
    if 'user' not in data:
        first_user = User.objects.first()
        if first_user:
            data['user'] = first_user.id
        else:
            return Response({'error': 'No user exists. Create a user first.'}, 
                          status=status.HTTP_400_BAD_REQUEST)
    
    serializer = PostCreateUpdateSerializer(data=data)
    if serializer.is_valid():
        post = serializer.save()
        # Return full post data using PostSerializer
        full_serializer = PostSerializer(post)
        return Response(full_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def post_update(request, id):
    """Update an existing post"""
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PostCreateUpdateSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        updated_post = serializer.save()
        full_serializer = PostSerializer(updated_post)
        return Response(full_serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def post_delete(request, id):
    """Delete a post"""
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    post.delete()
    return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# ==================== COMMENT VIEWS ====================

@api_view(['GET'])
def comment_list(request):
    """Get all comments"""
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def comment_list_by_post(request, post_id):
    """Get comments for a specific post"""
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    comments = post.comments.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def comment_create(request):
    """Create a new comment"""
    data = request.data.copy()
    
    # Temporary: use first user if not specified
    if 'user' not in data:
        first_user = User.objects.first()
        if first_user:
            data['user'] = first_user.id
        else:
            return Response({'error': 'No user exists. Create a user first.'}, 
                          status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CommentSerializer(data=data)
    if serializer.is_valid():
        comment = serializer.save()
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def comment_delete(request, id):
    """Delete a comment"""
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    comment.delete()
    return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# ==================== EDIT HISTORY VIEWS ====================

@api_view(['GET'])
def edit_history_list(request):
    """Get all edit history"""
    history = EditHistory.objects.all()
    serializer = EditHistorySerializer(history, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def edit_history_by_post(request, post_id):
    """Get edit history for a specific post"""
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    history = post.edit_history.all()
    serializer = EditHistorySerializer(history, many=True)
    return Response(serializer.data)