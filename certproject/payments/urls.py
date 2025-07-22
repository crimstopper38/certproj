from django.urls import path
from . import views
from .views import PaymentsUpdateView, DistrictPaymentsView, AddonPaymentsView, RenewalPaymentsView


urlpatterns = [
    path('<int:pk>/edit/', PaymentsUpdateView.as_view(), name='payments_edit'),
    path('renewal/<int:pk>/edit/', RenewalPaymentsView.as_view(), name='renewal-edit'),
    path('district/<int:pk>/edit/', DistrictPaymentsView.as_view(), name='district-edit'),
    path('addon/<int:pk>/edit/', AddonPaymentsView.as_view(), name='addon-edit'),
]