from python_framework import Controller, ControllerMethod, HttpStatus

from dto import AuthenticationDto

@Controller(url = '/authentication/force', tag='Authentication', description='Authentication controller')
class HardAuthenticationController:

    @ControllerMethod(url = '/',
        responseClass=[AuthenticationDto.AuthenticationResponseDto]
    )
    def post(self):
        return self.service.authentication.hardAuthenticate(), HttpStatus.CREATED
