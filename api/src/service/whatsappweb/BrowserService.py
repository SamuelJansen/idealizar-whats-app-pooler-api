from python_helper import ObjectHelper, log
from python_framework import Service, ServiceMethod

from io import BytesIO
import win32clipboard
from PIL import Image

from domain import BrowserConstants

@Service()
class BrowserService:

    browser = None
    booting = BrowserConstants.DEFAULT_BROWSER_BOTTING_VALUE
    booted = BrowserConstants.DEFAULT_BOOTED_VALUE

    @ServiceMethod()
    def accessUrl(self, url) :
        self.client.browser.accessUrl(url, self.browser)

    @ServiceMethod(requestClass=[str])
    def accessUrlInNewTab(self, url) :
        self.client.browser.accessUrlInNewTab(url, self.browser)

    @ServiceMethod(requestClass=[int])
    def closeTab(self, tabIndex) :
        self.client.browser.closeTab(tabIndex, self.browser)

    @ServiceMethod(requestClass=[str])
    def accessByXPath(self, xPath) :
        return self.client.browser.accessByXPath(xPath, self.browser)

    @ServiceMethod()
    def access(self, element=None) :
        return self.client.browser.access(self.browser, element=element)

    @ServiceMethod(requestClass=[str])
    def findByXPath(self, xPath) :
        return self.client.browser.findByXPath(xPath, self.browser)

    @ServiceMethod(requestClass=[str])
    def findAllByXPath(self, xPath) :
        return self.client.browser.findAllByXPath(xPath, self.browser)

    @ServiceMethod(requestClass=[str])
    def existsByXpath(self, xpath) :
        return self.client.browser.existsByXpath(xpath, self.browser)

    @ServiceMethod(requestClass=[str])
    def typeInAndHitEnter(self, text, element=None) :
        self.client.browser.typeInAndHitEnter(text, self.browser, element=element)

    @ServiceMethod(requestClass=[str])
    def pasteToBrowser(self, screenshotName, element=None):
        image = Image.open(screenshotName)
        output = BytesIO()
        image.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        self.client.browser.hitControlV(self.browser, element=element)

    @ServiceMethod(requestClass=[str])
    def screenshot(self, screenshotName) :
        return self.client.browser.screenshot(screenshotName, self.browser)

    @ServiceMethod()
    def inMemoryScreenshot(self) :
        return self.client.browser.inMemoryScreenshot(self.browser)

    @ServiceMethod(requestClass=[str])
    def scrollInto(self, xPath) :
        self.client.browser.scrollInto(self.browser, element=self.findByXPath(xPath))

    @ServiceMethod(requestClass=[str])
    def getAttribute(self, attributeName, element=None) :
        return self.client.browser.getAttribute(attributeName, self.browser, element=element)

    @ServiceMethod()
    def optimizeHiddenWindowSize(self, maxSize=False) :
        self.client.browser.optimizeHiddenWindowSize(self.browser, maxSize=maxSize)
        log.debug(self.optimizeHiddenWindowSize, f'windowSize: {self.browser.windowSize}, originalWindowSize: {self.browser.originalWindowSize}')

    @ServiceMethod()
    def isBooting(self) :
        return self.booting

    @ServiceMethod()
    def isBooted(self) :
        return self.booted

    @ServiceMethod()
    def isAvailable(self) :
        return ObjectHelper.isNotNone(self.browser) and not self.isBooting()

    @ServiceMethod()
    def openIfNedded(self, hidden=False) :
        log.log(self.openIfNedded, 'Started')
        if ObjectHelper.isNone(self.browser) and self.isNotBooting() :
            self.open(hidden=hidden)
        log.log(self.openIfNedded, 'Finished')

    @ServiceMethod()
    def open(self, hidden=False) :
        log.log(self.open, 'Started')
        self.booting = True
        self.safelyClose()
        self.browser = self.client.browser.getNewBrowser(hidden=hidden)
        self.client.browser.maximize(self.browser)
        sessionId = self.browser.session_id
        commandExecutor = self.browser.command_executor._url
        self.service.session.create(sessionId, commandExecutor)
        self.booted = True
        self.booting = False
        log.log(self.open, 'Finished')

    @ServiceMethod()
    def tearDown(self) :
        log.log(self.tearDown, 'Started')
        self.safelyClose()
        log.log(self.tearDown, 'Finished')

    def safelyClose(self) :
        log.log(self.safelyClose, 'Started')
        if ObjectHelper.isNotNone(self.browser) :
            try :
                self.client.browser.close(self.browser)
            except Exception as exception :
                log.log(self.safelyClose, 'Not possible to close browser', exception=exception)
        self.browser = None
        self.booted = False
        log.log(self.safelyClose, 'Finished')

    @ServiceMethod()
    def isNotBooting(self) :
        return not self.isBooting()

    @ServiceMethod()
    def isNotBooted(self) :
        return not self.isBooted()

    @ServiceMethod()
    def minimize(self) :
        self.client.browser.minimize(self.browser)

    # @ServiceMethod(requestClass=[int])
    # def setZoom(self, zoomPercentage) :
    #     return self.client.browser.setZoom(zoomPercentage, self.browser)

    # @ServiceMethod()
    # def setMinimumZoom(self) :
    #     self.client.browser.setMinimumZoom(self.browser)

    # @ServiceMethod(requestClass=[int])
    # def scroll(self, scrollAmmount) :
    #     self.client.browser.scroll(scrollAmmount, self.browser)
