from django.contrib import admin
from .models import Profile, Schedule, Predictions, Comment

admin.site.register(Profile)
admin.site.register(Schedule)
admin.site.register(Predictions)
admin.site.register(Comment)

# Register your models here.
