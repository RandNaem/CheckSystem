# Generated by Django 4.2.2 on 2023-06-10 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_tracker', '0002_rename_qr_code_check_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='qr_code',
            field=models.ImageField(upload_to='media'),
        ),
    ]