    from django.db import models
    class Teacher(models.Model):
        gen_choices=[('M','Male'),('F','Female'),('O',"Other")]
        t_name=models.CharField(max_length=75)
        qualification=models.CharField(max_length=30)
        years_of_exp=models.SmallIntegerField()
        gender=models.CharField(max_length=10,choices=gen_choices)
        t_Mail=models.EmailField(unique=True)
        log_pass=models.CharField(max_length=300)
        t_nationality=models.CharField(max_length=30)
        sub_id=models.ForeignKey('Subject',on_delete=models.Cascade)
    class Student(models.Model):
        gen_choices=[('M','Male'),('F','Female'),('O',"Other")]
        gr_choices=[('I','1st'),('II','2nd'),('III','3rd'),('IV','4th'),('V','5th'),('VI','6th')
        ('VII','7th'),('VIII','8th'),('IX','9th'),('X','10th'),('XI','11th'),('XII','12th')]
        s_name=models.CharField(max_length=75)
        grade=models.CharField(max_length=8,choices=gr_choices)
        school_name=models.CharField(max_length=50)
        login_pass=models.CharField(max_length=300)
        gender=models.CharField(max_length=10,choices=gen_choices)
        s_Mail=models.EmailField(unique=True)
        s_nationality=models.CharField(max_length=30)
        sub_id=models.ForeignKey('Subject',on_delete=models.Cascade)
    class Subject(models.Model):
        sub_name=models.CharField(max_length=50)
    class Posts(models.Model):
        s_id=models.ForeignKey('Student',on_delete=models.Cascade)
        sub_id=models.ForeignKey('Subject',on_delete=models.Cascade)
        t_id=models.ForeignKey('Teacher',on_delete=models.Cascade)
        content=models.TextField()
        created_at=models.DateTimeField(auto_now_add=True)