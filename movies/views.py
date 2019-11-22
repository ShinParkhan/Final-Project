from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Genre, Rating
from .forms import MovieForm, RatingForm
from accounts.models import User
from django.views.decorators.http import require_POST

# Create your views here.


def index(request):
    movies = Movie.objects.all()
    context = {'movies': movies, }
    return render(request, 'movies/index.html', context)


def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    ratings = movie.rating_set.all()
    rating_form = RatingForm()
    genre_ids = movie.genre_ids.all()
    context = {'movie': movie, 'ratings': ratings,
               'rating_form': rating_form, 'genre_ids': genre_ids, }
    return render(request, 'movies/detail.html', context)


@require_POST
def ratings_create(request, movie_pk):
    if request.user.is_authenticated:
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.movie_id = movie_pk
            rating.user = request.user
            rating.save()
    return redirect('movies:detail', movie_pk)


@require_POST
def ratings_delete(request, movie_pk, rating_pk):
    if request.user.is_authenticated:
        rating = get_object_or_404(Rating, pk=rating_pk)
        if request.user == rating.user:
            rating.delete()
        return redirect('movies:detail', movie_pk)


@login_required
def like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.like_users.filter(pk=request.user.pk).exists():
        movie.like_users.remove(request.user)
    else:
        movie.like_users.add(request.user)
    return redirect('movies:index')


@login_required
def follow(request, user_pk):
    person = get_object_or_404(User, pk=user_pk)
    user = request.user
    if person != user:
        if person.followers.filter(pk=user.pk).exists():
            person.followers.remove(user)
        else:
            person.followers.add(user)
    return redirect('accounts:userdetail', user_pk)
