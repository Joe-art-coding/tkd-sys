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
        ('waive', 'Waived'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(null=True, blank=True, help_text="For monthly fees (first day of month)")
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    receipt_number = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def generate_receipt_number(self):
        """Generate a unique permanent receipt number"""
        return f"REC-{self.id:06d}"
    
    def save(self, *args, **kwargs):
        # Don't override if status is 'waive'
        if self.status != 'waive':
            # Update status based on paid_date
            if self.paid_date:
                self.status = 'paid'
            else:
                # Check if overdue
                if self.due_date and self.due_date < date.today():
                    self.status = 'overdue'
                else:
                    self.status = 'pending'
        
        # Save first to get ID if it's a new record
        is_new = self.id is None
        super().save(*args, **kwargs)
        
        # Generate receipt number for paid fees without one
        if self.status == 'paid' and not self.receipt_number:
            self.receipt_number = self.generate_receipt_number()
            # Save again with receipt number (use update to avoid recursion)
            self.__class__.objects.filter(id=self.id).update(receipt_number=self.receipt_number)
    
    def __str__(self):
        return f"{self.student.name} - {self.fee_type} - RM{self.amount}"