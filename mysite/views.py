from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import datetime
import json
# Create your views here.
def hompage(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItem=order.get_cart_item
    else:
        items=[]
        order={'get_cart_item':0,'get_cart_item':0 ,'shipping':False
               }
        cartItem=order['get_cart_item']
    product=Product.objects.all()
    context = {'products':product,'cartItem':cartItem}
    return render(request,'homepage.html',context)
def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItem=order.get_cart_item
    else:
        items=[]
        order={'get_cart_item':0,'get_cart_item':0 ,'shipping':False}
        cartItem=order['get_cart_item']
    context = {'items':items,'order':order,'cartItem':cartItem}
    return render(request,'cart.html',context)
def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItem=order.get_cart_item
    else:
        items=[]
        order={'get_cart_item':0,'get_cart_item':0,'shipping':False}
        cartItem=order['get_cart_item']
    context = {'items':items,'order':order,'cartItem':cartItem}
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
def processOrder(request):
    transcation_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer= request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transcation_id=transcation_id
        
        if total == order.get_cart_total:
            order.complete = True
        order.save()
        
        if order.shipping==True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('user is not loged in ......................')
    return JsonResponse('payment sumitted',safe=False)