from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@shared_task
def payment_completed(order_id):
    """
    Задание по отправке уведомления по электронной почте
    при успешной оплате заказа
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    subject = f'My Shop - Invoice no. {order_id}'
    message = 'Please, find attached the invoice for your revent purchase.'
    email = EmailMessage(subject,
                         message,
                         'admin@myshop.com',
                         [order.email])
    # Генерация PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # Прикрепление PDF-файла
    email.attach(f'order_{order_id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    # Отправляем электронное письмо
    email.send()
    """
    При успешном прохождении платежа мы будем отправлять клиенту автоматическое электронное письмо со сгенерированным
    счетом-фактурой в формате PDF.
    С помощью декоратора @shared_task определяется задание payment_completed. В этом задании используется
    предоставляемый веб-фреймворком Django класс EmailMessage, служащий для создания объекта email. Затем шаблон
    прорисовывается в переменную html и из прорисованного шаблона генерируется PDF-файл, который выводится в экземпляр
    aBytesIO. Последний представляет собой резидентный байтовый буфер. Затем с помощью метода attach()
    сгенерированный PDF-файл прикрепляется к объекту EmailMessage вместе с содержимым выходного буфера и по итогу
    письмо отправляется.
    """