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
        """Auto-set max_students based on subscription tier"""
        tier_limits = {
            'free': 50,
            'basic': 100,
            'pro': 250,
            'enterprise': 9999,
        }
        obj.max_students = tier_limits.get(obj.subscription_tier, 50)
        super().save_model(request, obj, form, change)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'club', 'monthly_fee', 'phone', 'is_active']
    list_editable = ['monthly_fee']
    list_filter = ['club', 'is_active']
    search_fields = ['name', 'code', 'club__name']
    
    def get_queryset(self, request):
        """Filter schools by current club for Super Admin too"""
        qs = super().get_queryset(request)
        
        # For Super Admin, filter by current club from session/middleware
        if request.user.is_superuser:
            current_club = getattr(request, 'club', None)
            if current_club:
                return qs.filter(club=current_club)
            return qs
        
        # For non-superusers, only show schools from their club
        if hasattr(request.user, 'profile') and request.user.profile.club:
            return qs.filter(club=request.user.profile.club)
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit club choices based on current club for Super Admin"""
        current_club = getattr(request, 'club', None)
        
        if db_field.name == 'club':
            if current_club and request.user.is_superuser:
                kwargs['queryset'] = Club.objects.filter(id=current_club.id)
            elif not request.user.is_superuser and hasattr(request.user, 'profile') and request.user.profile.club:
                kwargs['queryset'] = Club.objects.filter(id=request.user.profile.club.id)
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'club', 'get_schools', 'phone']
    list_filter = ['role', 'club']
    search_fields = ['user__username', 'user__email', 'phone']
    filter_horizontal = ['schools']
    raw_id_fields = ['user']
    
    def get_queryset(self, request):
        """Filter user profiles by current club for Super Admin too"""
        qs = super().get_queryset(request)
        
        # For Super Admin, filter by current club from session/middleware
        if request.user.is_superuser:
            current_club = getattr(request, 'club', None)
            if current_club:
                return qs.filter(club=current_club)
            return qs
        
        # For non-superusers, only show profiles from their club
        if hasattr(request.user, 'profile') and request.user.profile.club:
            return qs.filter(club=request.user.profile.club)
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit club choices based on current club for Super Admin"""
        current_club = getattr(request, 'club', None)
        
        if db_field.name == 'club':
            if current_club and request.user.is_superuser:
                kwargs['queryset'] = Club.objects.filter(id=current_club.id)
            elif not request.user.is_superuser and hasattr(request.user, 'profile') and request.user.profile.club:
                kwargs['queryset'] = Club.objects.filter(id=request.user.profile.club.id)
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Filter schools by the selected club"""
        if db_field.name == 'schools':
            club_id = request.POST.get('club') or request.GET.get('club')
            
            if club_id:
                kwargs['queryset'] = School.objects.filter(club_id=club_id, is_active=True)
            elif hasattr(request, 'club') and request.club:
                kwargs['queryset'] = School.objects.filter(club=request.club, is_active=True)
            else:
                kwargs['queryset'] = School.objects.none()
        
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    def get_form(self, request, obj=None, **kwargs):
        """Override form to filter schools by club"""
        form = super().get_form(request, obj, **kwargs)
        current_club = getattr(request, 'club', None)
        
        if current_club:
            form.base_fields['schools'].queryset = School.objects.filter(club=current_club, is_active=True)
        
        return form
    
    def get_schools(self, obj):
        return ", ".join([s.name for s in obj.schools.all()])
    get_schools.short_description = 'Schools'
    
    def save_model(self, request, obj, form, change):
        """Auto-assign club based on user's club for non-superusers"""
        if not request.user.is_superuser:
            if hasattr(request.user, 'profile') and request.user.profile.club:
                obj.club = request.user.profile.club
        super().save_model(request, obj, form, change)


# ==================== CUSTOM USER ADMIN (SIMPLE VERSION - NO CUSTOM FORMS) ====================

class UserProfileInline(admin.StackedInline):
    """Inline profile for User admin"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    max_num = 1
    min_num = 1


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Simple User admin - using default Django forms (no custom forms)"""
    
    # Use default Django forms (NOT custom)
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
        """Filter users by current club"""
        qs = super().get_queryset(request)
        current_club = getattr(request, 'club', None)
        
        if current_club:
            return qs.filter(profile__club=current_club)
        return qs
    
    def save_model(self, request, obj, form, change):
        """Save user and create profile if needed"""
        super().save_model(request, obj, form, change)
        
        # Create profile if doesn't exist
        if not hasattr(obj, 'profile'):
            current_club = getattr(request, 'club', None)
            UserProfile.objects.create(
                user=obj,
                club=current_club,
                role='coach',  # default role
                phone=''
            )


# ==================== CLASS SCHEDULE ADMIN ====================

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ['school', 'get_club', 'day', 'start_time', 'end_time', 'belt_level', 'instructor', 'is_active']
    list_filter = ['club', 'school', 'day', 'is_active']
    search_fields = ['school__name', 'instructor', 'belt_level']
    
    def get_club(self, obj):
        return obj.club.name if obj.club else '-'
    get_club.short_description = 'Club'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        current_club = getattr(request, 'club', None)
        if current_club:
            return qs.filter(club=current_club)
        return qs
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        current_club = getattr(request, 'club', None)
        if db_field.name == 'club' and current_club:
            kwargs['queryset'] = Club.objects.filter(id=current_club.id)
        if db_field.name == 'school' and current_club:
            kwargs['queryset'] = School.objects.filter(club=current_club, is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==================== CONTACT INFO ADMIN ====================

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'phone', 'email', 'is_emergency', 'order']
    list_filter = ['club', 'is_emergency']
    search_fields = ['name', 'role', 'phone']
    list_editable = ['order']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        current_club = getattr(request, 'club', None)
        if current_club:
            return qs.filter(club=current_club)
        return qs
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        current_club = getattr(request, 'club', None)
        if db_field.name == 'club' and current_club:
            kwargs['queryset'] = Club.objects.filter(id=current_club.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)