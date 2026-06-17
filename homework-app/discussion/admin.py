from django.contrib import admin
from .models import Teacher,Student,Subject,Reply,Post
admin.register(Student)
admin.register(Teacher)
admin.register(Subject)
admin.register(Reply)
admin.register(Post)