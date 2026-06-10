from django.contrib import admin
from .models import User, Post, Comment, EditHistory

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(EditHistory)