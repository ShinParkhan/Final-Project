from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('intro/', views.intro, name='intro'),
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/ratings/', views.ratings_create, name='ratings_create'),
    path('<int:movie_pk>/ratings/<int:rating_pk>/delete/',
         views.ratings_delete, name='ratings_delete'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('follow/<int:user_pk>/', views.follow, name='follow'),
    path('<int:movie_pk>/like_actor/<int:actor_pk>/', views.like_actor, name='like_actor'),
    path('like_movie_list/', views.like_movie_list, name='like_movie_list'),
    path('like_actor_list/', views.like_actor_list, name='like_actor_list'),
    path('<int:genre_pk>/genre_movie_list/', views.genre_movie_list, name='genre_movie_list'),
    path('create/', views.create, name='create'),
    path('<int:movie_pk>/delete/', views.delete, name='delete'),
    path('<int:movie_pk>/update/', views.update, name='update'),
    path('<int:movie_pk>/rating_update/<int:rating_pk>/', views.rating_update, name='rating_update'),
]
