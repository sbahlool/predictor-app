# Generated by Django 4.2.7 on 2023-11-29 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0026_teams'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='team',
            field=models.CharField(choices=[('Arsenal', 'Arsenal'), ('Chelsea', 'Chelsea'), ('Liverpool', 'Liverpool'), ('Manchester Utd.', 'Manchester Utd.'), ('Manchester City', 'Manchester City'), ('Tottenham', 'Tottenham')], default='Arsenal', max_length=20, null=True),
        ),
    ]
