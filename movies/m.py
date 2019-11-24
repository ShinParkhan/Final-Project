class Actor(models.Model):
    name = models.CharField(max_length=40)
    profile_path = models.CharField(max_length=150)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_actors', blank=True)
​
​
class Movie(models.Model):
    title = models.CharField(max_length=40)
    poster_path = models.CharField(max_length=150)
    backdrop_path = models.CharField(max_length=150)
    overview = models.TextField()
    vote_average = models.FloatField()
    popularity = models.FloatField()
    original_title = models.CharField(max_length=30)
    actors = models.ManyToManyField(Actor, related_name='movies', blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies', blank=True)