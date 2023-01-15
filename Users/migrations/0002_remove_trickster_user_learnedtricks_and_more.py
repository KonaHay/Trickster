# Generated by Django 4.1.4 on 2023-01-14 22:43

import Users.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TricksterMain', '0006_delete_user'),
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trickster_user',
            name='LearnedTricks',
        ),
        migrations.RemoveField(
            model_name='trickster_user',
            name='ProfilePhoto',
        ),
        migrations.RemoveField(
            model_name='trickster_user',
            name='SkillLevel',
        ),
        migrations.RemoveField(
            model_name='trickster_user',
            name='UserDifficultyLevel',
        ),
        migrations.AlterField(
            model_name='trickster_user',
            name='FirstName',
            field=models.CharField(max_length=25, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='trickster_user',
            name='LastName',
            field=models.CharField(max_length=25, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='trickster_user',
            name='Username',
            field=models.CharField(max_length=25, unique=True, verbose_name='Username'),
        ),
        migrations.AlterField(
            model_name='trickster_user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='User_Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProfilePhoto', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('UserDifficultyLevel', models.PositiveIntegerField(default=1, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('Follows', models.ManyToManyField(blank=True, related_name='followed_by', to='Users.user_profile')),
                ('LearnedTricks', models.ManyToManyField(blank=True, to='TricksterMain.trick')),
                ('SkillLevel', models.ForeignKey(blank=True, default=Users.models.get_default_skill_level, null=True, on_delete=django.db.models.deletion.CASCADE, to='TricksterMain.skilllevel')),
                ('User', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
