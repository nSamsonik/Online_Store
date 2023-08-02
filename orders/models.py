from django.db import models
from django.conf import settings
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon

"""
Одна модель понадобится для хранения детальной информации о заказе и вторая - для хранения приобретенных товаров,
включая их цену и количество.
Модель Order содержит несколько полей для хранения информации о клиенте и булево поле paid, которое по умолчанию
имеет значение False. Это поле используется для того, чтобы различать оплаченные и неоплаченные заказы. Здесь также
определен метод get_total_cost(), который получает общую стоимость товаров, приобретенных в этом заказе.
Модель OrderItem позволяет хранить товар, количество и цену, уплаченную за каждый товар. Здесь определен метод
get_cost(), который возвращает стоимость товара путем умножения цены товара на количество.
"""


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)
    """
    Поля coupon и discount позволяют сохранять опциональный купон заказа и процентную скидку, применяемую к купону.
    Скидка хранится в связанном объекте Coupon, но ее можно включить в модель Order, чтобы ее сохранять, если купон
    был видоизменен или удален. Параметр on_delete задается равным models. SET_NULL, чтобы при удалении купона поле 
    coupon устанавливалось ранвым Null, но скидка сохранялась.
    """
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)])


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal

    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    """
    Метод get_stripe_url() используется для возврата URL-адреса информационной панели Stripe для платежа,
    связанного с заказом. Если ID платежа не хранится в поле stripe_id объекта Order, то возвращается пустая строка.
    В противном случае возвращается URL-адрес платежа в информационной панели Stripe. Далее проверяется наличие
    подстроки _test_ в настроечном параметре STRIPE_SECRET_KEY, чтобы отличить производственную среду от тестовой. 
    """

    def get_stripe_url(self):
        if not self.stripe_id:
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            # Путь Stripe для тестовых платежей
            path = '/test/'
        else:
            # Путь Stripe для настоящих платежей
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
