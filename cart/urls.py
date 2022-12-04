"""cart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('choose-movie/', views.choose_movie_view, name='choose-movie'),
    path('choose-theater/', views.choose_theater_view, name='choose-theater'),
    path('choose-date/', views.choose_date_view, name='choose-date'),
    path('choose-seat/', views.choose_seat_view, name='choose-seat'),
    path('payment/', views.payment, name='payment'),
    path('my-tickets/', views.my_tickets, name='my-tickets'),
]
