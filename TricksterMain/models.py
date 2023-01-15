from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class SkillLevel (models.Model):
    SkillLevelID = models.AutoField(primary_key=True)
    SkillLevelName = models.CharField(max_length=25)

    def __str__(self):
        return self.SkillLevelName

class Trick (models.Model):
    TrickID = models.AutoField(primary_key=True)
    TrickName = models.CharField(max_length=25)
    TrickDiscription = models.TextField(blank=True)
    TrickHowTo = models.TextField(blank=True)
    TrickRecLevel = models.ForeignKey(SkillLevel, blank=True, null=True, on_delete=models.CASCADE)
    TrickDifficulty = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    TrickImg = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.TrickName


