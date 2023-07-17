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
    employee_name = models.CharField(max_length=30)
    company = models.CharField(max_length=30, default='SolarEdge')
    position = models.CharField(max_length=30, default='QA_automation_engineer')
    employment_type = models.CharField(max_length=30, choices=employment_type_choices)
    staff = models.CharField(max_length=30, choices=staff_choices)

    def __str__(self):
        return f"{self.employee_name}"

class Check(models.Model):
    check_date = models.DateField(auto_now_add=True)
    check_time = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee} at {self.check_time}"

class InOut(models.Model):
    check_date = models.DateField(auto_now_add=True)
    checkIn_time = models.DateTimeField(auto_now_add=True)
    checkOut_time = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

@receiver(models.signals.post_save, sender=Check)
def update_inout(sender, instance, **kwargs):
    if instance.employee is not None:
        inout, created = InOut.objects.get_or_create(employee=instance.employee, check_date=instance.check_date)
        check_time = instance.check_time

        if not inout.checkIn_time or check_time < inout.checkIn_time:
            inout.checkIn_time = check_time

        if not inout.checkOut_time or check_time > inout.checkOut_time:
            inout.checkOut_time = check_time

        inout.save()
