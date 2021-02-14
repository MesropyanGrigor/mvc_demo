import re

from django import forms
from .models import User, Order, OrderItem

class FormOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = []
        exclude=['user']

class FormOrderItem(forms.ModelForm):
    #description = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder' : 'your description',
    #                                                                      'class' : 'new-class-name two',
    #                                                                      'id' : 'my-id-for-testarea',
    #                                                                      'rows':20,
    #                                                                      'cols':120}))
    class Meta:
        model = OrderItem
        fields = ['description', 'price', 'quantity']# 'order']
        exclude = ['order']
        name2field = {'Description' : 'description',
                      'Price' : 'price',
                      'Quantity' : 'quantity'}

    def clean_price(self, *args, **kwargs):
        price = self.cleaned_data.get('price')
        if price <= 0:
            self._errors['price'] = self.error_class(["The price has to be big than zero!"])
            #raise forms.ValidationError("The price has to be big than zero!")
        
    def clean_quantity(self, *args, **kwargs):
        quantity =  self.cleaned_data.get('quantity')
        if quantity < 0:
            self._errors['quantity'] = self.error_class(["Quantity cannot be negative!"])

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

    def clean(self): #defining for validation
        super().clean()
        email = self.cleaned_data.get('email')
        phone_number = self.cleaned_data.get('phone_number')
        if not email or not re.match(r"\w+@\w+\.\w+", email):
            self._errors['email'] = self.error_class(["Email form is not match"])
        if not re.match(r"\+?\d{8,}", str(phone_number)):
            self._errors['phone_number'] = self.error_class(["Phone number can be started with '+' and"\
                                                             " should has at least 8 digits"])
