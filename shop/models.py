from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):  # Класс Category является моделью данных Django
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,  # Хранение URL-строк
                            unique=True)

    class Meta:
        ordering = ['name']  # Сортировка по полю name в алфавитном порядке
        indexes = [
            models.Index(fields=['name']),  # Определение индекса для поисковых запросов по полю name
        ]
        verbose_name = 'category'  # Читаемые имена в ед. и множ. числе
        verbose_name_plural = 'categories'

    def __str__(self):  # Объект Category будет представлен в виде строки
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,  # Связь между моделью Product и Category.
                                 related_name='products',  # Обратное имя для связи. Доступ к прод. через объекты кат.
                                 on_delete=models.CASCADE)  # Связанные объекты будут удалены, если об. кат. будут уд.
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d',  # Загрузка и хранение изображений. Путь загрузки изобр.
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)  # Количество знаком после запятой
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)  # Дата и время в бд.
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),  # Индекс в обратном порядке. От самой позд. даты до ранней.
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
