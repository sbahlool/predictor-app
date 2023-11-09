from django.contrib import admin
from .models import Profile, Schedule, Predictions

admin.site.register(Profile)
admin.site.register(Schedule)
admin.site.register(Predictions)

# Register your models here.
