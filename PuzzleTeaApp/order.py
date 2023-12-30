from datetime import datetime
from django.contrib.auth.models import User
from .models import BatchQuantity, ShippingOrder, ShoppingCart, Stock

def processOrder(client, address, totalprice):
    date = datetime.now()
    user = User.objects.get(pk=client)
    shippingOrder = ShippingOrder(orderdate=date, client=user, shippingadress=address, totalprice=totalprice)
    shippingOrder.save()
    userShoppingCart = ShoppingCart.objects.filter(client=client) 

    for item in userShoppingCart:
        itemStock = Stock.objects.filter(product=item.product).order_by('batchid')

        for batch in itemStock:
            if batch.quantity >= item.quantity:
                quantityRow = BatchQuantity(stock=batch, quantity=item.quantity, shippingorder=shippingOrder)
                batch.quantity -= item.quantity
                item.quantity = 0 
                quantityRow.save()
                batch.save()
                break

            else:
                quantityRow = BatchQuantity(quantity=item.quantity, stock=batch, shippingorder=shippingOrder)
                item.quantity -= batch.quantity
                batch.quantity = 0
                quantityRow.save()
                batch.save()

        item.delete()
