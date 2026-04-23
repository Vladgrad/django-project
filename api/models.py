from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
       email = models.EmailField(unique=True)
       USERNAME_FIELD = 'email'
       REQUIRED_FIELDS = ['username']
       
       
class Coworking(models.Model):
       title = models.CharField(max_length=128, unique=True)
       city = models.CharField(max_length=64)
       address = models.CharField(max_length=256)
       
       class __str__(self):
              return self.title
       
       
class Desk(models.Model):
       desk_id = models.UUIDField(default=uuid.uuid4)
       coworking = models.ForeignKey(Coworking, on_delete=models.CASCADE)
       name = models.CharField(max_length=64)
       capacity = models.PositiveIntegerField()
       is_active = models.BooleanField(default=True)
       created_at = models.DateTimeField(auto_now_add=True)
       
       
class Booking(models.Model):
       booking_id = models.UUIDField(default=uuid.uuid4)
       desk = models.ForeignKey(Desk, on_delete=models.CASCADE)
       client = models.ForeignKey(User, on_delete=models.CASCADE)
       date = models.DateField()
       SLOT_CHICES = [
              ('morning', 'morning'), ('afternoon', 'afternoon'), ('full_day', 'full_day'), 
       ]
       slot = models.CharField(max_length=50, choices=SLOT_CHICES)
       STATUS_CHOICES = [
              ('active', 'active'), ('cancelled', 'cancelled') 
       ]
       status = models.CharField(max_length=50, choices=STATUS_CHOICES)
       created_at = models.DateTimeField(auto_now_add=True)
       