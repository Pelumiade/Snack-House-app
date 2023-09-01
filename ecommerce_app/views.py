from rest_framework import generics, status
from .models import Product, CartItem, Order, ShippingMethod, DeliveryDetails, Payment, Subscription, WishlistItem
from .serializers import ProductSerializer, CartItemSerializer, PaymentSerializer, DeliveryDetailsSerializer, ShippingMethodSerializer, OrderSerializer, CartTotalSerializer, SubscriptionSerializer, WishlistAddSerializer, CartItemListSerializer, RemoveCartItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.tasks import send_email
from rest_framework.permissions import IsAuthenticated


class ProductListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class LowestPriceProductsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        products = Product.objects.order_by('new_price')[:2]
        serializer = ProductSerializer(products, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class FeaturedProductsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        products = Product.objects.order_by('origin_type')[:6]
        serializer = ProductSerializer(products, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AddToCartView(APIView):
    serializer_class = CartItemSerializer 
    permission_classes = [IsAuthenticated] 

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

            serializer = self.serializer_class(cart_item) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            cart_item.delete()
            return Response({"detail": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
        

class ListCartItemsView(generics.ListAPIView):
    serializer_class = CartItemListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)


class RemoveFromCartView(APIView):
    serializer_class = RemoveCartItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):  # Define product_id as an argument here
        try:
            product = Product.objects.get(id=product_id)
            cart_item = CartItem.objects.get(product=product, user=request.user)
            cart_item.delete()
            return Response({'detail': 'Item removed from cart'}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({'detail': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        

        
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
    permission_classes = [IsAuthenticated] 

    def get(self, request, *args, **kwargs):
        user = request.user

        cart_items = CartItem.objects.filter(user=user)
        cart_total = sum(item.product.new_price * item.quantity for item in cart_items)

        serializer = self.serializer_class({"cart_total": cart_total}) 
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderView(APIView):
    serializer_class = OrderSerializer 
    permission_classes = [IsAuthenticated] 
 
    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = user.cartitem_set.all()  
        total_price = sum(item.total_price for item in cart_items)
        order = Order.objects.create(user=user, total_price=total_price)
        order.items.set(cart_items)  
        cart_items.delete()

        serializer = self.serializer_class(order)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShippingMethodOptionsView(APIView):
    serializer_class = ShippingMethodSerializer
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        shipping_methods = ShippingMethod.objects.all()

        serializer = ShippingMethodSerializer(shipping_methods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class DeliveryDetailsAPIView(APIView):
    serializer_class=DeliveryDetailsSerializer
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        serializer = DeliveryDetailsSerializer(data=request.data)

        if serializer.is_valid():
            delivery = serializer.save

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  
class PaymentView(APIView):
    serializer_class=PaymentSerializer
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid():
            payment = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class AddToWishlistAPIView(APIView):
    serializer_class = WishlistAddSerializer
    permission_classes = [IsAuthenticated] 


    def post(self, request, *args, **kwargs):
        serializer = WishlistAddSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            
            wishlist_item, created = WishlistItem.objects.get_or_create(
                user=request.user, product_id=product_id
            )
            
            if created:
                return Response({'message': 'Item added to wishlist'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Item is already in wishlist'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class RemoveFromWishlistAPIView(APIView):
    serializer_class = None
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        
        
        try:
            wishlist_item = WishlistItem.objects.get(user=request.user, product_id=product_id)
            wishlist_item.delete()
            return Response({'message': 'Item removed from wishlist'}, status=status.HTTP_204_NO_CONTENT)
        except WishlistItem.DoesNotExist:
            return Response({'message': 'Item not found in wishlist'}, status=status.HTTP_404_NOT_FOUND)


class SubscribeAPIView(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes=[]

    def post(self, request, *args, **kwargs):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            Subscription.objects.create(email=email)
            
            email_data = {
                'email_subject': 'Subscription Confirmation',
                'email_body': f'Thank you for subscribing to our newsletter! You will receive updates at {email}.',
                'to_email': email
            }
            send_email(email_data)
            
            return Response({'message': 'Subscription successful. Thank you for subscribing!'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
