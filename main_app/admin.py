from django.contrib import admin
from .models import Profile, Schedule, Predictions, Comment, Score, Teams

admin.site.register(Profile)
admin.site.register(Schedule)
admin.site.register(Predictions)
admin.site.register(Comment)
admin.site.register(Score)
admin.site.register(Teams)

# Register your models here.
