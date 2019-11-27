from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('', views.userlist, name='userlist'),
    path('<int:user_pk>/', views.userdetail, name='userdetail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:user_pk>/delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('password/', views.change_password, name='change_password'),
    path('staff/', views.staff, name='staff'),
]
