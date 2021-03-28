# 카트 기능은 사용자에게 입력을 받는 것이기 때문에 폼을 만들어 뷰에서 활용하는 방식으로 구현
from django import forms


class AddProductForm(forms.Form):
    # 제품 수량
    quantity = forms.IntegerField()
    # 상세 페이지에서 추가할 때와 장바구니에서 수량을 바꿀 때 동작하는 달리하기 위한 변수
    # 제품 상세 페이지에서는 수량을 선택하고 추가할 때마다 장바구니 수량에 더해지는 방식을 취할 것 = False
    # 장바구니 페이지에서 수량을 변경하는 것은 그 값 그대로 현재 수량에 반영해야하기 때문에 = True
    is_update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
