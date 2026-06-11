from django.db import models
class Teacher(models.Model):
    t_id=models.CharField(max_length=10,unique=True,primary_key=True)
    t_name=models.CharField(max_length=75)
    qualification=models.CharField(max_length=30)
    years_of_exp=models.SmallIntegerField()
    gender=models.CharField(max_length=10)
    t_Mail=models.EmailField(unique=True)
    log_pass=models.CharField(max_length=300)
    t_nationality=models.CharField(max_length=30)
    sub_id=models.ForeighKey('Subject',on_delete=models.Cascade)
class Student(models.Model):
    s_id=models.CharField(max_length=10,unique=True,primary_key=True)
    s_name=models.CharField(max_length=75)
    grade=models.CharField(max_length=8)
    school_name=models.CharField(max_length=50)
    login_pass=models.CharField(max_length=300)
    s_Mail=models.EmailField(unique=True)
    s_nationality=models.CharField(max_length=30)
    sub_id=models.ForeighKey('Subject',on_delete=models.Cascade)
class Subject(models.Model):
    sub_id=models.CharField(max_length=10,unique=True,primary_key=True)
    sub_name=models.CharField(max_length=50)
class Posts(models.Model):
    s_id=models.ForeignKey('Student',on_delete=models.Cascade)
    sub_id=models.ForeighKey('Subject',on_delete=models.Cascade)
    t_id=models.ForeignKey('Teacher',on_delete=models.Cascade)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)