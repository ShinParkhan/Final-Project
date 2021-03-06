# Generated by Django 2.1.1 on 2019-11-28 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tmbd_actor_id', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=40)),
                ('character', models.CharField(max_length=100)),
                ('profile_path', models.CharField(max_length=150)),
                ('like_users', models.ManyToManyField(blank=True, related_name='like_actors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tmbd_genre_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('original_name', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('poster_path', models.TextField()),
                ('backdrop_path', models.TextField(null=True)),
                ('overview', models.TextField()),
                ('vote_average', models.FloatField()),
                ('popularity', models.FloatField()),
                ('original_title', models.CharField(max_length=150)),
                ('release_date', models.DateField()),
                ('runtime', models.IntegerField(null=True)),
                ('director', models.CharField(max_length=150)),
                ('video', models.TextField(blank=True)),
                ('actors', models.ManyToManyField(blank=True, related_name='movies', to='movies.Actor')),
                ('genres', models.ManyToManyField(related_name='movies', to='movies.Genre')),
                ('like_users', models.ManyToManyField(blank=True, related_name='like_movies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=150)),
                ('score', models.IntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
