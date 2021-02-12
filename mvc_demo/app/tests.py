from django.test import TestCase
from mvc_demo.app.forms import FormUser, FormOrder, FormOrderItem
from mvc_demo.app.models import User, Order, OrderItem
# Create your tests here.

class TestForm(TestCase):
    def __init(self, *args, **kwargs):
        """constructor"""
        super().__init__(*args, **kwargs)

    def setUp(self):
        """Setuping before testing"""
        self.u_obj = User.objects.create(first_name='T_Name', surname='S_Name',
                                         phone_number=99999999,
                                         email='example@example.com',
                                         country='Armenia', city='Yerevan',
                                         street='the best')

    def test_is_valid_User(self):
        print("testing")
        data = {'first_name': self.u_obj.first_name,
                'surname' : self.u_obj.surname,
                'phone_number' : self.u_obj.phone_number,
                'email' : self.u_obj.email ,
                'country' : self.u_obj.country,
                'city' : self.u_obj.city,
                'street' : self.u_obj.street}
        form = FormUser(data=data)
        self.assertTrue(form.is_valid())

    def test_is_valid_Order(self):
        form = FormOrder(data={})
        self.assertTrue(form.is_valid())

    def test_is_valid_OrderItem(self):
        o_obj = Order.objects.create(user=self.u_obj)
        oi = OrderItem.objects.create(description="Book", price=40.12,
                                      quantity=2, order=o_obj)
        data = {'description' : oi.description,
                'price' : oi.price,
                'quantity' : oi.quantity}
        form = FormOrderItem(data=data)
        form.instance.order = o_obj
        self.assertTrue(form.is_valid())