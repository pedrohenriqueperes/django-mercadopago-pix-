# payments/services.py
import mercadopago
from django.conf import settings

def get_payment(price, description):
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    payment_data = {
        "transaction_amount": float(price),
        "description": str(description),
        "payment_method_id": "pix",
        "payer": {
            "email": "test@gmail.com",
            "first_name": "Juciley",
            "last_name": "Pires",
            "identification": {
                "type": "CPF",
                "number": "36069178807"
            },
            "address": {
                "zip_code": "06233-200",
                "street_name": "Av. das Nações Unidas",
                "street_number": "3003",
                "neighborhood": "Bonfim",
                "city": "Osasco",
                "federal_unit": "SP"
            }
        }
    }
    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]
    data = payment['point_of_interaction']['transaction_data']
    return {'clipboard': str(data['qr_code']), 'qrcode': 'data:image/jpeg;base64,{}'.format(data['qr_code_base64']), 'id': payment['id']}

def verify_payment(payment_id):
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    payment_response = sdk.payment().get(int(payment_id))
    payment = payment_response["response"]
    status = payment['status']
    detail = payment['status_detail']
    return {'id': payment_id, 'status': status, 'status_detail': detail}