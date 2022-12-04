"""
The following views handle account-related functions, including
user registration, login, logout, profiles' updates and order history view.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from cart.models import Order, Ticket
from .forms import RegisterForm, UpdateForm
from .decorators import anonymous_required

@ anonymous_required(redirect_url='home')
def register_view(request):
    """
    View that stores the data of the registration form to the database,
    authenticates users and logs them in once they have correctly completed the form.
    """

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            first_name = register_form.cleaned_data.get('first_name')
            last_name = register_form.cleaned_data.get('last_name')
            email = register_form.cleaned_data.get('email')
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password1')

            messages.success(request, 'Account was created for ' + username)

            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        register_form = RegisterForm()
    return render(request, 'accounts/register.html', {'register_form': register_form})

@ anonymous_required(redirect_url='home')
def login_view(request):
    """View that handles users' login."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        messages.info(request, 'Username or password is incorrect.')
        return render(request, 'accounts/login.html', {})

    return render(request, 'accounts/login.html', {})

@login_required
def logout_view(request):
    """View that logs users out of the application."""
    logout(request)
    return redirect('home')

@login_required
def change_password_view(request):
    """View that allows users to change their password."""
    storage = messages.get_messages(request)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password changed successfully!')
            return redirect('home')
        messages.error(request, 'Please fix the error.')
    else:
        form = PasswordChangeForm(request.user)

    context = {'form': form, 'messages': storage}

    return render(request, 'accounts/change_password.html', context)

@login_required
def update_profile_view(request):
    """
    View that allows users to update their first and last name and email.
    It saves the update form data to the DB and redirects users to he home page.
    """

    storage = messages.get_messages(request)

    initial = {'first_name': request.user.first_name,
               'last_name': request.user.last_name, 'email': request.user.email}

    if request.method == 'POST':
        form = UpdateForm(request.POST, initial)

        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('home')
        messages.error(request, 'Please fix your error.')
    else:
        form = UpdateForm(initial)

    context = {'form': form, 'messages': storage}
    return render(request, "accounts/update_profile.html", context)

@login_required
def my_orders_view(request):
    """View that allows users to view their order history."""
    orders = Order.objects.filter(user=request.user).order_by('-id')
    tickets = Ticket.objects.filter(
        user=request.user, paid=True, order__in=orders)

    context = {'orders': orders, 'tickets': tickets}
    return render(request, 'accounts/my_orders.html', context)
