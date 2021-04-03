from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    use_from = models.DateTimeField()
    use_to = models.DateTimeField()
    # 할인 가능 금액을 validators 인수로 MaxValueValidator, MinValueValidator 를 이용해 범위 제약 조건을 추가
    amount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)])
    active = models.BooleanField()

    def __str__(self):
        return self.code


class CouponP(models.Model):
    code = models.CharField(max_length=50, unique=True)
    use_from = models.DateTimeField()
    use_to = models.DateTimeField()
    percentile = models.IntegerField(validators=[MaxValueValidator(0), MaxValueValidator(30)])
    active = models.BooleanField()

    def __str__(self):
        return self.code
