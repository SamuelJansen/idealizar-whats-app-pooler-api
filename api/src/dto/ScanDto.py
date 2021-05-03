from converter.static import ContactStaticConverter, MessageStaticConverter

class ScanRequestDto :
    def __init__(self,
        contact = None,
        lastMessageKey = None
    ) :
        self.contact = ContactStaticConverter.convertToContactDto(contact)
        self.lastMessageKey = lastMessageKey

class ScanResponseDto :
    def __init__(self,
        messageList = None
    ) :
        self.messageList = messageList
