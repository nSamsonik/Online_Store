from django import forms
from .models import Order

"""
Это форма, которая будет использоваться для создания новых объектов Order
"""


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']
