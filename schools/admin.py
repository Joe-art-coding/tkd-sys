# schools/admin.py - FULL VERSION (SAMA UNTUK LOCAL DAN SERVER)

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import School, UserProfile, Club, ClassSchedule, ContactInfo


# Unregister the default User admin if already registered
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'subdomain', 'subscription_tier', 'is_active', 'created_at']
    list_filter = ['subscription_tier', 'is_active']
    search_fields = ['name', 'subdomain']
    prepopulated_fields = {'subdomain': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'subdomain', 'logo', 'is_active')
        }),
        ('Branding', {
            'fields': ('primary_color', 'secondary_color')
        }),
        ('Contact', {
            'fields': ('email', 'phone', 'address', 'website')
        }),
        ('Subscription', {
            'fields': ('subscription_tier', 'subscription_expiry', 'max_students')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        tier_limits = {
            'free': 50,
            'basic': 100,
            'pro': 250,
            'enterprise': 9999,
        }
        obj.max_students = tier_limits.get(obj.subscription_tier, 50)
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
        
        if hasattr(request.user, 'profile') and request.user.profile.club:
            return qs.filter(id=request.user.profile.club.id)
        
        return qs.none()


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'club', 'monthly_fee', 'phone', 'is_active']
    list_editable = ['monthly_fee']
    list_filter = ['club', 'is_active']
    search_fields = ['name', 'code', 'club__name']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            current_club = getattr(request, 'club', None)
            if current_club:
                return qs.filter(club=current_club)
            return qs
        
        if hasattr(request.user, 'profile') and request.user.profile.club:
            return qs.filter(club=request.user.profile.club)
        
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        current_club = getattr(request, 'club', None)
        
        if db_field.name == 'club':
            if request.user.is_superuser and current_club:
                kwargs['queryset'] = Club.objects.filter(id=current_club.id)
            elif hasattr(request.user, 'profile') and request.user.profile.club:
                kwargs['queryset'] = Club.objects.filter(id=request.user.profile.club.id)
            else:
                kwargs['queryset'] = Club.objects.none()
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'club', 'get_schools', 'phone']
    list_filter = ['role', 'club']
    search_fields = ['user__username', 'user__email', 'phone']
    filter_horizontal = ['schools']
    raw_id_fields = ['user']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            current_club = getattr(request, 'club', None)
            if current_club:
                return qs.filter(club=current_club)
            return qs
        
        if hasattr(request.user, 'profile') and request.user.profile.club:
            return qs.filter(club=request.user.profile.club)
        
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        current_club = getattr(request, 'club', None)
        
        if db_field.name == 'club':
            if request.user.is_superuser and current_club:
                kwargs['queryset'] = Club.objects.filter(id=current_club.id)
            elif hasattr(request.user, 'profile') and request.user.profile.club:
                kwargs['queryset'] = Club.objects.filter(id=request.user.profile.club.id)
            else:
                kwargs['queryset'] = Club.objects.none()
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'schools':
            club_id = None
            
            if hasattr(request.user, 'profile') and request.user.profile.club:
                club_id = request.user.profile.club.id
            else:
                club_id = request.POST.get('club') or request.GET.get('club')
            
            if club_id:
                kwargs['queryset'] = School.objects.filter(club_id=club_id, is_active=True)
            elif hasattr(request, 'club') and request.club:
                kwargs['queryset'] = School.objects.filter(club=request.club, is_active=True)
            else:
                kwargs['queryset'] = School.objects.none()
        
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        current_club = getattr(request, 'club', None)
        
        if current_club:
            form.base_fields['schools'].queryset = School.objects.filter(club=current_club, is_active=True)
        elif hasattr(request.user, 'profile') and request.user.profile.club:
            form.base_fields['schools'].queryset = School.objects.filter(
                club=request.user.profile.club, 
                is_active=True
            )
        
        return form
    
    def get_schools(self, obj):
        return ", ".join([s.name for s in obj.schools.all()])
    get_schools.short_description = 'Schools'
    
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            if hasattr(request.user, 'profile') and request.user.profile.club:
                obj.club = request.user.profile.club
        super().save_model(request, obj, form, change)


# ==================== CUSTOM USER ADMIN ====================

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    max_num = 1
    min_num = 1


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    inlines = [UserProfileInline]
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        current_club = getattr(request, 'club', None)
        
        if current_club:
            return qs.filter(profile__club=current_club)
        return qs
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        if not hasattr(obj, 'profile'):
            current_club = getattr(request, 'club', None)
            UserProfile.objects.create(
                user=obj,
                club=current_club,
                role='coach',
                phone=''
            )


# ==================== CLASS SCHEDULE ADMIN (AUTO-DETECT LOCATION) ====================

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ['get_day_display', 'start_time', 'end_time', 'school', 'get_club', 'belt_level', 'instructor', 'is_active']
    list_filter = ['club', 'school', 'day', 'belt_level', 'is_active']
    search_fields = ['school__name', 'instructor', 'belt_level']
    list_editable = ['is_active']
    
    def get_fieldsets(self, request, obj=None):
        """Auto-detect location field"""
        fieldsets = [
            ('Club & School', {
                'fields': ('club', 'school')
            }),
            ('Schedule Details', {
                'fields': ('day', 'start_time', 'end_time', 'belt_level')
            }),
            ('Instructor', {
                'fields': ('instructor',)
            }),
            ('Status', {
                'fields': ('is_active',)
            }),
        ]
        
        # Auto-detect if location field exists
        try:
            ClassSchedule._meta.get_field('location')
            fieldsets.insert(2, ('Location', {
                'fields': ('location',)
            }))
        except:
            pass  # No location field, skip
        
        return fieldsets
    
    def get_club(self, obj):
        return obj.club.name if obj.club else '-'
    get_club.short_description = 'Club'
    get_club.admin_order_field = 'club__name'
    
    def get_day_display(self, obj):
        days = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
        return days.get(obj.day, '-')
    get_day_display.short_description = 'Day'
    get_day_display.admin_order_field = 'day'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            current_club = getattr(request, 'club', None)
            if current_club:
                return qs.filter(club=current_club)
            return qs
        
        if hasattr(request.user, 'profile') and request.user.profile.club:
            return qs.filter(club=request.user.profile.club)
        
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        current_club = getattr(request, 'club', None)
        
        if not request.user.is_superuser and hasattr(request.user, 'profile') and request.user.profile.club:
            user_club = request.user.profile.club
            
            if db_field.name == 'club':
                kwargs['queryset'] = Club.objects.filter(id=user_club.id)
            
            if db_field.name == 'school':
                kwargs['queryset'] = School.objects.filter(club=user_club, is_active=True)
        
        elif request.user.is_superuser and current_club:
            if db_field.name == 'club':
                kwargs['queryset'] = Club.objects.filter(id=current_club.id)
            
            if db_field.name == 'school':
                kwargs['queryset'] = School.objects.filter(club=current_club, is_active=True)
        
        else:
            if db_field.name in ['club', 'school']:
                kwargs['queryset'] = Club.objects.none()
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and hasattr(request.user, 'profile') and request.user.profile.club:
            obj.club = request.user.profile.club
        
        elif request.user.is_superuser:
            current_club = getattr(request, 'club', None)
            if current_club and not obj.club:
                obj.club = current_club
        
        super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'profile') and request.user.profile.role == 'club_admin':
            return True
        return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'profile') and request.user.profile.role == 'club_admin':
            if obj and obj.club == request.user.profile.club:
                return True
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'profile') and request.user.profile.role == 'club_admin':
            if obj and obj.club == request.user.profile.club:
                return True
            return True
        return False
    
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'profile') and request.user.profile.role == 'club_admin':
            return True
        return False


# ==================== CONTACT INFO ADMIN ====================

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'get_schools_display', 'phone', 'email', 'is_emergency', 'order']
    list_filter = ['club', 'is_emergency']
    search_fields = ['name', 'role', 'phone']
    list_editable = ['order', 'is_emergency']
    filter_horizontal = ['schools']
    
    fieldsets = (
        ('Club', {
            'fields': ('club',)
        }),
        ('Schools (Leave blank for ALL schools)', {
            'fields': ('schools',)
        }),
        ('Contact Details', {
            'fields': ('name', 'role', 'phone', 'email')
        }),
        ('Settings', {
            'fields': ('is_emergency', 'order')
        }),
    )
    
    def get_schools_display(self, obj):
        return obj.get_schools_display()
    get_schools_display.short_description = 'Schools'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            current_club = getattr(request, 'club', None)
            if current_club:
                return qs.filter(club=current_club)
            return qs
        
        if hasattr(request.user, 'profile') and request.user.profile.club:
            return qs.filter(club=request.user.profile.club)
        
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        current_club = getattr(request, 'club', None)
        
        if db_field.name == 'club':
            if not request.user.is_superuser and hasattr(request.user, 'profile') and request.user.profile.club:
                kwargs['queryset'] = Club.objects.filter(id=request.user.profile.club.id)
            elif request.user.is_superuser:
                if current_club:
                    kwargs['queryset'] = Club.objects.filter(id=current_club.id)
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Filter schools by club"""
        if db_field.name == 'schools':
            current_club = getattr(request, 'club', None)
            
            if not request.user.is_superuser and hasattr(request.user, 'profile') and request.user.profile.club:
                kwargs['queryset'] = School.objects.filter(club=request.user.profile.club, is_active=True)
            elif request.user.is_superuser and current_club:
                kwargs['queryset'] = School.objects.filter(club=current_club, is_active=True)
            else:
                kwargs['queryset'] = School.objects.none()
        
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and hasattr(request.user, 'profile') and request.user.profile.club:
            obj.club = request.user.profile.club
        super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'profile') and request.user.profile.role == 'club_admin':
            return True
        return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'profile') and request.user.profile.role == 'club_admin':
            if obj and obj.club == request.user.profile.club:
                return True
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'profile') and request.user.profile.role == 'club_admin':
            if obj and obj.club == request.user.profile.club:
                return True
            return True
        return False
    
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'profile') and request.user.profile.role == 'club_admin':
            return True
        return False