import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.urls import reverse_lazy
from .services import initiate_mtn_payment, initiate_orange_payment
from django.views.decorators.csrf import csrf_exempt
import requests
from campay.sdk import Client as CamPayClient

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
    
    return render(request, "payments/process_payment.html")


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



campay = CamPayClient({
    "app_username" : settings.CAMPAY_USERNAME,
    "app_password" : settings.CAMPAY_PASSWORD,
    "environment" : "DEV" #use "DEV" for demo mode or "PROD" for live mode
})

@csrf_exempt
def campay_payment(request):
    try:
        # Generate a payment link
        payment_link = campay.get_payment_link({
         "amount": "5",
         "currency": "XAF",
         "description": "some description",
         "external_reference": "12345678",
         "from":"",
         "first_name": request.user.first_name,
         "last_name": request.user.last_name,
         "email": request.user.email,
         "redirect_url": reverse_lazy('dashboard_home'),
         "failure_redirect_url": reverse_lazy('dashboard_profile'),
         "payment_options":"MOMO"
      })
        

        # Check if the payment link was generated successfully
        if payment_link.get("status") == "SUCCESSFUL":
            return redirect(payment_link.get('link'))  # Return the payment link
        else:
            return None  # Handle unsuccessful payment link generation

    except Exception as e:
        # Handle exceptions (e.g., log the error)
        print(f"An error occurred: {e}")
        return None
    
@csrf_exempt
def campay_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            payment_status = data.get("status")
            external_reference = data.get("external_reference")

            # Check payment status
            if payment_status == "SUCCESSFUL":
                # Update your order/payment status in the database
                print(f"Payment successful for reference {external_reference}")
                # Your logic here to update payment status
                return JsonResponse({"message": "Payment confirmed"}, status=200)
            else:
                print(f"Payment failed for reference {external_reference}")
                return JsonResponse({"message": "Payment failed"}, status=400)

        except Exception as e:
            print(f"Error processing webhook: {e}")
            return JsonResponse({"message": "Error processing webhook"}, status=500)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=400)