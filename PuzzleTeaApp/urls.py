from django.urls import path
from . import views

urlpatterns = [
    # path('', views.debug)
    path('products/barcode/<str:barcode_id>/', views.product, name = 'products'),
    path('products/', views.productsIndex, name = 'productsIndex'),
    path('products/<str:type>', views.productsType, name = 'productsType'),
    path('', views.home, name = 'home'),
    path('register', views.userRegister, name = 'register'),
    path('login', views.userLogin, name = 'login'),
    path('logout', views.userLogout, name = 'logout'),
    path('shoppingCart/', views.userCart, name = 'shoppingCart'),
    path('shoppingCart/adjustCart', views.adjustCart, name = 'adjustCart'),
    path('shoppingCart/<str:barcode>/<str:operation>', views.cartUpdate, name = 'cartUpdate'),
] 
