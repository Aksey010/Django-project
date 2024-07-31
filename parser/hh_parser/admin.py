from django.contrib import admin
from .models import Requirements, Search, Skill

# Register your models here.

admin.site.register(Search)
admin.site.register(Skill)
admin.site.register(Requirements)
