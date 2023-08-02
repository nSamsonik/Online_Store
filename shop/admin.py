from django.contrib import admin
from .models import Category, Product

# Register your models here.


@admin.register(Category)
# Декоратор для регистрации модели Category в административной панели
class CategoryAdmin(admin.ModelAdmin):
    # Списко полей, которые будут отображаться в панели
    list_display = ['name', 'slug']
    # Автоматическое заполнение поля slug на основе значения name
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    # Поля, которые можно редактировать без необходимости входить в каждую запись отдельно
    list_editable = ['price', 'available']
    # Автоматическое заполнение поля slug на основе значения name
    prepopulated_fields = {'slug': ('name',)}
