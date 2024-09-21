from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from .constants import RATING
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug=models.SlugField(max_length=200,null=True,blank=True,unique=True)
    def __str__(self):
        return self.name
    
class BookModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    borro_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    category= models.ManyToManyField(Category,blank=True)
    image = models.ImageField(upload_to='media/book')


    def __str__(self):
        return self.name
    
    
class Review(models.Model):
    book = models.ForeignKey('BookModel', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    body = models.CharField(max_length=100000)
    rating = models.CharField(max_length=10, choices=RATING, null=True, blank=True)
    def __str__(self):
        return self.body
    

class Borrow(models.Model):
    book=models.ForeignKey(BookModel,on_delete=models.CASCADE,related_name='Borrow')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    borrow_date=models.DateTimeField(auto_now_add=True)
    return_date=models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return str(self.borrow_date)
    
    class Meta:
        ordering = ['borrow_date']