from django.db import models
from django.core.validators import RegexValidator


class WithdrawalRequest(models.Model):
    """
    Model to store withdrawal requests from users who won prizes.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    # Kenyan phone number validator (07xxxxxxxx or 01xxxxxxxx)
    phone_regex = RegexValidator(
        regex=r'^(07|01)\d{8}$',
        message="Phone number must be in format: '07xxxxxxxx' or '01xxxxxxxx'"
    )
    
    phone_number = models.CharField(
        max_length=10,
        validators=[phone_regex],
        help_text="Kenyan phone number (07xxxxxxxx or 01xxxxxxxx)"
    )
    amount_won = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount won by the user"
    )
    session_id = models.CharField(
        max_length=100,
        help_text="Session ID to track user"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of withdrawal request"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Withdrawal Request'
        verbose_name_plural = 'Withdrawal Requests'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['phone_number']),
        ]
    
    def __str__(self):
        return f"{self.phone_number} - Kshs {self.amount_won} ({self.status})"
    
    @property
    def formatted_amount(self):
        """Return formatted amount with currency"""
        return f"Kshs {self.amount_won:,.2f}"
