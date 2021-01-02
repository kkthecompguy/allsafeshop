from django.urls import path
from .views import store, cart, checkout, add_to_cart, place_order

app_name = "store"
urlpatterns = [
  path('', store, name='store'),
  path('cart', cart, name='cart'),
  path('checkout', checkout, name='checkout'),
  path('add-to-cart', add_to_cart, name='add-to-cart'),
  path('place-order', place_order, name='place-order'),
]