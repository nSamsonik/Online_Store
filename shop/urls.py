from django.urls import path
from . import views


app_name = 'shop'
# Задание имени приложения позволяет нам использовать его в шаблонах при указании URL-адресов


urlpatterns = [
    # Список url-паттернов, который будет содержать все маршруты URL для приложения
    path('', views.product_list, name='product_list'),
    # Стартовая страница связывается с функцией product_list. Имя задается чтобы мы могли сослаться на него в шаблоне
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    # Передаем аргумент slug в функцию product_list. Динамический параметр
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
    # Два динамических параметра для функции product_detail
]
