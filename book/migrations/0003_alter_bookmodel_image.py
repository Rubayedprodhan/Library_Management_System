# Generated by Django 5.0.6 on 2024-09-21 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_alter_bookmodel_category_alter_bookmodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmodel',
            name='image',
            field=models.ImageField(upload_to='media/book'),
        ),
    ]
