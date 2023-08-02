from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)


"""
Эта форма будет использоваться для добавления товаров в корзнину
Класс CartAddProductForm содержит два поля:
1. quantity - позволяет пользователю выбирать количество от 1 до 20. Для конвертирования входных данных в целое число
используя поле TypedChoiceField вместе с coerce=int
2. override - позволяет указывать, должно ли количество быть прибавлено к любому существующему количеству в корзине
для этого товара (False) или же существующее количество должно быть переопределено данным количеством (True).
3. Виджет HiddenInput - поле не будет показываться пользователю
"""