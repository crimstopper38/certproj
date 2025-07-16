from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView, TemplateView, ListView
from .models import Payments
from .forms import PaymentsForm, DistrictForm
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
        qs = Payments.objects.filter(activity='Ren')

        qs = qs.annotate(id_mod=ExpressionWrapper(F('id') % 2, output_field=IntegerField()))

        user = self.request.user
        if user.groups.filter(name='even_access').exists():
            return qs.filter(id_mod=0)
        elif user.groups.filter(name='odd_access').exists():
            return qs.filter(id_mod=1)
        return qs.none()

class DistrictPaymentsView(UpdateView):
    model = Payments
    form_class = DistrictForm
    template_name = 'payments/district.html'
    context_object_name = 'payment'
    success_url = '/payments/district/'

    def get_queryset(self):
        return Payments.objects.filter(activity='Dist')
    
    def get_success_url(self):
        # Skip missing primary keys and go to the next valid record
        next_payment = Payments.objects.filter(activity='Dist', pk__gt=self.object.pk).order_by('pk').first()
        if next_payment:
            return reverse('district-edit', kwargs={'pk': next_payment.pk})
        return reverse('district-edit', kwargs={'pk': self.object.pk})  # Stay on current if none
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prev_payment'] = Payments.objects.filter(activity='Dist', pk__lt=self.object.pk).order_by('-pk').first()
        return context
    

class AddonPaymentsView(ListView):
    model = 'Payments'
    template_name = 'payments/addon.html'
    context_object_name = 'payment'

    def get_queryset(self):
        return Payments.objects.filter(activity='Add')
    

class RenewalPaymentsView(ListView):
    model = 'Payments'
    template_name='payments/renewal.html'
    context_object_name = 'payments'

    def get_queryset(self):
        return Payments.objects.filter(activity='Ren')
    