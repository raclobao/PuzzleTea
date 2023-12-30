from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True

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
        return '#' + str(self.barcode) + " - " + str(self.name)

    class Meta:
        managed = True
        db_table = 'product'


class Stock(models.Model):
    batchid = models.CharField()  
    quantity = models.PositiveIntegerField(null=False, default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='barcode')

    def __str__(self):
        return str(self.product) + ' - batch ' + str(self.batchid)

    class Meta:
        managed = True
        db_table = 'stock'
        unique_together = (('batchid', 'product'),)


class Jigsaw(Product):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True, db_column='barcode', parent_link=True)
    theme = models.CharField(verbose_name="Theme", null=False, blank=False)
    pieceCount = models.IntegerField(verbose_name="Piece count", null=False, blank=False)

    DefaultType = 'jig'

    class Meta:
        managed = True
        db_table = 'jigsaw'


class Cube(Product):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True, db_column='barcode', parent_link=True)
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

    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True, db_column='barcode', parent_link=True)
    flavor = models.CharField(verbose_name="Flavor", null=False, blank=False)
    caffeineLevel = models.CharField(verbose_name="Caffeine level", choices=caffeineLevels.choices, default=caffeineLevels.medium)

    DefaultType = 'tea'

    class Meta:
        managed = True
        db_table = 'tea'



class ShippingOrder(models.Model):
    # orderid = models.BigIntegerField(primary_key=True)
    orderdate = models.DateField(null=False)
    shippingadress = models.CharField(null=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE, db_column='clientid')

    def __str__(self):
        return str(self.client) + ' - ' + str(self.orderdate)

    class Meta:
        managed = True
        db_table = 'shippingorder'


class BatchQuantity(models.Model):
    quantity = models.IntegerField(null=False)
    batchid = models.IntegerField(null=False)
    # shippingorder = models.OneToOneField('Shippingorder', on_delete=models.CASCADE, db_column='shippingorder_orderid', primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='barcode')
    shippingorder = models.ForeignKey(ShippingOrder, on_delete=models.CASCADE, db_column='orderid')  

    def __str__(self):
        return str(self.shippingorder) + ' - ' + str(self.product.name) + ' - batch ' + str(self.batchid)

    class Meta:
        managed = True
        db_table = 'quantity'
        unique_together = (('shippingorder', 'product', 'batchid'),)


class ShoppingCart(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, db_column='clientid')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='barcode') 
    quantity = models.IntegerField(verbose_name="Quantity", null=False, blank=False)

    def __str__(self):
        return str(self.client.username) + ' - ' + str(self.product.name) + ' - ' + str(self.quantity)


    class Meta:
        managed = True
        db_table = 'shoppingcart'
        unique_together = (('client', 'product'),)

