from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_mail_task():
    send_mail(
        subject='Test subject',
        message='run task celery beat',
        from_email='djamolovramazon90@gmail.com',
        recipient_list=['djamolovramazon90@gmail.com'],
        fail_silently=False,
    )


@shared_task
def add(a, b):
    return a + b


@shared_task
def print_hello():
    print("Salom, har 5 soniyada ishga tushdim!")
