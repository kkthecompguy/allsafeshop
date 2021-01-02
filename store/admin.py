from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, Shipping, Payment, PurchaseUnit, PaymentCapture, Link

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'email']
  list_display_links = ['id']
  list_filter = ['name', 'email']
  list_per_page = 25


class ProductAdmin(admin.ModelAdmin):
  list_display = ['id', 'title', 'digital']
  list_display_links = ['id', 'title']
  list_editable = ['digital']
  list_filter = ['title', 'digital']
  list_per_page = 25


class OrderAdmin(admin.ModelAdmin):
  list_display = ['id', 'customer', 'complete', 'transaction_id']
  list_display_links = ['id']
  list_editable = ['complete']
  list_filter = ['complete']
  list_per_page = 25


class ShippingAdmin(admin.ModelAdmin):
  list_display = ['id', 'customer', 'order', 'address', 'city']
  list_display_links = ['id']
  list_filter = ['customer', 'order', 'address', 'city']
  list_per_page = 25


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Shipping, ShippingAdmin)
admin.site.register(Payment)
admin.site.register(PurchaseUnit)
admin.site.register(PaymentCapture)
admin.site.register(Link)

admin.site.site_header = 'AllSafe Shop Limited System'
admin.site.site_title = 'AllSafeShop Limited | Administation'
admin.site.index_title = 'Welcome to Allsafe Shop'
