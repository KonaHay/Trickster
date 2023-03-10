# Generated by Django 4.1.4 on 2023-02-26 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TricksterMain', '0013_category_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Glossary_Term',
            fields=[
                ('TermID', models.AutoField(primary_key=True, serialize=False)),
                ('KeyWord', models.CharField(max_length=25)),
                ('Description', models.TextField(blank=True)),
                ('CommonlyUsed', models.BooleanField(default=False)),
            ],
        ),
    ]
