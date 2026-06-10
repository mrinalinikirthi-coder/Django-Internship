from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import User, Post, Comment, EditHistory
from django.utils import timezone

# ==================== AUTHENTICATION VIEWS ====================

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('signup')
        
        user = User(name=name, email=email)
        user.set_password(password)
        user.save()
        
        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')
    
    return render(request, 'signup.html')  # Changed

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Custom authentication using email
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid password')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email')
        
    return render(request, 'login.html')  # Changed

def logout_view(request):
    logout(request)
    return redirect('home')

# ==================== POST VIEWS ====================

def home_view(request):
    posts = Post.objects.all().order_by('-created_at')  # Newest first
    return render(request, 'home.html', {'posts': posts})  # Changed

def single_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(
                comment=comment_text,
                user=request.user,
                post=post
            )
            messages.success(request, 'Comment added')
            return redirect('single_post', post_id=post.id)
    
    return render(request, 'single_post.html', {  # Changed
        'post': post,
        'comments': comments
    })

@login_required
def create_post_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        Post.objects.create(
            title=title,
            content=content,
            user=request.user
        )
        messages.success(request, 'Post created successfully')
        return redirect('home')
    
    return render(request, 'create_post.html')  # Changed

@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if current user is the author
    if post.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this post")
    
    if request.method == 'POST':
        new_title = request.POST.get('title')
        new_content = request.POST.get('content')
        
        # Track changes for EditHistory
        old_title = post.title
        old_content = post.content
        
        # Check what changed
        title_changed = (old_title != new_title)
        content_changed = (old_content != new_content)
        
        if title_changed or content_changed:
            EditHistory.objects.create(
                post=post,
                user=request.user,
                old_title=old_title if title_changed else None,
                new_title=new_title if title_changed else None,
                old_content=old_content if content_changed else None,
                new_content=new_content if content_changed else None
            )
        
        # Update the post
        post.title = new_title
        post.content = new_content
        post.save()
        
        messages.success(request, 'Post updated successfully')
        return redirect('single_post', post_id=post.id)
    
    return render(request, 'edit_post.html', {'post': post})  # Changed

@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if current user is the author
    if post.user != request.user:
        return HttpResponseForbidden("You don't have permission to delete this post")
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully')
        return redirect('home')
    
    return render(request, 'delete_post.html', {'post': post})  # Changed