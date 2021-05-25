from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

from config import WhatsAppWebConfig

@Validator()
class WhatsAppWebValidator :

    @ValidatorMethod()
    def isAvailable(self) :
        self.validator.authentication.isAuthenticated()
        if self.service.whatsAppWeb.isNotAvailable() :
            raise GlobalException(
                message = f'WhatsAppWeb is processing a request already',
                status = HttpStatus.TOO_MANY_REQUESTS,
                logMessage = 'Authenticated but busy'
            )
