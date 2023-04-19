from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Movie, Category, Actor
from .forms import ReviewForm


class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = model.objects.filter(draft=False)
    template_name = 'movies/movies.html' #если не указать, будет искать movie_list.html

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context


class MovieDetailView(DetailView):
    """Описание фильма"""
    model = Movie
    slug_field = 'url'

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context
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

class ActorDetailView(DetailView):
    """Вывод информации об актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'