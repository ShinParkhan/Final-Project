from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Genre, Rating, Actor
from accounts.models import User
from .forms import MovieForm, RatingForm
from accounts.models import User
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
import random

# Create your views here.

def index(request):
    movies = Movie.objects.all()
    topten = Movie.objects.order_by('-popularity')[:10]
    all_genres = Genre.objects.all()
    if request.user.is_authenticated:
        like_movie = request.user.like_movies.all()
        if like_movie.count():
            selected_movie = random.choice(like_movie)
            selected_genre = random.choice(selected_movie.genres.all())
            selected_movies = list(Movie.objects.filter(genres=selected_genre))
            random.shuffle(selected_movies)
            context = {'movies': movies,  'like_movie': like_movie, 'all_genres': all_genres, 'selected_movie': selected_movie, 'selected_movies': selected_movies[:5], 'selected_genre': selected_genre, 'topten': topten,}
        else:
            context = {'movies': movies, 'like_movie': like_movie, 'all_genres': all_genres, 'topten': topten,}
    else:
        context = {'movies': movies, 'all_genres': all_genres, 'topten': topten,}
    return render(request, 'movies/index.html', context)

def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    ratings = movie.rating_set.all()
    rating_form = RatingForm()
    actors = movie.actors.all()
    genres = movie.genres.all()
    context = {'movie': movie, 'ratings': ratings,
               'rating_form': rating_form, 'genres': genres, 'actors': actors,}
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

# 좋아요한 영화들
@login_required
def like(request, movie_pk):
    if request.is_ajax():
        movie = get_object_or_404(Movie, pk=movie_pk)
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
            liked = False
        else:
            movie.like_users.add(request.user)
            liked = True
        context = {'liked': liked, 'count': movie.like_users.count(),}
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest

# 좋아요한 배우들
@login_required
def like_actor(request, movie_pk, actor_pk):
    if request.is_ajax():
        actor = get_object_or_404(Actor, pk=actor_pk)
        if actor.like_users.filter(pk=request.user.pk).exists():
            actor.like_users.remove(request.user)
            liked = False
        else:
            actor.like_users.add(request.user)
            liked = True
        context = {'liked': liked, 'count': actor.like_users.count(),}
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest


# @login_required
# def like_actor(request, movie_pk, actor_pk):
#     actor = get_object_or_404(Actor, pk=actor_pk)
#     if actor.like_users.filter(pk=request.user.pk).exists():
#         actor.like_users.remove(request.user)
#     else:
#         actor.like_users.add(request.user)
#     return redirect('movies:detail', movie_pk)

@login_required
def follow(request, user_pk):
    if request.is_ajax():
        person = get_object_or_404(User, pk=user_pk)
        user = request.user
        if person.followers.filter(pk=user.pk).exists():
            person.followers.remove(user)
            f = False
        else:
            person.followers.add(user)
            f = True
        context = {'f': f, 'count': person.followers.count(),}
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest

# @login_required
# def follow(request, user_pk):
#     person = get_object_or_404(User, pk=user_pk)
#     user = request.user
#     if person != user:
#         if person.followers.filter(pk=user.pk).exists():
#             person.followers.remove(user)
#         else:
#             person.followers.add(user)
#     return redirect('accounts:userdetail', user_pk)

def movie_recommendation(request, user_pk):
    # 좋아요한 영화들 있는 경우엔 해당 영화와 같은 장르의 다른 영화들 랜덤으로 보여주기
    # 좋아요한 영화들 없는 경우 & 비회원 => popularity 순으로 탑10 보여주기

    # 좋아요한 영화의 장르들 뽑아오기
    # 해당 장르와 같은 장르의 영화들 랜덤으로 5~10개정도 보여주기
    movies = Movie.objects.all()
    user = request.user
    like_movie = user.like_movies.all()
    # context = {'movies': movies, 'like_movie': like_movie,}
    return redirect('movies:index')

# 좋아요한 영화 리스트
@login_required
def like_movie_list(request):
    like_movie = request.user.like_movies.all()
    context = {'like_movie': like_movie, }
    return render(request, 'movies/like_movie_list.html', context)

# 좋아요한 배우 리스트
@login_required
def like_actor_list(request):
    like_actor = request.user.like_actors.all()
    context = {'like_actor': like_actor, }
    return render(request, 'movies/like_actor_list.html', context)

# 장르별 영화 리스트
def genre_movie_list(request, genre_pk):
    movies = Movie.objects.all()
    genre = get_object_or_404(Genre, pk=genre_pk)
    context = {'movies': movies, 'genre': genre,}
    return render(request, 'movies/genre_movie_list.html', context)