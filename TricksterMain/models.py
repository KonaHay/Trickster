from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from embed_video.fields import EmbedVideoField
from PIL import Image

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
    self.slug = slugify(self.CategoryName)
    super(Category,self).save(*args,**kwargs)

    if self.CategoryImg:
      img = Image.open(self.CategoryImg.path)
      default_size = (960, 540)
      resized_img = img.resize(default_size)
      resized_img.format = img.format
      resized_img.save(self.CategoryImg.path)

class Trick (models.Model):
  TrickID = models.AutoField(primary_key=True)
  TrickName = models.CharField(max_length=25)
  TrickDiscription = models.TextField(blank=True)
  TrickHowTo = models.TextField(blank=True)
  TrickRecLevel = models.ForeignKey(SkillLevel, blank=True, null=True, on_delete=models.CASCADE)
  TrickDifficulty = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
  TrickImg = models.ImageField(null=True, blank=True, upload_to="images/")
  TrickVideo = EmbedVideoField(blank=True)
  TrickCategory = models.ManyToManyField(Category, related_name='trick_category_tags', blank=True)
  SubmittedByID = models.IntegerField("Submitted By ID", null=True)
  approved = models.BooleanField('Approved', default=False)

  def __str__(self):
    return self.TrickName
  
  def save(self,*args,**kwargs):
    super().save(*args, **kwargs)

    if self.TrickImg:
      img = Image.open(self.TrickImg.path)
      default_size = (960, 540)
      resized_img = img.resize(default_size)
      resized_img.format = img.format
      resized_img.save(self.TrickImg.path)

class Trick_Programme (models.Model):
  ProgrammeID = models.AutoField(primary_key=True)
  ProgrammeName = models.CharField(max_length=25)
  ProgrammeDiscription = models.TextField(blank=True)
  ProgrammeTricks = models.ManyToManyField(Trick, related_name='programme_tricks', blank=True)
  ProgrammeRecLevel = models.ForeignKey(SkillLevel, blank=True, null=True, on_delete=models.CASCADE)
  ProgrammeDifficulty = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
  ProgrammeImg = models.ImageField(null=True, blank=True, upload_to="images/")
  ProgrammeCategory = models.ManyToManyField(Category, related_name='programme_category_tags', blank=True)
  ProgrammeCreatorID = models.IntegerField("Programme Creator ID", blank=False, default=1)

  def __str__(self):
    return self.ProgrammeName
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    if self.ProgrammeImg:
      img = Image.open(self.ProgrammeImg.path)
      default_size = (960, 540)
      resized_img = img.resize(default_size)
      resized_img.format = img.format
      resized_img.save(self.ProgrammeImg.path)

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
  slug = models.SlugField(null=True)

  def __str__(self):
    return self.KeyWord

  def save(self,*args,**kwargs):
        self.slug = slugify(self.KeyWord)
        super(Glossary_Term,self).save(*args,**kwargs)
