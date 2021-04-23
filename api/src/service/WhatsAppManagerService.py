from python_framework import Service, ServiceMethod

from dto import QRCodeDto

@Service()
class WhatsAppManagerService :

    @ServiceMethod()
    def startAuthentication(self) :
        try :
            self.client.whatsAppManager.startAuthentication()
        except Exception as exception :
            log.log(self.authenticate, 'Not possible to inform authentication started to Whats App Manager', exception=exception)

    @ServiceMethod(requestClass=[QRCodeDto.QRCodeRequestDto])
    def updateQRCode(self, dto) :
        return self.client.whatsAppManager.updateQRCode(dto)

    @ServiceMethod()
    def resumeAuthentication(self) :
        try :
            self.client.whatsAppManager.resumeAuthentication()
        except Exception as innerException :
            log.log(self.authenticate, 'Not possible to inform authentication resumed to Whats App Manager', exception=exception)
