from django.urls import path

from api import views

urlpatterns = [
    path('get_movies_list/', views.MovieAPI.as_view()),
]
