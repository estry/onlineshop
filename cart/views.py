from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from shop.models import Product
from .forms import AddProductForm
from coupon.forms import AddCouponForm


# Create your views here.


@require_POST
def add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    form = AddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'])

    return redirect('cart:detail')


def remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')


# 장바구니 페이지
def detail(request):
    cart = Cart(request)
    add_coupon = AddCouponForm()
    # 제품 수량 수정을 위해서 폼을 제품마다 하나씩 추가, 수량은 수정하는 대로 반영해야 하기 때문에 is_update를 True로 설정
    for product in cart:
        product['quantity_form'] = AddProductForm(initial={'quantity': product['quantity'], 'is_update': True})
    return render(request, 'cart/detail.html', {'cart': cart, 'add_coupon': add_coupon})
