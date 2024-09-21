from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER

class UserLibraryAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE, null=True)  # Temporarily set to nullable
    account_no = models.IntegerField(unique=True)
    phone_number = models.CharField(max_length=12)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, default=None)
    initial_deposit_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return str(self.account_no)


class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=20)

    def __str__(self):
        return str(self.user.email)

class Deposit(models.Model):
    account = models.ForeignKey(UserLibraryAccount, related_name='deposits', on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.amount)
