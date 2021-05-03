from python_framework import Controller, ControllerMethod, HttpStatus

from dto import ScanDto

@Controller(url = '/scan/message', tag='Scan', description='Scan messages by contact')
class ScanMessageController:

    @ControllerMethod(url = '/',
        requestClass=[ScanDto.ScanRequestDto]
    )
    def patch(self, dto):
        return self.service.scan.scanMessage(dto), HttpStatus.OK
