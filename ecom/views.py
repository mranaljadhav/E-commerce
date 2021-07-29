from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .utils import cookieCart, cartData, guestData
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from .forms import *
import datetime
import json

# Create your views here.
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    prod = Product.objects.all()
    return render(request, 'store.html', {'prod':prod, 'cartItems':cartItems, 'shipping' :False })

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    return render(request, 'cart.html',{'items':items, 'order':order, 'cartItems':cartItems,'shipping' :False })

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    return render(request, 'checkout.html', {'items':items, 'order':order, 'cartItems':cartItems, 'shipping' :False })

# Below method executes only when user is logged in 
def updateOrder(request):
    # we get the data in string format as dictionary from cart.js(UpdateUserOrder).
    data = json.loads(request.body)
    print('Data :', data)
    productID = data['productID']
    action = data['action']
    print('ProductId :', productID)
    print('Action :', action)
    
    customer = request.user.customer # we get the login customer.
    product = Product.objects.get(id=productID) # we get the product
    # get existing or create new order
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    # here we are using below method because if orderItem exist we wont to create new, simply we have to change the quantity, we have add or subtract .
    orderitem, created  = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action =='remove':
        orderitem.quantity = (orderitem.quantity - 1)
    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()
    
    return JsonResponse('Item is added', safe = False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print('Data :', request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        
    else:
        customer, order = guestData(request,data)
        
    # Below code is for both the user i.e for loggedin user and not loggein user
    total = float(data['form']['total'])
    order.transation_id = transaction_id

    # here we are checking this conition because we have to make sure that user will not manipulate the data from front end .
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()    

    if(order.shipping == True):
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode']
        )
    
    return JsonResponse('Payment Submitted', safe = False)


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():       
            user = form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            print('Username :', username)
            print('Email :', email)
            Customer.objects.create( user = user, name = user.username, email=email)
            messages.success(request, 'Account Created for ' + username)
            return redirect('login')

    return render(request, 'register.html', {'form':form})
    
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password )
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'Username or password is incorrect')

    return render(request, 'login.html')

def logoutPage(request):
    logout(request)
    return redirect('store')

@login_required(login_url = 'login')
def setting(request):
    customer = request.user.customer
    form = CustomerForm(instance = customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance = customer)
        if form.is_valid():
            form.save()
            return redirect("/")
    return render(request, 'setting.html',{'form':form})