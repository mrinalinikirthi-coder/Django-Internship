from django.db import models
class Teachers(models.Model):
    T_id=models.CharField(max_length=10,unique=True,primary_key=True)
    T_name=models.CharField(max_length=75)
    Subject=models.CharField(max_length=25)
    Qualification=models.CharField(max_length=30)
    Years_of_Exp=models.SmallIntegerField()
    Gender=models.CharField(max_length=10)
    Mail=models.EmailField(unique=True)
    Log_Pass=models.CharField(max_length=300)