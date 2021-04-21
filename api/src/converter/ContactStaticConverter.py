from python_framework import Serializer
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
