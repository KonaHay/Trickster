# Generated by Django 4.1.4 on 2023-03-29 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TricksterMain', '0018_remove_quiz_question_questionquiz_and_more'),
        ('TricksterQuiz', '0002_alter_bonus_answer_answertext_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz_section',
            options={'verbose_name_plural': 'Quiz Sections'},
        ),
        migrations.RemoveField(
            model_name='quiz_section',
            name='SectionType',
        ),
        migrations.AddField(
            model_name='quiz_section',
            name='SectionLevel',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, related_name='section_level', to='TricksterMain.skilllevel'),
        ),
    ]