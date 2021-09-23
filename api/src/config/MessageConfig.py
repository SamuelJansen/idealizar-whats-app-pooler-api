from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()

SCHEDULE_CURRENT_SCANNING_MESSAGE_MINUTES_INTERVAL = int(globalsInstance.getApiSetting('whats-app.web.message.current-scanning-message-time'))
