from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """
    Задание по отправке уведомления по электронной почте
    при успешном создании заказа.
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])
    return mail_sent


"""
Функция order_created была определена с помощью декоратора @shared_task. Как видно, задание Celery - это просто функция
Python, декорированная функцией-декоратором @shared_task. Функция задания order_created получает параметр order_id. При
исполнении задания рекомендуется всегда передавать идентификаторы функциям задания и извлекать объекты из базы данных.
Тем самым избегается доступ к устаревшей информации, поскольку данные в базе данных могли измениться за то время, пока
задаение стояло в очереди. Для отправки уведомления по электронной почте разместившему заказ пользователю была
использована предоставляемая фрейморком Django функция send_mail().
"""