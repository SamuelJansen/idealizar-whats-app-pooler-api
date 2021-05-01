from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper
from python_framework import Client, ClientMethod, HttpStatus

import json
import requests

from config import WhatsAppManagerConfig
from dto import QRCodeDto

QR_CODE_URL = f'{WhatsAppManagerConfig.BASE_URL}/login/qr-code'

@Client()
class WhatsAppManagerClient :

    @ClientMethod()
    def startAuthentication(self) :
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(QR_CODE_URL, headers=headers)
        return response.json(), HttpStatus.OK

    @ClientMethod(requestClass=[QRCodeDto.QRCodeRequestDto])
    def updateQRCode(self, dto) :
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        payload = json.dumps({"qRCodeAsBase64": dto.qRCodeAsBase64})
        response = requests.put(QR_CODE_URL, data=payload, headers=headers)
        return response.json(), HttpStatus.OK

    @ClientMethod()
    def resumeAuthentication(self) :
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.patch(QR_CODE_URL, headers=headers)
        return response.json(), HttpStatus.OK
