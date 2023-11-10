from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

TEAMS = (
  ('Arsenal', 'Arsenal'),
  ('Chelsea', 'Chelsea'),
  ('Liverpool', 'Liverpool'),
  ('Manchester Utd.', 'Manchester Utd.'),
  ('Manchester City', 'Manchester City'),
  ('Tottenham', 'Tottenham'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to = "main_app/static/uploads", default="main_app/static/uploads/default.jpeg")
    team = models.CharField(max_length=20, choices=TEAMS, default=TEAMS[0][0])

    def __str__(self):
        return (self.user.username)

    def save(self, *args, **kwargs):
      super().save()

      img = Image.open(self.avatar.path)

      if img.height > 100 or img.width > 100:
        new_img = (100, 100)
        img.thumbnail(new_img)
        img.save(self.avatar.path)

class Schedule(models.Model):
    date = models.DateField()
    time = models.TimeField()
    hometeam = models.CharField(max_length=20)
    hometeamscore = models.IntegerField(blank=True, null=True)
    awayteam = models.CharField(max_length=20)
    awayteamscore = models.IntegerField(blank=True, null=True)
    

    def __str__(self):
        return (f'{self.hometeam} vs {self.awayteam} on {self.date} at {self.time}')

class Predictions(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    predhometeamscore = models.IntegerField()
    predawayteamscore = models.IntegerField()
    timestamp = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    def __str__(self):
        return (f'{self.user} predicted {self.predhometeamscore} - {self.predawayteamscore} for {self.schedule.hometeam} vs {self.schedule.awayteam} at {self.timestamp}')