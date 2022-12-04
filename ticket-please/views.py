"""
The following view displayes the movies that are played currently
and those that are scheduled to play in the future.
"""
from datetime import datetime, timedelta
from django.shortcuts import render
from movies.models import Show, Movie

def home_view(request):
    """
    Finds the movies played from the current date up to next week,
    and from the next week on, and passes them to the template.
    """
    today = datetime.now().date()
    next_week = today + timedelta(7)
    after_next_week = today + timedelta(8)
    current_shows = Show.objects.filter(
        program__day__gte=today,
        program__day__lte=next_week
        ).values('movie')
    current_movies = Movie.objects.filter(id__in=current_shows)

    coming_shows = Show.objects.filter(
        program__day__gte=after_next_week).values('movie')
    coming_movies = Movie.objects.filter(id__in=coming_shows)

    context = {'current_movies': current_movies,
               'coming_movies': coming_movies}
    return render(request, 'index.html', context)
