# Generated by Django 3.1.1 on 2020-09-22 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0011_auto_20200923_0045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='soldout',
        ),
    ]