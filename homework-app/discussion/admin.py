from django.contrib import admin

from .models import Teacher, Student, Subject, Reply, Post

admin.site.register(Student)

admin.site.register(Teacher)

admin.site.register(Subject)

admin.site.register(Reply)

admin.site.register(Post)
