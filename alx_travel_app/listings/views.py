import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Payment
from django.core.mail import send_mail
from django.conf import settings

CHAPA_URL = "https://api.chapa.co/v1/transaction/initialize"

class InitiatePaymentView(View):
    @csrf_exempt
    def post(self, request):
        data = request.POST
        amount = data.get("amount")
        email = data.get("email")
        booking_reference = data.get("booking_reference")

        payload = {
            "amount": amount,
            "currency": "ETB",
            "email": email,
            "tx_ref": booking_reference,
            "callback_url": "http://localhost:8000/listings/verify-payment/",
        }

        headers = {
            "Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}"
        }

        response = requests.post(CHAPA_URL, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200 and response_data.get("status") == "success":
            Payment.objects.create(
                booking_reference=booking_reference,
                amount=amount,
                status="Pending",
                transaction_id=response_data["data"]["tx_ref"],
            )
            return JsonResponse({
                "checkout_url": response_data["data"]["checkout_url"]
            })
        else:
            return JsonResponse({
                "error": "Payment initiation failed",
                "details": response_data
            }, status=400)

class VerifyPaymentView(View):
    @csrf_exempt
    def get(self, request):
        tx_ref = request.GET.get("tx_ref")
        url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
        headers = {
            "Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}"
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
            if data.get("status") == "success" and data["data"]["status"] == "success":
                payment.status = "Completed"
                payment.save()

                # Optionally send confirmation email
                send_mail(
                    "Payment Successful",
                    f"Your payment for booking {payment.booking_reference} was successful!",
                    settings.DEFAULT_FROM_EMAIL,
                    [data["data"]["email"]],
                )

                return JsonResponse({"message": "Payment verified successfully!"})
            else:
                payment.status = "Failed"
                payment.save()
                return JsonResponse({"message": "Payment verification failed."}, status=400)
        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment not found."}, status=404)
