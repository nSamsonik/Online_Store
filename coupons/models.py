from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


"""
Это модель для хранения купонов. Модель содержит:
1. code: код, который пользователи должны ввести, чтобы пременить купон к своей покупке;
2. valid_from: значение даты/времени, указывающее, когда купон становится действительным;
3. valid_to: значение даты/времени, указывающее, когда купон становится недействительным;
4. discount: применяемый уровень скидки (это процент, поэтому принимает значение в интервале от 0 до 100). Для этого
поля мы используемы валидаторы, чтобы ограничить минимальное и максимальное допустимые значения;
5. active: булево значение, указывающее, является ли купон активным/неактивным.
"""


class Coupon(models.Model):
    code = models.CharField(max_length=50,
                            unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)],
        help_text='Percentage value (0 to 100)')
    active = models.BooleanField()

    def __str__(self):
        return self.code
