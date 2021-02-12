from django import forms
from .models import User, Order, OrderItem


class FormOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = []
        exclude=['user']

class FormOrderItem(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['description', 'price', 'quantity']# 'order']
        exclude = ['order']
        name2field = {'Description' : 'description',
                      'Price' : 'price',
                      'Quantity' : 'quantity'}

class FormUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'surname', 'phone_number', 'email',
                  'country', 'city', 'street']
        name2field = {'First Name' : 'first_name',
                      'Middle Name' : 'surname',
                      'Phone Number' : 'phone_number',
                      'E-mail' : 'email',
                      'Country' : 'country',
                      'City' : 'city',
                      'Street' : 'street'
                    }