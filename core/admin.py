from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Patient, Doctor, PatientDoctorMapping

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'is_staff', 'is_doctor', 'is_patient')
    search_fields = ('email', 'name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                  'is_doctor', 'is_patient', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'gender', 'phone_number')
    search_fields = ('user__name', 'user__email', 'phone_number')
    list_filter = ('gender',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'license_number', 'hospital')
    search_fields = ('user__name', 'user__email', 'license_number', 'hospital')
    list_filter = ('specialization',)

@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'assigned_date', 'is_active')
    search_fields = ('patient__user__name', 'doctor__user__name')
    list_filter = ('is_active', 'assigned_date')

admin.site.register(User, CustomUserAdmin)
