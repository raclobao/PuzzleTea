from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from .models import Jigsaw, Product, Cube, Tea, ShoppingCart
from .forms import CreateUserForm, LoginForm, ShoppingForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.template.defaulttags import register

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
    except:
        raise Http404("Product not found....")

    if request.method == 'POST':
        form = ShoppingForm(request.POST)
        quantity = (request.POST.get('quantity'))

        if form.is_valid():
            NewShoppingCartEntry = ShoppingCart(quantity=quantity, client=request.user, product=product) 
            NewShoppingCartEntry.save()
            messages.info(request, "Item added to your cart!")
        else:
            messages.info(request, "Invalid input!")

    context = {'product_ref': product, 'specific_ref': specificProduct, 'specific_fields': Specific_fields, 'ShoppingForm': form}

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

def UserCart(request):
     
    @register.filter
    def by_currentUser(objs):
        # user = User.objects.get(pk=id)
        # username = user.id
        userId = request.user.id
        print(userId)
        return objs.filter(client=userId).order_by('product')

    if not request.user.is_authenticated:
        return redirect('/')

    ShoppingCartTable = ShoppingCart.objects.all()
    context = {'shoppingCart_ref': ShoppingCartTable}
    return render(request, 'shoppingCart.html', context)

def CartUpdate(request, barcode, operation):

    try:
        cartItem = ShoppingCart.objects.get(product=barcode, client=request.user.id)
    except:
        return redirect('shoppingCart')

    if operation == '+':
        cartItem.quantity += 1;
        if cartItem.quantity >= 0:
            cartItem.save()
        return redirect('shoppingCart')

    elif operation == '-':
        cartItem.quantity -= 1;
        if cartItem.quantity >= 0:
            cartItem.save()
        return redirect('shoppingCart')

    else:
        return redirect('/')



def UserRegister(request):

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

def UserLogin(request):

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


def UserLogout(request):
    auth.logout(request)
    return redirect("/")

