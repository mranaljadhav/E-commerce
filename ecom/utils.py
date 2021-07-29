import json
from .models import *

def cookieCart(request):
	# Create empty cart for now for non-logged in user
	try:
		# here our cookie are string , we have parse it using  json.loads in backend to the python dictionary .
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_total_item':0, 'shipping':False}
	cartItems = order['get_cart_total_item']
	print('CART:', cart)

    # here i is key and all keys are productID
	for i in cart:
		# We use try block to prevent items in cart that may have been removed from database that causing error
		try:
			cartItems += cart[i]['quantity'] # increment cartItem at each iteration .
			# here we used product  because product contain all the values like price, ID 
			product = Product.objects.get(id=i)
			# getting total of each item
			total = (product.price * cart[i]['quantity'])
			order['get_cart_total'] += total # update the total price of entire item 
			order['get_cart_total_item'] += cart[i]['quantity'] # total of each quantity of each item in cart 

			item = {
				'id':product.id,
				'product':{
                    'id':product.id,'name':product.name, 'price':product.price, 'img':product.img
                     }, 
                'quantity':cart[i]['quantity'],
				'digital':product.digital,
                'get_total':total,
				}
			items.append(item)

			if product.digital == False:
				order['shipping'] = True
		except:
			pass
			
	return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		# create an order or get an order if its exist.
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# it will give all the orderItems which have this(e.g. mranal) order as the parent .
		items = order.orderitem_set.all()
		print('Items :', items)
		cartItems = order.get_cart_total_item
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems ,'order':order, 'items':items}

def guestData(request, data):
	print('User is not logged in...')
	print('Cookies :', request.COOKIES)

	name =  data['form']['name']  
	email = data['form']['email'] 

	cookiesData = cookieCart(request) # requesting the data from cookieCart function
	items =  cookiesData['items']

	# here we will check out the email is exist, if exist we attach them with their old values and allow them for shopping
	customer , created = Customer.objects.get_or_create( 
				email=email,
				)
	# here we taken name outside the get_or_create method because customer may want to change the name  
	customer.name = name
	customer.save()

	order = Order.objects.create(customer = customer, complete = False)
    # in items we have list of dictinary and we have to use that items to store into the database
	for item in items:
		product = Product.objects.get(id = item['product']['id'])
		orderItem = OrderItem.objects.create(product=product, order=order, quantity=item['quantity'])

	return customer, order