# Generated by Django 4.1.4 on 2023-02-25 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TricksterMain', '0012_programme_lesson_lessonnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]