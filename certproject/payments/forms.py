from django import forms
from .models import Payments

class PaymentsForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        read_only_fields = [
            'activity', 'first_name', 'last_name', 'order_num', 'amt', 'purchase_notes' 
        ]

        for field in read_only_fields:
            self.fields[field].disabled=True