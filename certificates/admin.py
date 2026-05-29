from django.contrib import admin
from .models import Department, CertificateType

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(CertificateType)
class CertificateTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'department')
    list_filter = ('department',)
    search_fields = ('name',)