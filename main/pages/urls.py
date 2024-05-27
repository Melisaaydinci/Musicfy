
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_page,name='home_page'),
    path('favorites', views.favorite_page,name='favorite_page'),
    path('profile', views.profile_page,name='profile_page'),
    path('accounts/login/', views.login_page,name='login_page'),
    path('accounts/register/', views.signup_page,name='signup_page'),
    path('music/<str:music_id>/',views.music_page,name='music_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('add_or_remove_favorite/', views.add_or_remove_favorite, name='add_or_remove_favorite'),
    path('search_music/', views.search_music, name='search_music'),
    ]