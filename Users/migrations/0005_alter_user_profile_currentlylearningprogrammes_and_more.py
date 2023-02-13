# Generated by Django 4.1.4 on 2023-01-24 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TricksterMain', '0008_rename_trick_programmes_trick_programme'),
        ('Users', '0004_user_profile_currentlylearningprogrammes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='CurrentlyLearningProgrammes',
            field=models.ManyToManyField(blank=True, related_name='currently_learning_programme', to='TricksterMain.trick'),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='SavedProgrammes',
            field=models.ManyToManyField(blank=True, related_name='saved_programme', to='TricksterMain.trick'),
        ),
    ]