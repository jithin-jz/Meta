# Generated by Django 5.1.4 on 2025-01-09 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.URLField(default='https://cdn-icons-png.flaticon.com/512/236/236832.png'),
        ),
    ]
