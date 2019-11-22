from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/ratings/', views.ratings_create, name='ratings_create'),
    path('<int:movie_pk>/ratings/<int:rating_pk>/delete/',
         views.ratings_delete, name='ratings_delete'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('follow/<int:user_pk>/', views.follow, name='follow'),



]
