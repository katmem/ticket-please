"""
The following forms are related to cart handling, and
are used for selecting movies, theaters, dates and ticket payment.
"""

from datetime import datetime, timedelta
from django import forms
from movies.models import Show, Movie, Theater, Program
from .models import Payment

class ChooseMovieForm(forms.Form):
    """
    Allows users to select a movie they want to book tickets for,
    from a list including movies played at that time and up to 1 week after.
    """

    now = datetime.now()
    today = now.date()
    next_week = today + timedelta(7)
    current_shows = Show.objects.filter(
        program__day__gte=today, program__day__lte=next_week).values('movie')
    current_movies = Movie.objects.filter(id__in=current_shows)
    movie = forms.ModelChoiceField(queryset=current_movies)

class ChooseTheaterForm(forms.Form):
    """
    Allows users to select a theater of their choice
    where they want to watch a movie at.
    """

    theater = forms.ModelChoiceField(queryset=Theater.objects.none())

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('qs')
        super(ChooseTheaterForm, self).__init__(*args, **kwargs)
        self.fields['theater'].queryset = qs

class ChooseDateForm(forms.Form):
    """Allows users to select the date at which they want to book tickets for."""
    date = forms.ModelChoiceField(queryset=Program.objects.none())

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('qs')
        super(ChooseDateForm, self).__init__(*args, **kwargs)
        self.fields['date'].queryset = qs

class PaymentForm(forms.ModelForm):
    """
    Allows users to pay for their booked ticket by entering
    their card's cc number, expiration date and security code.
    """
    class Meta:
        model = Payment
        fields = ['cc_number', 'cc_expiry', 'cc_code',]
