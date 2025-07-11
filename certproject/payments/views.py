from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView, TemplateView
from .models import Payments
from .forms import PaymentsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, ExpressionWrapper, IntegerField
from django.http import HttpRequest

# Create your views here.
class PaymentsUpdateView(UpdateView):
    model = Payments
    form_class = PaymentsForm
    template_name = 'payments/payments_list.html'
    context_object_name = 'payments'

    def get_success_url(self):
        # Skip missing primary keys and go to the next valid record
        next_payment = Payments.objects.filter(pk__gt=self.object.pk).order_by('pk').first()
        if next_payment:
            return reverse('payments_edit', kwargs={'pk': next_payment.pk})
        return reverse('payments_edit', kwargs={'pk': self.object.pk})  # Stay on current if none

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add previous record context, skipping non-sequential keys
        context['prev_payment'] = Payments.objects.filter(pk__lt=self.object.pk).order_by('-pk').first()
        return context

class RenewalUpdateview(LoginRequiredMixin, UpdateView):
    model = Payments
    form_class = PaymentsForm
    template_name = 'renewal.html'
    context_object_name = 'payments'

    def get_queryset(self):
        qs = Payments.objects.filter(activity='ren')

        qs = qs.annotate(id_mod=ExpressionWrapper(F('id') % 2, output_field=IntegerField()))

        user = self.request.user
        if user.groups.filter(name='even_access').exists():
            return qs.filter(id_mod=0)
        elif user.groups.filter(name='odd_access').exists():
            return qs.filter(id_mod=1)
        return qs.none()

class DistrictPaymentsView(TemplateView):
    template_name='payments/district.html'

class AddonPaymentsView(TemplateView):
    template_name='payments/addon.html'

class RenewalDashboard(TemplateView):
    template_name='payments/renewal.html'