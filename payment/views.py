from django.shortcuts import render, redirect, reverse, get_object_or_404
from decimal import Decimal
import stripe
from django.conf import settings
from orders.models import Order


# Создаем экземпляр Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        # Данные сеанса оформления платежа Stripe
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        # Добавляем товарные позиции заказа
        # в сеанс оформления платежа Stripe
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })
        # Купон Stripe
        """
        В коде ниже выполняется проверка на наличие у заказа связанного с ним купона. В этом случае SDK Stripe
        используется для создания купона Stripe с помощью stripe.Coupon.create(). При этом в купоне используются
        следующие атрибуты:
        1. name: применяется связанный с объектом order код (code) купона;
        2. percent_off: скидка (discount) объекта order;
        3. duration: используется значение once. Оно указывает Stripe, что это купон для разового платежа.
        """
        if order.coupon:
            stripe_coupon = stripe.Coupon.create(
                name=order.coupon.code,
                percent_off=order.discount,
                duration='once')
            session_data['discounts'] = [{
                'coupon': stripe_coupon.id
            }]
        # Создаем сеанс оформления платежа Stripe
        session = stripe.checkout.Session.create(**session_data)
        # Перенаправляем к платежной форме Stripe
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())


"""
Здесь мы импортируем модуль stripe и с помощью значения настроечного параметра STRIPE_SECRET_KEY задается ключ
API Stripe. Кроме того, с помощью значения настроечного параметра STRIPE_API_VERSION задается используемая версия API.
Представление payment_process выполняет следующую работу.
1. Текущий объект Order извлекается по сеансовому ключу order_id, который ранее был сохранен в сеансе представлением
order_create.
2. Объект Order извлекается из базы данных по данному order_id. Если при использовании функции сокращенного доступа
get_object_or_404() возникает исключение Http404 (страница не найдена), то заказ с заданным ID не найден.
3. Если представление загружается с помощью запроса методом GET, то прорисовывается и возвращается шаблон
payment/process.html. Этот шаблон будет содержать сводную информацию о заказе и кнопку для перехода к платежу, которая
будет генерировать запрос методом POST к представлению.
4. Если представление загружается с помощью запроса методом POST, то сеанс Stripe оформления платежа создается с
использование Strioe.checkout.Session.create() со следующими ниже параметрами:
    - mode: режим сеанса оформлени платежа. Здесь используется значение payment, указывающее на разовый платеж.
    - client_reference_id: уникальная ссылка для этого платежа. Она будет использоваться для согласования сеанса
    оформления платежа Stripe с заказом. Передавая ID заказа, платежи Stripe связываются с заказами в нашей системе, и
    мы можем получать уведомление от Stripe о платежах, чтобы помечать заказы как оплаченные.
    - success_url: URL-адрес, на который Stripe перенаправляет пользователя в случае успешного платежа. Здесь мы
    используем request.build_absolute_uri(), чтобы формировать абсолютный URI-идентификатор из пути URL-адреса.
    - cancel_url: URL-адрес, на который Stripe перенарвляет пользователя в случае отмены платежа.
    - line_items: это пуустой список. Далее он будет заполнен приобретаемыми товарными позициями заказа.
5. После создания сеанса оформления платежа возвращается HTTP-перенаправление с кодом состояния, равным 303, чтобы
перенаправить пользователя к Stripe. Код состояния 303 рекомендуется для перенаправления веб-приложений на новый URI-
идентификатор после выполнения HTTP-запроса методом POST.
=====Код с добавлением товарных позиций=====
По каждой товарной позиции используется следующая информация:
 - price_data: информация, связанная с ценой.
 - unit_amount: сумма в центах, которую необходимо получить при оплате. Это положительное целое число, показывающее,
 сколько взимать в наименьшей денежной единице без десятичных знаков.
 - currency: используемая валюта в трехбуквенном формате ISO.
 - product_data: информация, связанная с товаром.
 - name: название товара.
 - quantity: число приобретаемых единиц товара.
"""


"""
Представления для успешного и отмененного платежей
"""


def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
