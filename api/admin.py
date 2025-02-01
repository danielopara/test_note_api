from django.contrib import admin

from .models import Notes, UserProfile

# Register your models here.
admin.site.register(Notes)
admin.site.register(UserProfile)
