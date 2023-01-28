from django.contrib import admin
from django.contrib.auth.models import Group

#Import Models
from .models import SkillLevel, Trick, Trick_Programme

#Unregister Groups
admin.site.unregister(Group)


@admin.register(Trick)
class TrickAdmin(admin.ModelAdmin):
    fields = ('TrickName', 'TrickRecLevel', 'TrickDifficulty','TrickDiscription', 'TrickHowTo', 'TrickImg',)
    list_display = ('TrickName', 'TrickRecLevel', 'TrickDifficulty',)
    ordering = ('TrickRecLevel', 'TrickDifficulty', 'TrickName')
    search_fields = ('TrickName',)

@admin.register(SkillLevel)
class SkillLevelAdmin(admin.ModelAdmin):
    list_display = ('SkillLevelName', 'SkillLevelID',)
    ordering = ('SkillLevelID',)
    search_fields = ('SkillLevelName', 'SkillLevelID',)

@admin.register(Trick_Programme)
class TrickProgrammeAdmin(admin.ModelAdmin):
    fields = ('ProgrammeName', 'ProgrammeRecLevel', 'ProgrammeDifficulty','ProgrammeDiscription', 'ProgrammeTricks', 'ProgrammeImg',)
    list_display = ('ProgrammeName', 'ProgrammeRecLevel', 'ProgrammeDifficulty',)
    ordering = ('ProgrammeRecLevel', 'ProgrammeDifficulty', 'ProgrammeName')
    search_fields = ('ProgrammeName',)