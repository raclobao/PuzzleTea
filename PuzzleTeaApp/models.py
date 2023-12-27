from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True

# Create your models here.

# class ClientProfile(models.Model):
#     # clientid = models.BigIntegerField(primary_key=True)
#     address = models.CharField(null=False)
#
#     def __str__(self):
#         return str(self.name)
#
#     class Meta:
#         managed = True
#         db_table = 'client'


        
# class Internalshipping(models.Model):
#     originwarehouse = models.CharField(null=False) 
#     batchid = models.IntegerField(null=False)
#     finalwarehouse = models.CharField(null=False)
#     quantity = models.IntegerField(null=False)
#     shippingorder_orderid = models.ForeignKey('Shippingorder', on_delete=models.CASCADE, db_column='orderid')
#     # quantity_shippingorder_orderid = models.ForeignKey('Quantity', on_delete=models.CASCADE, db_column='quantity_shippingorder_orderid')
#     quantity_product_barcode = models.IntegerField(null=False)
#
#     class Meta:
#         managed = True
#         db_table = 'internalshipping'
#         unique_together = (('shippingorder_orderid', 'batchid'),)
#


class Product(models.Model):

    DefaultType = 'jig'

    barcode = models.IntegerField(primary_key=True)
    type = models.CharField()
    name = models.CharField(null=False)
    price = models.FloatField(verbose_name="Price (€)", null=False, blank=False)
    picture = models.URLField(verbose_name="Picture", max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):   # cada tipo de producto possui um valor diferente para o atributo "type"
        if not self.type:
            self.type = self.DefaultType
        super(Product, self).save(*args, **kwargs)

    def __str__(self):  # para aparecer o barcode em vez de "product object {barcode}" no admin do stock
        return str(self.barcode) + " - " + str(self.name)

    class Meta:
        managed = True
        db_table = 'product'

class Stock(models.Model):
    batchid = models.CharField()  
    quantity = models.IntegerField(null=False, default=0)
    product_barcode = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='barcode')

    def __str__(self):
        return '#' + str(self.product_barcode) + ' - batch ' + str(self.batchid)

    class Meta:
        managed = True
        db_table = 'stock'
        unique_together = (('batchid', 'product_barcode'),)


class Jigsaw(Product):
    product_barcode = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True, db_column='barcode', parent_link=True)
    theme = models.CharField(verbose_name="Theme", null=False, blank=False)
    pieceCount = models.IntegerField(verbose_name="Piece count", null=False, blank=False)

    DefaultType = 'jig'

    class Meta:
        managed = True
        db_table = 'jigsaw'


class Cube(Product):
    product_barcode = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True, db_column='barcode', parent_link=True)
    dimensions = models.CharField(verbose_name="Dimensions (mm3)", blank=True, null=True)
    weight = models.FloatField(verbose_name="Weight (g)")

    DefaultType = 'cube'

    class Meta:
        managed = True
        db_table = 'cube'
        

class Tea(Product):

    class caffeineLevels(models.TextChoices):
        low = "1", "Low"
        medium = "2", "Medium"
        high = "3", "High"

    product_barcode = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True, db_column='barcode', parent_link=True)
    flavor = models.CharField(verbose_name="Flavor", null=False, blank=False)
    caffeineLevel = models.CharField(verbose_name="Caffeine level", choices=caffeineLevels.choices, default=caffeineLevels.medium)

    DefaultType = 'tea'

    class Meta:
        managed = True
        db_table = 'tea'



class Shippingorder(models.Model):
    # orderid = models.BigIntegerField(primary_key=True)
    orderdate = models.DateField(null=False)
    shippingadress = models.CharField(null=False)
    client_clientid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='clientid')

    class Meta:
        managed = True
        db_table = 'shippingorder'


class Quantity(models.Model):
    quantity = models.IntegerField(null=False)
    # shippingorder_orderid = models.OneToOneField('Shippingorder', on_delete=models.CASCADE, db_column='shippingorder_orderid', primary_key=True)
    product_barcode = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='barcode')
    shippingorder_orderid = models.ForeignKey(Shippingorder, on_delete=models.CASCADE, db_column='orderid')  

    class Meta:
        managed = True
        db_table = 'quantity'
        unique_together = (('shippingorder_orderid', 'product_barcode'),)


class ShoppingCart(models.Model):
    client_clientid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='clientid')
# class Warehouse(models.Model):
#     name = models.CharField(primary_key=True)
#     address = models.CharField(unique=True, null=False)
#
#     def __str__(self):
#         return self.name
#
#
#     class Meta:
#         managed = True
#         db_table = 'warehouse'
#

