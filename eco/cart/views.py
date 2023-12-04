from django.shortcuts import render,get_object_or_404,redirect
from ecom.models import Product,CartItem,Cart,Order
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from .forms import OrderForm

def _cart_id(request):
    cart=request.user
    # print('you are',request.session.get('username'))
    if not cart:
        cart=request.user()
        print(f"Generated new cart ID: {cart}")
    cart.save()
    return cart

def add_cart(request,prd_id):
    product=Product.objects.get(id=prd_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('cart:cart_detail')

def cart_detail(request,total=0,counter=0,cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,active=True)
        for cart_item in cart_items:
            if cart_item.product.is_sale:
                price=cart_item.product.sale_price
            else:
                price=cart_item.product.price
            total+=(price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,'cartsum.html',dict(cart_items=cart_items,total=total,counter=counter))

def cart_remove(request,prd_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=prd_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')

def full_remove(request,prd_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=prd_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')


def create_order(request,prd_id):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            current_user = request.user
            print(current_user)
            order = form.save(commit=False)
            # if current_user.is_staff and not current_user.is_superuser:
            order.customer = current_user
            product = Product.objects.get(pk=prd_id) 
            image = product.image
            order.image=image
            order.product = product

            order.save()
            full_remove(request,prd_id)
            return redirect('home')
    else:
        form = OrderForm()

    return render(request, 'order.html', {'form': form})

def myorder(request):
    ord=Order.objects.filter(customer=_cart_id(request))
    prd=Product.objects.filter
    return render(request, 'myorder.html',{'ord':ord})
