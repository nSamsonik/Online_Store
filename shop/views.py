from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm

# Create your views here.


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    # Получение всех объектов модели Category из базы данных
    products = Product.objects.filter(available=True)
    # Получение всех объектов модели Product (Доступных)
    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        # Пытаемся найти объект модели Category. Если объект не найден - вызывается исключение 404
        products = products.filter(category=category)
        # Если категория найдена - фильтруем продукты по выбранной категории
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
