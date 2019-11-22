from django.contrib import admin
from .models import Movie, Genre, Rating
# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'original_title', 'release_date',
                    'popularity', 'overview', 'director', 'runtime', 'video' )


admin.site.register(Movie, MovieAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tmbd_genre_id', 'name')

    
admin.site.register(Genre, GenreAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content', 'score', 'user', 'movie')


admin.site.register(Rating, RatingAdmin)
