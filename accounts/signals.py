from django.dispatch import receiver
from django.db.models.signals import post_save

from accounts.models import User


@receiver(post_save, sender=User)
def Notifity_user_created(sender, instance, created, **kwargs):
    if created:
        print("sugnal ishladi")
        notify_users = (f"siz royhatdan muofiqiyatli otdingiz o'tdingiz  {instance.email}")
