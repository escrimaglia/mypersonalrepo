# ApiTest - By Ed Scrimaglia

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64

visitas = 0

@csrf_exempt
def api_test(request):
    global visitas
    visitas += 1
    headers_o = dict(request.headers)
    api_test = dict()
    headers_auth = dict()

    for key,value in headers_o.items():
        if key == "Authorization":
            tipo_auth = request.headers['Authorization'].split()[0]
            credentials = get_credentials(request,tipo_auth)
            auth_v = dict()
            if "Basic" in tipo_auth:
                auth_v['Tipo'] = credentials[0]
                auth_v['Encoded'] = value
                auth_v['User'] = credentials[1]
                auth_v['Password'] = credentials[2]
            else:
                auth_v['Tipo'] = credentials[0]
                auth_v['Encoded'] = credentials[1]
            headers_auth[key] = auth_v
        else:    
            headers_auth[key] = value

    api_test_result = dict()
    api_test_result['About'] = f"Welcome to ApiTest V1.1 by OctUPus - Ed Scrimaglia, Año 2022 / {visitas}"
    api_test['Status_Code'] = HttpResponse.status_code
    api_test['Method'] = request.method
    api_test['Scheme'] = request.scheme
    api_test['Headers'] = headers_auth
    if bool(request.encoding): 
        api_test['Encoding'] = request.encoding
    if bool(request.content_params):
        api_test['Params'] = request.content_params
    if bool(request.COOKIES):
        api_test['Cookies'] = request.COOKIES
    if bool(request.GET):
        api_test['GET'] = request.GET
    if bool(request.POST):
        api_test['POST'] = request.POST
    if bool(request.body):
        api_test['Body'] = json.loads(request.body)
    api_test_result['Content'] = api_test
    msg = None
    if bool(msg):
        api_test_result['Msg'] = msg

    return JsonResponse(api_test_result, safe=False)

def get_credentials(request, tipo):
    auth = request.headers['Authorization'].split()[1]
    cred_l = list()
    if "basic" in tipo.lower():
        auth_decoded = base64.b64decode(auth).decode('utf-8').split(":")
        usuario_h = auth_decoded[0]
        password_h = auth_decoded[1]
        cred_l.append(tipo)
        cred_l.append(usuario_h)
        cred_l.append(password_h)
    elif "bearer" in tipo.lower():
        cred_l.append("Bearer")
        cred_l.append(auth)
    else:
        cred_l.append(tipo)
        cred_l.append(auth)

    return cred_l
