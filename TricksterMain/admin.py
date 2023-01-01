from django.contrib import admin
from .models import SkillLevel
from .models import Trick
from .models import User

admin.site.register(SkillLevel)
admin.site.register(Trick)
admin.site.register(User)

