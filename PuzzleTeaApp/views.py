from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from .models import Jigsaw, Product, Cube, Stock, Tea, ShoppingCart
from .forms import AddressForm, CreateUserForm, LoginForm, ShoppingForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth
from django.contrib import messages
from django.template.defaulttags import register
from numpy import sum
from .order import processOrder

# Create your views here.

def home(request):
    products = Product.objects.all()
    context = {'product_ref': products}
    return render(request, 'home.html', context)


def product(request, barcode_id):
    @register.filter
    def get_attr(obj, attr):
        if attr == 'caffeineLevel':
            caffeineDict = (dict(Tea.caffeineLevels.choices))
            return caffeineDict[str(getattr(obj, attr))]
        return getattr(obj, attr)

    @register.filter
    def alreadyAdded(obj):
        '''
        Check if an specified object is already in the user's shopping cart 
        '''
        ShoppingItem =  ShoppingCart.objects.filter(product = obj.barcode, client = request.user.id).first()
        return ShoppingItem != None 

    try:
        form = ShoppingForm()

        product = Product.objects.get(barcode = barcode_id)
        type = product.type
        if type == 'cube':
            Type_fields = Cube._meta.get_fields()
            specificProduct = Cube.objects.get(barcode = barcode_id)
        elif type == 'jig':
            specificProduct = Jigsaw.objects.get(barcode = barcode_id)
            Type_fields = Jigsaw._meta.get_fields()
        elif type == 'tea':
            specificProduct = Tea.objects.get(barcode = barcode_id)
            Type_fields = Tea._meta.get_fields()

        Product_fields = Product._meta.get_fields()
        Specific_fields = list(set(Type_fields) - set(Product_fields))

        Specific_fields = ([f for f in Specific_fields if f.name != 'product']) #removes product_barcode

        itemStocks = Stock.objects.filter(product = product)
        availableQuantity = int(sum([stock.quantity for stock in itemStocks]))

    except:
        raise Http404("Product not found....")

    if request.method == 'POST':
        form = ShoppingForm(request.POST)
        quantity = (request.POST.get('quantity'))

        if form.is_valid():
            NewShoppingCartEntry = ShoppingCart(quantity=quantity, client=request.user, product=product) 
            NewShoppingCartEntry.save()

    context = {'product_ref': product, 'specific_ref': specificProduct, 'specific_fields': Specific_fields, 'ShoppingForm': form, 'availableQuantity':availableQuantity}

    return render(request, 'products.html', context)


def productsIndex(request):
    context = { 'numJigsaws':Jigsaw.objects.all().count(),
               'numCubes':Cube.objects.all().count(),
               'numTeas':Tea.objects.all().count(),}
    return render(request, 'productsIndex.html', context)


def productsType(request, type):
    @register.filter
    def is_type(objs, type):
        return objs.filter(type=type)

    products = Product.objects.all()
    context = {'products_ref': products, 'type_ref': type}

    if type not in ["jig", "cube", "tea"]:
        raise Http404("Wrong type!")

    return render(request, 'productsType.html', context)


def userCart(request):
    @register.filter
    def get_totalPrice(obj):
        return obj.quantity*obj.product.price

    @register.filter
    def by_currentUser(objs, correctUser):  #why not using userId instead of passing "correctUser"? weird bug with userId not changing with different accounts
        return objs.filter(client=correctUser).order_by('product')


    if not request.user.is_authenticated:
        return redirect('/')

    userId = request.user.id

    if request.method == 'POST':
        form = AddressForm(request.POST)

        if form.is_valid():
            address = request.POST.get('address')
            processOrder(userId, address)
            redirect('shoppingCart')

    userShoppingCart = ShoppingCart.objects.filter(client=userId) 
    form = AddressForm(request.POST)

    ShoppingCartTable = ShoppingCart.objects.all()
    totalQuantity = sum([item.quantity for item in ShoppingCartTable if item.client.id == userId])
    totalPrice = sum([item.quantity*item.product.price for item in ShoppingCartTable if item.client.id == userId])

    numMessages = 0

    for item in userShoppingCart:
        itemStocks = Stock.objects.filter(product=item.product)
        availabelQuantity = int(sum([stock.quantity for stock in itemStocks]))

        if availabelQuantity == 0:
            messages.info(request, 'Item "{}": UNAVAILABLE'.format(item.product.name, item.quantity, availabelQuantity))
            numMessages+=1

        elif availabelQuantity < item.quantity:
            messages.info(request, 'Item "{}": {} in cart but only {} in stock '.format(item.product.name, item.quantity, availabelQuantity))
            numMessages+=1


    context = {'shoppingCart_ref': ShoppingCartTable, 'totalPrice':totalPrice, 'totalQuantity':totalQuantity, \
               'cartEmpty': userShoppingCart.count() <= 0, 'hasMessages':numMessages > 0, 'correctUser':userId, 'AddressForm':form}

    return render(request, 'shoppingCart.html', context)


def adjustCart(request):
    userId = request.user.id
    userShoppingCart = ShoppingCart.objects.filter(client=userId) 

    for item in userShoppingCart:
        itemStocks = Stock.objects.filter(product=item.product)
        availabelQuantity = int(sum([stock.quantity for stock in itemStocks]))

        if availabelQuantity == 0:
            item.delete()

        elif availabelQuantity < item.quantity:
            item.quantity = availabelQuantity
            item.save()

    return redirect('shoppingCart')


def cartUpdate(request, barcode, operation):
    try:
        cartItem = ShoppingCart.objects.get(product=barcode, client=request.user.id)
    except:
        return redirect('shoppingCart')

    if operation == '+':
        cartItem.quantity += 1;
        if cartItem.quantity >= 1:
            cartItem.save()
        return redirect('shoppingCart')

    elif operation == '-':
        cartItem.quantity -= 1;
        if cartItem.quantity >= 1:
            cartItem.save()
        return redirect('shoppingCart')

    elif operation == 'remove':
        cartItem.delete()
        return redirect('shoppingCart')

    else:
        return redirect('/')


def userRegister(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            GivenUsername = request.POST.get('username')
            GivenPassword = request.POST.get('password')

            user = authenticate(request, username=GivenUsername, password=GivenPassword)
            auth.login(request, user)

            return redirect("/")
        # else:
        #     return render(request, "register.html", context={'RegisterForm': form})
    else:
        form = CreateUserForm()

    context = {'RegisterForm': form}
    return render(request, 'register.html', context)
# def debug(request):
#     return HttpResponse('....')


def userLogin(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            GivenUsername = request.POST.get('username')
            GivenPassword = request.POST.get('password')

            user = authenticate(request, username=GivenUsername, password=GivenPassword)
            if user is not None:
                auth.login(request, user)
                return redirect("/")
        else:
            messages.info(request, "Username or Password is incorrect")
    else:
        form = LoginForm()

    context = {'LoginForm': form}
    return render(request, 'login.html', context)


def userLogout(request):
    auth.logout(request)
    return redirect("/")

