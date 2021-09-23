import time
from python_helper import log, ObjectHelper, ReflectionHelper
from python_framework import Service, ServiceMethod

from util import KeyboardUtil
from config import WhatsAppWebConfig
from domain import WhatsAppWebConstants

from dto import ContactDto, QRCodeDto

@Service()
class WhatsAppWebService:

    available = WhatsAppWebConstants.DEFAULT_AVAILABLE_STATUS
    authenticating = WhatsAppWebConstants.DEFAULT_AUTHENTICATING_STATUS
    authenticated = WhatsAppWebConstants.DEFAULT_AUTHENTICATED_VALUE

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto])
    def accessContact(self, contact) :
        contactConversationXPath = self.helper.whatsApp.getContactConversationXPath(contact)
        try:
            self.service.browser.accessByXPath(contactConversationXPath)
            time.sleep(contact.accessTime)
        except Exception as exception:
            errorMessage = f'Not possible to acces contact: {contactConversationXPath}'
            log.failure(self.accessContact, errorMessage, exception)
            raise Exception(errorMessage)

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto])
    def getInputTextBox(self, contact) :
        return self.service.browser.findAllByXPath(WhatsAppWebConstants.XPATH_TEXT_BOX)[-1]

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto, str])
    def typeTextAndSend(self, contact, text, element=None) :
        self.service.browser.typeInAndHitEnter(text, element=element)

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto])
    def getMessageList(self, contact) :
        return self.service.browser.findAllByXPath(WhatsAppWebConstants.XPATH_MESSAGE_LIST)[::-1]

    @ServiceMethod()
    def getMessageKey(self, message=None) :
        return self.service.browser.getAttribute(WhatsAppWebConstants.ATTR_MESSAGE_ID, element=message)

    @ServiceMethod()
    def getHtml(self, element=None) :
        return self.service.browser.getAttribute('outerHTML', element=element)

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto])
    def moveUpConversation(self, contact) :
        try :
            self.service.browser.scrollInto(WhatsAppWebConstants.XPATH_MESSAGE_LIST)
        except Exception as exception :
            if 'StaleElementReferenceException' == ReflectionHelper.getName(type(exception)) :
                return self.moveUpConversation(contact)
            raise exception

    @ServiceMethod()
    def authenticate(self) :
        log.log(self.authenticate, 'Started')
        self.setToAuthenticating()
        authenticationBegin = time.time()
        while self.isNotAuthenticated() :
            self.updateQRCode(authenticationBegin)
            self.validator.authentication.authenticationTimeOut(authenticationBegin)
        self.setToAuthenticated()
        self.setToAvailable()
        self.service.browser.optimizeHiddenWindowSize(maxSize=True)
        log.log(self.authenticate, 'Finished')

    @ServiceMethod()
    def access(self, element=None) :
        self.service.browser.access(element=element)

    @ServiceMethod()
    def setToAvailable(self) :
        self.available = True

    @ServiceMethod()
    def setToBusy(self) :
        self.validator.whatsAppWeb.isAvailable()
        self.available = False

    @ServiceMethod()
    def setToAuthenticating(self) :
        self.available = False
        self.authenticated = False
        self.authenticating = True

    @ServiceMethod()
    def setToAuthenticated(self) :
        self.authenticated = True
        self.authenticating = False

    @ServiceMethod()
    def setToNotAuthenticated(self) :
        self.authenticated = False
        self.authenticating = False

    @ServiceMethod()
    def isBooting(self) :
        return self.service.browser.isBooting()

    @ServiceMethod()
    def isAvailable(self) :
        self.bootIfNeeded()
        return self.service.browser.isAvailable() and self.available

    @ServiceMethod()
    def isNotAvailable(self) :
        return not self.isAvailable()

    @ServiceMethod()
    def isAuthenticated(self):
        return True if self.authenticated else False ###- cannot pass a refference here

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
    def isNotAuthenticated(self) :
        return not self.isAuthenticated()

    @ServiceMethod()
    def isAuthenticating(self) :
        return self.authenticating

    @ServiceMethod()
    def isNotAuthenticating(self) :
        return not self.isAuthenticating()

    @ServiceMethod()
    def pingBrowser(self) :
        self.switchWhastAppToANewTab()

    @ServiceMethod(requestClass=[float])
    def updateQRCode(self, authenticationBegin) :
        log.debug(self.updateQRCode, f'Accessing {WhatsAppWebConfig.BASE_URL}')
        self.service.browser.accessUrl(WhatsAppWebConfig.BASE_URL)
        time.sleep(WhatsAppWebConfig.PRE_AUTHENTICATION_DELAY_IN_SECONDS)
        log.debug(self.updateQRCode, f'Screenshotting')
        qRCodeAsBase64 = self.service.browser.inMemoryScreenshot()
        log.debug(self.updateQRCode, f'Sending screenshot to Whats App Manager')
        self.service.whatsAppManager.updateQRCode(QRCodeDto.QRCodeRequestDto(qRCodeAsBase64=qRCodeAsBase64))
        log.debug(self.updateQRCode, f'Waiting for QR-Code authentication')
        nextQRCodeUpdateAt = self.getNextQRCodeUpdateTime(authenticationBegin)
        while self.isNotAuthenticated() and time.time() < nextQRCodeUpdateAt :
            time.sleep(0.5)
            self.updateIsAuthenticated()
            self.validator.authentication.authenticationTimeOut(authenticationBegin)

    def switchWhastAppToANewTab(self) :
        try :
            self.service.browser.accessUrlInNewTab(WhatsAppWebConfig.BASE_URL)
            self.service.browser.closeTab(-2)
            time.sleep(WhatsAppWebConfig.TAB_ALTERNATINGT_TIME_IN_SECONDS)
            self.service.browser.minimize()
        except Exception as exception :
            log.failure(self.switchWhastAppToANewTab, 'Not possible to switch whats app tab properly', exception)

    def getNextQRCodeUpdateTime(self, authenticationBegin) :
        return time.time() + WhatsAppWebConfig.AUTHENTICATION_SCREENSHOT_RENEW_TIME_IN_SECONDS

    def bootIfNeeded(self):
        log.log(self.bootIfNeeded, 'Started')
        self.service.browser.openIfNedded(hidden=WhatsAppWebConstants.HIDDEN_BROWSER)
        log.log(self.bootIfNeeded, 'Finished')

    def boot(self):
        log.log(self.boot, 'Started')
        self.service.browser.open(hidden=WhatsAppWebConstants.HIDDEN_BROWSER)
        log.log(self.boot, 'Finished')

    # @ServiceMethod(requestClass=[ContactDto.ContactRequestDto])
    # def scrollUpConversation(self, contact, ammount=WhatsAppWebConstants.DEFAULT_AMMOUNT_OF_MESSAGE_SCROLL_UP) :
    #     self.service.browser.scroll(ammount)
