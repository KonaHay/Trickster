from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from TricksterMain.models import Trick, SkillLevel

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
  Username = models.CharField(('Username'),max_length=25, unique=True)
  FirstName = models.CharField(('First Name'),max_length=25)
  LastName = models.CharField(('Last Name'),max_length=25)
  DateOfJoining = models.DateField(default=timezone.now)
  ProfilePhoto = models.ImageField(null=True, blank=True, upload_to="images/")
  SkillLevel = models.ForeignKey(SkillLevel, default=get_default_skill_level, blank=True, null=True, on_delete=models.CASCADE)
  LearnedTricks  = models.ManyToManyField(Trick, blank=True)
  UserDifficultyLevel = models.PositiveIntegerField(default=1, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)

  objects = CustomUserManager()

  USERNAME_FIELD = 'Email'
  REQUIRED_FIELDS = ['Username', 'FirstName', 'LastName']

  def __str__(self):
      return self.FirstName + ' ' + self.LastName


  # class Meta:
  #     db_table = 'auth_user'
