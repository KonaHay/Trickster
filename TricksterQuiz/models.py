from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from PIL import Image
import random


from TricksterMain.models import Trick, SkillLevel, Glossary_Term
from Users.models import User_Profile


class Skill_Level_Quiz(models.Model):
  QuizID = models.AutoField(primary_key=True)
  QuizTitle = models.CharField(max_length=30)
  QuizDiscription = models.TextField(blank=True)
  QuizNoOfSections = models.IntegerField()
  QuizImg = models.ImageField(null=True, blank=True, upload_to="images/quiz_images")

  def __str__(self):
    return self.QuizTitle
  
  class Meta:
    verbose_name_plural = 'Skill Level Quizes'

SECTION_TYPES = (
  ('tricks', 'tricks'),
  ('terms', 'terms'),
)

class Quiz_Section(models.Model):
  SectionID = models.AutoField(primary_key=True)
  SectionName = models.CharField(max_length=30)
  SectionQuiz = models.ForeignKey(Skill_Level_Quiz, on_delete=models.CASCADE, related_name="section")
  SectionDiscription = models.TextField(blank=True)
  SectionNoOfQuestions = models.IntegerField()
  SectionLevel = models.ForeignKey(SkillLevel, on_delete=models.CASCADE, related_name="section_level")
  SectionFailScore = models.IntegerField()
  SectionPassScore = models.IntegerField()
  SectionNumber = models.IntegerField()
  SectionImg = models.ImageField(null=True, blank=True, upload_to="images/quiz_images")

  def __str__(self):
    return f"{self.SectionName} - {self.SectionQuiz}"
  
  def get_questions(self):
    return self.questions.all()[:self.SectionNoOfQuestions]
  
  def get_bonus(self):
    return self.bonus_questions.all()
  
  class Meta:
    verbose_name_plural = 'Quiz Sections'

VALID_VALUES = (
  (1, 1),
  (2, 2),
  (4, 4),
  (8, 8),
  (16, 16),
  (32, 32),
)

class Section_Trick(models.Model):
  Trick = models.ForeignKey(Trick, on_delete=models.CASCADE, related_name='section_tricks')
  TrickSection = models.ForeignKey(Quiz_Section, on_delete=models.CASCADE, related_name="questions")
  TrickValue = models.IntegerField(choices=VALID_VALUES)

  def __str__(self):
    return f"Section: {self.Trick.TrickName}, Value: {self.TrickValue}, Trick: {self.Trick.TrickName}"

class Term_Bonus(models.Model):
  BonusName = models.CharField(max_length=30)
  BonusSection = models.ForeignKey(Quiz_Section, on_delete=models.CASCADE, related_name="bonus_questions")
  BonusNoOfTerms = models.IntegerField()
  BonusImg = models.ImageField(null=True, blank=True, upload_to="images/quiz_images")

  def __str__(self):
    return f"{self.BonusName} - {self.BonusSection}"
  
  def get_questions(self):
    questions = list(self.questions.all())
    random.shuffle(questions)
    return questions[:self.BonusNoOfTerms]
  
  class Meta:
    verbose_name_plural = 'Term Bonuses'

class Bonus_Question(models.Model):
  QuestionText = models.CharField(max_length=150)
  QuestionNumber = models.IntegerField()
  QuestionSection = models.ForeignKey(Term_Bonus, on_delete=models.CASCADE, related_name="questions")
  QuestionTerm = models.ForeignKey(Glossary_Term, on_delete=models.CASCADE, related_name='question_terms')
  QuestionImg = models.ImageField(null=True, blank=True, upload_to="images/quiz_images")

  def __str__(self):
    return self.QuestionText
  
  def get_answers(self):
    return self.answers.all()
  
class Bonus_Answer(models.Model):
  AnswerText = models.CharField(max_length=150)
  AnswerCorrect = models.BooleanField(default=False)
  AnswerQuestion = models.ForeignKey(Bonus_Question, on_delete=models.CASCADE, related_name="answers")

  def __str__(self):
    return f"question: {self.AnswerQuestion.QuestionText}, answer: {self.AnswerText}, correct: {self.AnswerCorrect}"
  
class Section_Result(models.Model):
  ResultSection = models.ForeignKey(Quiz_Section, on_delete=models.CASCADE, related_name="results")
  ResultBonus = models.ForeignKey(Term_Bonus, on_delete=models.CASCADE, related_name="bonus")
  ResultUser = models.ForeignKey(User_Profile, on_delete=models.CASCADE, related_name="user_profile")
  TrickScore = models.FloatField()
  BonusScore = models.FloatField()

  def __str__(self):
    return f"User: {self.ResultUser.User.Username}, Trick Score: {self.TrickScore}, Bonus Score: {self.BonusScore}"