from json.encoder import JSONEncoder
import re
from braintree import transaction
from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# setting up server
import braintree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="gvyp6jpkyjqcp49f",
        public_key="87r2mzqqfhjsbxx7",
        private_key="b35242ebc92102bab7213f447b46bd70"
    )
)

# by now the gateway is ready, and now we need to generate the token and before generating token we need a simple method to check if user signed up or not


def validate_user_session(id, token):
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False


# now we need to send the token back to the client 

@csrf_exempt
def generate_token(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'Invalid session, Please login again!'})

    return JsonResponse({'clientToken': gateway.client_token.genertate(), 'success': True})

@csrf_exempt
def process_payment(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'Invalid session, Please login again!'})
    
    nonce_from_the_client = request.POST("paymentMethodNonce")
    amount_from_the_client = request.POST("paymentMethodNonce")

    result = gateway.transaction.sale({
        "amount": amount_from_the_client,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        return JsonResponse({"success": result.is_success, "transaction": {'id': result.transaction.id, 'amount': result.transaction.amount}})
    else:
        return JsonResponse({'error': True, 'success': False})