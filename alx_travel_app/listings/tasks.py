from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(customer_email, booking_details):
    subject = "Booking Confirmation"
    message = f"Dear Customer,\n\nYour booking was successful!\n\nDetails:\n{booking_details}\n\nThank you!"
    from_email = "noreply@alxtravel.com"
    recipient_list = [customer_email]
    
    send_mail(subject, message, from_email, recipient_list)
    print(f"Booking confirmation email sent to {customer_email}")
