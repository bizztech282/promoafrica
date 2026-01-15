from django.contrib import admin
from .models import WithdrawalRequest


@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    """
    Admin interface for managing withdrawal requests.
    """
    list_display = [
        'phone_number',
        'amount_won',
        'status',
        'created_at',
        'updated_at'
    ]
    list_filter = [
        'status',
        'created_at',
        'updated_at'
    ]
    search_fields = [
        'phone_number',
        'session_id'
    ]
    readonly_fields = [
        'session_id',
        'created_at',
        'updated_at'
    ]
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User Information', {
            'fields': ('phone_number', 'session_id')
        }),
        ('Prize Information', {
            'fields': ('amount_won', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_processing', 'mark_as_completed', 'mark_as_failed']
    
    def mark_as_processing(self, request, queryset):
        """Mark selected requests as processing"""
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} requests marked as processing.')
    mark_as_processing.short_description = 'Mark as Processing'
    
    def mark_as_completed(self, request, queryset):
        """Mark selected requests as completed"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} requests marked as completed.')
    mark_as_completed.short_description = 'Mark as Completed'
    
    def mark_as_failed(self, request, queryset):
        """Mark selected requests as failed"""
        updated = queryset.update(status='failed')
        self.message_user(request, f'{updated} requests marked as failed.')
    mark_as_failed.short_description = 'Mark as Failed'
