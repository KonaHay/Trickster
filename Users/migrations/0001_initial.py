# Generated by Django 4.1.4 on 2023-01-12 18:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('TricksterMain', '0006_delete_user'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trickster_User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('UserID', models.AutoField(primary_key=True, serialize=False)),
                ('Email', models.EmailField(max_length=254, unique=True, verbose_name='Email Address')),
                ('Username', models.CharField(max_length=25, unique=True)),
                ('FirstName', models.CharField(max_length=25)),
                ('LastName', models.CharField(max_length=25)),
                ('DateOfJoining', models.DateField(default=django.utils.timezone.now)),
                ('ProfilePhoto', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('UserDifficultyLevel', models.PositiveIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('LearnedTricks', models.ManyToManyField(blank=True, to='TricksterMain.trick')),
                ('SkillLevel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TricksterMain.skilllevel')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
