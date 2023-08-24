from django.contrib import admin
from .models import Country, Product, CartItem, Order, ShippingMethod, DeliveryDetails, Payment
# Register your models here.



admin.site.register(Country)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(ShippingMethod)
admin.site.register(DeliveryDetails)
admin.site.register(Payment)
