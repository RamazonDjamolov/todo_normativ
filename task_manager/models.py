from django.db import models


# Create your models here.

class TaskStatus(models.TextChoices):
    TODO = 'todo', 'TODO'
    IN_PROGRESS = 'in_progress', 'IN_PROGRESS'
    DONE = 'done', 'Done'
    REJECTED = 'rejected', 'Rejected'


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='project_own',
                              null=True)  # egasi
    members = models.ManyToManyField('accounts.User', related_name='project_members', blank=True)  # azolari

    class Meta:
        db_table = 'projects'
        # unique_together = ('name','description')


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=255, choices=TaskStatus.choices, default=TaskStatus.TODO)
    assign_to = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='task_assign',
                                  null=True)  # kimga biriktirlganligi
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name='task_project')

    class Meta:
        db_table = 'task'
