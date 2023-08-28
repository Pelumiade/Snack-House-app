from django.urls import path
from .views import (
    ProductListView,
    AddToCartView,
    RemoveFromCartView,
    CartTotalView,
    OrderView,
    DeliveryDetailsView,
    ShippingMethodOptionsView,
    PaymentView,
    SubscribeAPIView,
    AddToWishlistAPIView,
    RemoveFromWishlistAPIView
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('add_to_cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove_from_cart/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart_total/', CartTotalView.as_view(), name='cart-total'),
    path('create_order/', OrderView.as_view(), name='create-order'),
    #path('delivery_details/', DeliveryDetailsView.as_view(), name='delivery-details'),
   # path('delivery_details/<int:pk>/', DeliveryDetailsView.as_view(), name='delivery-details-detail'),
    path('shipping_methods/', ShippingMethodOptionsView.as_view(), name='shipping-methods'),
    path('make_payment/', PaymentView.as_view(), name='make-payment'),
    path('subscribe/', SubscribeAPIView.as_view(), name='subscribe'),
    path('wishlist/add/', AddToWishlistAPIView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/', RemoveFromWishlistAPIView.as_view(), name='remove_from_wishlist'),
]




