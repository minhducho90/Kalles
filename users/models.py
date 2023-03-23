from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return f'{self.user.username} có số điện thoại là {self.phone_number}'

    class Meta:
        db_table = u'customers'
