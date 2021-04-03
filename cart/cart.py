from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupon.models import Coupon


class Cart(object):
    def __init__(self, request):
        # requset.session에 데이터를 저장하고 꺼내오는 방식
        self.session = request.session
        # 세션에 값을 저장하려면 키 값을 설정해야 한다. CART_ID라는 변수를 만들고 설정된 값을 사용
        cart = self.session.get(settings.CART_ID)
        if not cart:
            cart = self.session[settings.CART_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)
        # print(self.cart.values())
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']

            yield item

    def add(self, product, quantity=1, is_update=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        # 장바구니 페이지에서 수량 추가
        if is_update:
            self.cart[product_id]['quantity'] = quantity
        # 제품 상세 페이지에서 수량 추가
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    # 상품을 담을 때
    def save(self):
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True

    # 상품을 삭제할 때
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del (self.cart[product_id])
            self.save()

    # 주문을 완료했을 때, 장바구니를 비울 때
    def clear(self):
        self.session[settings.CART_ID] = {}
        self.session['coupon_id'] = None
        self.session.modified = True

    # 총 가격 계산
    def get_product_total(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    # @property 다음 메소드를 getter로 취급
    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount_total(self):
        if self.coupon:
            if self.get_product_total() >= self.coupon.amount:
                return self.coupon.amount
        return Decimal(0)

    def get_total_price(self):
        return self.get_product_total() - self.get_discount_total()