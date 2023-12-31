# Generated by Django 4.2.7 on 2023-11-08 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.AddField(
            model_name='profile',
            name='team',
            field=models.CharField(choices=[('A', 'Arsenal'), ('C', 'Chelsea'), ('L', 'Liverpool'), ('MU', 'Manchester Utd.'), ('MC', 'Manchester City'), ('T', 'Tottenham')], default='A', max_length=2),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='', upload_to='main_app/static/uploads'),
        ),
    ]
