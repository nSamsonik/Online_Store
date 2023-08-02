from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon


class Cart:
    def __init__(self, request):
        """
        Инициализируем корзину
        :param request:
        """
        self.session = request.session
        # Сохранение текущего сеанса
        cart = self.session.get(settings.CART_SESSION_ID)
        # Попытка получения корзины из текущего сеанса
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # Сохранить текущий применный купон
        self.coupon_id = self.session.get('coupon_id')
        # Если корзины нет, то с помощью словаря в сеансе создается пустая корзина
    """
    Необходимо сформировать словарь cart с идентификаторами товаров в качестве ключей и словарем,
    который будет содержать количество и цену, по каждому ключу товара. Поступая таким образом, можно 
    гарантировать, что товар не будет добавляться в корзину более одного раза. Благодаря этому также
    упрощается извлечение товаров из корзины
    """
    def add(self, product, quantity=1, override_quantity=False):
        """
        Параметр override_quantity - булево значение, указывающее, нужно ли заменить количество переданным количеством
        (True) либо прибавить новое количество к существующему количеству (False)
        Добавляем товар в корзину или обновляем его количество
        :param product:
        :param quantity:
        :param override_quantity:
        :return:
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Помечаем сеанс как "измененный"
        чтобы обеспечить его сохранение
        :return:
        """
        self.session.modified = True

    """
    Метод удаления товаров из корзины
    """
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    """
    Прокрутка товарных позиций корзины в цикле и получение товаров из базы данных
    """
    def __iter__(self):
        product_ids = self.cart.keys()
        # получаем объекты product и добавляем их в корзину
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    """
    Мы извлекаем присутствующие в корзине объекты класса Product, чтобы включить их в товарные позиции корзины. 
    Текущая корзина копируется в переменную cart, и в нее добавляются объекты класса Product. 
    Товары корзины прокручиваются в цикле, конвертируя цену каждого товара обратно в десятичное число 
    фиксированной точности и добавляя в каждый товар атрибут total_price. 
    """

    """
    Метод, который будет возвращать общее число товаров в корзине
    """
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    """
    Метод для расчета общей стоимости товаров в корзине
    """
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    """
    Метод для очистки сеанса корзины
    """
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
