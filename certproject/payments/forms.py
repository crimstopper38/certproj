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

class DistrictForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        read_only_fields = [
            'activity', 'first_name', 'last_name', 'order_num', 'amt', 'purchase_notes'
        ]

        # deactivate editing of the read_only_fields list
        for field_name in read_only_fields:
            if field_name in self.fields:
              self.fields[field_name].disabled = True

class AddonForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        read_only_fields = [
            'activity', 'first_name', 'last_name', 'order_num', 'amt', 'purchase_notes'
        ]

        for field_name in read_only_fields:
            if field_name in self.fields:
                self.fields[field_name].disabled = True
