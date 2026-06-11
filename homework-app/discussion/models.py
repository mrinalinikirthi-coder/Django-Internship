from django.db import models
class Teachers(models.Model):
    T_id=models.CharField(max_length=10,unique=True,primary_key=True)
    T_name=models.CharField(max_length=75)
    Qualification=models.CharField(max_length=30)
    Years_of_Exp=models.SmallIntegerField()
    Gender=models.CharField(max_length=10)
    T_Mail=models.EmailField(unique=True)
    Log_Pass=models.CharField(max_length=300)
    T_Nationality=models.CharField(max_length=30)
class Students(models.Model):
    S_id=models.CharField(max_length=10,unique=True,primary_key=True)
    S_name=models.CharField(max_length=75)
    Grade=models.CharField(max_length=8)
    School_Name=models.CharField(max_length=50)
    Login_Pass=models.CharField(max_length=300)
    S_Mail=models.EmailField(unique=True)
    S_Nationality=models.CharField(max_length=30)