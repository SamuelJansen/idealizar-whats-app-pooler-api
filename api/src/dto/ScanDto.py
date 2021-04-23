from converter.static import ContactStaticConverter, MessageStaticConverter

class ScanRequestDto :
    def __init__(self,
        contact = None,
        lastOwner = None,
        lastMessageKeyList = None
    ) :
        self.contact = ContactStaticConverter.convertToContactDto(contact)
        self.lastOwner = MessageStaticConverter.getLastOwnerOrDefault(lastOwner)
        self.lastMessageKeyList = lastMessageKeyList
