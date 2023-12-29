from django.contrib import admin
from .models import Cube, BatchQuantity, ShippingOrder, Tea, Jigsaw, Stock, ShoppingCart
# Register your models here.

# class Admin_Product(admin.ModelAdmin):
#     fieldsets = [
#         ('Cube details', {'fields': ['name']}),
#     ]

class Admin_Cube(admin.ModelAdmin):
    fieldsets = [
        ('Cube details' , {'fields': ['name', 'barcode', 'price', 'picture', 'dimensions', 'weight']}),
    ]

class Admin_Tea(admin.ModelAdmin):
    fieldsets = [
        ('Tea details' , {'fields': ['name', 'barcode', 'price', 'picture', 'flavor', 'caffeineLevel']}),
    ]

class Admin_Jigsaw(admin.ModelAdmin):
    fieldsets = [
        ('Jigsaw details' , {'fields': ['name', 'barcode', 'price', 'picture', 'pieceCount', 'theme']}),
    ]



admin.site.register(Cube, Admin_Cube)
admin.site.register(Jigsaw, Admin_Jigsaw)
admin.site.register(Tea, Admin_Tea)
admin.site.register(Stock)
admin.site.register(ShoppingCart)
admin.site.register(BatchQuantity)
admin.site.register(ShippingOrder)
