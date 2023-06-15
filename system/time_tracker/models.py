from django.db import models

# Create your models here.

class Checks(models.Model):
    check_date = models.DateField(auto_now_add=True)
    check_time = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='media')
    employee_id = models.IntegerField()