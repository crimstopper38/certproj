from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView, TemplateView
from .models import Payments
from .forms import PaymentsForm, DistrictForm, AddonForm, RenewalForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.functions import Mod

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

class DistrictSelectView(TemplateView):
    template_name = 'payments/district_select.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        annotated_qs = Payments.objects.annotate(mod_pk=Mod('pk', 2)).filter(activity='Dist')

        first_all = annotated_qs.order_by('pk').first()
        first_incomplete = annotated_qs.filter(done__isnull=True).order_by('pk').first()

        context['dist_groups'] = []

        if first_incomplete:
            context['dist_groups'].append({
                'label': 'Pending District',
                'url': reverse('district-pending-edit', kwargs={'pk': first_incomplete.pk})
            })

        if first_all:
            context['dist_groups'].append({
                'label': 'All District',
                'url': reverse('district-edit', kwargs={'pk': first_all.pk})
            })

        return context

    def _first_pk(self, filter_q):
        match = Payments.objects.filter(filter_q).order_by('pk').first()
        return match.pk if match else 0  # You can show a fallback message if match is None
    
class FilteredDistrictView(UpdateView):
    model = Payments
    form_class = DistrictForm
    template_name = 'payments/district.html'
    context_object_name = 'payment'

    filter_q = Q(activity='Dist')  # override this per subclass
    success_url_name = None       # override this per subclass

    def get_queryset(self):
        return Payments.objects.filter(self.filter_q)

    def get_success_url(self):
        next_payment = self.get_queryset().filter(pk__gt=self.object.pk).order_by('pk').first()
        return reverse(self.success_url_name, kwargs={
            'pk': next_payment.pk if next_payment else self.object.pk
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prev_payment'] = self.get_queryset().filter(pk__lt=self.object.pk).order_by('-pk').first()
        return context
    
class PendingDistrictView(FilteredDistrictView):
    filter_q = Q(activity='Dist') & Q(done__isnull=True)
    success_url_name = 'district-pending-edit'

class DistrictPaymentsView(FilteredDistrictView):  # Your existing flow
    filter_q = Q(activity='Dist')
    success_url_name = 'district-edit'

class AddonSelectView(TemplateView):
    template_name = 'payments/addon_select.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        annotated_qs = Payments.objects.annotate(mod_pk=Mod('pk', 2)).filter(activity='Add')

        first_all = annotated_qs.order_by('pk').first()
        first_incomplete = annotated_qs.filter(done__isnull=True).order_by('pk').first()

        context['addon_groups'] = []

        if first_incomplete:
            context['addon_groups'].append({
                'label': 'Pending Addon',
                'url': reverse('addon-pending-edit', kwargs={'pk': first_incomplete.pk})
            })

        if first_all:
            context['addon_groups'].append({
                'label': 'All Addon',
                'url': reverse('addon-edit', kwargs={'pk': first_all.pk})
            })

        return context

    def _first_pk(self, filter_q):
        match = Payments.objects.filter(filter_q).order_by('pk').first()
        return match.pk if match else 0  # You can show a fallback message if match is None
    
class FilteredAddonView(UpdateView):
    model = Payments
    form_class = AddonForm
    template_name = 'payments/addon.html'
    context_object_name = 'payment'

    filter_q = Q(activity='Add')  # override this per subclass
    success_url_name = None       # override this per subclass

    def get_queryset(self):
        return Payments.objects.filter(self.filter_q)

    def get_success_url(self):
        next_payment = self.get_queryset().filter(pk__gt=self.object.pk).order_by('pk').first()
        return reverse(self.success_url_name, kwargs={
            'pk': next_payment.pk if next_payment else self.object.pk
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prev_payment'] = self.get_queryset().filter(pk__lt=self.object.pk).order_by('-pk').first()
        return context
    
class PendingAddonView(FilteredDistrictView):
    filter_q = Q(activity='Add') & Q(done__isnull=True)
    success_url_name = 'addon-pending-edit'

class AddonPaymentsView(FilteredDistrictView):  # Your existing flow
    filter_q = Q(activity='Add')
    success_url_name = 'addon-edit'

class RenewalSelectView(TemplateView):
    template_name = 'payments/renewal_select.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        annotated_qs = Payments.objects.annotate(mod_pk=Mod('pk', 2)).filter(activity='Ren')

        first_all = annotated_qs.order_by('pk').first()
        first_odd = annotated_qs.filter(mod_pk=1).order_by('pk').first()
        first_even = annotated_qs.filter(mod_pk=0).order_by('pk').first()
        first_incomplete = annotated_qs.filter(done__isnull=True).order_by('pk').first()

        context['ren_groups'] = []

        if first_odd:
            context['ren_groups'].append({
                'label': 'Odd Renewals',
                'url': reverse('renewal-odd-edit', kwargs={'pk': first_odd.pk})
            })

        if first_even:
            context['ren_groups'].append({
                'label': 'Even Renewals',
                'url': reverse('renewal-even-edit', kwargs={'pk': first_even.pk})
            })

        if first_incomplete:
            context['ren_groups'].append({
                'label': 'Pending Renewals',
                'url': reverse('renewal-pending-edit', kwargs={'pk': first_incomplete.pk})
            })

        if first_all:
            context['ren_groups'].append({
                'label': 'All Renewals',
                'url': reverse('renewal-edit', kwargs={'pk': first_all.pk})
            })

        return context

    def _first_pk(self, filter_q):
        match = Payments.objects.filter(filter_q).order_by('pk').first()
        return match.pk if match else 0  # You can show a fallback message if match is None

# Parent class for our renewal pages, will all follow the same logic, only filtering is different and done by subclass views
class FilteredRenewalView(UpdateView):
    model = Payments
    form_class = RenewalForm
    template_name = 'payments/renewal.html'
    context_object_name = 'payment'

    filter_q = Q(activity='Ren')  # override this per subclass
    success_url_name = None       # override this per subclass

    def get_queryset(self):
        return Payments.objects.filter(self.filter_q)

    def get_success_url(self):
        next_payment = self.get_queryset().filter(pk__gt=self.object.pk).order_by('pk').first()
        return reverse(self.success_url_name, kwargs={
            'pk': next_payment.pk if next_payment else self.object.pk
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prev_payment'] = self.get_queryset().filter(pk__lt=self.object.pk).order_by('-pk').first()
        return context
    
class OddRenewalView(FilteredRenewalView):
    success_url_name = 'renewal-odd-edit'

    def get_queryset(self):
        return Payments.objects.annotate(mod_pk=Mod('pk', 2)).filter(
            activity='Ren',
            mod_pk=1
        )


class EvenRenewalView(FilteredRenewalView):
    success_url_name = 'renewal-even-edit'

    def get_queryset(self):
        return Payments.objects.annotate(mod_pk=Mod('pk', 2)).filter(
            activity='Ren',
            mod_pk=0
        )


class PendingRenewalView(FilteredRenewalView):
    filter_q = Q(activity='Ren') & Q(done__isnull=True)
    success_url_name = 'renewal-pending-edit'

class RenewalPaymentsView(FilteredRenewalView):  # Your existing flow
    filter_q = Q(activity='Ren')
    success_url_name = 'renewal-edit'

    