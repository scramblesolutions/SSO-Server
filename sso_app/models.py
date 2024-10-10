from django.contrib.auth.models import User
from django.db import models
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Vendor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    client_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Pseudonym(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pseudonyms')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    pseudonym = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        unique_together = ('user', 'vendor')

    def __str__(self):
        return f"{self.user.username} - {self.vendor.name}: {self.pseudonym}"