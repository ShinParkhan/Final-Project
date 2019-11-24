from django import forms
from django.forms import ModelForm
from .models import Movie, Genre, Rating


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'original_title', 'genres', 'release_date',
                    'popularity', 'overview', 'director', 'runtime', 'video')


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('content', 'score',)
