from django.db import models
from django.utils.timezone import now
from datetime import timedelta

# Create your models here.
class Register(models.Model):
    username = models.CharField(max_length=90)
    password = models.CharField(max_length=400)
    email = models.CharField(max_length=250,unique=True)
    address = models.CharField(max_length=1500)
    phonenumber = models.CharField(max_length=10,unique=True)
    role = models.CharField(max_length= 9,default='customer')
    saved_posts = models.ManyToManyField("Posts", related_name="saved_users", blank=True)
    def __str__(self):
        return f"{self.id}, {self.email}"

class Posts(models.Model):
    userId = models.ForeignKey(Register, on_delete= models.CASCADE)
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=2000)
    picture = models.URLField(max_length=10000)
    price = models.FloatField()
    catagery = models.CharField(max_length=13, default='shirts')
    discount = models.IntegerField()
    discount_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey(Register, on_delete=models.CASCADE, related_name="cart")
    items = models.ManyToManyField(Posts, related_name="cart")

    def total_price(self):
        return sum(item.discount_price for item in self.items.all())
    
    def __str__(self):
        return str(self.customer.id)
    
class Otp(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='otp')
    otp = models.CharField(max_length=6)
    otp_created_at = models.DateTimeField(auto_now_add=True)

    def is_otp_vaild(self):
        return now() <= self.otp_created_at + timedelta(minutes=3)    
