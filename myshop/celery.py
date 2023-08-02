import os
from celery import Celery


"""
1. Задается переменная DJANGO_SETTINGS_MODELU для встроенной в Celery программы командой строки
2. Посредством инструкции app = Celery('my shop') создается экземпляр приложения
3. Используя метод config_from_object(), загружается любая конкретно-прикладная конфигурация из настроек проекта.
Атрибут namespace задает префикс, который будет в нашем файле setting.py у настроек, связанных с Celery. Задав
именное пространство CELERY, все настройки Celery должны включать в свое имя префикс CELERY_ 
(например, CELERY_BROKER_URL)
4. Чтобы очередь заданий Celery автоматически обнаруживала асинхронные задания в приложениях. Celery будет искать
файл task.py в каждом каталоге приложений, добавленных в INSTALLED_APPS, чтобы загружать определенные в нем
асинхронные задания
"""


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
app = Celery('myshop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
