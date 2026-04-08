from django.db import models
from schools.models import School, Club  # Import Club from schools app
from django.utils import timezone
from django.contrib.auth.models import User


# REMOVED: Duplicate Club class (now imported from schools.models)


class Student(models.Model):
    BELT_CHOICES = [
        ('white', 'White Belt'),
        ('yellow_1', 'Yellow Belt 1'),
        ('yellow_2', 'Yellow Belt 2'),
        ('green_1', 'Green Belt 1'),
        ('green_2', 'Green Belt 2'),
        ('blue_1', 'Blue Belt 1'),
        ('blue_2', 'Blue Belt 2'),
        ('red_1', 'Red Belt 1'),
        ('red_2', 'Red Belt 2'),
        ('black_1', 'Black Belt 1st DAN'),
        ('black_2', 'Black Belt 2nd DAN'),
        ('black_3', 'Black Belt 3rd DAN'),
        ('black_4', 'Black Belt 4th DAN'),
        ('black_5', 'Black Belt 5th DAN'),
        ('black_6', 'Black Belt 6th DAN'),
        ('black_7', 'Black Belt 7th DAN'),
        ('black_8', 'Black Belt 8th DAN'),
        ('black_9', 'Black Belt 9th DAN'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    # Multi-club support (now using Club from schools app)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    
    # School (each student belongs to one school within their club)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    
    # Personal Info
    student_id = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=100)
    ic_number = models.CharField(max_length=12, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    # Parent Info
    parent_ic = models.CharField(max_length=12, blank=True, help_text="Parent IC number for auto-create parent account")
    
    # Taekwondo Info
    belt_rank = models.CharField(max_length=20, choices=BELT_CHOICES, default='white')
    join_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    # Contact Info
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField()
    emergency_contact = models.CharField(max_length=15)
    emergency_name = models.CharField(max_length=100)
    
    # Medical Info
    medical_conditions = models.TextField(blank=True)
    blood_type = models.CharField(max_length=3, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Auto-generate student_id with club prefix
        if not self.student_id:
            import datetime
            year = datetime.datetime.now().strftime('%Y')
            # Use club subdomain prefix instead of hardcoded 'TTC'
            prefix = self.club.subdomain.upper() if self.club else 'CLUB'
            last_student = Student.objects.filter(
                student_id__startswith=f'{prefix}{year}'
            ).order_by('-student_id').first()
            if last_student:
                last_num = int(last_student.student_id[-3:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.student_id = f'{prefix}{year}{new_num:03d}'
        
        # Check if this is a new student (no primary key yet)
        is_new = self.pk is None
        
        # First save the student
        super().save(*args, **kwargs)
        
        # Auto-create parent if parent_ic is provided and this is a new student
        if is_new and self.parent_ic:
            from .models import Parent
            
            # Create or get user for parent (include club in username for uniqueness across clubs)
            username = f"parent_{self.club.subdomain}_{self.parent_ic}" if self.club else f"parent_{self.parent_ic}"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': f"{username}@example.com"}
            )
            if created:
                user.set_password('user123456')
                user.save()
            
            # Create parent record
            parent, created = Parent.objects.get_or_create(
                user=user,
                student=self
            )
        
        # Generate fees for current year if this is a new student
        if is_new:
            from fees.models import Fee
            from datetime import date
            from dateutil.relativedelta import relativedelta
            
            today = date.today()
            current_year = today.year
            
            for month in range(1, 13):
                first_day = date(current_year, month, 1)
                due_date = first_day + relativedelta(months=1)
                
                Fee.objects.create(
                    student=self,
                    fee_type='monthly',
                    amount=self.school.monthly_fee,
                    month=first_day,
                    due_date=due_date,
                    status='pending'
                )
    
    def __str__(self):
        club_name = self.club.name if self.club else 'No Club'
        return f"{self.name} - {club_name} - {self.school.name} - {self.student_id}"


class Parent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_profiles')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parents')
    phone = models.CharField(max_length=15, blank=True)
    relationship = models.CharField(max_length=50, default='Parent')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'student')
    
    def __str__(self):
        return f"{self.user.username} - {self.student.name}"
        
