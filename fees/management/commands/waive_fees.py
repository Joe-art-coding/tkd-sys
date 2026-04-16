from django.core.management.base import BaseCommand
from fees.models import Fee
from datetime import date

class Command(BaseCommand):
    help = 'Waive fees for specific months'

    def add_arguments(self, parser):
        parser.add_argument('--month', type=int, help='Month number (1-12)')
        parser.add_argument('--year', type=int, help='Year (e.g., 2026)')
        parser.add_argument('--all', action='store_true', help='Waive all pending fees')

    def handle(self, *args, **options):
        if options['all']:
            fees = Fee.objects.filter(status='pending')
        else:
            month = options.get('month')
            year = options.get('year')
            
            if not month or not year:
                self.stdout.write(self.style.ERROR('Please specify --month and --year'))
                return
                
            fees = Fee.objects.filter(
                month__year=year,
                month__month=month,
                status='pending'
            )
        
        count = fees.update(status='waived', paid_date=None)
        self.stdout.write(self.style.SUCCESS(f'Successfully waived {count} fees'))