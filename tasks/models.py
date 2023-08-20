from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

priority_choices = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
status_choices = (
        (True, 'Completed'),
        (False, 'Uncompleted'),
    )
class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    priority = models.CharField(max_length=10,choices=priority_choices,default='Low')
    description = models.TextField(max_length=100,null=True)
    due_date = models.DateField()
    status = models.BooleanField(choices=status_choices,default = 0,null=True)
    def __str__(self):
        return f"{self.user.username} Task : {self.title}"
    def get_absolute_url(self):
        return reverse("user_tasks", kwargs={"username": self.user.username})
