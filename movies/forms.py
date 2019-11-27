from django import forms
from django.forms import ModelForm
from .models import Movie, Genre, Rating


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'poster_path', 'backdrop_path', 'overview', 'vote_average', 'popularity', 'vote_average', 'original_title', 'release_date', 'runtime', 'genres', 'director', 'actors',
                    'video')


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('content', 'score',)
