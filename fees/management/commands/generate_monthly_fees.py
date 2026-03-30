from django.core.management.base import BaseCommand
from students.models import Student
from fees.models import Fee
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class Command(BaseCommand):
    help = 'Generate monthly fees for all active students for current year'

    def handle(self, *args, **options):
        today = date.today()
        current_year = today.year
        
        # Generate for Jan to Dec of current year
        months = []
        for month in range(1, 13):
            first_day = date(current_year, month, 1)
            due_date = first_day + relativedelta(months=1)
            months.append((first_day, due_date))
        
        students = Student.objects.filter(is_active=True)
        created_count = 0
        skipped_count = 0
        
        for student in students:
            for first_day, due_date in months:
                # Check if fee already exists for this month
                existing_fee = Fee.objects.filter(
                    student=student,
                    fee_type='monthly',
                    month=first_day
                ).exists()
                
                if not existing_fee:
                    Fee.objects.create(
                        student=student,
                        fee_type='monthly',
                        amount=student.school.monthly_fee,
                        month=first_day,
                        due_date=due_date,
                        status='pending'
                    )
                    created_count += 1
                else:
                    skipped_count += 1
        
        self.stdout.write(f'Created {created_count} monthly fees for year {current_year}')
        self.stdout.write(f'Skipped {skipped_count} existing fees')