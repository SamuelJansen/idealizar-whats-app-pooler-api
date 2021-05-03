from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper
from python_framework import Service, ServiceMethod, GlobalException, HttpStatus

from enumeration.AuthenticationStatus import AuthenticationStatus
from dto import AuthenticationDto


@Service()
class AuthenticationService:

    @ServiceMethod()
    def isAuthenticated(self) :
        return self.service.whatsAppWeb.isAuthenticated()

    @ServiceMethod()
    def getAuthenticationStatus(self) :
        if self.isAuthenticated() :
            return self.converter.authentication.toResponse(AuthenticationStatus.AUTHENTICATED)
        else :
            return self.converter.authentication.toResponse(AuthenticationStatus.NOT_AUTHENTICATED)

    @ServiceMethod()
    def authenticateIfNeeded(self) :
        if self.isAuthenticated() :
            return self.converter.authentication.toResponse(AuthenticationStatus.ALREADY_AUTHENTICATED)
        else :
            return self.authenticate()

    @ServiceMethod()
    def authenticate(self) :
        self.validator.authentication.isAvailableForAuthentication()
        log.debug(self.authenticateIfNeeded, 'Authenticating')
        responseDto = None
        try :
            self.service.whatsAppManager.startAuthentication()
            if self.isAuthenticated() :
                self.logOut()
                self.service.whatsAppWeb.reboot()
            self.service.whatsAppWeb.authenticate()
            responseDto = self.converter.authentication.toResponse(AuthenticationStatus.AUTHENTICATED)
            self.service.whatsAppManager.resumeAuthentication()
            log.debug(self.authenticateIfNeeded, 'Authenticated')
        except Exception as exception :
            self.logOut()
            self.service.whatsAppManager.resumeAuthentication()
            log.failure(self.authenticate, 'Not possible to authenticate', exception)
            raise exception
        return responseDto

    @ServiceMethod()
    def hardAuthenticate(self) :
        log.debug(self.hardAuthenticate, 'Forcedly authenticating')
        self.service.whatsAppManager.startAuthentication()
        self.logOut()
        self.service.whatsAppWeb.reboot()
        self.service.whatsAppWeb.authenticate()
        self.service.whatsAppManager.resumeAuthentication()
        log.log(self.authenticateIfNeeded, 'Forcedly authenticated')
        return self.converter.authentication.toResponse(AuthenticationStatus.AUTHENTICATED)

    @ServiceMethod()
    def logOut(self) :
        log.debug(self.logOut, 'Loging out')
        self.service.whatsAppWeb.tearDown()
        log.debug(self.logOut, 'Loged out')
        return self.converter.authentication.toResponse(AuthenticationStatus.NOT_AUTHENTICATED)

    def isAvailable(self) :
        return self.service.whatsAppWeb.isAuthenticated() or self.service.whatsAppWeb.isAvailable()
