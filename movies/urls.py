from django.urls import path
from . import views


urlpatterns = [
    path('', views.MoviesView.as_view(), name='main'),
    path('filter/', views.FilterMoviesView.as_view(), name='filter'),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('review/<int:pk>', views.AddReviews.as_view(), name='add_review'),
    path('actor/<str:slug>/', views.ActorDetailView.as_view(), name='actor_detail'),
]