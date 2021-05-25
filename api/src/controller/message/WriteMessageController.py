from python_framework import Controller, ControllerMethod, HttpStatus

from dto import WriteDto

@Controller(url = '/message/write', tag='Message', description='Write messages to contact')
class WriteMessageController:

    @ControllerMethod(url = '/',
        requestClass=[WriteDto.WriteRequestDto],
        responseClass=[WriteDto.WriteResponseDto]
    )
    def patch(self, dto):
        return self.service.write.writeMessage(dto), HttpStatus.OK
