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
        exclude = []#['order']
        name2field = {'Description' : 'description',
                      'Price' : 'price',
                      'Quantity' : 'quantity'}

    def clean_price(self, *args, **kwargs): # This method is not passed any parameters
        price = self.cleaned_data.get('price')
        if price <= 0:
            self._errors['price'] = self.error_class(["Ensure this value has to be biger from zero!"])
            #raise forms.ValidationError("The price has to be big than zero!")
        return price
        
    def clean_quantity(self, *args, **kwargs):
        quantity =  self.cleaned_data.get('quantity')
        if quantity < 0:
            self._errors['quantity'] = self.error_class(["Ensure that value of quantity cannot be negative!"])
        return quantity

class FormUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'surname', 'phone_number', 'email',
                  'country', 'city', 'street']
        name2field = {#'User ID' : 'id_n',
                      'First Name' : 'first_name',
                      'Middle Name' : 'surname',
                      'Phone Number' : 'phone_number',
                      'E-mail' : 'email',
                      'Country' : 'country',
                      'City' : 'city',
                      'Street' : 'street'
                    }

    def clean(self): #defining for validation
        """For example, in cases where you have multiple fields that depend on 
           each other, you can override the Form.clean() function and again raise"""
        super().clean()
        email = self.cleaned_data.get('email')
        phone_number = self.cleaned_data.get('phone_number')
        if not email or not re.match(r"\w+@\w+\.\w+", email):
            self._errors['email'] = self.error_class(["Email form is not match"])
        if not re.match(r"\+?\d{8,}", str(phone_number)):
            self._errors['phone_number'] = self.error_class(["Phone number can be started with '+' and"\
                                                             " should has at least 8 digits"])
