import time
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

from config import WhatsAppWebConfig

@Validator()
class AuthenticationValidator :

    @ValidatorMethod(requestClass=[float])
    def authenticationTimeOut(self, authenticationBegin) :
        if self.service.whatsAppWeb.isNotAuthenticated() and (
            time.time() - authenticationBegin > WhatsAppWebConfig.AUTHENTICATION_TIME_OUT
        ) :
            self.service.whatsAppWeb.setToNotAuthenticated()
            raise GlobalException.GlobalException(
                message = f'Authentication must happens within {WhatsAppWebConfig.AUTHENTICATION_TIME_OUT} seconds',
                status = HttpStatus.UNAUTHORIZED,
                logMessage = 'Authentication time out'
            )

    @ValidatorMethod()
    def isAvailableForAuthentication(self) :
        if self.service.whatsAppWeb.isNotAvailable() and self.service.whatsAppWeb.isNotAuthenticated() :
            self.service.whatsAppWeb.setToNotAuthenticated()
            state = 'Booting' if self.service.browser.isBooting() else 'Authenticating'
            raise GlobalException.GlobalException(
                message = f'WhatsAppWeb is {state}. Try again later seconds',
                status = HttpStatus.UNAUTHORIZED,
                logMessage = 'Authentication time out'
            )

    @ValidatorMethod()
    def isAuthenticated(self) :
        if self.service.whatsAppWeb.isNotAuthenticated() and self.service.whatsAppWeb.isNotAuthenticating() :
            self.service.whatsAppWeb.setToNotAuthenticated()
            raise GlobalException.GlobalException(
                message = f'WhatsAppWeb is not authenticated',
                status = HttpStatus.UNAUTHORIZED,
                logMessage = 'Not authenticated'
            )
