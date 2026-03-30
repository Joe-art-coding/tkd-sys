from django.db import models
from schools.models import School
from django.utils import timezone

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
    
    # School (each student belongs to one school)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    
    # Personal Info
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    ic_number = models.CharField(max_length=12, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
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
        # Check if this is a new student (no primary key yet)
        is_new = self.pk is None
        
        # First save the student
        super().save(*args, **kwargs)
        
        # Generate fees for current year if this is a new student
        if is_new:
            from fees.models import Fee
            from datetime import date
            from dateutil.relativedelta import relativedelta
            
            today = date.today()
            current_year = today.year
            
            # Generate Jan to Dec of current year
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
        return f"{self.name} - {self.school.name}"
        
        
from django.contrib.auth.models import User

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parents')
    phone = models.CharField(max_length=15, blank=True)
    relationship = models.CharField(max_length=50, default='Parent')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.student.name}"


from django.contrib.auth.models import User

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parents')
    phone = models.CharField(max_length=15, blank=True)
    relationship = models.CharField(max_length=50, default='Parent')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.student.name}"