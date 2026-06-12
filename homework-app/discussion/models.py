from django.db import models
from django.contrib.auth.models import User
class Teacher(models.Model):
    gen_choices=[('M','Male'),('F','Female'),('O',"Other")]
    name=models.CharField(max_length=75)
    qualification=models.CharField(max_length=30)
    years_of_exp=models.SmallIntegerField()
    gender=models.CharField(max_length=10,choices=gen_choices)
    nationality=models.CharField(max_length=30)
    subject=models.ForeignKey('Subject',on_delete=models.CASCADE)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
class Student(models.Model):
    gen_choices=[('M','Male'),('F','Female'),('O',"Other")]
    gr_choices=[('I','1st'),('II','2nd'),('III','3rd'),('IV','4th'),('V','5th'),('VI','6th'),
    ('VII','7th'),('VIII','8th'),('IX','9th'),('X','10th'),('XI','11th'),('XII','12th')]
    name=models.CharField(max_length=75)
    grade=models.CharField(max_length=8,choices=gr_choices)
    school_name=models.CharField(max_length=50)
    gender=models.CharField(max_length=10,choices=gen_choices)
    nationality=models.CharField(max_length=30)
    subject=models.ForeignKey('Subject',on_delete=models.CASCADE)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
class Subject(models.Model):
    name=models.CharField(max_length=50)
class Post(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
class Reply(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    reply=models.TextField()
    created_at=models.DateTimeField()
