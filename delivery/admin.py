from django.contrib import admin
from .models import Register,Posts,Cart,CartItem
# Register your models here.
admin.site.register(Register)
admin.site.register(Posts)
admin.site.register(Cart)
admin.site.register(CartItem)