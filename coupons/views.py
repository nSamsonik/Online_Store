from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm
"""
Представление coupon_apply выполняет валидацию купона и сохраняет его в сеансе пользователя. Здесь декоратор 
require_POST применяется для того, чтобы ограничивать представление запросами POST. В данном представлении выполняется
следующая работа:
1. Используя отправленные данные, создается экземпляр формы CouponApplyForm и проверяется валидность формы.
2. Если форма валидна, то из словаря clean_data формы берется введенный пользователем код (code) и делается попытка
получить объект Coupon с заданным кодом. При этом поиск в поле осуществляется с использованием оператора iexact, чтобы
отыскать нечувствительное к регитру точное совпадние. Купон должен быть активен в данный момент (active=True) и
действителен на текущую дату/время. С целью получения текущей даты/времени с учетом часового пояса используется
функция Django timezone.now(), и полученный результат сравнивается с полями valid_from и valid_to, просматривая поле
с применением операторов соответственно lte (меньше или равно) и gte(больше или равно).
3. ID купона сохраняется в сеасе пользователя.
4. Пользователь перенаправляется на URL-адрес cart_detail, чтобы отобразить корзину с прмиененным купоном.
"""
@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')
