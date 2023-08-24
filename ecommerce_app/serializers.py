from rest_framework import serializers
from .models import Product, CartItem, Order, ShippingMethod, DeliveryDetails, Payment, Country


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    item_price = serializers.SerializerMethodField() 

    class Meta:
        model = CartItem
        #fields = ('product', 'quantity') 
        fields = ('product', 'quantity', 'item_price')  


    def get_item_price(self, obj):
        return obj.product.new_price * obj.quantity  
    
    def get_item_price(self, obj: CartItem) -> float:
        return obj.product.new_price * obj.quantity


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name')


class DeliveryDetailsSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = DeliveryDetails
        fields = ('id', 'user', 'country', 'first_name', 'last_name', 'address', 'apartment')

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


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


class SubscriptionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    
