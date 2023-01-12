from django.contrib import admin
from .models import Trickster_User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = Trickster_User
    search_fields = ('Email', 'Username', 'FirstName', 'LastName')
    list_filter = ('Email', 'Username', 'FirstName', 'LastName', 'is_active', 'is_staff')
    ordering = ('-DateOfJoining',)
    list_display = ('Email', 'Username', 'FirstName', 'LastName','is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('Email', 'Username', 'FirstName', 'LastName')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Trickster Data', {'fields': ('SkillLevel', 'LearnedTricks', 'UserDifficultyLevel')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('Email', 'Username', 'FirstName', 'LastName', 'password1', 'password2', 'SkillLevel', 'LearnedTricks', 'UserDifficultyLevel', 'is_active', 'is_staff')}
         ),
    )

admin.site.register(Trickster_User, UserAdminConfig)

