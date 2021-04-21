import ContactConstants

WHATS_APP_URL = "https://web.whatsapp.com/"

XPATH_GROUP_MESSAGE_SECTION = '//div//div//div[@aria-label="Message list. Press right arrow key on a message to open message context menu."]'
XPATH_GROUP_MESSAGE_LIST = '//div[contains(@class,"focusable-list-item")]'
XPATH_TEXT_BOX = '//div//div//div[@contenteditable="true"]'
XPATH_SEND_IMAGE = '//div//div//span[@data-icon="send"]'
XPATH_GROUP = f'//div//div//span[@title="{ContactConstants.TOKEN_CONTACT_KEY}"]'
XPATH_USER = f'//div//div//span//span[@title="{ContactConstants.TOKEN_CONTACT_KEY}"]'

CLASS_MESSAGE_OWNER = 'copyable-text'
CLASS_PARTIAL_MESSAGE_CONTENT = 'selectable-text copyable-text'

ATTR_MESSAGE_ID = 'data-id'
ATTR_OWNER_CONTENT = 'data-pre-plain-text'
ATTR_IS_POOLER_MESSAGE = 'class'
