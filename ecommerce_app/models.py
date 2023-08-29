from django.db import models
from base.managers import MyUserManager, ActiveManager
from accounts.models import User
# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')  
    svg_image = models.FileField(upload_to='product/', blank=True, null=True)  
    description = models.TextField()
    is_on_sale = models.BooleanField(default=False)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.CharField(max_length=20) 
    origin_type = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)


class ShippingMethod(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    

class DeliveryDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField()
    apartment = models.CharField(max_length=20)
    #shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.CASCADE)


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder_name = models.CharField(max_length=100)
    expiry_date = models.DateField()
    security_code = models.CharField(max_length=4)


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

# class Category(models.Model):
#     name = models.CharField(max_length=80, null=True)

#     def __str__(self):
#         return self.name


# class Product(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
#     title = models.CharField(max_length=2000)
#     price = models.models.DecimalField(null=True, blank=True, default=1.99)   
#     old_price = models.DecimalField(null=True, blank=True, default=0.00)                                                                     
#     description = models.TextField()
#     image= models.ImageField(upload_to="media/")
    
#     #is_active = models.BooleanField(default=True)

#     objects = MyUserManager()
#     active_objects = ActiveManager()

#     class Meta:
#         unique_together = ("title", "description")

#     def __str__(self):
#         return self.name


#     def get_price_percentage(self):
#         return int(round((self.discount / self.price) * 100))

#     def get_real_price(self):
#         try:
#             return abs(self.old_price - self.price)
#         except:
#             return self.price


