from django.test import TestCase
from mvc_demo.app.forms import FormUser, FormOrder, FormOrderItem
from mvc_demo.app.models import User, Order, OrderItem
from django.urls import reverse
# Create your tests here.

class OrderFormTest(TestCase):
    def __init(self, *args, **kwargs):
        """constructor"""
        super().__init__(*args, **kwargs)

    def setUp(self):
        """Setuping before testing"""
        self.u_obj = User.objects.create(first_name='T_Name', surname='S_Name',
                                         phone_number=9999999999,
                                         email='example@example.com',
                                         country='Armenia', city='Yerevan',
                                         street='the best')

    def test_is_valid_User(self):
        """Validating User Form """
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
        """ Validating Order Form"""
        form = FormOrder(data={})
        self.assertTrue(form.is_valid())

    def test_is_valid_OrderItem(self):
        """Validating OrderItem Form"""
        o_obj = Order.objects.create(user=self.u_obj)
        oi = OrderItem.objects.create(description="Book", price=40.12,
                                      quantity=2, order=o_obj)
        data = {'description' : oi.description,
                'price' : oi.price,
                'quantity' : oi.quantity}
        form = FormOrderItem(data=data)
        form.instance.order = o_obj
        self.assertTrue(form.is_valid())

    def test_User_dot_clean(self):
        """Providing Fail data and checking errors count"""
        data = {'first_name': self.u_obj.first_name,
                'surname' : self.u_obj.surname,
                'phone_number' : 1234567,
                'email' :  "example",
                'country' : self.u_obj.country,
                'city' : self.u_obj.city,
                'street' : self.u_obj.street}
        form = FormUser(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue(len(list(form._errors.values())) == 2)

class OrderViewTest(TestCase):
    """views module testing"""
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/order/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/order_list/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_order(self):
        response = self.client.get(reverse('order'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order.html')

    def test_view_uses_correct_template_order_list(self):
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_list.html')
