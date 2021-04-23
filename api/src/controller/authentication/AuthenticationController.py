from python_framework import Controller, ControllerMethod, HttpStatus

from dto import AuthenticationDto

@Controller(url = '/authentication', tag='Authentication', description='Authentication controller')
class AuthenticationController:

    @ControllerMethod(url = '/',
        responseClass=[AuthenticationDto.AuthenticationResponseDto]
    )
    def get(self):
        return self.service.authentication.getAuthenticationStatus(), HttpStatus.OK

    @ControllerMethod(url = '/',
        responseClass=[AuthenticationDto.AuthenticationResponseDto]
    )
    def patch(self):
        return self.service.authentication.authenticateIfNeeded(), HttpStatus.OK

    @ControllerMethod(url = '/',
        responseClass=[AuthenticationDto.AuthenticationResponseDto]
    )
    def post(self):
        return self.service.authentication.authenticate(), HttpStatus.CREATED

    @ControllerMethod(url = '/',
        responseClass=[AuthenticationDto.AuthenticationResponseDto]
    )
    def delete(self):
        return self.service.authentication.logOut(), HttpStatus.OK
