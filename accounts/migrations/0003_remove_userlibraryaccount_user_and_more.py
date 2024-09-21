# Generated by Django 5.0.6 on 2024-09-20 12:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_useraddress_postal_code'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlibraryaccount',
            name='user',
        ),
        migrations.AddField(
            model_name='userlibraryaccount',
            name='user',
            field=models.ManyToManyField(related_name='acount', to=settings.AUTH_USER_MODEL),
        ),
    ]
