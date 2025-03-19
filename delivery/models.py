from django.db import models

# Create your models here.
class Register(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=400)
    email = models.CharField(max_length=20 ,unique=True)
    address = models.CharField(max_length=150)
    phonenumber = models.CharField(max_length=10,unique=True)
    role = models.CharField(max_length= 9,default='customer')
    
    def __str__(self):
        return self.username

class Posts(models.Model):
    userId = models.ForeignKey(Register, on_delete= models.CASCADE)
    name = models.CharField(max_length=22)
    bio = models.CharField(max_length=90)
    picture = models.URLField(max_length=300)
    price = models.FloatField()
    catagery = models.CharField(max_length=13, default='shirts')
    discount = models.IntegerField()
    discount_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey(Register, on_delete=models.CASCADE, related_name="cart")
    items = models.ManyToManyField("Posts", related_name="cart")

    def total_price(self):
        return sum(item.price for item in self.items.all())
    
    def __str__(self):
        return f"{self.customer.username} {self.total_price}"
    
