from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('coach', 'Coach'),
        ('assistant_coach', 'Assistant Coach'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='assistant_coach')
    schools = models.ManyToManyField(School, blank=True, help_text="Schools this user can access")
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"