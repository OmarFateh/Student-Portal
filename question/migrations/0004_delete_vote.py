# Generated by Django 2.2.19 on 2021-06-24 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_auto_20210624_2137'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Vote',
        ),
    ]