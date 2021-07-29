from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
	# OneToOneField --> user can have one customer and one customer can have one user 
	# on_delete=models.CASCADE --> we want to delete this when user is deleted.
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)
	profile_pic = models.ImageField(null = True, blank = True,  default='/static/images/download.png')

	def __str__(self):
		return str(self.user)

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	digital = models.BooleanField(default=False, null=True, blank=True)
	img = models.ImageField(null = True)

	def __str__(self):
		return str(self.name)


class Order(models.Model):
	# Many to one relationship means customer can have multiple order.
	# on_delete=models.SET_NULL --> if customer get deleted we want delete the order, we want to set customer value to null.
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)


	@property
	def shipping(self):
		shipping = False
		order_item = self.orderitem_set.all()
		for i in order_item:
			if i.product.digital == False:
				shipping = True
		return shipping		

	@property
	def get_cart_total(self):
		order_item = self.orderitem_set.all()
		print('Order Item :', order_item)
		total = sum(item.get_total for item in order_item)
		return total
	
	@property
	def get_cart_total_item(self):
		order_item = self.orderitem_set.all()
		total = sum(item.quantity for item in order_item)
		return total

	def __str__(self):
		return str(self.customer)
	
class OrderItem(models.Model):
	# Many to one relationship means customer product can have multiple OrderItems. 
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	# Order is our cart and orderItem is Item within our cart, So cart can have multiple orderItem .
	# Single Order can have multiple orderItems .  
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total
	
	def __str__(self):
		return str(self.product)

class ShippingAddress(models.Model):
	# customer is taken because if order is get deleted i would  like to have shipping address for customer.
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.address)