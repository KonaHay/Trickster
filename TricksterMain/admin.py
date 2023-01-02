from django.contrib import admin
from .models import SkillLevel
from .models import Trick
from .models import User

#admin.site.register(SkillLevel)
#admin.site.register(Trick)
#admin.site.register(User)


@admin.register(Trick)
class TrickAdmin(admin.ModelAdmin):
    fields = ('TrickName', 'TrickRecLevel', 'TrickDifficulty','TrickDiscription', 'TrickHowTo', 'TrickImg',)
    list_display = ('TrickName', 'TrickRecLevel', 'TrickDifficulty',)
    ordering = ('TrickDifficulty',)
    search_fields = ('TrickName',)
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('FirstName', 'LastName', 'Username','Email', 'SkillLevel', 'DateOfJoining', 'ProfilePhoto', 'LearnedTricks',)
    list_display = ('LastName', 'FirstName', 'Username','SkillLevel', 'DateOfJoining',)
    ordering = ('-DateOfJoining',)
    search_fields = ('Username', 'UserID')

@admin.register(SkillLevel)
class SkillLevelAdmin(admin.ModelAdmin):
    list_display = ('SkillLevelName', 'SkillLevelID',)
    ordering = ('SkillLevelID',)
    search_fields = ('SkillLevelName', 'SkillLevelID',)