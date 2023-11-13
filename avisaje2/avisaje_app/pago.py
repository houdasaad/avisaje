import requests
import json
import webbrowser
from django.shortcuts import redirect
import requests
'''
Request simple a la API,
que redirecciona a la pagina de pago.
'''
def iniciar_pago(request):
    costo = request.POST.get('costo')

    #Variables globales
    API_URL = r'https://sandbox-alb.etpayment.com/sandbox'
    PTM_URL = r'https://pmt-sandbox.etpay.com'
    INIT_API = r'/session/initialize'
    MERCHANT_CODE = "cl_sandbox_desenfoque"
    MERCHANT_API_TOKEN = "MdduCzbdr0IsMYXBvRCM5IqRcu4KfeYcZbYbJBZ0m7rHU2xLVQdCWSg1OdLknZd8"


    request_data = {
        "merchant_code": MERCHANT_CODE,
        "merchant_api_token": MERCHANT_API_TOKEN,
        "merchant_order_id": "order-1992", #id de orden de compra propio del comercio
        "order_amount" : costo,
    }

    #Obtención de session token

    resp = requests.post(API_URL+INIT_API, json=request_data)
    if resp.status_code == 200:
        token = resp.json()['token']

        payment_url = PTM_URL + '/session/' + token

        # En lugar de usar webbrowser, redirigimos al cliente con Django
        return redirect(payment_url)
    else:
        # Manejar errores aquí
        pass

    #Se lanza sesión del cliente
    #webbrowser.open(PTM_URL+'/session/'+token)
    '''Notar que en este código no se guarda el valor del signature_token. Más adelante se explicará en detalle su utilidad, pero se debe tener en cuenta que es necesario obtener el valor de este.'''