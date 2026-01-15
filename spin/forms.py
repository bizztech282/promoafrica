from django import forms
from django.core.validators import RegexValidator
from .models import WithdrawalRequest


class WithdrawalRequestForm(forms.ModelForm):
    """
    Form for withdrawal requests with phone number validation.
    """
    phone_number = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary transition-colors',
            'placeholder': '07xxxxxxxx or 01xxxxxxxx',
            'pattern': '^(07|01)[0-9]{8}$',
            'title': 'Enter a valid Kenyan phone number',
            'id': 'phone-input',
            'maxlength': '10',
            'autocomplete': 'tel'
        }),
        validators=[
            RegexValidator(
                regex=r'^(07|01)\d{8}$',
                message='Phone number must start with 07 or 01 and be exactly 10 digits'
            )
        ],
        help_text='Enter your Kenyan phone number (07xxxxxxxx or 01xxxxxxxx)'
    )
    
    class Meta:
        model = WithdrawalRequest
        fields = ['phone_number']
    
    def clean_phone_number(self):
        """Additional validation for phone number"""
        phone = self.cleaned_data.get('phone_number')
        
        # Remove any spaces or dashes
        phone = phone.replace(' ', '').replace('-', '')
        
        # Ensure it's exactly 10 digits
        if len(phone) != 10:
            raise forms.ValidationError('Phone number must be exactly 10 digits')
        
        # Ensure it starts with 07 or 01
        if not (phone.startswith('07') or phone.startswith('01')):
            raise forms.ValidationError('Phone number must start with 07 or 01')
        
        # Ensure all characters are digits
        if not phone.isdigit():
            raise forms.ValidationError('Phone number must contain only digits')
        
        return phone
