from datetime import datetime
from django.contrib.auth.models import User
from .models import BatchQuantity, ShippingOrder, ShoppingCart, Stock

def processOrder(client, address):
    date = datetime.now()
    user = User.objects.get(pk=client)
    shippingOrder = ShippingOrder(orderdate=date, client=user, shippingadress=address)
    shippingOrder.save()
    userShoppingCart = ShoppingCart.objects.filter(client=client) 

    for item in userShoppingCart:
        itemStock = Stock.objects.filter(product=item.product).order_by('batchid')

        for batch in itemStock:
            if batch.quantity >= item.quantity:
                quantityRow = BatchQuantity(product=item.product, quantity=item.quantity, batchid=batch.batchid, shippingorder=shippingOrder)
                batch.quantity -= item.quantity
                item.quantity = 0 
                quantityRow.save()
                batch.save()
                break

            else:
                quantityRow = BatchQuantity(product=item.product, quantity=batch.quantity, batchid=batch.batchid, shippingorder=shippingOrder)
                item.quantity -= batch.quantity
                batch.quantity = 0
                quantityRow.save()
                batch.save()

        item.delete()
