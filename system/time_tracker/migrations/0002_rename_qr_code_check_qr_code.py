# Generated by Django 4.2.2 on 2023-06-09 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('time_tracker', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='check',
            old_name='QR_code',
            new_name='qr_code',
        ),
    ]
