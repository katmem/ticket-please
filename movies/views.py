"""
The following views handle movie-related functions, including
displaying movies on the homepage, showing details about a single movie,
and listing the schedule of the movies that are played.
"""

from django.shortcuts import render
from django.utils.timezone import datetime
from .models import Show, Movie, Theater

def home_view(request):
    """Finds the movies that are currently played and renders the homepage template."""
    today = datetime.now().date()
    current_shows = Show.objects.filter(program__day__gte=today)
    current_movies = Movie.objects.filter(id__in=current_shows)
    context = {'current_movies': current_movies}
    return render(request, 'movies/home.html', context)

def single_view(request, id):
    """
    Finds movies that belong to the same genre as the selected movie
    to suggest to the user and passes them to the template.
    """

    related_movies_list = []
    movie = Movie.objects.get(id=id)

    for genre in movie.genre.all():
        related_movies = Movie.objects.filter(genre=genre).exclude(id=id)
        for temp in related_movies:
            if temp not in related_movies_list:
                related_movies_list.append(temp)

    context = {'movie': movie, 'related_movies':related_movies_list[:6]}
    return render(request, 'single.html', context)

def program_view(request):
    """Finds the schedule of the movies that are played in theaters."""
    today = datetime.now().date()
    theaters = Theater.objects.all().order_by('city')
    current_shows = Show.objects.filter(program__day__gte=today).distinct()
    context = {'theaters':theaters, 'shows': current_shows}
    return render(request, 'movies/program.html', context)
