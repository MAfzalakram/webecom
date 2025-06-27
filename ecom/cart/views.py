from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from ecomstore.models import Product
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from .cart import Cart 
from django.urls import reverse


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url='login')
def create_checkout_session(request):
    cart = Cart(request)
    products = cart.getProducts()
    quantities = cart.getQuantity()

    line_items = []

    for product in products:
        quantity = quantities[str(product.id)]
        price = product.sale_price if product.is_sale else product.price

        line_items.append({
            'price_data': {
                'currency': 'pkr',  
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': int(price * 100), 
            },
            'quantity': quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success')),
        cancel_url=request.build_absolute_uri(reverse('cartsummary')),

    )

    return redirect(session.url, code=303)


@login_required(login_url='login')
def payment_success(request):

    request.session['usersessionkey'] = {}
    request.session.modified = True
    return render(request, 'payment_success.html')

@login_required(login_url='login')
def payment_cancel(request):
    cart = Cart(request)
    request.session['usersessionkey'] = {}
    request.session.modified = True
     
    return render(request, 'payment_cancel.html')

@login_required(login_url='login')
def addToCart(request):
    cart_session = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        quantity =  int(request.POST.get("quantity"))
        product = get_object_or_404(Product , id=product_id)
        

        # Save product
        cart_session.add(product=product, quantity=quantity)
        quantity = cart_session.__len__()
        # Response
        messages.success(request, ("Your Product has been added successfully"))
        response = JsonResponse({"qty": str(quantity)})
        return response
    
@login_required(login_url='login')   
def updateCart(request):
    cart_session = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        quantity =  int(request.POST.get("quantity"))
        product = get_object_or_404(Product , id=product_id)
        # Save product
        cart_session.update(product=product, quantity=quantity)
        quantity = cart_session.__len__()
        # Response
        messages.success(request, "Product has been updated succefully")
        response = JsonResponse({"qty": str(quantity)})
        return response
    

def deleteCart(request):
    cart_session = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product = get_object_or_404(Product , id=product_id)
        # Save product
        cart_session.delete(product=product)
        quantity = cart_session.__len__()
        # Response
        messages.success(request, "Product has been deleted succefully")
        response = JsonResponse({"qty": str(quantity)})
        return response

    
    


@login_required(login_url='login')
def cartSummary(request):
    cart = Cart(request)
    products = cart.getProducts()
    quantity = cart.getQuantity()
    total = cart.getTotal()
    
    return render(request, "cartsummary.html", {"products": products, "quantity": quantity, "total": total})




   