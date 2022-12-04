"""The following models are related to cart."""
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from creditcards import types
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
from movies.models import Show, Seat, Program

class Payment(models.Model):
    """Stores payment info"""
    cc_number = CardNumberField(_('card number'))
    cc_expiry = CardExpiryField(_('expiration date'))
    cc_code = SecurityCodeField(_('security code'))

    assert types.get_type('4444333322221111') == types.CC_TYPE_VISA
    assert types.get_type('343434343434343') == types.CC_TYPE_AMEX
    assert types.get_type('0000000000000000') == types.CC_TYPE_GENERIC

class Order(models.Model):
    """Stores info about orders"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=4, decimal_places=2, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Ticket(models.Model):
    """Stores info about booked tickets"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return ('Show:'+str(self.show)+'  '+'Date'+str(self.program)+
                '  '+'Seat'+str(self.seat.__str__())+','+str(self.user))
