from django.db import models
from django.contrib.auth. models import User
from django.db.models.signals import post_save
import datetime

#Catagort Table

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_email_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)
    datetime = models.DateTimeField(User, auto_now=datetime)
    temporary_address = models.CharField(max_length=200, blank=True)
    permanant_address = models.CharField(max_length=200, blank=True)
    country =  models.CharField(max_length=20, blank=True)
    zipcode =  models.CharField(max_length=20, blank=True)
    province =  models.CharField(max_length=100, blank=True)
    city =  models.CharField(max_length=100, blank=True)
    town =  models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user = instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)


class Catagory(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'catagories'

class Customer(models.Model):
    fisrt_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.fisrt_name} -{self.last_name} -{self.phone} !!!'


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    catagory = models.ForeignKey(Catagory, on_delete= models.CASCADE, default=1)
    description = models.CharField(max_length=200, default="", blank=True)
    image = models.ImageField(upload_to='uploads/prodocts')
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default= 0, decimal_places=2, max_digits=7)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length= 300, default= "", blank = True)
    phone = models.CharField(max_length=100, default="", blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product}'



