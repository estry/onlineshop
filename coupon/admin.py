from django.contrib import admin
from .models import Coupon, CouponP


# Register your models here.

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'use_from', 'use_to', 'amount', 'active']
    # 관리자 페이지에 필터를 통해 원하는 목록 쉽게 접근 가능 우측면
    list_filter = ['active', 'use_from', 'use_to']
    search_fields = ['code']


admin.site.register(Coupon, CouponAdmin)
