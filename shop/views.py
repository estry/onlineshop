from django.shortcuts import render, get_object_or_404
from .models import *


# Create your views here.
# 카테고리 페이지, URL로부터 category_slug를  찾아서 현재 어느 카테고리를 보여주는 것인지 판단,
# 선택한 카테고리가 없을 경우 전체 상품 목록 노출
def product_in_category(request, category_slug=None):
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available_display=True)

    # products에서 filter를 여러번 실행하는데 실제로 데이터베이스에 질의는 딱 한번만 전달,
    # 장고의 QuerySet은 지연평가 방식을 사용하기 때문에 데이터를 질의하는 시점까지는 몇 번의 필터를 걸더라도 부하가 걸리지 않음
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    print(products.query)
    return render(request, 'shop/list.html',
                  {'current_category': current_category, 'categories': categories, 'products': products})


# URL로부터 슬러그 값을 읽어와서 해당 제품을 찾고 그 제품을 노출
def product_detail(request, id, product_slug=None):
    product = get_object_or_404(Product, id=id, slug=product_slug)
    return render(request, 'shop/detail.html', {'product': product})
