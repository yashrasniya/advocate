# Generated by Django 4.1.3 on 2022-11-08 05:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='adhar_number',
            field=models.CharField(default=django.utils.timezone.now, max_length=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='advocate_license',
            field=models.ImageField(blank=True, upload_to='advocate_license'),
        ),
        migrations.AddField(
            model_name='user',
            name='profession',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='profile_pic'),
        ),
    ]
