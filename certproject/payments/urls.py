from django.urls import path
from . import views
from .views import PaymentsUpdateView, RenewalUpdateview, DistrictPaymentsView, AddonPaymentsView, RenewalPaymentsView


urlpatterns = [
    path('<int:pk>/edit/', PaymentsUpdateView.as_view(), name='payments_edit'),
    path('renewal/<int:pk>/edit/', RenewalUpdateview.as_view(), name='renewal-edit'),
    path('district/<int:pk>/edit/', DistrictPaymentsView.as_view(), name='district-edit'),
    path('addon/<int:pk>/edit/', AddonPaymentsView.as_view(), name='addon-edit'),
    path('renewal/', RenewalPaymentsView.as_view(), name='renewal-view'),
]