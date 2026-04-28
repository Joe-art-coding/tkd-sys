from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_groups(sender, **kwargs):
    """Auto-create Club Admin and Coach groups when migrations run"""
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from students.models import Student
    from fees.models import Fee
    from attendance.models import Attendance
    from schools.models import School, UserProfile
    from django.contrib.auth.models import User
    
    print("🔧 Checking required groups...")
    
    # Create Club Admin Group
    club_group, created = Group.objects.get_or_create(name='Club Admin')
    if created:
        models = [Student, Fee, Attendance, School, UserProfile]
        for model in models:
            ct = ContentType.objects.get_for_model(model)
            for perm in Permission.objects.filter(content_type=ct):
                club_group.permissions.add(perm)
        # Add user permissions
        user_ct = ContentType.objects.get_for_model(User)
        for perm in Permission.objects.filter(content_type=user_ct):
            club_group.permissions.add(perm)
        print(f"✅ Club Admin group created with {club_group.permissions.count()} permissions")
    else:
        print(f"✅ Club Admin group already exists")
    
    # Create Coach Group
    coach_group, created = Group.objects.get_or_create(name='Coach')
    if created:
        coach_perms = [
            'view_student', 'add_student', 'change_student',
            'view_fee', 'add_fee', 'change_fee',
            'view_attendance', 'add_attendance', 'change_attendance',
            'view_school'
        ]
        for codename in coach_perms:
            try:
                perm = Permission.objects.get(codename=codename)
                coach_group.permissions.add(perm)
            except Permission.DoesNotExist:
                pass
        print(f"✅ Coach group created with {coach_group.permissions.count()} permissions")
    else:
        print(f"✅ Coach group already exists")


class SchoolsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'schools'
    
    def ready(self):
        post_migrate.connect(create_groups, sender=self)