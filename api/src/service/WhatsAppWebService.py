import time
from python_helper import log
from python_framework import Service, ServiceMethod

from config import WhatsAppWebConfig
from domain import WhatsAppWebConstants

from dto import ContactDto, QRCodeDto

@Service()
class WhatsAppWebService:

    available = WhatsAppWebConstants.DEFAULT_AVAILABLE_STATUS
    authenticated = WhatsAppWebConstants.DEFAULT_AUTHENTICATED_VALUE

    @ServiceMethod()
    def isBooting(self) :
        return self.service.browser.isBooting()

    @ServiceMethod()
    def isAvailable(self) :
        self.bootIfNeeded()
        return self.service.browser.isAvailable() and self.available

    @ServiceMethod()
    def isAuthenticated(self):
        return True if self.authenticated else False ###- cannot pass a refference here

    @ServiceMethod()
    def authenticate(self) :
        log.log(self.authenticate, 'Started')
        self.available = False
        authenticationBegin = time.time()
        self.authenticated = False
        while self.isNotAuthenticated() :
            self.updateQRCode(authenticationBegin)
            self.validator.whatsAppWeb.authenticationTimeOut(authenticationBegin)
        self.available = True
        log.log(self.authenticate, 'Finished')

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto])
    def accessContact(self, contact) :
        contactConversationXPath = self.helper.whatsApp.getContactConversationXPath(contact)
        self.service.broser.accessXPath(contactConversationXPath)

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto])
    def getMessageList(self, contact) :
        return self.service.browser.findAllByXPath(WhatsAppConstants.XPATH_GROUP_MESSAGE_LIST)

    @ServiceMethod()
    def tearDown(self) :
        log.log(self.tearDown, 'Started')
        self.service.browser.tearDown()
        self.available = WhatsAppWebConstants.DEFAULT_AVAILABLE_STATUS
        self.authenticated = WhatsAppWebConstants.DEFAULT_AUTHENTICATED_VALUE
        log.log(self.tearDown, 'Finished')

    @ServiceMethod()
    def reboot(self) :
        log.log(self.reboot, 'Started')
        self.tearDown()
        self.boot()
        log.log(self.reboot, 'Finished')

    @ServiceMethod()
    def updateIsAuthenticated(self) :
        self.authenticated = self.service.browser.existsByXpath(WhatsAppWebConstants.XPATH_AUTHENTICATED_USER)

    @ServiceMethod()
    def isNotAvailable(self) :
        return not self.isAvailable()

    @ServiceMethod()
    def isNotAuthenticated(self) :
        return not self.isAuthenticated()

    def updateQRCode(self, authenticationBegin) :
        log.debug(self.updateQRCode, f'Accessing {WhatsAppWebConfig.BASE_URL}')
        self.service.browser.accessUrl(WhatsAppWebConfig.BASE_URL)
        time.sleep(WhatsAppWebConfig.PRE_AUTHENTICATION_DELAY)
        log.debug(self.updateQRCode, f'Screenshotting')
        qRCodeAsBase64 = self.service.browser.inMemoryScreenshot()
        log.debug(self.updateQRCode, f'Sending screenshot to Whats App Manager')
        self.service.whatsAppManager.updateQRCode(QRCodeDto.QRCodeRequestDto(qRCodeAsBase64=qRCodeAsBase64))
        log.debug(self.updateQRCode, f'Waiting for QR-Code authentication')
        nextQRCodeUpdateAt = self.getNextQRCodeUpdateTime(authenticationBegin)
        while self.isNotAuthenticated() and time.time() < nextQRCodeUpdateAt :
            time.sleep(0.5)
            self.updateIsAuthenticated()
            self.validator.whatsAppWeb.authenticationTimeOut(authenticationBegin)

    def getNextQRCodeUpdateTime(self, authenticationBegin) :
        # cumulativeTime = WhatsAppWebConfig.AUTHENTICATION_SCREENSHOT_RENEW * ((time.time() - authenticationBegin) // WhatsAppWebConfig.AUTHENTICATION_SCREENSHOT_RENEW)
        # difference = WhatsAppWebConfig.AUTHENTICATION_SCREENSHOT_RENEW - (time.time() - (authenticationBegin + cumulativeTime))
        # if difference < .2 * WhatsAppWebConfig.AUTHENTICATION_SCREENSHOT_RENEW :
        #     time.sleep(difference)
        #     cumulativeTime = WhatsAppWebConfig.AUTHENTICATION_SCREENSHOT_RENEW * ((time.time() - authenticationBegin) // WhatsAppWebConfig.AUTHENTICATION_SCREENSHOT_RENEW)
        #     difference = WhatsAppWebConfig.AUTHENTICATION_SCREENSHOT_RENEW - (time.time() - (authenticationBegin + cumulativeTime))
        # delay = WhatsAppWebConfig.AUTHENTICATION_SCREENSHOT_RENEW * ((difference if 0 < difference else -1 * difference) // WhatsAppWebConfig.AUTHENTICATION_SCREENSHOT_RENEW)
        # residue = delay + ((100 * WhatsAppWebConfig.AUTHENTICATION_SCREENSHOT_RENEW) + difference) % WhatsAppWebConfig.AUTHENTICATION_SCREENSHOT_RENEW
        # nextQRCodeUpdateAt = authenticationBegin + cumulativeTime + residue
        # # nextQRCodeUpdateAt = authenticationBegin + cumulativeTime + (difference if 0 < difference else WhatsAppWebConfig.AUTHENTICATION_SCREENSHOT_RENEW + difference)
        # print(f'authenticationBegin: {authenticationBegin}, now: {time.time()}, cumulativeTime:{cumulativeTime}, difference: {difference}, nextQRCodeUpdateAt: {nextQRCodeUpdateAt}')
        # return nextQRCodeUpdateAt
        return time.time() + WhatsAppWebConfig.AUTHENTICATION_SCREENSHOT_RENEW

    def bootIfNeeded(self):
        log.log(self.bootIfNeeded, 'Started')
        self.service.browser.openIfNedded(hidden=WhatsAppWebConstants.HIDDEN_BROWSER)
        log.log(self.bootIfNeeded, 'Finished')

    def boot(self):
        log.log(self.boot, 'Started')
        self.service.browser.open(hidden=WhatsAppWebConstants.HIDDEN_BROWSER)
        log.log(self.boot, 'Finished')
