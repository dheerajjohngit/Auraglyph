from django.contrib import admin
from .models import OrderItem, Product, Vendor, Wishlist, Cart, Order, OrderItem

admin.site.register(Product)
admin.site.register(Vendor)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)