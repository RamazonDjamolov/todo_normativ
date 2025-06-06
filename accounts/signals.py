from accounts.models import User
from notifications.consumer import notify_user
from notifications.models import Notification
from task_manager.models import Task, Project
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import RefreshToken

# user = User.objects.get(username="user1")
# refresh = RefreshToken.for_user(user)

# access_token = str(refresh.access_token)


@receiver(post_save, sender=Project)
def assign_task(sender, created, instance, **kwargs):
    if created:
        if instance.owner:
            Notification.objects.create(
                to_user=instance.owner,
                title='Assigned to task',
                description=f'''Project {instance.name} has been assigned to you etc...'''
            )
            print(instance.owner.id, "my nimadur id ")
            notify_user(instance.owner.id,
                        f"Project {instance.name} has been assigned to you etc...")

    else:
        if instance.owner:
            Notification.objects.create(
                to_user=instance.owner,
                title='Task Updated',
                description=f'''
                title  {instance.name} has been updated
                '''
            )
            print(instance.owner.id, "my nimadur id ")

            notify_user(instance.owner.id,
                        f'''Project {instance.name} has been updated
                {instance.description}''')