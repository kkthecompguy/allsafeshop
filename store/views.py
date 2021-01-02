import json
from datetime import datetime
from decimal import Decimal
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Order, OrderItem, Customer, Shipping
from .utils  import cart_data, cookie_cart, guest_order, save_payment

# Create your views here.
def store(request):
  data = cart_data(request)
  cart_items = data['cartItems']
  products = Product.objects.all()

  context = {
    'products': products,
    'cartItems': cart_items
  }
  return render(request, 'store/store.html', context)


def cart(request):
  data = cart_data(request)
  cart_items = data['cartItems']
  order = data['order']
  items = data['items']

  context = {
    'items': items,
    'order': order,
    'cartItems': cart_items
  }
  return render(request, 'store/cart.html', context)


def checkout(request):
  data = cart_data(request)
  cart_items = data['cartItems']
  order = data['order']
  items = data['items']

  context = {
    'items': items,
    'order': order,
    'cartItems': cart_items
  }
  return render(request, 'store/checkout.html', context)


def add_to_cart(request):
  data = json.loads(request.body)
  product_id = data['productId']
  action = data['action']

  customer = request.user.customer
  product = Product.objects.get(id=product_id)
  order, created = Order.objects.get_or_create(customer=customer, complete=False)

  order_item, created = OrderItem.objects.get_or_create(product=product, order=order)

  if action == 'add':
    order_item.quantity = (order_item.quantity + 1)
  elif action == 'remove':
    order_item.quantity = (order_item.quantity - 1)

  order_item.save()

  if order_item.quantity <= 0:
    order_item.delete()

  return JsonResponse({'item': 'item was added to cart'}, safe=False)


def place_order(request):
  data = json.loads(request.body)
  transaction_id = datetime.now().timestamp()

  if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
  else:
    customer, order = guest_order(request, data)

  total = Decimal(data['userData']['total'])
  order.transaction_id = transaction_id

  if total == order.get_cart_total:
    order.complete = True

  order.save()

  if order.shipping == True:
    Shipping.objects.create(
      customer=customer,
      order=order,
      address=data['shippingInfo']['address'],
      city=data['shippingInfo']['city'],
      state=data['shippingInfo']['state'],
      zipcode=data['shippingInfo']['zipcode']
    )

  payment_save_complete = save_payment(request, order)
  print(payment_save_complete)
    
  return JsonResponse({'response': 'Your payment was complete'})