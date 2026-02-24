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


class AdminActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_activities")
    action = models.CharField(max_length=64)
    object_repr = models.CharField(max_length=255)
    change_message = models.TextField(blank=True)
    app_label = models.CharField(max_length=64, blank=True)
    model = models.CharField(max_length=64, blank=True)
    action_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-action_time"]

    def __str__(self):
        return f"{self.user.username}: {self.action} {self.object_repr}"
