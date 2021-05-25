from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()

BASE_URL = globalsInstance.getApiSetting('whats-app.web.base-url')

PRE_AUTHENTICATION_DELAY_IN_SECONDS = int(globalsInstance.getApiSetting('whats-app.web.authentication.pre-delay-in-seconds'))
AUTHENTICATION_TIME_OUT_IN_SECONDS = int(globalsInstance.getApiSetting('whats-app.web.authentication.time-out-in-seconds'))
AUTHENTICATION_SCREENSHOT_RENEW_TIME_IN_SECONDS = int(globalsInstance.getApiSetting('whats-app.web.authentication.screenshot-time-renew-in-seconds'))
TAB_ALTERNATINGT_TIME_IN_SECONDS = int(globalsInstance.getApiSetting('whats-app.web.tab-alternating-time-in-seconds'))
SCHEDULE_PING_MINUTES_INTERVAL = int(globalsInstance.getApiSetting('whats-app.web.ping-time-in-minutes'))

if AUTHENTICATION_SCREENSHOT_RENEW_TIME_IN_SECONDS > AUTHENTICATION_SCREENSHOT_RENEW_TIME_IN_SECONDS :
    raise Exception('Authentication time out cannot be bigger than authentication screenshot time renew')

if PRE_AUTHENTICATION_DELAY_IN_SECONDS > AUTHENTICATION_SCREENSHOT_RENEW_TIME_IN_SECONDS :
    raise Exception('Authentication pre delay cannot be bigger than authentication screenshot time renew')
