from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Genre, Rating, Actor
from accounts.models import User
from .forms import MovieForm, RatingForm
from accounts.models import User
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.admin.views.decorators import staff_member_required
import random

# Create your views here.
def intro(request):
    return render(request, 'movies/intro.html')

def index(request):
    movies = Movie.objects.all()
    topten = Movie.objects.order_by('-popularity')[:10]
    topfive = Movie.objects.order_by('-popularity')[:5]
    p_topfive = Movie.objects.order_by('-vote_average')[:5]
    all_genres = Genre.objects.all()
    if request.user.is_authenticated:
        like_movie = request.user.like_movies.all()
        if like_movie.count():
            selected_movie = random.choice(like_movie)
            selected_genre = random.choice(selected_movie.genres.all())
            selected_movies = list(Movie.objects.filter(genres=selected_genre))
            random.shuffle(selected_movies)
            context = {'movies': movies,  'like_movie': like_movie, 'all_genres': all_genres, 'selected_movie': selected_movie, 'selected_movies': selected_movies[:5], 'selected_genre': selected_genre, 'topten': topten,'topfive': topfive, 'p_topfive': p_topfive,}
        else:
            context = {'movies': movies, 'like_movie': like_movie, 'all_genres': all_genres, 'topten': topten, 'topfive': topfive, 'p_topfive': p_topfive,}
    else:
        context = {'movies': movies, 'all_genres': all_genres, 'topten': topten,'topfive': topfive, 'p_topfive': p_topfive,}
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
#-----------------------------------------
@staff_member_required # 로그인된 사람만 create로 접근가능함
def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST) # 인스턴스 생성(통째로 받아온다... -> FORM이 데이터에 맞춰서 알아서 매칭해줌)
        if form.is_valid():
            # article = form.save() # 유효성 검사후 저장만 하면 된다(어느 필드에 있는지 model form을 쓰면 알게됨!)
            movie = form.save(commit=False)   # article 객체만 만들고 저장은 안함
            movie.user = request.user   # 왜래키값을 받고 저장!
            movie.save()
            return redirect('movies:detail', movie.pk) # get_absolute_url 작성하면 인스턴스 객체에 바로 넣을 수 있음
    else:
        form = MovieForm() # 인스턴스 생성
    context = {'form': form,}
    return render(request, 'movies/form.html', context)  # get 방식일때...

@require_POST
def delete(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user.is_staff: # 인증된 사용자만 delete 가능!!
        movie.delete()
        return redirect('movies:index')
    return redirect('movies:detail', movie_pk)    # 자기 글이 아니면 삭제 불가능

@login_required
def update(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user.is_staff: # 작성자와 현재유저가 같아야 수정 가능!!!
        if request.method == "POST":
            form = MovieForm(request.POST, instance=movie) # request, instance 둘다 적어줘야함
            if form.is_valid():
                movie.save()
                return redirect('movies:detail', movie_pk)
        else:
            form = MovieForm(instance=movie)
    else:
        return redirect('movies:index')   # 동일 인물이 아니면 홈으로 보냄.
    # 1. POST : 검증에 실패한 form(오류 메세지도 포함된 상태)
    # 2. GET : 초기화된 form
    context = {'form': form, 'movie': movie,}
    return render(request, 'movies/form.html', context) # create랑 html 공유함!(둘 다 form을 사용하므로...)

# -----------------------------

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


def rating_update(request, movie_pk, rating_pk):
    rating = get_object_or_404(Rating, pk=rating_pk)
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user == rating.user:
        if request.method == 'POST':
            rating_form = RatingForm(request.POST, instance=rating)
            if rating_form.is_valid():
                rating_form.save()
                return redirect('movies:detail', movie_pk)   
        else:
            rating_form = RatingForm(instance=rating)
    else: redirect('movies:detail', movie_pk)
    context = {'rating': rating, 'rating_form': rating_form, 'movie': movie,}
    return render(request, 'movies/rating_form.html', context)


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