from django.urls import path
from . import views
from .views import PaymentsUpdateView, DistrictPaymentsView, AddonPaymentsView, RenewalPaymentsView, OddRenewalView, EvenRenewalView, PendingRenewalView, RenewalSelectView, DistrictSelectView, PendingDistrictView, AddonSelectView, PendingAddonView, PaymentSearchView


urlpatterns = [
    path('<int:pk>/edit/', PaymentsUpdateView.as_view(), name='payments_edit'),
    path('renewal/choose/', RenewalSelectView.as_view(), name='renewal-select'),
    path('renewal/<int:pk>/edit/', RenewalPaymentsView.as_view(), name='renewal-edit'),
    path('renewal/odd/<int:pk>/edit/', OddRenewalView.as_view(), name='renewal-odd-edit'),
    path('renewal/even/<int:pk>/edit/', EvenRenewalView.as_view(), name='renewal-even-edit'),
    path('renewal/incomplete/<int:pk>/edit/', PendingRenewalView.as_view(), name='renewal-pending-edit'),
    path('district/choose/', DistrictSelectView.as_view(), name='district-select'),
    path('district/<int:pk>/edit/', DistrictPaymentsView.as_view(), name='district-edit'),
    path('district/incomplete/<int:pk>/edit/', PendingDistrictView.as_view(), name='district-pending-edit'),
    path('addon/choose/', AddonSelectView.as_view(), name='addon-select'),
    path('addon/<int:pk>/edit/', AddonPaymentsView.as_view(), name='addon-edit'),
    path('addon/incomplete/<int:pk>/edit/', PendingAddonView.as_view(), name='addon-pending-edit'),
    path('search/', PaymentSearchView.as_view(), name='payment-search'),
]