from rest_framework import serializers
from .models import Product, CartItem, Order, ShippingMethod, DeliveryDetails, Payment, Country


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'image', 'new_price')


# class CartItemSerializer(serializers.ModelSerializer):
#     product = ProductCartSerializer()
#     item_price = serializers.SerializerMethodField() 

#     class Meta:
#         model = CartItem
        
#         fields = ('product', 'quantity', 'item_price')  


#     def get_item_price(self, obj):
#         return obj.product.new_price * obj.quantity  
    
#     def get_item_price(self, obj: CartItem) -> float:
#         return obj.product.new_price * obj.quantity

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True) 
    item_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('product_id', 'quantity', 'item_price')

    def get_item_price(self, obj):
        return obj.product.new_price * obj.quantity



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name')


class DeliveryDetailsSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='country.country_name')

    class Meta:
        model = DeliveryDetails
        fields = ('id', 'country', 'first_name', 'last_name', 'address', 'apartment')


class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = ('id', 'name', 'description', 'cost')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'card_number', 'card_holder_name', 'expiry_date', 'security_code')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user', 'items', 'total_price', 'order_date')


class CartTotalSerializer(serializers.Serializer):
    cart_total = serializers.DecimalField(max_digits=10, decimal_places=2)


class WishlistAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()


class SubscriptionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    

