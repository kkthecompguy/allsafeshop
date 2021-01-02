import json
from .models import Product, Order, Customer, OrderItem, Payment, PurchaseUnit, PaymentCapture, Link


def cookie_cart(request):
  try:
    cart = json.loads(request.COOKIES['cart'])
  except:
    cart = {}

  items = []
  order = {'get_cart_items': 0, 'get_cart_total': 0, 'shipping': False}
  cart_items = order['get_cart_items']

  for i in cart:
    try:
      cart_items += cart[i]['quantity']

      product = Product.objects.get(id=i)
      total = (product.price * cart[i]['quantity'])

      order['get_cart_total'] += total
      order['get_cart_items'] += cart[i]['quantity']

      item = {
        'product': {
          'id': product.id,
          'title': product.title,
          'price': product.price,
          'imageURL': product.imageURL
        },
        'quantity': cart[i]['quantity'],
        'get_total': total
      }
      items.append(item)

      if product.digital == False:
        order['shipping'] = True
    except:
      pass
  return {'items': items, 'order': order, 'cartItems': cart_items}


def cart_data(request):
  if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cart_items = order.get_cart_items
  else:
    cookie_data = cookie_cart(request)
    cart_items = cookie_data['cartItems']
    order = cookie_data['order']
    items = cookie_data['items']

  return {'items': items, 'order': order, 'cartItems': cart_items}


def guest_order(request, data):
  print('User is not authenticated')

  name = data['userData']['name']
  email = data['userData']['email']

  cookie_data = cookie_cart(request)
  items = cookie_data['items']

  customer, created = Customer.objects.get_or_create(email=email)
  customer.name = name
  customer.save()

  order = Order.objects.create(customer=customer, complete=False)

  for item in items:
    product = Product.objects.get(id=item['product']['id'])
    order_item = OrderItem.objects.create(
      product=product,
      order=order, 
      quantity=item['quantity']
    )

  return customer, order


def save_payment(request, order):
  data = json.loads(request.body)
  payment = data['order']

  payment_save_complete = False

  try:
    payment_obj = Payment.objects.create(
      order = order,
      payment_id = payment['id'],
      intent = payment['intent'],
      status = payment['status'],
      payer_email_address = payment['payer']['email_address'],
      payer_id = payment['payer']['payer_id'],
      payer_country_code = payment['payer']['address']['country_code'],
      payer_first_name = payment['payer']['name']['given_name'],
      payer_last_name = payment['payer']['name']['surname'],
      create_time = payment['create_time'],
      update_time = payment['update_time'],
    )

    payment_capture = PaymentCapture.objects.create(
      status = payment['purchase_units'][0]['payments']['captures'][0]['status'],
      _id = payment['purchase_units'][0]['payments']['captures'][0]['id'],
      final_capture = payment['purchase_units'][0]['payments']['captures'][0]['final_capture'],
      amount = payment['purchase_units'][0]['payments']['captures'][0]['amount']['value'],
      seller_protection_status = payment['purchase_units'][0]['payments']['captures'][0]['seller_protection']['status'],
      dispute_categories = (payment['purchase_units'][0]['payments']['captures'][0]['seller_protection']['dispute_categories'][0], payment['purchase_units'][0]['payments']['captures'][0]['seller_protection']['dispute_categories'][1]),
      links = (payment['purchase_units'][0]['payments']['captures'][0]['links'][0], payment['purchase_units'][0]['payments']['captures'][0]['links'][1], payment['purchase_units'][0]['payments']['captures'][0]['links'][2]),
      create_time = payment['purchase_units'][0]['payments']['captures'][0]['create_time'],
      update_time = payment['purchase_units'][0]['payments']['captures'][0]['update_time'],
    )

    PurchaseUnit.objects.create(
      payment_id = payment_obj,
      amount = payment['purchase_units'][0]['amount']['value'],
      currency_code = payment['purchase_units'][0]['amount']['currency_code'],
      description = payment['purchase_units'][0]['description'],
      payee_email_address = payment['purchase_units'][0]['payee']['email_address'],
      merchant_id = payment['purchase_units'][0]['payee']['merchant_id'],
      reference_id = payment['purchase_units'][0]['reference_id'],
      shipping_to_name = payment['purchase_units'][0]['shipping']['name']['full_name'],
      shipping_to_address = (payment['purchase_units'][0]['shipping']['address']['address_line_1'], payment['purchase_units'][0]['shipping']['address']['admin_area_2'], payment['purchase_units'][0]['shipping']['address']['postal_code'], payment['purchase_units'][0]['shipping']['address']['country_code']),
      payments_capture = payment_capture
    )

    Link.objects.create(
      payment_id = payment_obj,
      href = payment['links'][0]['href'],
      rel = payment['links'][0]['rel'],
      method = payment['links'][0]['method'],
      title = payment['links'][0]['title'],
    )
    payment_save_complete = True
  except:
    payment_save_complete = False
  
  return payment_save_complete