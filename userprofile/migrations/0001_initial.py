# Generated by Django 2.2.19 on 2021-05-30 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import userprofile.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Userprofile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('birth_date', models.DateField(null=True)),
                ('phone', models.CharField(max_length=17, null=True)),
                ('address', models.CharField(max_length=256, null=True)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=8, null=True)),
                ('photo', models.ImageField(default='user_default.jpg', upload_to=userprofile.models.user_image)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__full_name'],
            },
        ),
    ]