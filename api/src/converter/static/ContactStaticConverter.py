from python_framework import Serializer, StaticConverter

from domain import ContactConstants
from dto import ContactDto

def convertToContactDto(value) :
    if isinstance(value, ContactDto.ContactRequestDto) :
        return value
    else :
        returnValue = None
        try :
            returnValue = Serializer.convertFromJsonToObject(
                Serializer.getObjectAsDictionary(value),
                ContactDto.ContactRequestDto
            )
        except :
            returnValue = value
        return returnValue

def getAccessTime(value) :
    return StaticConverter.getValueOrDefault(value, ContactConstants.DEFAULT_ACCESS_TIME)
