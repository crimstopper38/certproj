from django import template
from payments.models import Payments

register = template.Library()

@register.simple_tag
def first_district_pk():
    payment = Payments.objects.filter(activity__iexact='Dist').order_by('pk').first()
    return payment.pk if payment else None