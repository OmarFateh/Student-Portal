# Generated by Django 2.2.19 on 2021-05-30 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
