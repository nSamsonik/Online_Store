from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm

"""
Это представление добавления товаров в корзину или обновления количества существующих товаров
В нем используется декоратор require_POST, чтобы разрешать запросы только методом POST
Указанное представление получает ID товара в качестве параметра. Затем извлекается объект класса Product
с заданным ID и выполняется валидация формы посредством CartAddProductForm
Если форма валидна, то товар в корзине либо добавляется, либо обновляется
Представление перенарпавляет на URL-адрес cart_detail, который будет отображать содержимое корзины
"""


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')

"""
Представление удаления товаров из корзины
Представление cart_remove получает ID товара в качестве параметра
В нем использзуется декоратор require_POST, чтобы разрешать запросы только методом POST
Объект товара извлекается с заданным ID, и товар удаляется из корзины
Затем пользователь перенаправляется на URL-адрес cart_detail
"""


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


"""
Представление отображения корзины и ее товаров
В целях обеспечения функции изменения количества товаров перед размещение заказа необходимо разрешить
пользователям изменять количество на странице детальной информации о корзине
По каждому товару в корзине создается объект класса CartAddProductForm, чтобы разрешить изменение количества
товара
Форма инициализируется текущим количеством товара, и поле override получает значение True, чтобы при передаче
формы на обработку в представление cart_add текущее количество заменялось новым
"""


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/detail.html', {'cart': cart,
                                                'coupon_apply_form': coupon_apply_form})

