from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
# Create your views here.
def hompage(request):
    product=Product.objects.all()
    context = {'products':product}
    return render(request,'homepage.html',context)
def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
    else:
        items=[]
        order={'get_cart_item':0,'get_cart_item':0}
    context = {'items':items,'order':order}
    return render(request,'cart.html',context)
def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
    else:
        items=[]
        order={'get_cart_item':0,'get_cart_item':0}
    context = {'items':items,'order':order}
    return render(request,'checkout.html',context)

def updateItem(request):
    data=json.loads(request.body)
    productID=data['productID']
    action=data['action']
    print('action:',action)
    print('productID',productID)
    
    
    customer=request.user.customer
    product=Product.objects.get(id=productID)
    order,created=Order.objects.get_or_create(customer=customer, complete=False)
    OrderItem,created=orderItem.objects.get_or_create(order=order, product=product)
    
    if action=='add':
        OrderItem.quantity=(OrderItem.quantity + 1)
    elif action=='remove':
        OrderItem.quantity=(OrderItem.quantity - 1)
    
    OrderItem.save()
    
    if OrderItem.quantity <=0:
        OrderItem.delete()    
        
    return JsonResponse('Item was added',safe=False)
    