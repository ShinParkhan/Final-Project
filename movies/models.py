from django.conf import settings
from django.db import models

# Create your models here.

class Genre(models.Model):
    tmbd_genre_id = models.IntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Movie(models.Model):
    tmbd_id = models.IntegerField()
    title = models.CharField(max_length=150)
    original_title = models.CharField(max_length=150)
    poster_path = models.TextField()
    backdrop_path = models.TextField(null=True)
    popularity = models.FloatField()
    vote_average = models.FloatField()
    genre_ids = models.ManyToManyField(Genre, related_name='movies')
    overview = models.TextField()
    release_date = models.DateField(auto_now=False, auto_now_add=False)
    director = models.CharField(max_length=150)
    runtime = models.IntegerField(null=True)
    video = models.TextField()
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
    