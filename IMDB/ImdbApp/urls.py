from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='main'),

    path('title/movies/<str:KeyWord>', views.movies, name='movies'),
    
    path('title/<str:id>', views.moviedetail, name='md'),
    
    path('movies/<str:KeyWord>', views.movies, name='movies'),

    path('movies/movies/<str:KeyWord>', views.movies, name='movies'),

    path('title/movies/movies/<str:KeyWord>', views.movies, name='movies')
   
]

