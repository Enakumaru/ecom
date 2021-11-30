from django.urls import path
from . import views
urlpatterns = (
    path("",views.hompage,name="homepage"),
    path("cart/",views.cart,name="cart"),
    path("checkout/",views.checkout,name="checkout"),
    path( "update_item/" ,views.updateItem, name="update_item"),
)