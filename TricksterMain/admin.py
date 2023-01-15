from django.contrib import admin
from django.contrib.auth.models import Group

#Import Models
from .models import SkillLevel
from .models import Trick

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