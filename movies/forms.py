"""The following form is used for adding a new movie show."""
import time
import datetime
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django import forms
from .models import Show, Program

class ShowForm(forms.ModelForm):
    """Form used for adding a new Show entry."""
    class Meta:
        model = Show
        fields = ('movie', 'theater', 'screen', 'program', 'price')

    def clean(self):
        """
        Creates a new Show entry after checking that the chosen screen
        is free during the time the movie will be played.
        """

        movie = self.cleaned_data['movie']
        theater = self.cleaned_data['theater']
        screen = self.cleaned_data['screen']
        program = self.cleaned_data['program']
        price = self.cleaned_data['price']

        if price > 15:
            raise ValidationError('Price cannot be more than 15 euros.')
        if screen.theater.id != theater.id:
            raise ValidationError('Screen must belong to the theater!')

        for prog in program:
            shows = Show.objects.filter(screen=screen, program__day=prog.day).exclude(
                pk=self.instance.pk).distinct()

            for show in shows:
                ex_movie_duration = int(show.movie.duration)*60 + 1800
                new_movie_duration = int(movie.duration)*60 + 1800
                new_time_str = time.strftime(
                    '%H:%M:%S', time.gmtime(new_movie_duration))
                new_time_object = datetime.datetime.strptime(
                    new_time_str, '%H:%M:%S').time()
                programs = show.program.filter(day=prog.day)

                for progr in programs:
                    diff = datetime.datetime.combine(date.today(
                    ), progr.hour) - datetime.datetime.combine(date.today(), new_time_object)
                    add = (datetime.datetime.combine(
                        date.today(), progr.hour) + timedelta(seconds=ex_movie_duration)).time()
                    if str(progr.hour) < str(add) and str(progr.hour) > str(diff):
                        raise ValidationError(
                            'Movie overlaps with another movie.')
        for prog in program:
            obj = Program.objects.filter(
                day=prog.day, hour=prog.hour
            ).values('hour')
            shows = Show.objects.filter(
                screen=screen,
                program__day=prog.day,
                program__hour__in=obj
            ).exclude(pk=self.instance.pk)
            if shows.exists():
                raise ValidationError(
                    'Screen is reserved for same day and same hour')

        return self.cleaned_data
