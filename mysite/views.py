from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from .utils import *
from .models import *
import datetime
import json

# Create your views here.
def hompage(request):
    Data=cartData(request)
    cartItem = Data['cartItem']
    order = Data['order']
    items = Data['items']
    product=Product.objects.all()
    context = {'products':product,'cartItem':cartItem}
    return render(request,'homepage.html',context)
def cart(request):
    Data=cartData(request)
    cartItem = Data['cartItem']
    order = Data['order']
    items = Data['items']
    context = {'items':items,'order':order,'cartItem':cartItem}
    return render(request,'cart.html',context)
def checkout(request):
    Data=cartData(request)
    cartItem = Data['cartItem']
    order = Data['order']
    items = Data['items']
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
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)    
    else:
        print('User is not logged in')
        customer, order = guestOrder(request, data)
        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    
    if total == order.get_cart_total:
        order.complete = True
    order.save()
    
    if order.shipping == True:
            ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)

    return JsonResponse('Payment submitted..', safe=False)