from django.urls import path
from django import views
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('postare', views.postare, name='postare'),
    path('prieteni/<str:pk>', views.prieteni, name='prieteni'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('settings', views.settings, name='settings'),
    path('like', views.like, name='like'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),

]