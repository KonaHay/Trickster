from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from embed_video.fields import EmbedVideoField

class SkillLevel (models.Model):
  SkillLevelID = models.AutoField(primary_key=True)
  SkillLevelName = models.CharField(max_length=25)

  def __str__(self):
    return self.SkillLevelName

class Category (models.Model):
  CategoryID = models.AutoField(primary_key=True)
  CategoryName = models.CharField(max_length=25)
  CategoryDescription = models.TextField(blank=True)
  CategoryImg = models.ImageField(null=True, blank=True, upload_to="images/")
  slug = models.SlugField(null=True)

  def __str__(self):
    return self.CategoryName
  
  def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)

class Trick (models.Model):
  TrickID = models.AutoField(primary_key=True)
  TrickName = models.CharField(max_length=25)
  TrickDiscription = models.TextField(blank=True)
  TrickHowTo = models.TextField(blank=True)
  TrickRecLevel = models.ForeignKey(SkillLevel, blank=True, null=True, on_delete=models.CASCADE)
  TrickDifficulty = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
  TrickImg = models.ImageField(null=True, blank=True, upload_to="images/")
  TrickCategory = models.ManyToManyField(Category, related_name='trick_category_tags', blank=True)

  def __str__(self):
    return self.TrickName

class Trick_Programme (models.Model):
  ProgrammeID = models.AutoField(primary_key=True)
  ProgrammeName = models.CharField(max_length=25)
  ProgrammeDiscription = models.TextField(blank=True)
  ProgrammeTricks = models.ManyToManyField(Trick, related_name='programme_tricks', blank=True)
  ProgrammeRecLevel = models.ForeignKey(SkillLevel, blank=True, null=True, on_delete=models.CASCADE)
  ProgrammeDifficulty = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
  ProgrammeImg = models.ImageField(null=True, blank=True, upload_to="images/")
  ProgrammeCategory = models.ManyToManyField(Category, related_name='programme_category_tags', blank=True)

  def __str__(self):
    return self.ProgrammeName

class Programme_Lesson (models.Model):
  LessonID = models.AutoField(primary_key=True)
  Programme = models.ForeignKey(Trick_Programme, related_name='lesson', blank=True, null=True, on_delete=models.CASCADE)
  LessonNumber = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
  LessonName = models.CharField(max_length=25)
  LessonShortDesc = models.TextField(blank=True)
  LessonLongDesc = models.TextField(blank=True)
  LessonVideo = EmbedVideoField(blank=True)

  def __str__(self):
    return self.LessonName

class Glossary_Term (models.Model):
  TermID = models.AutoField(primary_key=True)
  KeyWord = models.CharField(max_length=25)
  Description = models.TextField(blank=True)
  CommonlyUsed = models.BooleanField(default=False)