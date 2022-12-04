"""The following models are related to movies."""
import datetime
from django.db.models.signals import post_save, m2m_changed
from djongo import models
from .choices import COUNTY_CHOICES, SEAT_CHOICES, SEATING_PATTERNS, year_choices
from .seating_patterns import SEATING_ARRAYS

class Genre(models.Model):
    """Stores the genre of a movie."""
    name = models.CharField(max_length=20, blank=False)

    class Meta:
        verbose_name_plural = "Genres"
        ordering = ('name',)

    def __str__(self):
        return str(self.name)

class Theater(models.Model):
    """Stores info about theaters, including name and adress."""
    name = models.CharField(max_length=40, blank=False)
    city = models.CharField(max_length=40, blank=False)
    county = models.CharField(
        max_length=40, choices=COUNTY_CHOICES, blank=False)
    address = models.CharField(max_length=40, blank=False)
    zipcode = models.CharField(max_length=5, blank=False)

    class Meta:
        verbose_name_plural = "Theaters"

    def __str__(self):
        return f"{self.name}, {self.city}"

class Movie(models.Model):
    """Stores info about movies."""
    name = models.CharField(max_length=40, blank=False)
    description = models.CharField(max_length=255, blank=False)
    language = models.CharField(max_length=20, blank=True)
    genre = models.ManyToManyField(Genre)
    year = models.PositiveIntegerField(choices=year_choices(), blank=False)
    rating = models.DecimalField(blank=True, decimal_places=1, max_digits=2)
    duration = models.IntegerField(blank=False)
    director = models.CharField(max_length=30, blank=False)
    cast = models.CharField(max_length=255, blank=False)
    trailer = models.URLField(blank=True)  # embed url form youtube
    image = models.ImageField(null=True, blank=True, upload_to='img/')
    theater = models.ManyToManyField(Theater, through='Show')

    class Meta:
        verbose_name_plural = "Movies"

    def __str__(self):
        return str(self.name)

class Screen(models.Model):
    """Stores info about the theaters' screens(auditoriums), including seating plan."""
    name = models.CharField(max_length=20)
    no_rows = models.PositiveIntegerField()
    no_cols = models.PositiveIntegerField()
    no_seats = models.PositiveIntegerField()
    seating_pattern = models.CharField(
        choices=SEATING_PATTERNS, max_length=255)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Screens"

    def __str__(self):
        return f"{self.name}, {self.theater}"

def create_seats(sender, instance, created, **kwargs):
    """Creates the seats of a theater's screen according to the seating plan of the screen."""
    num_seats = 0
    if created:
        seating_pattern = SEATING_ARRAYS[instance.seating_pattern]
        for row, seats in enumerate(seating_pattern):
            for pos, seat in enumerate(seats):
                if seat:
                    num_seats = num_seats+1
                    Seat.objects.create(
                        screen=instance,
                        position=f"{str(row+1)}, {str(pos+1)}",
                        status=1
                    )

        instance.no_rows = row+1
        instance.no_cols = pos+1
        instance.no_seats = num_seats
        instance.save()

post_save.connect(create_seats, sender=Screen)

class Program(models.Model):
    """Stores the date and time at which the movies are played."""
    day = models.DateField(default=datetime.date.today)
    hour = models.TimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name_plural = "Programs"

    def __str__(self):
        return f"{str(self.day)}, {str(self.hour)}"

class Show(models.Model):
    """
    Stores info about the movies played, including theater and screen
    where they are played, time, and price of the ticket.
    """

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    program = models.ManyToManyField(Program)
    price = models.DecimalField(max_digits=3, decimal_places=2, blank=False)

    class Meta:
        verbose_name_plural = "Shows"

    def __str__(self):
        return f"{self.movie.name}, {self.screen.name}, {self.theater.name}"

def create_show_seat(sender, instance, action, **kwargs):
    """Creates an instance of ShowSeat."""
    if action == "post_add":
        seat_obj = Seat.objects.filter(screen=instance.screen)
        for pk in instance.program.all():
            for obj in seat_obj:
                show_seat_obj = ShowSeat.objects.create(
                    seat=obj, show=instance, program=pk, status=1, position=obj.position)
                show_seat_obj.save()

m2m_changed.connect(create_show_seat, sender=Show.program.through)

class Seat(models.Model):
    """
    Stores info about screens' seats, including their position,
    availability and the show they are booked for.
    """

    status = models.CharField(max_length=20, choices=SEAT_CHOICES)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    position = models.CharField(max_length=6)
    show = models.ManyToManyField(Show, through='ShowSeat')

    class Meta:
        verbose_name_plural = "Seats"

    def __str__(self):
        return f"{self.position}, {self.screen}"

class ShowSeat(models.Model):
    """Stores info about the seats of a specific show."""
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=SEAT_CHOICES)
    position = models.CharField(max_length=6)

    class Meta:
        verbose_name_plural = "ShowSeat"

    def __str__(self):
        return f"{self.seat}, {self.show}, {self.program}"
