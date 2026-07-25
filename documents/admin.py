from django.contrib import admin

from .models import (
    DeclarationOfPerformance,
    DopSettings,
    En1279Document,
    En1279FieldOption,
    En1279Settings,
)


@admin.register(DopSettings)
class DopSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not DopSettings.objects.exists()


@admin.register(En1279Settings)
class En1279SettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not En1279Settings.objects.exists()


@admin.register(DeclarationOfPerformance)
class DeclarationOfPerformanceAdmin(admin.ModelAdmin):
    list_display = (
        'document_number',
        'source_document_type',
        'source_document_number',
        'created_by',
        'created_at',
    )
    list_filter = ('source_document_type', 'created_at')
    search_fields = (
        'document_number',
        'source_document_number',
    )


@admin.register(En1279Document)
class En1279DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'document_number',
        'product_designation',
        'thermal_performance',
        'created_by',
        'created_at',
    )
    list_filter = ('created_at',)
    search_fields = (
        'document_number',
        'product_designation',
    )


@admin.register(En1279FieldOption)
class En1279FieldOptionAdmin(admin.ModelAdmin):
    list_display = ('field_key', 'value', 'sort_order', 'is_active', 'created_at')
    list_filter = ('field_key', 'is_active')
    search_fields = ('value',)
    ordering = ('field_key', 'sort_order', 'value')
