from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomeUser(AbstractUser):
    is_id = models.CharField(max_length=10, blank=True, null=True)
    user_id =models.IntegerField(blank=True, null=True)
    is_manager = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_login = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    
