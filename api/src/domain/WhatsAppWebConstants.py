from python_helper import Constant as c
from python_helper import EnvironmentHelper
from domain import ContactConstants

from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()

XPATH_AUTHENTICATED_USER = '//span[@data-testid="default-user"]'
XPATH_GROUP_MESSAGE_SECTION = '//div//div//div[@aria-label="Message list. Press right arrow key on a message to open message context menu."]'
XPATH_MESSAGE_LIST = '//div[contains(@class,"focusable-list-item")]'
XPATH_MESSAGE_IN_LIST = '//div[contains(@class,"message-in focusable-list-item")]'
XPATH_MESSAGE_OUT_LIST = '//div[contains(@class,"message-out focusable-list-item")]'
XPATH_TEXT_BOX = '//div//div//div[@contenteditable="true"]'
XPATH_SEND = '//div//div//span[@data-icon="send"]'
XPATH_GROUP = f'//div//div//span[@title="{ContactConstants.TOKEN_CONTACT_KEY}"]'
XPATH_USER = f'//div//div//span//span[@title="{ContactConstants.TOKEN_CONTACT_KEY}"]'

CLASS_MESSAGE_OWNER = 'copyable-text'
CLASS_PARTIAL_MESSAGE_CONTENT = 'selectable-text copyable-text'

ATTR_MESSAGE_ID = 'data-id'
ATTR_OWNER_CONTENT = 'data-pre-plain-text'
ATTR_IS_POOLER_MESSAGE = 'class'

HIDDEN_BROWSER = globalsInstance.getApiSetting('whats-app.web.browser.hidden')

DEFAULT_AVAILABLE_STATUS = True
DEFAULT_AUTHENTICATING_STATUS = False
DEFAULT_AUTHENTICATED_VALUE = False

STATIC_PATH_NAME = 'static'
STATIC_PACKAGE_PATH = f'{globalsInstance.baseApiPath}{STATIC_PATH_NAME}'

# DEFAULT_AMMOUNT_OF_MESSAGE_SCROLL_UP = 15

AUTHENTICATION_TEMPLATE_PACKAGE = f'authentication'
QR_CODE_IMAGE_NAME = f'{STATIC_PACKAGE_PATH}{EnvironmentHelper.OS_SEPARATOR}{AUTHENTICATION_TEMPLATE_PACKAGE}{EnvironmentHelper.OS_SEPARATOR}qr-code.png'
QR_CODE_TEMPLATE_NAME = f'/{AUTHENTICATION_TEMPLATE_PACKAGE}/qr-code.html'
QR_CODE_IMAGE_STATIC_PATH = f'/{STATIC_PATH_NAME}/{AUTHENTICATION_TEMPLATE_PACKAGE}/qr-code.png'
