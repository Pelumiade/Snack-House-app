from rest_framework import generics, status
from .models import Product, CartItem, Order, ShippingMethod, DeliveryDetails, Payment
from .serializers import ProductSerializer, CartItemSerializer, PaymentSerializer, DeliveryDetailsSerializer, ShippingMethodSerializer, OrderSerializer, CartTotalSerializer, SubscriptionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class AddToCartView(APIView):
    serializer_class = CartItemSerializer 

    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1)) 

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(user=user, product=product)

        # Update quantity and total price
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.total_price = product.new_price * quantity  
            cart_item.save()

            serializer = self.serializer_class(cart_item)  # Use serializer_class
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            cart_item.delete()
            return Response({"detail": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
      

class RemoveFromCartView(APIView):
    serializer_class = None 

    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get("product_id")

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart_item = CartItem.objects.get(user=user, product=product)
            cart_item.delete()
            return Response({"detail": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"detail": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)
        

# class RemoveFromCartView(APIView):
#     def post(self, request, pk, id, *args, **kwargs):
#         if request.user.id != pk:
#             return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

#         selected_cart = CartItem.active_objects.filter(user_id=pk).first()
#         selected_product = Product.not_moved_objects.filter(user_id=pk, product_id=id).first()

#         if selected_cart and selected_product:
#             selected_cart.ordered_products.remove(selected_product)
#             selected_product.quantity = 1
#             selected_product.save()

#             return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
#         else:
#             return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)        


class CartTotalView(APIView):
    serializer_class = CartTotalSerializer 

    def get(self, request, *args, **kwargs):
        user = request.user

        cart_items = CartItem.objects.filter(user=user)
        cart_total = sum(item.product.new_price * item.quantity for item in cart_items)

        serializer = self.serializer_class({"cart_total": cart_total}) 
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderView(APIView):
    serializer_class = OrderSerializer  

    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = user.cartitem_set.all()  
        total_price = sum(item.total_price for item in cart_items)
        order = Order.objects.create(user=user, total_price=total_price)
        order.items.set(cart_items)  
        cart_items.delete()

        serializer = self.serializer_class(order)  # Use serializer_class
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeliveryDetailsView(APIView):
    serializer_class = DeliveryDetailsSerializer
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = DeliveryDetailsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShippingMethodOptionsView(APIView):
    serializer_class = ShippingMethodSerializer

    def get(self, request, *args, **kwargs):
        shipping_methods = ShippingMethod.objects.all()

        serializer = ShippingMethodSerializer(shipping_methods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class PaymentView(APIView):
    serializer_class=PaymentSerializer
    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid():
            payment = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


# class SubscribeAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = SubscriptionSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
            
#             # Save the email to your database
#             # Assuming you have a Subscription model to store emails
#             Subscription.objects.create(email=email)
            
#             # Send a confirmation email
#             subject = 'Subscription Confirmation'
#             message = f'Thank you for subscribing to our newsletter! You will receive updates at {email}.'
#             from_email = 'noreply@example.com'
#             recipient_list = [email]
#             send_mail(subject, message, from_email, recipient_list, fail_silently=True)
            
#             return Response({'message': 'Subscription successful. Thank you for subscribing!'}, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)