from django.db import models
from django.contrib.auth.models import User
# Create your models here.

TEAMS = (
  ('A', 'Arsenal'),
  ('C', 'Chelsea'),
  ('L', 'Liverpool'),
  ('MU', 'Manchester Utd.'),
  ('MC', 'Manchester City'),
  ('T', 'Tottenham'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to = "main_app/static/uploads", default="")
    team = models.CharField(max_length=2, choices=TEAMS, default=TEAMS[0][0])

    def __str__(self):
        return self.user.username