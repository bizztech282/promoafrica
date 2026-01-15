from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.loading_animation, name='loading_animation'),
    path('home/', views.landing_page, name='landing_page'),
    path('withdrawal/', views.withdrawal_request, name='withdrawal_request'),
    path('subscription/', views.subscription_instructions, name='subscription_instructions'),
    path('confirmation/', views.processing_confirmation, name='processing_confirmation'),
    
    # AJAX endpoints
    path('api/spin/', views.spin_wheel, name='spin_wheel'),
    path('api/submit-withdrawal/', views.submit_withdrawal, name='submit_withdrawal'),
    
    # Info pages
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('terms/', views.terms_and_conditions, name='terms_and_conditions'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
]
