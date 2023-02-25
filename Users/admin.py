from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Trickster_User, User_Profile

class ProfileInline(admin.StackedInline):
  model = User_Profile
  fieldsets = (
        ('Profile Info', {'fields': ('User', 'ProfilePhoto', 'SkillLevel', 'UserDifficultyLevel', 'UserLevelProgress', 'Follows')}),
        ('Trick Data', {'fields': ('LearnedTricks', 'SavedTricks')}),
        ('Programme Data', {'fields': ('CurrentlyLearningProgrammes', 'CompletedProgrammes', 'SavedProgrammes', 'CompletedLessons')}),
    )
  #fields = ['User', 'ProfilePhoto', 'SkillLevel', 'UserDifficultyLevel', 'UserLevelProgress', 'LearnedTricks', 'SavedTricks', 'CurrentlyLearningProgrammes', 'CompletedProgrammes', 'CompletedLessons', 'SavedProgrammes', 'Follows']
  #'CurrentlyLearningProgrammes', 'SavedProgrammes',

class UserAdminConfig(UserAdmin):
    model = Trickster_User
    inlines = [ProfileInline]
    search_fields = ('Email', 'Username', 'FirstName', 'LastName')
    list_filter = ('Email', 'Username', 'FirstName', 'LastName', 'is_active', 'is_staff')
    ordering = ('-DateOfJoining',)
    list_display = ('Email', 'Username', 'FirstName', 'LastName', 'is_active', 'is_staff')
    fieldsets = (
        ('Personal Info', {'fields': ('Email', 'Username', 'FirstName', 'LastName')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('Email', 'Username', 'FirstName', 'LastName', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )

admin.site.register(Trickster_User, UserAdminConfig)
