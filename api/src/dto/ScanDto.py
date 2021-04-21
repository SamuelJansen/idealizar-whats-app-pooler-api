import ContactStaticConverter

class ScanRequestDto :
    def __init__(self,
        contact = None,
        lastOwner = None,
        lastMessageKeyList = None
    ) :
        self.contact = ContactStaticConverter.convertToContactDto(contact)
        self.lastOwner = MessageStaticConverter.getLastOwnerOrDefault(lastOwner)
        self.lastMessageKeyList = lastMessageKeyList
