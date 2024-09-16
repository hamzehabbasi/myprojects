
from django.db import models
from django.utils import timezone
import uuid

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def api(self):
        return {
            'username':self.username,
            'email':self.email
        }

class License(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license_key = models.CharField(max_length=30, unique=True, default=uuid.uuid4().hex[:30])
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    def api(self):
        return {
            'user':self.user,
            'license_key':self.license_key,
            'expires_at':self.created_at
        }

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license = models.ForeignKey(License, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()


    def api(self):
        return {
            'name':self.name,
            'description':self.description
        }

