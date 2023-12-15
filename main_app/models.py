from django.db import models
from django.contrib.auth.models import User
from datetime import date
from PIL import Image
import datetime
# Create your models here.

TEAMS = (
  ('Arsenal', 'Arsenal'),
  ('Chelsea', 'Chelsea'),
  ('Liverpool', 'Liverpool'),
  ('Manchester Utd.', 'Manchester Utd.'),
  ('Manchester City', 'Manchester City'),
  ('Tottenham', 'Tottenham'),
)

class Teams(models.Model):
    team_name = models.CharField(max_length=20)
    logo = models.ImageField(upload_to = "main_app/static/uploads")

    def __str__(self):
        return (self.team_name)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="main_app/static/uploads", default="main_app/static/uploads/default.jpeg")
    team = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True)  # Use ForeignKey to link to Teams model
    totalpoints = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

    def __str__(self):
        return (self.user.username)

    def save(self, *args, **kwargs):
        # If the user is new, set the rank to the maximum value to make them last
        if not self.pk:
            max_rank = Profile.objects.aggregate(models.Max('rank'))['rank__max']
            self.rank = max_rank + 1 if max_rank is not None else 1

        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    def calculate_total_points(self):
        self.totalpoints = Score.objects.filter(user=self.user).aggregate(models.Sum('points'))['points__sum'] or 0
        self.save(update_fields=['totalpoints']) 

    def update_rank(self):
        profiles = Profile.objects.all().order_by('-totalpoints')
        rank = 1
        for profile in profiles:
            profile.rank = rank
            profile.save(update_fields=['rank'])
            rank += 1

    class Meta:
        ordering = ['rank']

    

class Schedule(models.Model):
    gameweek = models.IntegerField(default=1)
    date = models.DateField()
    time = models.TimeField(default=datetime.time(12, 0, 0))
    
    # Use ForeignKey to reference the Teams model for home and away teams
    hometeam = models.ForeignKey('Teams', related_name='home_games', on_delete=models.CASCADE)
    hometeamscore = models.IntegerField(blank=True, null=True)
    
    awayteam = models.ForeignKey('Teams', related_name='away_games', on_delete=models.CASCADE)
    awayteamscore = models.IntegerField(blank=True, null=True)
    
    match_completed = models.BooleanField(default=False)

    def __str__(self):
        return (f'{self.hometeam} vs {self.awayteam} on {self.date} at {self.time}')

    def save(self, *args, **kwargs):
        if self.match_completed:
            super().save(*args, **kwargs)
        else:
            self.update_scores()
            super().save(*args, **kwargs)

    def update_scores(self):
        predictions = Predictions.objects.filter(schedule=self)
        for prediction in predictions:
            points = calculate_points(self.hometeamscore, self.awayteamscore, prediction.predhometeamscore, prediction.predawayteamscore)
            Score.objects.update_or_create(
                user=prediction.user,
                schedule=self,
                prediction=prediction,
                defaults={'points': points}
            )
        if self.hometeamscore is not None and self.awayteamscore is not None:
            self.match_completed = True            

def calculate_points(actual_home_score, actual_away_score, predicted_home_score, predicted_away_score):
    if actual_home_score == predicted_home_score and actual_away_score == predicted_away_score:
        return 3  # Correct score
    elif (actual_home_score - actual_away_score) * (predicted_home_score - predicted_away_score) > 0:
        return 1  # Correct outcome
    else:
        return 0  # No points

class Predictions(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    predhometeamscore = models.IntegerField()
    predawayteamscore = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    def __str__(self):
        return (f'{self.user} predicted {self.predhometeamscore} - {self.predawayteamscore} for {self.schedule.hometeam} vs {self.schedule.awayteam} at {self.timestamp}')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    comment = models.TextField(max_length=250)
    date = models.DateField(default=datetime.date.today)
    edited = models.BooleanField(default=False)
    timestamp = models.TimeField()

    class Meta:
      ordering = ['-date', '-timestamp']

    def __str__(self):
        return (f'{self.user} said {self.comment} at {self.timestamp}')

    def get_absolute_url(self):
      return reverse('comment', kwargs={'comment_id': self.id})

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    prediction = models.ForeignKey(Predictions, on_delete=models.CASCADE)
    points = models.IntegerField()

    def __str__(self):
        return (f'{self.user} scored {self.points} for {self.schedule.hometeam} vs {self.schedule.awayteam}')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.update_profile()

    def update_profile(self):
        user_profile = Profile.objects.get(user=self.user)
        user_profile.calculate_total_points()
        user_profile.update_rank()
