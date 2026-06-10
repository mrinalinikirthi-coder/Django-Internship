from rest_framework import serializers
from .models import User, Post, Comment, EditHistory

# ==================== USER SERIALIZER ====================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']


# ==================== COMMENT SERIALIZER ====================

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.name')
    user_id = serializers.ReadOnlyField(source='user.id')
    
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'user', 'user_name', 'user_id', 'post', 'created_at']
        read_only_fields = ['id', 'created_at', 'user_name', 'user_id']


# ==================== EDIT HISTORY SERIALIZER ====================

class EditHistorySerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.name')
    post_title = serializers.ReadOnlyField(source='post.title')
    
    class Meta:
        model = EditHistory
        fields = ['id', 'post', 'post_title', 'user', 'user_name', 
                  'old_title', 'new_title', 'old_content', 'new_content', 'edited_at']
        read_only_fields = ['id', 'edited_at', 'user_name', 'post_title']


# ==================== POST SERIALIZER (with nested data) ====================

class PostSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.name')
    user_id = serializers.ReadOnlyField(source='user.id')
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    edit_history = EditHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'user', 'user_name', 'user_id', 
                  'created_at', 'updated_at', 'comments', 'comment_count', 'edit_history']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user_name', 'user_id', 
                           'comments', 'comment_count', 'edit_history']


# ==================== POST SERIALIZER (for create/update - without nested fields) ====================

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'user', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


# ==================== REGISTER SERIALIZER (for creating users via API) ====================

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'confirm_password']
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already registered"})
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User(
            name=validated_data['name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# ==================== LOGIN SERIALIZER ====================

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)