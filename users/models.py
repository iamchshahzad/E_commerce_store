from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)


class CustomerLoginActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_login_activities")
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    logged_in_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-logged_in_at"]

    def __str__(self):
        return f"{self.user.username} @ {self.logged_in_at}"
