"""d"""
from django.contrib import admin
from .models import Ticket, Order, Payment

admin.site.register(Ticket)
admin.site.register(Order)
admin.site.register(Payment)
