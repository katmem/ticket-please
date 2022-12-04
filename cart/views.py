"""
The following views handle cart-related functions, including
movie, theater, date and seat selection, payment, and tickets view.
"""

from datetime import datetime, timedelta
from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core import serializers
from movies.models import Show, Theater, Program, Seat, ShowSeat
from movies.seating_patterns import SEATING_ARRAYS
from .forms import ChooseMovieForm, ChooseTheaterForm, ChooseDateForm, PaymentForm
from .models import Ticket, Order

def choose_movie_view(request):
    """Checks whether the user's choice of a movie is valid and saves it."""
    if request.method == 'POST':
        form = ChooseMovieForm(request.POST)
        if form.is_valid():
            movie = form.cleaned_data.get('movie')
            request.session['movie'] = movie.id
            return redirect('cart:choose-theater')
    else:
        form = ChooseMovieForm()
    context = {'form': form}
    return render(request, 'cart/choose_movie.html', context)

def choose_theater_view(request):
    """
    Finds the theaters where a movie is currently played (up until next week),
    checks if the user's choice of a theater is valid and saves it.
    """

    movie_id = request.session.get('movie')
    now = datetime.now()
    today = now.date()
    next_week = today + timedelta(7)
    current_show = Show.objects.filter(
        movie__id=movie_id, program__day__gte=today, program__day__lte=next_week).values('theater')
    theaters_qs = Theater.objects.filter(id__in=current_show)

    if request.method == 'POST':
        form = ChooseTheaterForm(request.POST, qs=theaters_qs)
        if form.is_valid():
            theater = form.cleaned_data.get('theater')
            request.session['theater'] = theater.id
            return redirect('cart:choose-date')
    else:
        form = ChooseTheaterForm(qs=theaters_qs)

    context = {'form': form, 'movie': movie_id}
    return render(request, 'cart/choose_theater.html', context)

def choose_date_view(request):
    """
    Finds the dates at which the chosen movie is played at the selected theater,
    checks if the user's choice is valid and saves it.
    """

    show_id = []
    movie_id = request.session.get('movie')
    theater_id = request.session.get('theater')
    now = datetime.now()
    today = now.date()
    next_week = today + timedelta(7)

    current_show = Show.objects.filter(
        movie__id=movie_id,
        theater__id=theater_id,
        program__day__gte=today,
        program__day__lte=next_week
        ).values_list('program', flat=True)

    for show in current_show:
        show_id.append(show)
    date_qs = Program.objects.filter(id__in=show_id).order_by('day')

    if request.method == 'POST':
        form = ChooseDateForm(request.POST, qs=date_qs)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            request.session['date'] = date.id
            return redirect('cart:choose-seat')
    else:
        form = ChooseDateForm(qs=date_qs)

    context = {'form': form, 'theater': theater_id}
    return render(request, 'cart/choose_date.html', context)

def choose_seat_view(request):
    """Handles seat selection and calculates total price of the tickets."""
    movie_id = request.session.get('movie')
    theater_id = request.session.get('theater')
    date_id = request.session.get('date')
    total = 0
    ticket_list = []

    current_show = Show.objects.filter(
        movie__id=movie_id, theater__id=theater_id, program__id=date_id).first()
    screen = current_show.screen
    seats = ShowSeat.objects.filter(show=current_show, program__id=date_id)
    seating_pattern = SEATING_ARRAYS[screen.seating_pattern]

    if request.method == 'POST':
        seat = request.POST.getlist('seat')
        for position in seat:
            show_seat_obj = ShowSeat.objects.get(
                show=current_show, position=position, program__id=date_id)
            show_seat_obj.status = 3
            show_seat_obj.save()
            show = Show.objects.get(
                movie__id=movie_id, theater__id=theater_id, screen=screen, program__id=date_id)
            seat_obj = Seat.objects.get(screen=screen, position=position)

            program = Program.objects.get(id=date_id)
            ticket_obj = Ticket.objects.create(
                user=request.user, seat=seat_obj, show=show, program=program)
            ticket_list.append(ticket_obj)

            price = current_show.price
            total = total + float(price)
        request.session['total'] = total

        if not seat:
            messages.add_message(request, messages.INFO,
                                 'You have to select a seat before continuing.')
            return redirect('cart:choose-seat')
        return redirect('cart:payment')

    seats = serializers.serialize('json', list(
        seats), fields=('position', 'status'))
    context = {'seats': seats,
               'seating_pattern': seating_pattern, 'date': date_id}
    return render(request, 'cart/choose_seat.html', context)

def payment(request):
    """Handles payment and creates an Order entry."""
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            total = request.session.get('total')
            total = Decimal(total)

            movie_id = request.session.get('movie')
            theater_id = request.session.get('theater')
            date_id = request.session.get('date')
            order_obj = Order.objects.create(
                user=request.user, payment=payment, total=total)
            current_show = Show.objects.filter(
                movie__id=movie_id, theater__id=theater_id, program__id=date_id).first()
            ticket_qs = Ticket.objects.filter(
                user=request.user, show=current_show, paid=False, program__id=date_id)
            for obj in ticket_qs:
                obj.paid = True
                obj.order = order_obj
                obj.save()
            return redirect('cart:my-tickets')
    else:
        form = PaymentForm()

    context = {'form': form}
    return render(request, 'cart/payment.html', context)

def my_tickets(request):
    """Finds booked tickets."""
    movie_id = request.session.get('movie')
    theater_id = request.session.get('theater')
    date_id = request.session.get('date')
    current_show = Show.objects.filter(
        movie__id=movie_id, theater__id=theater_id, program__id=date_id).first()
    tickets = Ticket.objects.filter(
        user=request.user, show=current_show, paid=True, program__id=date_id)
    context = {'tickets': tickets}
    return render(request, 'cart/my_tickets.html', context)
