from django.db import models
#null=true means use value when needed

class User(models.Model):
    """User table"""
    id_n = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number = models.BigIntegerField()
    email = models.EmailField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)

class Order(models.Model):
    """Order table"""
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateField(auto_now=True)
    #deleting User will delete also Order 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class OrderItem(models.Model):
    """OrderItem table"""
    description = models.CharField(max_length=255)
    price = models.FloatField()
    quantity = models.IntegerField()
    order = models.OneToOneField(Order, on_delete=models.CASCADE,
                                 primary_key=True)

    def save(self,*args,**kwargs):
        #this function can be extanded
        super().save(*args,**kwargs)