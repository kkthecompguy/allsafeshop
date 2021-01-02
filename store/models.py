from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
  name = models.CharField(max_length=100, blank=True)
  email = models.EmailField()

  def __str__(self):
    return self.name


class Product(models.Model):
  title = models.CharField(max_length=100)
  price = models.DecimalField(max_digits=9, decimal_places=2)
  image = models.ImageField(upload_to='media/%Y/%m/%d')
  digital = models.BooleanField(default=False)

  def __str__(self):
    return self.title

  @property
  def imageURL(self):
    try:
      url = self.image.url
    except: 
      url = ''
    return url


class Order(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
  complete = models.BooleanField(default=False)
  transaction_id = models.CharField(max_length=100, blank=True)
  date_ordered = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(self.pk)

  @property
  def get_cart_total(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.get_total for item in orderitems])
    return total

  @property
  def get_cart_items(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.quantity for item in orderitems])
    return total

  @property
  def shipping(self):
    shipping = False
    orderitems = self.orderitem_set.all()
    for i in orderitems:
      if i.product.digital == False:
        shipping = True
    return shipping


class OrderItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
  quantity = models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)

  @property
  def get_total(self):
    total = self.product.price * self.quantity
    return total


class Shipping(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
  address = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  zipcode = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.customer.name


class Payment(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
  payment_id = models.CharField(max_length=50)
  intent = models.CharField(max_length=50)
  status = models.CharField(max_length=50)
  payer_email_address = models.EmailField()
  payer_id = models.CharField(max_length=50)
  payer_country_code = models.CharField(max_length=20)
  payer_first_name = models.CharField(max_length=100)
  payer_last_name = models.CharField(max_length=100)
  create_time = models.DateTimeField()
  update_time = models.DateTimeField()

  def __str__(self):
    return self.payment_id


class PurchaseUnit(models.Model):
  payment_id = models.OneToOneField(Payment, on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=9, decimal_places=2)
  currency_code = models.CharField(max_length=20)
  description = models.CharField(max_length=50)
  payee_email_address = models.EmailField()
  merchant_id = models.CharField(max_length=50)
  reference_id = models.CharField(max_length=20)
  shipping_to_name = models.CharField(max_length=100)
  shipping_to_address = models.CharField(max_length=255)
  payments_capture = models.OneToOneField('PaymentCapture', on_delete=models.CASCADE)

  def __str__(self):
    return str(self.amount)


class PaymentCapture(models.Model):
  status = models.CharField(max_length=100)
  _id = models.CharField(max_length=100)
  final_capture = models.BooleanField(default=False)
  amount = models.DecimalField(max_digits=9, decimal_places=2)
  seller_protection_status = models.CharField(max_length=100)
  dispute_categories = models.TextField()
  links = models.TextField()
  create_time = models.DateTimeField()
  update_time = models.DateTimeField()

  def __str__(self):
    return str(self.pk)



class Link(models.Model):
  payment_id = models.OneToOneField(Payment, on_delete=models.CASCADE)
  href = models.CharField(max_length=255)
  rel = models.CharField(max_length=255)
  method = models.CharField(max_length=50)
  title = models.CharField(max_length=100)

  def __str__(self):
    return f'Payment ID {self.payment_id}'