from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from .models import Jigsaw, Product, Cube, Tea
from .forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib import messages
from django.template.defaulttags import register

# Create your views here.

def home(request):
    products = Product.objects.all()
    context = {'product_ref': products}
    return render(request, 'home.html', context)

def product(request, barcode_id):
    try:
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

        Specific_fields = ([f for f in Specific_fields if f.name != 'product_barcode']) #removes product_barcode

        context = {'product_ref': product, 'specific_ref': specificProduct, 'specific_fields': Specific_fields}
    except:
        raise Http404("Product not found....")

    @register.filter
    def get_attr(obj, attr):
        if attr == 'caffeineLevel':
            caffeineDict = (dict(Tea.caffeineLevels.choices))
            return caffeineDict[str(getattr(obj, attr))]
        return getattr(obj, attr)

    return render(request, 'products.html', context)

def productsIndex(request):
    context = { 'numJigsaws':Jigsaw.objects.all().count(),
               'numCubes':Cube.objects.all().count(),
               'numTeas':Tea.objects.all().count(),}
    return render(request, 'productsIndex.html', context)


def productsType(request, type):
    products = Product.objects.all()
    context = {'products_ref': products, 'type_ref': type}
    
    if type not in ["jig", "cube", "tea"]:
        raise Http404("Wrong type!")

    @register.filter
    def is_type(objs, type):
        return objs.filter(type=type)

    return render(request, 'productsType.html', context)

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
        print("hi")
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

