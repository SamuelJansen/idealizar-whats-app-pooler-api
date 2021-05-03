from enumeration.ContactType import ContactType
from enumeration.ContactStatus import ContactStatus

from converter.static import ContactStaticConverter

class ContactRequestDto :
    def __init__(self,
        key = None,
        type = None,
        accessTime = None
    ) :
        self.key = key
        self.type = ContactType.map(type)
        self.accessTime = ContactStaticConverter.getAccessTime(accessTime)

class ContactResponseDto :
    def __init__(self,
        id = None,
        key = None,
        type = None,
        status = None,
        name = None
    ) :
        self.id = id
        self.key = key
        self.type = ContactType.map(type)
        self.status = ContactStatus.map(status)
        self.name = name
