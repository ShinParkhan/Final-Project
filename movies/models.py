from django.conf import settings
from django.db import models

# Create your models here.


class Genre(models.Model):
    tmbd_genre_id = models.IntegerField()
    name = models.CharField(max_length=100)
    original_name = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.name

class Actor(models.Model):
    tmbd_actor_id = models.IntegerField(null=True)
    name = models.CharField(max_length=40)
    character = models.CharField(max_length=100)
    profile_path = models.CharField(max_length=150)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_actors', blank=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=150)
    poster_path = models.TextField()
    backdrop_path = models.TextField(null=True)
    overview = models.TextField()
    vote_average = models.FloatField()
    popularity = models.FloatField()
    original_title = models.CharField(max_length=150)
    release_date = models.DateField(auto_now=False, auto_now_add=False)
    runtime = models.IntegerField(null=True)
    director = models.CharField(max_length=150)
    actors = models.ManyToManyField(Actor, related_name='movies', blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    video = models.TextField(blank=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_movies', blank=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    content = models.CharField(max_length=150)
    score = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.content
    