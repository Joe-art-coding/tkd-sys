from django.db import models
from django.contrib.auth.models import User


class Club(models.Model):
    """Multi-club support - each club is a separate taekwondo organization"""
    name = models.CharField(max_length=200)
    subdomain = models.SlugField(unique=True, help_text="e.g., 'taiping', 'ipoh', 'klang'")
    logo = models.ImageField(upload_to='club_logos/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, default='#007bff', help_text="Brand color (hex code)")
    secondary_color = models.CharField(max_length=7, default='#6c757d', help_text="Secondary brand color")
    
    # Contact info
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    
    # Subscription
    is_active = models.BooleanField(default=True)
    subscription_tier = models.CharField(max_length=20, choices=[
        ('free', 'Free Trial'),
        ('basic', 'Basic ($10/mo)'),
        ('pro', 'Pro ($20/mo)'),
        ('enterprise', 'Enterprise ($35/mo)'),
    ], default='free')
    max_students = models.IntegerField(default=50, help_text="Maximum students allowed")
    subscription_expiry = models.DateField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.subdomain})"
    
    def save(self, *args, **kwargs):
        # Set max_students based on subscription tier
        tier_limits = {
            'free': 50,
            'basic': 100,
            'pro': 250,
            'enterprise': 9999,
        }
        self.max_students = tier_limits.get(self.subscription_tier, 50)
        super().save(*args, **kwargs)


class School(models.Model):
    """School/branch within a club (e.g., Taiping Club - Main Branch, Taiping Club - Kamunting Branch)"""
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='schools', null=True, blank=True)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [['club', 'name'], ['club', 'code']]  # Names unique per club, not globally
    
    def __str__(self):
        club_prefix = f"{self.club.name} - " if self.club else ""
        return f"{club_prefix}{self.name}"


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('club_admin', 'Club Admin'),
        ('coach', 'Coach'),
        ('assistant_coach', 'Assistant Coach'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='assistant_coach')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='users', null=True, blank=True, help_text="Which club this user belongs to")
    schools = models.ManyToManyField(School, blank=True, help_text="Schools this user can access")
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        club_name = f"({self.club.name})" if self.club else ""
        return f"{self.user.username} - {self.role} {club_name}"


class ClassSchedule(models.Model):
    """Class schedule for each school/club - parents can view this in parent portal"""
    DAY_CHOICES = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ]
    
    BELT_LEVEL_CHOICES = [
        ('all', 'All Belts'),
        ('white', 'White Belt'),
        ('yellow', 'Yellow Belt'),
        ('green', 'Green Belt'),
        ('blue', 'Blue Belt'),
        ('red', 'Red Belt'),
        ('black', 'Black Belt'),
        ('children', 'Children Class'),
        ('adult', 'Adult Class'),
    ]
    
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='schedules')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='schedules', null=True, blank=True, help_text="Leave blank for club-wide schedule")
    day = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    belt_level = models.CharField(max_length=50, choices=BELT_LEVEL_CHOICES, default='all')
    instructor = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True, help_text="Training venue/location")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['day', 'start_time']
    
    def __str__(self):
        return f"{self.get_day_display()}: {self.start_time} - {self.end_time} ({self.get_belt_level_display()}) - {self.instructor}"
    
    def get_day_display(self):
        """Return the day name (overrides the default to handle integer choices)"""
        days = dict(self.DAY_CHOICES)
        return days.get(self.day, 'Unknown')


class ContactInfo(models.Model):
    """Contact information (emergency contacts, admin contacts) - parents can view this"""
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='contacts')
    schools = models.ManyToManyField(School, related_name='contacts', blank=True, help_text="Select specific schools or leave blank for ALL schools")
    name = models.CharField(max_length=100, help_text="e.g., Coach Ali, Admin Office")
    role = models.CharField(max_length=50, help_text="e.g., Head Coach, Admin")
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    is_emergency = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        if self.schools.count() == 0:
            return f"{self.name} - {self.role} (All Schools)"
        elif self.schools.count() == 1:
            return f"{self.name} - {self.role} ({self.schools.first().name})"
        else:
            return f"{self.name} - {self.role} ({self.schools.count()} schools)"
    
    def get_schools_display(self):
        """Return comma-separated list of schools"""
        if self.schools.count() == 0:
            return "🏫 All Schools"
        return ", ".join([s.name for s in self.schools.all()])