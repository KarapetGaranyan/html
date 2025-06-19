from django.db import models

# Create your models here.
from users.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.CharField(max_length=30)
    price = models.IntegerField()
