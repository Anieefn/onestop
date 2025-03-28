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
        return f"{self.id}"

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

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(Posts, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.item.discount_price * self.quantity

class Cart(models.Model):
    customer = models.ForeignKey(Register, on_delete=models.CASCADE, related_name="cart")
    # other fields if needed

    def total_price(self):
        return sum(cart_item.total_price() for cart_item in self.cart_items.all())
    
class Otp(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='otp')
    otp = models.CharField(max_length=6)
    otp_created_at = models.DateTimeField(auto_now_add=True)

    def is_otp_vaild(self):
        return now() <= self.otp_created_at + timedelta(minutes=3)  
