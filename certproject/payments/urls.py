from django.urls import path
from . import views
from .views import PaymentsUpdateView, RenewalUpdateview, DistrictPaymentsView


urlpatterns = [
    path('<int:pk>/edit/', PaymentsUpdateView.as_view(), name='payments_edit'),
    path('renewal/<int:pk>/edit/', RenewalUpdateview.as_view(), name='renewal-edit'),
    path('district/<int:pk>/', DistrictPaymentsView.as_view(), name='district-view'),
]