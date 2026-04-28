import sys
import os

# Set Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taekwondo_system.settings')

import django
django.setup()

from django.db import models
from schools.models import Club, School, UserProfile
from students.models import Student, Parent
from fees.models import Fee
from django.contrib.auth.models import User
from datetime import date

# Redirect output to file
with open('raintown_report.txt', 'w', encoding='utf-8') as f:
    sys.stdout = f

    # Get RainTown club
    raintown = Club.objects.get(subdomain='rtc')

    print("=" * 60)
    print(f"DATA RAINTOWN TAEKWONDO CLUB")
    print(f"Tarikh: {date.today()}")
    print("=" * 60)

    # Club Info
    print(f"\n🏢 CLUB:")
    print(f"   Nama: {raintown.name}")
    print(f"   Subdomain: {raintown.subdomain}")
    print(f"   Warna: {raintown.primary_color}")

    # Schools
    print(f"\n🏫 SCHOOLS ({raintown.schools.count()}):")
    for school in raintown.schools.all():
        print(f"   - {school.name}")
        print(f"     Code: {school.code}")
        print(f"     Monthly Fee: RM {school.monthly_fee}")
        print(f"     Phone: {school.phone}")

    # Club Admin
    print(f"\n👑 CLUB ADMIN:")
    for admin in User.objects.filter(profile__club=raintown, profile__role='club_admin'):
        print(f"   - {admin.username}")
        print(f"     Email: {admin.email}")
        print(f"     Phone: {admin.profile.phone}")

    # Coaches
    print(f"\n👨‍🏫 COACHES ({User.objects.filter(profile__club=raintown, profile__role='coach').count()}):")
    for coach in User.objects.filter(profile__club=raintown, profile__role='coach'):
        schools_list = ", ".join([s.name for s in coach.profile.schools.all()])
        print(f"   - {coach.username}")
        print(f"     Nama: {coach.first_name} {coach.last_name}")
        print(f"     Phone: {coach.profile.phone}")
        print(f"     Schools: {schools_list}")

    # Students
    print(f"\n🎓 STUDENTS ({Student.objects.filter(club=raintown).count()}):")
    for student in Student.objects.filter(club=raintown):
        print(f"   - {student.name}")
        print(f"     ID: {student.student_id}")
        print(f"     IC: {student.ic_number}")
        print(f"     Belt: {student.get_belt_rank_display()}")
        print(f"     School: {student.school.name}")
        print(f"     Phone: {student.phone}")

    # Parents
    print(f"\n👨‍👩‍👧 PARENTS ({Parent.objects.filter(student__club=raintown).count()}):")
    for parent in Parent.objects.filter(student__club=raintown):
        print(f"   - {parent.user.username}")
        print(f"     Student: {parent.student.name}")
        print(f"     Password: parent123456")

    # Fees Summary
    print(f"\n💰 FEES SUMMARY:")
    total_fees = Fee.objects.filter(student__club=raintown).count()
    total_paid = Fee.objects.filter(student__club=raintown, status='paid').count()
    total_pending = Fee.objects.filter(student__club=raintown, status='pending').count()
    total_overdue = Fee.objects.filter(student__club=raintown, status='overdue').count()
    total_amount = Fee.objects.filter(student__club=raintown).aggregate(total=models.Sum('amount'))['total'] or 0

    print(f"   Total Fees: {total_fees}")
    print(f"   Paid: {total_paid}")
    print(f"   Pending: {total_pending}")
    print(f"   Overdue: {total_overdue}")
    print(f"   Total Amount: RM {total_amount:,.2f}")

    # Fees by month
    print(f"\n📅 FEES BY MONTH 2026:")
    for month in range(1, 13):
        month_fees = Fee.objects.filter(
            student__club=raintown,
            month=date(2026, month, 1)
        )
        paid = month_fees.filter(status='paid').count()
        pending = month_fees.filter(status='pending').count()
        total = month_fees.count()
        amount = month_fees.aggregate(total=models.Sum('amount'))['total'] or 0
        if total > 0:
            print(f"   Month {month:02d}: {paid} paid, {pending} pending | Amount: RM {amount:,.2f}")

    print("\n" + "=" * 60)
    print("✅ REPORT COMPLETE")
    print("=" * 60)

    # Restore stdout
    sys.stdout = sys.__stdout__

print("✅ Report saved to: raintown_report.txt")