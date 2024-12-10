import requests

PRIMARY_KEY = "00027fd76eaf48a2b77a43c8cfd77394"
SECONDARY_KEY = "6bf981223a344dd4b46374d46b8ec9c6"

def initiate_mtn_payment(amount, phone_number, reference):
    url = "https://api.mtn.cm/collection/v1_0/requesttopay"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "X-Target-Environment": "sandbox",  # Adjust this for production
        "Ocp-Apim-Subscription-Key": PRIMARY_KEY,  # Primary key
        "Content-Type": "application/json",
    }
    payload = {
        "amount": str(amount),
        "currency": "XAF",
        "externalId": reference,
        "payer": {
            "partyIdType": "MSISDN",
            "partyId": phone_number,
        },
        "payerMessage": "Payment message",
        "payeeNote": "Note",
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def get_access_token():
    token_url = "https://api.mtn.cm/v1_0/token"
    headers = {
        "Ocp-Apim-Subscription-Key": SECONDARY_KEY,  # Secondary key
        "Content-Type": "application/json",
    }
    payload = {}

    response = requests.post(token_url, headers=headers, json=payload)
    token_data = response.json()
    return token_data.get('access_token')  # Adjust this based on actual response structure
    
def initiate_orange_payment(amount, phone_number, reference):
    url = "https://api.orange.com/orange-money-webpay/cm/v1/requesttopay"
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "Content-Type": "application/json",
    }
    payload = {
        "amount": amount,
        "currency": "XAF",
        "order": reference,
        "customer": phone_number,
        "description": "Payment description",
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

    