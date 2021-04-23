import time
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

from config import WhatsAppWebConfig

@Validator()
class WhatsAppWebValidator :

    @ValidatorMethod(requestClass=[float])
    def authenticationTimeOut(self, authenticationBegin) :
        if self.service.whatsAppWeb.isNotAuthenticated() and (
            time.time() - authenticationBegin > WhatsAppWebConfig.AUTHENTICATION_TIME_OUT
        ) :
            raise GlobalException.GlobalException(
                message = f'Authentication must happens within {WhatsAppWebConfig.AUTHENTICATION_TIME_OUT} seconds',
                status = HttpStatus.UNAUTHORIZED,
                logMessage = 'Authentication time out'
            )

    @ValidatorMethod()
    def isAvailableForAuthentication(self) :
        if self.service.whatsAppWeb.isNotAvailable() and self.service.whatsAppWeb.isNotAuthenticated() :
            state = 'Booting' if self.service.browser.isBooting() else 'Authenticating'
            raise GlobalException.GlobalException(
                message = f'WhatsAppWeb is {state}. Try again later seconds',
                status = HttpStatus.UNAUTHORIZED,
                logMessage = 'Authentication time out'
            )

# [DEBUG  ] BrowserClient.getNewBrowser: session_id: fb1e997bed478015c17cb68ae0e67c4b
# [DEBUG  ] BrowserClient.getNewBrowser: command_executor: http://127.0.0.1:55209
# [DEBUG  ] BrowserService.open: Finished
# [DEBUG  ] BrowserService.openIfNedded: Finished
# [DEBUG  ] WhatsAppWebService.bootIfNeeded: Finished
# [DEBUG  ] AuthenticationService.logOut: Started
# [DEBUG  ] WhatsAppWebService.tearDown: Started
# [DEBUG  ] BrowserService.tearDown: Started
# [DEBUG  ] BrowserService.safelyClose: Started
