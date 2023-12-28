from django.urls import path
from . import views

urlpatterns = [
    # path('', views.debug)
    path('products/barcode/<str:barcode_id>/', views.product, name = 'products'),
    path('products/', views.productsIndex, name = 'productsIndex'),
    path('products/<str:type>', views.productsType, name = 'productsType'),
    path('', views.home, name = 'home'),
    path('register', views.UserRegister, name = 'register'),
    path('login', views.UserLogin, name = 'login'),
    path('logout', views.UserLogout, name = 'logout'),
    path('shoppingCart/', views.UserCart, name = 'shoppingCart'),
    path('shoppingCart/<str:barcode>/<str:operation>', views.CartUpdate, name = 'cartUpdate'),
] 
