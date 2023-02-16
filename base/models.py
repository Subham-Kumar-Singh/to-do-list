from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    
    def get_absolute_url(self):
        return reverse('todo_detail', args=[str(self.id)])

    # we have used this meta class to arrange the order of t=our list according to our complete if it is true take
    # it to the bottom of the list    
    class Meta:
        permissions = [
            ('can_view_all_todos', 'Can view all todos'),
        ]
        