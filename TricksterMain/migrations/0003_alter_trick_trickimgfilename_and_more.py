# Generated by Django 4.1.4 on 2023-01-01 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TricksterMain', '0002_rename_skilllevels_skilllevel_rename_tricks_trick_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trick',
            name='TrickImgFileName',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='PhotoFileName',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
