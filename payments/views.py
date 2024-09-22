from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from .services import initiate_mtn_payment, initiate_orange_payment
import requests

MONETBILL_URL = 'https://www.monetbill.com/payment/v1/place_payment'

def initiate_monetbil_payment(request):
    if request.method == "POST":
        # Get data from the request
        phone_number = request.POST.get("phone_number")
        amount = request.POST.get("amount")
        # notify_url = "https://your.server.com/monetbil/notifications"
        
        # Prepare the payload
        payload = {
            "service": settings.MONETBIL_SERVICE_KEY,  # Set this in your settings.py
            "phonenumber": phone_number,
            "amount": amount,
            # "notify_url": notify_url
        }
        
        # Make the API request to Monetbil
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            "https://api.monetbil.com/payment/v1/placePayment",
            json=payload,
            headers=headers
        )
        
        # Handle the response
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({"error": "Payment initiation failed"}, status=response.status_code)
    
    return JsonResponse({"error": "Invalid request method"}, status=400)

def process_payment(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        phone_number = request.POST.get("phone_number")
        reference = request.POST.get("reference")
        provider = request.POST.get("provider")

        if provider == "MTN":
            response = initiate_mtn_payment(amount, phone_number, reference)
        elif provider == "Orange":
            response = initiate_orange_payment(amount, phone_number, reference)
        
        return render(request, "payments/payment_result.html", {"response": response})
    
    return render(request, "payments/process_payment.html")\


def payments_view(request):
    amount = 1000  # Amount in the smallest currency unit (e.g., XAF for CFA Franc)
    phonenumber = "+237680991499"  # Phone number of the user
    
    # Pass the data to the template
    context = {
        'monetbil_service_key': settings.MONETBIL_SERVICE_KEY,  # Get the service key from settings
        'amount': amount,
        'phonenumber': phonenumber
    }
    
    return render(request, 'payments/pay.html', context)