from django.contrib import admin
from django.contrib.auth.models import Group

#Import Models
from .models import SkillLevel, Trick, Trick_Programme, Category, Programme_Lesson, Glossary_Term

#Unregister Groups
admin.site.unregister(Group)

@admin.register(Trick)
class TrickAdmin(admin.ModelAdmin):
  fields = ('TrickName', 'TrickRecLevel', 'TrickDifficulty', 'TrickDiscription', 'TrickHowTo', 'TrickCategory', 'TrickImg', 'TrickVideo', 'SubmittedByID', 'approved')
  list_display = ('TrickName', 'TrickRecLevel', 'TrickDifficulty',)
  ordering = ('TrickRecLevel', 'TrickDifficulty', 'TrickName')
  search_fields = ('TrickName',)
  list_filter = ('TrickCategory', 'TrickRecLevel', 'approved')

@admin.register(SkillLevel)
class SkillLevelAdmin(admin.ModelAdmin):
  list_display = ('SkillLevelName', 'SkillLevelID',)
  ordering = ('SkillLevelID',)
  search_fields = ('SkillLevelName', 'SkillLevelID',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('CategoryName', 'CategoryID',)
  ordering = ('CategoryID',)
  search_fields = ('CategoryName', 'CategoryID',)

@admin.register(Trick_Programme)
class TrickProgrammeAdmin(admin.ModelAdmin):
  fields = ('ProgrammeName', 'ProgrammeRecLevel', 'ProgrammeDifficulty','ProgrammeDiscription', 'ProgrammeTricks', 'ProgrammeImg', 'ProgrammeCreatorID')
  list_display = ('ProgrammeName', 'ProgrammeRecLevel', 'ProgrammeDifficulty',)
  ordering = ('ProgrammeRecLevel', 'ProgrammeDifficulty', 'ProgrammeName')
  search_fields = ('ProgrammeName',)

@admin.register(Programme_Lesson)
class ProgrammeLessonAdmin(admin.ModelAdmin):
  fields = ('Programme', 'LessonName', 'LessonNumber', 'LessonShortDesc','LessonLongDesc', 'LessonVideo', )
  list_display = ('LessonName', 'LessonShortDesc',)
  ordering = ('Programme', 'LessonName',)
  search_fields = ('LessonName', 'Programme',)

@admin.register(Glossary_Term)
class GlossaryAdmin(admin.ModelAdmin):
  fields = ('KeyWord', 'Description', 'CommonlyUsed')
  list_display = ('KeyWord', 'Description',)
  ordering = ('CommonlyUsed', 'KeyWord',)
  search_fields = ('KeyWord', 'CommonlyUsed',)
