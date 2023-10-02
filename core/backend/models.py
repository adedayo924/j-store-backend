from django.db import models


class User(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    fullname = models.CharField(max_length=100)
    password = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

class Otp(models.Model):
    phone = models.CharField(max_length=10)
    otp = models.IntegerField()
    validity = models.DateTimeField()
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.phone