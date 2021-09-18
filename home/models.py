from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    pass

class Notes(models.Model):
    content = models.CharField(max_length=240)
    color = models.CharField(max_length=10, blank=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="noteUser", null=True, default="")


