from django.db import models
from students.models import Student
from django.utils import timezone

class Attendance(models.Model):
    CLASS_TYPE = [
        ('beginner', 'Beginner Class'),
        ('intermediate', 'Intermediate Class'),
        ('advanced', 'Advanced Class'),
        ('sparring', 'Sparring Class'),
        ('poomsae', 'Poomsae Class'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField(default=timezone.now)
    check_in_time = models.TimeField(auto_now_add=True, blank=True, null=True)
    class_type = models.CharField(max_length=20, choices=CLASS_TYPE)
    instructor = models.CharField(max_length=100)
    is_present = models.BooleanField(default=True)  # ADD THIS FIELD
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date']
    
    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student.name} - {self.date} - {status}"