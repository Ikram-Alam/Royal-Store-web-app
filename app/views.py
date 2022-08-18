from contextlib import redirect_stderr
from itertools import product
from sre_constants import SUCCESS
from unicodedata import category
from urllib import response
from urllib.request import Request
from django.shortcuts import  render, redirect
from django.views import View
from .models import Cart, Product, Customer, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from app import forms

# def home(request):
# return render(request, 'app/home.html')


class ProductView(View):
    def get(self, request):
        Winter = Product.objects.filter(category='Win')
        Summer = Product.objects.filter(category='Sum')
        Watches = Product.objects.filter(category='Wat')
        Shoes = Product.objects.filter(category='Sh')
        return render(request, 'app/home.html',
        {'Winter': Winter, 'Summer': Summer, 'Watches': Watches, 'Shoes':Shoes})


# def product_detail(request):
 #   return render(request, 'app/productdetail.html')


class ProductDetailView(View):
    def get(self, request, pk):
      product = Product.objects.get(pk=pk)
      item_already_in_cart = False
      if request.user.is_authenticated: 
        item_already_in_cart = Cart.objects.filter(Q(product=product.id)
        & Q(User=request.user)).exists() 
      return render(request, 'app/productdetail.html',
      {'product': product, 'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(User=user, product=product).save()
    return redirect('/cart') 

@login_required
def show_cart(request):
  if request.user.is_authenticated:
    user = request.user
    cart = Cart.objects.filter(User=user)
    #print(cart)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.User == user]
    #print(cart_product)
    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        totalamount = amount + shipping_amount
      return render(request, 'app/addtocart.html',
      {'carts':cart, 'totalamount':totalamount, 'amount':amount})
    else:
      return render(request, 'app/emptycart.html') 



def plus_cart(request):
  if request.method  == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(User=request.user))
    c.quantity+=1
    c.save()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.User == request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount

    data = {
      'quantity' : c.quantity,
      'amount'  : amount,
      'totalamount': amount + shipping_amount
    }
    return JsonResponse(data)


def minus_cart(request):
  if request.method  == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(User=request.user))
    c.quantity-=1
    c.save()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.User ==request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount

    data = {
      'quantity' : c.quantity,
      'amount'  : amount,
      'totalamount': amount + shipping_amount
    }
    return JsonResponse(data)




def remove_cart(request):
  if request.method  == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(User=request.user))
    c.delete()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.User ==request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount

    data = {
      'amount'  : amount,
      'totalamount': amount + shipping_amount
    }
    return JsonResponse(data)

        








def buy_now(request):
    return render(request, 'app/buynow.html')




#def address(request):
#    return render(request, 'app/address.html')



@login_required
def address(request):
 add = Customer.objects.filter(User=request.user)
 return render(request, 'app/address.html',{'add':add,'active': 'btn-primary'})




@login_required
def orders(request):
  op = OrderPlaced.objects.filter(User=request.user)
  return render(request, 'app/orders.html',{'order_placed':op})



def watches(request):     
  watches = Product.objects.filter(category='Wat')    
  return render(request, 'app/mobile.html', {'watches': watches})



def shoes(request):
  shoes = Product.objects.filter(category='Sh') 
  return render(request, 'app/shoes.html',{'shoes':shoes}) 


def winter(request):
  winter = Product.objects.filter(category='Win')
  return render(request, 'app/winter.html', {'winter':winter}) 

def summer(request):
  summer = Product.objects.filter(category='Sum')
  return render(request, 'app/summer.html', {'summer':summer}) 


def login(request):
    return render(request, 'app/login.html')


#def customerregistration(request):
 #   return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html',
  {'form': form}) 
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulation || Registered Successfully') 
   form.save()
  return render(request, 'app/customerregistration.html',
  {'form': form}) 

@login_required
def checkout(request):
  user = request.user
  add = Customer.objects.filter(User=user)
  cart_items = Cart.objects.filter(User=user)
  amount = 0.0
  shipping_amount = 70.0
  totalamount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.User == request.user]
  if cart_product:
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
    totalamount = amount + shipping_amount

  return render(request, 'app/checkout.html', {'add':add,
   'totalamount':totalamount, 'cart_items':cart_items})

@login_required
def payment_done(request):
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id=custid)
  cart = Cart.objects.filter(User=user)
  for c in cart:
    OrderPlaced(User=user, Customer=customer, product=c.product,
    quantity=c.quantity).save()
    c.delete()
  return redirect("orders")    

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
  def get(self, request):
    form = CustomerProfileForm()
    return render(request, 'app/profile.html',{'form':form, 
    'active':'btn-primary'})

  def post(self, request):
   form = CustomerProfileForm(request.POST)
   if form.is_valid(): 
     usr = request.user
     name = form.cleaned_data['name']
     locality = form.cleaned_data['locality']
     city = form.cleaned_data['city']
     state = form.cleaned_data['state']
     zipcode = form.cleaned_data['zipcode']
     reg = Customer(User=usr, name=name, locality=locality,city=city,
     state=state, zipcode=zipcode)   
     reg.save()
     messages.success(request, 'Congratulations || Profile Updated Successfully')
   return render(request, 'app/profile.html', {'form':form,
   'active': 'btn-primary'})

