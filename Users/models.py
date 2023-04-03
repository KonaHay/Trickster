from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.utils import timezone
from PIL import Image, ImageSequence

from TricksterMain.models import Trick, SkillLevel, Trick_Programme, Programme_Lesson



class CustomUserManager(BaseUserManager):

  def create_superuser(self, Email, Username, FirstName, LastName, password, **other_fields):

    other_fields.setdefault('is_staff', True)
    other_fields.setdefault('is_superuser', True)
    other_fields.setdefault('is_active', True)

    if other_fields.get('is_staff') is not True:
      raise ValueError(
        'Superuser must be assigned to is_staff=True.')
    if other_fields.get('is_superuser') is not True:
      raise ValueError(
        'Superuser must be assigned to is_superuser=True.')

    return self.create_user(Email, Username, FirstName, LastName, password, **other_fields)

  def create_user(self, Email, Username, FirstName, LastName, password, **other_fields):

    if not Email:
      raise ValueError('You must provide an email address')

    Email = self.normalize_email(Email)
    user = self.model(Email=Email, Username=Username, FirstName=FirstName, LastName=LastName, **other_fields)
    user.set_password(password)
    user.save()
    return user

def get_default_skill_level():
  return SkillLevel.objects.get(SkillLevelName="Beginner")

class Trickster_User(AbstractBaseUser, PermissionsMixin):

  UserID = models.AutoField(primary_key=True)
  Email = models.EmailField(('Email Address'), unique=True)
  Username = models.CharField(('Username'),max_length=16, unique=True)
  FirstName = models.CharField(('First Name'),max_length=25)
  LastName = models.CharField(('Last Name'),max_length=25)
  DateOfJoining = models.DateField(default=timezone.now)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)

  objects = CustomUserManager()

  USERNAME_FIELD = 'Email'
  REQUIRED_FIELDS = ['Username', 'FirstName', 'LastName']

  def __str__(self):
    return self.FirstName + ' ' + self.LastName

class User_Profile(models.Model):

  User = models.OneToOneField(Trickster_User, on_delete=models.CASCADE)
  ProfilePhoto = models.ImageField(null=True, blank=True, upload_to="images/profile")
  Bio = models.TextField(max_length=150, blank=True)
  SkillLevel = models.ForeignKey(SkillLevel, default=get_default_skill_level, blank=True, null=True, on_delete=models.CASCADE)
  MasteryLevel = models.PositiveIntegerField(default=1, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
  LevelProgress = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
  LearnedTricks = models.ManyToManyField(Trick, related_name='learned_trick', blank=True)
  SavedTricks = models.ManyToManyField(Trick, related_name='saved_trick', blank=True)
  CurrentlyLearningProgrammes = models.ManyToManyField(Trick_Programme, related_name='currently_learning_programme', blank=True)
  CompletedProgrammes = models.ManyToManyField(Trick_Programme, related_name='completed_programme', blank=True)
  CompletedLessons = models.ManyToManyField(Programme_Lesson, related_name='completed_lessons', blank=True)
  SavedProgrammes = models.ManyToManyField(Trick_Programme, related_name='saved_programme', blank=True)
  Follows =  models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
  completed_skill_quiz = models.BooleanField(default=False)

  def __str__(self):
    return self.User.Username
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    
    if self.ProfilePhoto:
      img = Image.open(self.ProfilePhoto.path)
      default_size = (500, 500)

      if img.format == 'GIF':
         # im is your original image
        resized_img = img.resize(default_size)
        resized_img.format = img.format
        resized_img.save(self.ProfilePhoto.path, save_all=True, append_images=[resized_img])

      else:
        resized_img = img.resize(default_size)
        resized_img.format = img.format
        resized_img.save(self.ProfilePhoto.path)

def create_profile(sender, instance, created, **kwargs):
  if created:
    New_Profile = User_Profile(User=instance)
    New_Profile.save()

post_save.connect(create_profile, sender=Trickster_User)