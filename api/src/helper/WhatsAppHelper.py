from python_framework import Helper, HelperMethod

from dto import ContactDto
from domain import ContactConstants, WhatsAppWebConstants
from enumeration.ContactType import ContactType

@Helper()
class WhatsAppHelper :

    @HelperMethod(requestClass=ContactDto.ContactRequestDto)
    def getContactConversationXPath(self, dto) :
        if ContactType.USER == dto.type :
            return WhatsAppWebConstants.XPATH_USER.replace(ContactConstants.TOKEN_CONTACT_KEY, dto.key)
        if ContactType.GROUP == dto.type :
            return WhatsAppWebConstants.XPATH_GROUP.replace(ContactConstants.TOKEN_CONTACT_KEY, dto.key)
