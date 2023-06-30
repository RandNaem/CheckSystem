from django.db import models
from django.dispatch import receiver

# Create your models here.
class Employee(models.Model):
    employment_type_choices = (
        ('Full_time', 'Full_time'),
        ('Part_time', 'Part_time'),
        )
    staff_choices = (
        ('Production', 'Production'),
        ('Operation', 'Operation'),
        ('Sales', 'Sales'),
        ('Finance', 'Finance'),
        )
    employee_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    position = models.CharField(max_length=30, default='QA_automation_engineer')
    employment_type = models.CharField(max_length=30, choices=employment_type_choices)
    staff = models.CharField(max_length=30, choices=staff_choices)

class Check(models.Model):
    check_date = models.DateField(auto_now_add=True)
    check_time = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='media')
    employee_id = models.IntegerField()

    def __str__(self):
        return f"{self.employee_id} at {self.check_time}"

class InOut(models.Model):
    check_date = models.DateField(auto_now_add=True)
    checkIn_time = models.DateTimeField(auto_now_add=True)
    checkOut_time = models.DateTimeField(auto_now_add=True)
    employee_id = models.IntegerField()

@receiver(models.signals.post_save, sender=Check)
def update_inout(sender, instance, **kwargs):
    if instance.employee_id is not None:
        inout, created = InOut.objects.get_or_create(employee_id=instance.employee_id, check_date=instance.check_date)
        check_time = instance.check_time

        if not inout.checkIn_time or check_time < inout.checkIn_time:
            inout.checkIn_time = check_time

        if not inout.checkOut_time or check_time > inout.checkOut_time:
            inout.checkOut_time = check_time

        inout.save()