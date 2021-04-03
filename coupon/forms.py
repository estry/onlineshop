from django import forms
from .models import Coupon


class AddCouponForm(forms.Form):
    code = forms.ModelChoiceField(label='Select Coupon', queryset=Coupon.objects.all())
