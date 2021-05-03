from python_helper import log
from python_framework import Service, ServiceMethod

from dto import QRCodeDto

@Service()
class WhatsAppManagerService :

    @ServiceMethod()
    def startAuthentication(self) :
        try :
            self.client.whatsAppManager.startAuthentication()
        except Exception as exception :
            log.log(self.startAuthentication, 'Not possible to inform authentication started to Whats App Manager', exception=exception)

    @ServiceMethod(requestClass=[QRCodeDto.QRCodeRequestDto])
    def updateQRCode(self, dto) :
        return self.client.whatsAppManager.updateQRCode(dto)

    @ServiceMethod()
    def resumeAuthentication(self) :
        try :
            self.client.whatsAppManager.resumeAuthentication()
        except Exception as exception :
            log.log(self.resumeAuthentication, 'Not possible to inform authentication resumed to Whats App Manager', exception=exception)
