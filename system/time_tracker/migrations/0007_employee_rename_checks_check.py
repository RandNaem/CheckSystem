# Generated by Django 4.2.2 on 2023-06-17 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_tracker', '0006_inout_delete_checkin_delete_checkout'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField(unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('position', models.CharField(default='QA_automation_engineer', max_length=30)),
                ('employment_type', models.CharField(choices=[('Full_time', 'Full_time'), ('Part_time', 'Part_time')], max_length=30)),
                ('staff', models.CharField(choices=[('Production', 'Production'), ('Operation', 'Operation'), ('Sales', 'Sales'), ('Finance', 'Finance')], max_length=30)),
            ],
        ),
        migrations.RenameModel(
            old_name='Checks',
            new_name='Check',
        ),
    ]