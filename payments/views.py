from django.http import JsonResponse
from django.shortcuts import redirect, render
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

def payment_error(request):
    return render(request, 'payments/payment_error.html')

def payment_success(request):
    return render(request, 'payments/payment_success.html')


def monetbil_payment(request):
    # Data to be sent to Monetbil
    data = {
        'amount': 1000,  # The amount you want the customer to pay
        'phone': '680991499',  # Optional: customer phone number
        'currency': 'XAF',  # Currency
    }

    # Correct URL construction with version and service_key
    monetbil_url = f"https://api.monetbil.com/widget/v2.1/{settings.MONETBIL_SERVICE_KEY}"
    
    # Make a POST request to Monetbil API
    response = requests.post(monetbil_url, data=data)
    
    if response.status_code == 200:
        payment_url = response.json().get('payment_url')
        if payment_url:
            # Redirect to Monetbil payment page
            return redirect(payment_url)
        else:
            return render(request, 'payments/payment_error.html', {'error': 'No payment URL in response'})
    else:
        return render(request, 'payments/payment_error.html', {'error': 'Failed to communicate with Monetbil API'})

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