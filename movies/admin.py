"""d"""
from django.contrib import admin
from .models import Genre, Screen, Seat, Program, Movie, Theater, Show, ShowSeat
from .forms import ShowForm

admin.site.register(Genre)
admin.site.register(Screen)
admin.site.register(Seat)
admin.site.register(Program)
admin.site.register(Movie)
admin.site.register(Theater)
admin.site.register(ShowSeat)

class ShowAdmin(admin.ModelAdmin):
    """d"""
    form = ShowForm

admin.site.register(Show, ShowAdmin)
