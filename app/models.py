from ast import mod
from distutils.command.upload import upload
from itertools import product
from sre_constants import CATEGORY
from turtle import title
from unicodedata import category, name
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

STATE_CHOICES = (
    ('Sindh', 'Sindh'),
    ('Punjab', 'Punjab'),
    ('Balochistan', 'Balochistan'),
    ('khyber Pakhunkha', 'K-P-K'),
    ('Gilghit', 'Gilghit'),
    ('Islamabad', 'Islamabad'),
    ('Azad Jammu and kashmir', 'Azad Jammu and kashmir'),
    

)


class Customer(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)    
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,  max_length=50) 

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES = (
    ('Wat', 'Watches'),
    ('Sh', 'Shoes'),
    ('Win', 'Winter'),
    ('Sum', 'Summer'),
)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


    @property 
    def total_cost(self):
      return self.quantity * self.product.discounted_price     





STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
) 


class OrderPlaced(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(
    max_length=50, choices=STATUS_CHOICES, default='Accepted')
    @property 
    def total_cost(self):
      return self.quantity * self.product.discounted_price     





