from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()

BASE_URL = globalsInstance.getApiSetting('whats-app.web.base-url')

AUTHENTICATION_TIME_OUT = int(globalsInstance.getApiSetting('whats-app.web.authentication.time-out'))
PRE_AUTHENTICATION_DELAY = int(globalsInstance.getApiSetting('whats-app.web.authentication.pre-delay'))
AUTHENTICATION_SCREENSHOT_RENEW = int(globalsInstance.getApiSetting('whats-app.web.authentication.screenshot-time-renew'))

if AUTHENTICATION_SCREENSHOT_RENEW > AUTHENTICATION_SCREENSHOT_RENEW :
    raise Exception('Authentication time out cannot be bigger than authentication screenshot time renew')

if PRE_AUTHENTICATION_DELAY > AUTHENTICATION_SCREENSHOT_RENEW :
    raise Exception('Authentication pre delay cannot be bigger than authentication screenshot time renew')
