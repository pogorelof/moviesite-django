from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Movie
from .forms import ReviewForm


class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = model.objects.filter(draft=False)
    template_name = 'movies/movies.html' #если не указать, будет искать movie_list.html


class MovieDetailView(DetailView):
    """Описание фильма"""
    model = Movie
    slug_field = 'url'


class AddReviews(View):
    """Отправка отзывов"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False) #приостановить сохранение формы
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            #привязка комментария к фильму
            form.movie = movie
            form.save() #сохранение формы
        return redirect(movie.get_absolute_url())