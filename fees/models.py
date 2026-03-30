from django.db import models
from students.models import Student
from datetime import date
from dateutil.relativedelta import relativedelta

class Fee(models.Model):
    FEE_TYPE = [
        ('monthly', 'Monthly Fee'),
        ('grading', 'Grading Fee'),
        ('uniform', 'Uniform'),
        ('tshirt', 'T-Shirt'),
        ('tournament', 'Tournament'),
        ('other', 'Other'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(null=True, blank=True, help_text="For monthly fees (first day of month)")
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    receipt_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Auto-update status based on paid_date
        if self.paid_date:
            self.status = 'paid'
        else:
            # Check if overdue
            if self.due_date and self.due_date < date.today():
                self.status = 'overdue'
            else:
                self.status = 'pending'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.name} - {self.fee_type} - RM{self.amount}"