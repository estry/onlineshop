from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    # db_index=True: 이름 열을 데이터베이스의 인덱스 열로 지정
    name = models.CharField(max_length=200, db_index=True)
    # SEO(Search Engine Optimization)을 위한 필드, 구글 등 검색엔진에서 상품이 잘 검색되도록 함, 추가적으로 연구 필요
    meta_description = models.TextField(blank=True)
    # 카테고리와 상품 모두에 설정되는데 상품명 등을 이용해서 URL을 만드는 방식
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_in_category', args=[self.slug])


class Product(models.Model):
    # 외래키 필드를 사용해 카테고리 모델과 관계를 만들었고 카테고리를 삭제해도 상품이 남아있어야 하기 때문에 on_delete를 SET_NULL로 설정
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    description = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    # 쇼핑몰의 필수적 요소, 가격같은 경우 기준 가격에 할인 가격을 추가하거나 다양한 지역의 세금을 자동으로 계산해 보여주는 방식도 있다.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    available_display = models.BooleanField('Display', default=True)
    available_order = models.BooleanField('Order', default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        # 멀티 칼럼 색인 기능, id와 slug 필드를 묶어서 색인이 가능하도록 하는 옵션
        index_together = [['id', 'slug']]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
