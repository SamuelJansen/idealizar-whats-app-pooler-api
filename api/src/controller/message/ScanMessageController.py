from python_framework import Controller, ControllerMethod, HttpStatus

from dto import ScanDto

@Controller(url = '/message/scan', tag='Message', description='Scan messages by contact')
class ScanMessageController:

    @ControllerMethod(url = '/',
        requestClass=[ScanDto.ScanRequestDto],
        responseClass=[ScanDto.ScanResponseDto]
    )
    def patch(self, dto):
        return self.service.scan.scanMessage(dto), HttpStatus.OK
