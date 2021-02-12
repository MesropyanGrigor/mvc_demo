from django.contrib import admin
from .models import OrderItem, User, Order
# Register your models here.

admin.site.register(User)
admin.site.register(OrderItem)
admin.site.register(Order)


