from domain import BrowserConstants 


@Service()
class BrowserService:

    browser = None
    booting = BrowserConstants.DEFAULT_BROWSER_BOOTING_VALUE
    available = BrowserConstants.DEFAULT_AVAILABLE_STATUS

    @ServiceMethod(requestClass=[str, DEFAULT_BOWSER_CLASS])
    def pasteToBrowser(self, screenshotName, browser, element=None):
        image = Image.open(screenshotName)
        output = BytesIO()
        image.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        self.client.browser.hitControlV(browser, element=element)
        # KeyboardUtil.ctrlV()


    @ServiceMethod(requestClass=[str])
    def openBrowserIfNedded(self, url) :
        if not self.browserIsBooted() and not self.browserIsBooting() :
            self.booting = True
            # mostRecentSession = self.service.session.findMostRecent()
            # if ObjectHelper.isNone(mostRecentSession) :
            #     self.browser = self.client.browser.getNewBrowser()
            #     self.service.session.create(
            #         Session.Session(
            #             sessionId = self.browser.session_id,
            #             commandExecutor = self.browser.command_executor._url
            #         )
            #     )
            # else :
            #     self.browser = self.client.browser.retrieveBrowserSession(mostRecentSession.sessionId, mostRecentSession.commandExecutor)
            self.browser = self.client.browser.getNewBrowser()
            self.service.session.create(
                Session.Session(
                    sessionId = self.browser.session_id,
                    commandExecutor = self.browser.command_executor._url
                )
            )
            self.client.browser.accessUrl(url, self.browser)
            time.sleep(AUTHENTICATION_TIME_OUT)
            self.client.browser.screeshotWebPage('QRCode.png', url, self.browser)
            time.sleep(AUTHENTICATION_TIME_OUT)
            self.booting = False
            self.available = True

    @ServiceMethod()
    def browserIsBooted(self) :
        return ObjectHelper.isNotNone(self.browser)

    @ServiceMethod()
    def browserIsBooting(self) :
        return self.booting

    @ServiceMethod()
    def browserIsAvailable(self) :
        return self.browserIsBooted() and self.available
