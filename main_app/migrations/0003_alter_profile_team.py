# Generated by Django 4.2.7 on 2023-11-09 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_remove_profile_bio_profile_team_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='team',
            field=models.CharField(choices=[('A', 'Arsenal'), ('C', 'Chelsea'), ('L', 'Liverpool'), ('MU', 'Manchester Utd.'), ('MC', 'Manchester City'), ('T', 'Tottenham')], default='A', max_length=20),
        ),
    ]